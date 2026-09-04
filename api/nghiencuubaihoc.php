<?php
require_once __DIR__ . '/helpers.php';
if (session_status() === PHP_SESSION_NONE) session_start();
if (empty($_SESSION['user_id'])) respond(['error' => 'Chưa đăng nhập.'], 401);

function ensure_nghien_cuu_bai_hoc_sessions(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS nghien_cuu_bai_hoc_sessions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        mon_hoc VARCHAR(160) NOT NULL DEFAULT '',
        lop VARCHAR(30) NOT NULL DEFAULT '',
        bai_hoc VARCHAR(255) NOT NULL DEFAULT '',
        bo_sgk VARCHAR(160) NOT NULL DEFAULT '',
        gv_day VARCHAR(160) NOT NULL DEFAULT '',
        session_title VARCHAR(255) NOT NULL DEFAULT '',
        current_step INT NOT NULL DEFAULT 1,
        session_data LONGTEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_ncbh_user (user_id),
        INDEX idx_ncbh_updated (updated_at)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

$userId = (int)$_SESSION['user_id'];
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$action = $_GET['action'] ?? '';

try {
    ensure_nghien_cuu_bai_hoc_sessions($pdo);

    if ($method === 'GET' && $action === 'list') {
        $s = $pdo->prepare('SELECT id, mon_hoc, lop, bai_hoc, bo_sgk, gv_day, session_title, current_step, created_at, updated_at FROM nghien_cuu_bai_hoc_sessions WHERE user_id=? ORDER BY updated_at DESC');
        $s->execute([$userId]);
        respond(['ok' => true, 'sessions' => $s->fetchAll()]);
    }

    if ($method === 'GET' && isset($_GET['id'])) {
        $s = $pdo->prepare('SELECT * FROM nghien_cuu_bai_hoc_sessions WHERE id=? AND user_id=?');
        $s->execute([(int)$_GET['id'], $userId]);
        $row = $s->fetch();
        if (!$row) respond(['error' => 'Không tìm thấy hồ sơ nghiên cứu bài học.'], 404);
        $row['session_data'] = json_decode((string)$row['session_data'], true);
        if (!is_array($row['session_data'])) respond(['error' => 'Dữ liệu hồ sơ không hợp lệ.'], 422);
        respond(['ok' => true, 'session' => $row]);
    }

    if ($method === 'POST' && $action === 'delete') {
        $b = json_body();
        $s = $pdo->prepare('DELETE FROM nghien_cuu_bai_hoc_sessions WHERE id=? AND user_id=?');
        $s->execute([(int)($b['id'] ?? 0), $userId]);
        respond(['ok' => true]);
    }

    if ($method === 'POST') {
        $b = json_body();
        $data = $b['session_data'] ?? null;
        if (!is_array($data)) respond(['error' => 'Dữ liệu hồ sơ không hợp lệ.'], 422);
        $json = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        if ($json === false) respond(['error' => 'Không thể mã hóa dữ liệu hồ sơ.'], 422);
        $values = [
            trim((string)($b['mon_hoc'] ?? '')),
            trim((string)($b['lop'] ?? '')),
            trim((string)($b['bai_hoc'] ?? '')),
            trim((string)($b['bo_sgk'] ?? '')),
            trim((string)($b['gv_day'] ?? '')),
            trim((string)($b['session_title'] ?? '')),
            max(1, min(12, (int)($b['current_step'] ?? 1))),
            $json,
        ];
        $id = (int)($b['id'] ?? 0);
        if ($id) {
            $exists = $pdo->prepare('SELECT 1 FROM nghien_cuu_bai_hoc_sessions WHERE id=? AND user_id=?');
            $exists->execute([$id, $userId]);
            if (!$exists->fetchColumn()) respond(['error' => 'Không tìm thấy hồ sơ nghiên cứu bài học.'], 404);
            $s = $pdo->prepare('UPDATE nghien_cuu_bai_hoc_sessions SET mon_hoc=?,lop=?,bai_hoc=?,bo_sgk=?,gv_day=?,session_title=?,current_step=?,session_data=?,updated_at=CURRENT_TIMESTAMP WHERE id=? AND user_id=?');
            $s->execute([...$values, $id, $userId]);
        } else {
            $s = $pdo->prepare('INSERT INTO nghien_cuu_bai_hoc_sessions(user_id,mon_hoc,lop,bai_hoc,bo_sgk,gv_day,session_title,current_step,session_data) VALUES (?,?,?,?,?,?,?,?,?)');
            $s->execute([$userId, ...$values]);
            $id = (int)$pdo->lastInsertId();
        }
        $s = $pdo->prepare('SELECT id, mon_hoc, lop, bai_hoc, bo_sgk, gv_day, session_title, current_step, created_at, updated_at FROM nghien_cuu_bai_hoc_sessions WHERE id=? AND user_id=?');
        $s->execute([$id, $userId]);
        respond(['ok' => true, 'session' => $s->fetch()]);
    }

    respond(['error' => 'Method not allowed.'], 405);
} catch (Throwable $e) {
    respond(['error' => 'Không thể lưu hồ sơ nghiên cứu bài học.'], 500);
}
