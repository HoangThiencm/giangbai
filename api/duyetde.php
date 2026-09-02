<?php
require_once __DIR__ . '/helpers.php';
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
if (empty($_SESSION['user_id'])) {
    respond(['error' => 'Chưa đăng nhập.'], 401);
}

function ensure_duyetde_sessions(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS duyetde_sessions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(255) NOT NULL DEFAULT '',
        to_chuyen_mon VARCHAR(150) NOT NULL DEFAULT '',
        mon_hoc VARCHAR(80) NOT NULL DEFAULT '',
        khoi_lop VARCHAR(30) NOT NULL DEFAULT '',
        loai_de VARCHAR(50) NOT NULL DEFAULT '',
        nam_hoc VARCHAR(30) NOT NULL DEFAULT '',
        current_version INT NOT NULL DEFAULT 1,
        status VARCHAR(50) NOT NULL DEFAULT 'draft',
        final_decision VARCHAR(50) NOT NULL DEFAULT '',
        leader_feedback TEXT DEFAULT NULL,
        session_data LONGTEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_duyetde_user (user_id),
        INDEX idx_duyetde_status (status),
        INDEX idx_duyetde_updated (updated_at)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

function duyetde_decode_session_data($raw): array
{
    if (is_array($raw)) {
        return $raw;
    }
    if (!is_string($raw) || $raw === '') {
        return [];
    }
    $decoded = json_decode($raw, true);
    return is_array($decoded) ? $decoded : [];
}

function duyetde_public_session(array $row, bool $includeData = false): array
{
    $out = [
        'id' => (int)$row['id'],
        'title' => (string)($row['title'] ?? ''),
        'to_chuyen_mon' => (string)($row['to_chuyen_mon'] ?? ''),
        'mon_hoc' => (string)($row['mon_hoc'] ?? ''),
        'khoi_lop' => (string)($row['khoi_lop'] ?? ''),
        'loai_de' => (string)($row['loai_de'] ?? ''),
        'nam_hoc' => (string)($row['nam_hoc'] ?? ''),
        'current_version' => (int)($row['current_version'] ?? 1),
        'status' => (string)($row['status'] ?? 'draft'),
        'final_decision' => (string)($row['final_decision'] ?? ''),
        'leader_feedback' => (string)($row['leader_feedback'] ?? ''),
        'created_at' => $row['created_at'] ?? null,
        'updated_at' => $row['updated_at'] ?? null,
    ];
    if ($includeData) {
        $out['session_data'] = duyetde_decode_session_data($row['session_data'] ?? '');
    }
    return $out;
}

function duyetde_fetch_owned(PDO $pdo, int $userId, int $id): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM duyetde_sessions WHERE id = ? AND user_id = ?');
    $stmt->execute([$id, $userId]);
    $row = $stmt->fetch();
    return $row ?: null;
}

$userId = (int)$_SESSION['user_id'];
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$action = trim((string)($_GET['action'] ?? ''));

try {
    ensure_duyetde_sessions($pdo);

    if ($method === 'GET' && $action === 'list') {
        $stmt = $pdo->prepare('SELECT id, title, to_chuyen_mon, mon_hoc, khoi_lop, loai_de, nam_hoc, current_version, status, final_decision, created_at, updated_at FROM duyetde_sessions WHERE user_id = ? ORDER BY updated_at DESC');
        $stmt->execute([$userId]);
        $sessions = array_map(static fn(array $row): array => duyetde_public_session($row), $stmt->fetchAll() ?: []);
        respond(['ok' => true, 'sessions' => $sessions]);
    }

    if ($method === 'GET' && isset($_GET['id'])) {
        $row = duyetde_fetch_owned($pdo, $userId, (int)$_GET['id']);
        if (!$row) {
            respond(['error' => 'Không tìm thấy đợt duyệt đề.'], 404);
        }
        respond(['ok' => true, 'session' => duyetde_public_session($row, true)]);
    }

    if ($method !== 'POST') {
        respond(['error' => 'Method not allowed.'], 405);
    }

    $body = json_body();
    if ($action === '') {
        $action = trim((string)($body['action'] ?? ''));
    }
    $id = (int)($body['id'] ?? 0);

    if ($action === 'delete') {
        $stmt = $pdo->prepare('DELETE FROM duyetde_sessions WHERE id = ? AND user_id = ?');
        $stmt->execute([$id, $userId]);
        respond(['ok' => true]);
    }

    if ($action === 'submit') {
        $row = duyetde_fetch_owned($pdo, $userId, $id);
        if (!$row) {
            respond(['error' => 'Không tìm thấy đợt duyệt đề.'], 404);
        }
        $stmt = $pdo->prepare('UPDATE duyetde_sessions SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?');
        $stmt->execute(['pending_leader', $id, $userId]);
        $row = duyetde_fetch_owned($pdo, $userId, $id);
        respond(['ok' => true, 'session' => duyetde_public_session($row, true)]);
    }

    if ($action === 'decide') {
        $row = duyetde_fetch_owned($pdo, $userId, $id);
        if (!$row) {
            respond(['error' => 'Không tìm thấy đợt duyệt đề.'], 404);
        }
        $allowed = ['co_the_su_dung', 'can_chinh_sua', 'khong_su_dung'];
        $decision = trim((string)($body['final_decision'] ?? ''));
        if (!in_array($decision, $allowed, true)) {
            respond(['error' => 'Quyết định thẩm duyệt không hợp lệ.'], 422);
        }
        $statusMap = [
            'co_the_su_dung' => 'approved',
            'can_chinh_sua' => 'revision_needed',
            'khong_su_dung' => 'rejected',
        ];
        $feedback = trim((string)($body['leader_feedback'] ?? ''));
        $data = duyetde_decode_session_data($row['session_data'] ?? '');
        $data['leader'] = [
            'decision' => $decision,
            'feedback' => $feedback,
            'decided_at' => date('c'),
        ];
        $json = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $stmt = $pdo->prepare('UPDATE duyetde_sessions SET status = ?, final_decision = ?, leader_feedback = ?, session_data = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?');
        $stmt->execute([$statusMap[$decision], $decision, $feedback, $json, $id, $userId]);
        $row = duyetde_fetch_owned($pdo, $userId, $id);
        respond(['ok' => true, 'session' => duyetde_public_session($row, true)]);
    }

    $data = $body['session_data'] ?? null;
    if (!is_array($data)) {
        respond(['error' => 'Dữ liệu đợt duyệt không hợp lệ.'], 422);
    }
    $json = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    $title = trim((string)($body['title'] ?? $data['title'] ?? ''));
    $toChuyenMon = trim((string)($body['to_chuyen_mon'] ?? $data['to_chuyen_mon'] ?? ''));
    $monHoc = trim((string)($body['mon_hoc'] ?? $data['mon_hoc'] ?? ''));
    $khoiLop = trim((string)($body['khoi_lop'] ?? $data['khoi_lop'] ?? ''));
    $loaiDe = trim((string)($body['loai_de'] ?? $data['loai_de'] ?? ''));
    $namHoc = trim((string)($body['nam_hoc'] ?? $data['nam_hoc'] ?? ''));
    $currentVersion = max(1, (int)($body['current_version'] ?? $data['current_version'] ?? 1));
    $status = trim((string)($body['status'] ?? $data['status'] ?? 'draft')) ?: 'draft';
    $finalDecision = trim((string)($body['final_decision'] ?? $data['final_decision'] ?? ''));
    $leaderFeedback = array_key_exists('leader_feedback', $body)
        ? trim((string)$body['leader_feedback'])
        : trim((string)($data['leader']['feedback'] ?? ''));

    if ($id) {
        $exists = duyetde_fetch_owned($pdo, $userId, $id);
        if (!$exists) {
            respond(['error' => 'Không tìm thấy đợt duyệt đề.'], 404);
        }
        $stmt = $pdo->prepare('UPDATE duyetde_sessions SET title = ?, to_chuyen_mon = ?, mon_hoc = ?, khoi_lop = ?, loai_de = ?, nam_hoc = ?, current_version = ?, status = ?, final_decision = ?, leader_feedback = ?, session_data = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?');
        $stmt->execute([$title, $toChuyenMon, $monHoc, $khoiLop, $loaiDe, $namHoc, $currentVersion, $status, $finalDecision, $leaderFeedback, $json, $id, $userId]);
    } else {
        $stmt = $pdo->prepare('INSERT INTO duyetde_sessions (user_id, title, to_chuyen_mon, mon_hoc, khoi_lop, loai_de, nam_hoc, current_version, status, final_decision, leader_feedback, session_data) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)');
        $stmt->execute([$userId, $title, $toChuyenMon, $monHoc, $khoiLop, $loaiDe, $namHoc, $currentVersion, $status, $finalDecision, $leaderFeedback, $json]);
        $id = (int)$pdo->lastInsertId();
    }

    $row = duyetde_fetch_owned($pdo, $userId, $id);
    respond(['ok' => true, 'session' => duyetde_public_session($row, true)]);
} catch (Throwable $e) {
    respond(['error' => 'Không thể lưu hồ sơ duyệt đề.'], 500);
}
