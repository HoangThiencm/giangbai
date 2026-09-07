<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-User-Account, X-Admin-Key');
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') {
    http_response_code(204);
    exit;
}

require_once __DIR__ . '/helpers.php';
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

function ensure_sgk_knowledge_tables(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS sgk_books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        book_key VARCHAR(100) NOT NULL UNIQUE,
        subject VARCHAR(100) NOT NULL DEFAULT '',
        grade VARCHAR(20) NOT NULL DEFAULT '',
        series VARCHAR(120) NOT NULL DEFAULT '',
        semester VARCHAR(50) NOT NULL DEFAULT 'all',
        publisher VARCHAR(150) NOT NULL DEFAULT '',
        total_lessons INT NOT NULL DEFAULT 0,
        is_verified TINYINT(1) NOT NULL DEFAULT 0,
        created_by VARCHAR(100) NOT NULL DEFAULT '',
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_sgk_books_lookup (subject, grade, series)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    $pdo->exec("CREATE TABLE IF NOT EXISTS sgk_lessons (
        id INT AUTO_INCREMENT PRIMARY KEY,
        book_id INT NOT NULL,
        lesson_order INT NOT NULL DEFAULT 0,
        chapter VARCHAR(255) NOT NULL DEFAULT '',
        lesson_code VARCHAR(100) NOT NULL DEFAULT '',
        lesson_title VARCHAR(255) NOT NULL DEFAULT '',
        page_start INT NOT NULL DEFAULT 0,
        page_end INT NOT NULL DEFAULT 0,
        yccd MEDIUMTEXT NOT NULL,
        activities_json MEDIUMTEXT NOT NULL,
        digital_candidates TEXT NOT NULL,
        digital_evidence TEXT NOT NULL,
        ai_pedagogy_hint TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_sgk_lessons_book (book_id),
        INDEX idx_sgk_lessons_title (lesson_title(100))
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

function normalize_sgk_book_key(string $subject, string $grade, string $series, string $semester = 'all'): string
{
    $str = mb_strtolower(trim("$subject-$grade-$series-$semester"));
    $trans = [
        'à'=>'a','á'=>'a','ả'=>'a','ã'=>'a','ạ'=>'a','ă'=>'a','ằ'=>'a','ắ'=>'a','ẳ'=>'a','ẵ'=>'a','ặ'=>'a',
        'â'=>'a','ầ'=>'a','ấ'=>'a','ẩ'=>'a','ẫ'=>'a','ậ'=>'a',
        'è'=>'e','é'=>'e','ẻ'=>'e','ẽ'=>'e','ẹ'=>'e','ê'=>'e','ề'=>'e','ế'=>'e','ể'=>'e','ễ'=>'e','ệ'=>'e',
        'ì'=>'i','í'=>'i','ỉ'=>'i','ĩ'=>'i','ị'=>'i',
        'ò'=>'o','ó'=>'o','ỏ'=>'o','õ'=>'o','ọ'=>'o','ô'=>'o','ồ'=>'o','ố'=>'o','ổ'=>'o','ỗ'=>'o','ộ'=>'o',
        'ơ'=>'o','ờ'=>'o','ớ'=>'o','ở'=>'o','ỡ'=>'o','ợ'=>'o',
        'ù'=>'u','ú'=>'u','ủ'=>'u','ũ'=>'u','ụ'=>'u','ư'=>'u','ừ'=>'u','ứ'=>'u','ử'=>'u','ữ'=>'u','ự'=>'u',
        'ỳ'=>'y','ý'=>'y','ỷ'=>'y','ỹ'=>'y','ỵ'=>'y',
        'đ'=>'d'
    ];
    $clean = strtr($str, $trans);
    $clean = preg_replace('/[^a-z0-9]+/i', '_', $clean);
    return trim($clean, '_');
}

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$action = trim((string)($_GET['action'] ?? ''));

try {
    ensure_sgk_knowledge_tables($pdo);

    if ($method === 'GET' && $action === 'check') {
        $subject = trim((string)($_GET['subject'] ?? ''));
        $grade = trim((string)($_GET['grade'] ?? ''));
        $series = trim((string)($_GET['series'] ?? ''));
        $semester = trim((string)($_GET['semester'] ?? ''));

        if ($subject === '' || $grade === '' || $series === '') {
            respond(['error' => 'Thiếu thông tin tra cứu (môn học, khối lớp, bộ sách).'], 422);
        }

        // Check exact match first
        $stmt = $pdo->prepare('SELECT id, book_key, subject, grade, series, semester, publisher, total_lessons, is_verified, created_by, updated_at FROM sgk_books WHERE subject = ? AND grade = ? AND series = ?' . ($semester !== '' ? ' AND (semester = ? OR semester = "all")' : '') . ' ORDER BY is_verified DESC, updated_at DESC LIMIT 1');
        $params = [$subject, $grade, $series];
        if ($semester !== '') {
            $params[] = $semester;
        }
        $stmt->execute($params);
        $book = $stmt->fetch();

        if ($book) {
            respond([
                'ok' => true,
                'exists' => true,
                'book' => $book
            ]);
        } else {
            respond([
                'ok' => true,
                'exists' => false,
                'book' => null
            ]);
        }
    }

    if ($method === 'GET' && $action === 'get') {
        $bookId = (int)($_GET['book_id'] ?? $_GET['id'] ?? 0);
        $bookKey = trim((string)($_GET['book_key'] ?? ''));

        $book = null;
        if ($bookId > 0) {
            $stmt = $pdo->prepare('SELECT * FROM sgk_books WHERE id = ? LIMIT 1');
            $stmt->execute([$bookId]);
            $book = $stmt->fetch();
        } elseif ($bookKey !== '') {
            $stmt = $pdo->prepare('SELECT * FROM sgk_books WHERE book_key = ? LIMIT 1');
            $stmt->execute([$bookKey]);
            $book = $stmt->fetch();
        } else {
            $subject = trim((string)($_GET['subject'] ?? ''));
            $grade = trim((string)($_GET['grade'] ?? ''));
            $series = trim((string)($_GET['series'] ?? ''));
            $semester = trim((string)($_GET['semester'] ?? ''));

            if ($subject !== '' && $grade !== '' && $series !== '') {
                $stmt = $pdo->prepare('SELECT * FROM sgk_books WHERE subject = ? AND grade = ? AND series = ?' . ($semester !== '' ? ' AND (semester = ? OR semester = "all")' : '') . ' ORDER BY is_verified DESC, updated_at DESC LIMIT 1');
                $params = [$subject, $grade, $series];
                if ($semester !== '') $params[] = $semester;
                $stmt->execute($params);
                $book = $stmt->fetch();
            }
        }

        if (!$book) {
            respond(['error' => 'Không tìm thấy bộ sách trong kho tri thức dùng chung.'], 404);
        }

        $stmtLessons = $pdo->prepare('SELECT id, book_id, lesson_order, chapter, lesson_code, lesson_title, page_start, page_end, yccd, activities_json, digital_candidates, digital_evidence, ai_pedagogy_hint, created_at FROM sgk_lessons WHERE book_id = ? ORDER BY lesson_order ASC, id ASC');
        $stmtLessons->execute([(int)$book['id']]);
        $rawLessons = $stmtLessons->fetchAll();

        $lessons = [];
        foreach ($rawLessons as $row) {
            $act = json_decode((string)$row['activities_json'], true);
            $row['activities'] = is_array($act) ? $act : [];
            $titleFold = mb_strtolower((string)($row['lesson_title'] ?? ''));
            $evFold = mb_strtolower((string)($row['digital_evidence'] ?? ''));
            if (preg_match('/(so tu nhien|so nguyen|phan so|so thap phan|so huu ti|chia het|uoc chung|boi chung|so nguyen to|tap hop)/i', $titleFold) &&
                preg_match('/(kiem tra nghiem|ve do thi|giai he)/i', $evFold)) {
                $cleanT = preg_replace('/^(bài|tiết)\s*\d+[\s:.-]*/iu', '', (string)$row['lesson_title']);
                $cleanT = trim($cleanT);
                $row['digital_evidence'] = "Sử dụng máy tính cầm tay để thực hành tính toán, kiểm tra kết quả so sánh và phần mềm trực quan tia số/trục số trong bài $cleanT.";
            }
            $lessons[] = $row;
        }

        respond([
            'ok' => true,
            'book' => $book,
            'lessons' => $lessons
        ]);
    }

    if ($method === 'GET' && ($action === 'list' || $action === '')) {
        $stmt = $pdo->prepare('SELECT id, book_key, subject, grade, series, semester, publisher, total_lessons, is_verified, created_by, updated_at FROM sgk_books ORDER BY subject ASC, grade ASC, series ASC');
        $stmt->execute();
        respond([
            'ok' => true,
            'books' => $stmt->fetchAll()
        ]);
    }

    if ($method === 'POST' && $action === 'save') {
        $body = json_body();
        $bookData = $body['book'] ?? [];
        $lessonsData = $body['lessons'] ?? [];

        if (!is_array($bookData) || !is_array($lessonsData)) {
            respond(['error' => 'Dữ liệu bản đồ tri thức SGK không đúng định dạng.'], 422);
        }

        $subject = trim((string)($bookData['subject'] ?? ''));
        $grade = trim((string)($bookData['grade'] ?? ''));
        $series = trim((string)($bookData['series'] ?? ''));
        $semester = trim((string)($bookData['semester'] ?? 'all'));
        $publisher = trim((string)($bookData['publisher'] ?? ''));
        $userAccount = trim((string)($body['user_account'] ?? ($_SESSION['username'] ?? 'shared_user')));

        if ($subject === '' || $grade === '' || $series === '') {
            respond(['error' => 'Vui lòng cung cấp đầy đủ: Môn học, Khối lớp, Bộ sách.'], 422);
        }

        if (empty($lessonsData)) {
            respond(['error' => 'Danh sách bài học trong bản đồ tri thức không được rỗng.'], 422);
        }

        $bookKey = normalize_sgk_book_key($subject, $grade, $series, $semester);
        $totalLessons = count($lessonsData);

        $pdo->beginTransaction();
        try {
            // Check existing book by book_key
            $checkStmt = $pdo->prepare('SELECT id FROM sgk_books WHERE book_key = ? LIMIT 1');
            $checkStmt->execute([$bookKey]);
            $existingId = (int)$checkStmt->fetchColumn();

            if ($existingId > 0) {
                $bookId = $existingId;
                $updStmt = $pdo->prepare('UPDATE sgk_books SET subject=?, grade=?, series=?, semester=?, publisher=?, total_lessons=?, created_by=?, updated_at=CURRENT_TIMESTAMP WHERE id=?');
                $updStmt->execute([$subject, $grade, $series, $semester, $publisher, $totalLessons, $userAccount, $bookId]);

                // Clear existing lessons for this book to replace with new knowledge map
                $delStmt = $pdo->prepare('DELETE FROM sgk_lessons WHERE book_id = ?');
                $delStmt->execute([$bookId]);
            } else {
                $insStmt = $pdo->prepare('INSERT INTO sgk_books (book_key, subject, grade, series, semester, publisher, total_lessons, is_verified, created_by) VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)');
                $insStmt->execute([$bookKey, $subject, $grade, $series, $semester, $publisher, $totalLessons, $userAccount]);
                $bookId = (int)$pdo->lastInsertId();
            }

            // Insert lessons
            $insLessonStmt = $pdo->prepare('INSERT INTO sgk_lessons (book_id, lesson_order, chapter, lesson_code, lesson_title, page_start, page_end, yccd, activities_json, digital_candidates, digital_evidence, ai_pedagogy_hint) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');

            $order = 1;
            foreach ($lessonsData as $les) {
                if (!is_array($les)) continue;
                $chapter = trim((string)($les['chapter'] ?? ''));
                $code = trim((string)($les['lesson_code'] ?? 'bai_' . $order));
                $title = trim((string)($les['lesson_title'] ?? ($les['title'] ?? 'Bài ' . $order)));
                $pageStart = (int)($les['page_start'] ?? 0);
                $pageEnd = (int)($les['page_end'] ?? 0);
                $yccd = trim((string)($les['yccd'] ?? ''));
                $activities = $les['activities'] ?? ($les['activities_json'] ?? []);
                $actJson = is_string($activities) ? $activities : json_encode($activities, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
                $digitalCandidates = trim((string)($les['digital_candidates'] ?? ''));
                $digitalEvidence = trim((string)($les['digital_evidence'] ?? ''));
                $titleFold = mb_strtolower($title);
                $evFold = mb_strtolower($digitalEvidence);
                if (preg_match('/(so tu nhien|so nguyen|phan so|so thap phan|so huu ti|chia het|uoc chung|boi chung|so nguyen to|tap hop)/i', $titleFold) &&
                    preg_match('/(kiem tra nghiem|ve do thi|giai he)/i', $evFold)) {
                    $cleanT = preg_replace('/^(bài|tiết)\s*\d+[\s:.-]*/iu', '', $title);
                    $cleanT = trim($cleanT);
                    $digitalEvidence = "Sử dụng máy tính cầm tay để thực hành tính toán, kiểm tra kết quả so sánh và phần mềm trực quan tia số/trục số trong bài $cleanT.";
                }
                $aiPedagogyHint = trim((string)($les['ai_pedagogy_hint'] ?? ''));

                $insLessonStmt->execute([
                    $bookId,
                    $order,
                    $chapter,
                    $code,
                    $title,
                    $pageStart,
                    $pageEnd,
                    $yccd,
                    $actJson ?: '[]',
                    $digitalCandidates,
                    $digitalEvidence,
                    $aiPedagogyHint
                ]);
                $order++;
            }

            $pdo->commit();

            respond([
                'ok' => true,
                'message' => "Đã lưu thành công Bản đồ Tri thức SGK ($subject - Lớp $grade - $series) gồm $totalLessons bài học vào kho dùng chung.",
                'book_id' => $bookId,
                'book_key' => $bookKey,
                'total_lessons' => $totalLessons
            ]);
        } catch (Throwable $ex) {
            $pdo->rollBack();
            respond(['error' => 'Lỗi trong quá trình ghi CSDL tri thức SGK: ' . $ex->getMessage()], 500);
        }
    }

    if ($method === 'POST' && $action === 'verify') {
        $body = json_body();
        $bookId = (int)($body['book_id'] ?? $_GET['book_id'] ?? 0);
        $isVerified = isset($body['is_verified']) ? (int)(bool)$body['is_verified'] : 1;

        if ($bookId <= 0) {
            respond(['error' => 'Mã bộ sách không hợp lệ.'], 422);
        }

        $stmt = $pdo->prepare('UPDATE sgk_books SET is_verified = ? WHERE id = ?');
        $stmt->execute([$isVerified, $bookId]);

        respond([
            'ok' => true,
            'book_id' => $bookId,
            'is_verified' => $isVerified,
            'message' => $isVerified ? 'Bộ sách đã được xác nhận kiểm định chuẩn.' : 'Đã bỏ cờ kiểm định.'
        ]);
    }

    if (($method === 'POST' || $method === 'GET') && $action === 'delete') {
        $body = $method === 'POST' ? json_body() : [];
        $bookId = (int)($body['book_id'] ?? $body['id'] ?? $_GET['book_id'] ?? $_GET['id'] ?? 0);

        if ($bookId <= 0) {
            $bookKey = trim((string)($body['book_key'] ?? $_GET['book_key'] ?? ''));
            if ($bookKey !== '') {
                $stmtFind = $pdo->prepare('SELECT id FROM sgk_books WHERE book_key = ? LIMIT 1');
                $stmtFind->execute([$bookKey]);
                $bookId = (int)$stmtFind->fetchColumn();
            }
        }

        if ($bookId <= 0) {
            respond(['error' => 'Mã bộ sách cần xóa không hợp lệ.'], 422);
        }

        $pdo->beginTransaction();
        try {
            $delLessons = $pdo->prepare('DELETE FROM sgk_lessons WHERE book_id = ?');
            $delLessons->execute([$bookId]);

            $delBook = $pdo->prepare('DELETE FROM sgk_books WHERE id = ?');
            $delBook->execute([$bookId]);

            $pdo->commit();
            respond([
                'ok' => true,
                'message' => 'Đã xóa bộ sách và toàn bộ bài học khỏi Kho Tri thức dùng chung.',
                'deleted_id' => $bookId
            ]);
        } catch (Throwable $ex) {
            $pdo->rollBack();
            respond(['error' => 'Lỗi xóa bộ sách: ' . $ex->getMessage()], 500);
        }
    }

    respond(['error' => 'Action or method not allowed.'], 405);
} catch (Throwable $e) {
    respond(['error' => 'Lỗi kết nối hoặc xử lý Kho Tri thức SGK: ' . $e->getMessage()], 500);
}
