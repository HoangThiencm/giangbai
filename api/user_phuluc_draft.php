<?php
require_once __DIR__ . '/helpers.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

if (empty($_SESSION['user_id'])) {
    respond(['error' => 'Chưa đăng nhập.'], 401);
}

function ensure_user_phuluc_drafts_table(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS user_phuluc_drafts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        mon_hoc VARCHAR(160) NOT NULL DEFAULT '',
        lop VARCHAR(30) NOT NULL DEFAULT '',
        nam_hoc VARCHAR(30) NOT NULL DEFAULT '',
        draft_data LONGTEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_user_phuluc_draft_user (user_id),
        INDEX idx_user_phuluc_drafts_updated (updated_at)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

function draft_config_value(array $draft, string $key): string
{
    $config = $draft['config'] ?? [];
    return is_array($config) ? trim((string)($config[$key] ?? '')) : '';
}

$userId = (int)$_SESSION['user_id'];
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

try {
    ensure_user_phuluc_drafts_table($pdo);

    if ($method === 'GET') {
        $statement = $pdo->prepare('SELECT draft_data, updated_at FROM user_phuluc_drafts WHERE user_id = ? LIMIT 1');
        $statement->execute([$userId]);
        $row = $statement->fetch();
        if (!$row) {
            respond(['ok' => true, 'draft' => null, 'updated_at' => null]);
        }

        $draft = json_decode((string)$row['draft_data'], true);
        if (!is_array($draft)) {
            respond(['error' => 'Bản nháp đã lưu không hợp lệ.'], 422);
        }
        respond(['ok' => true, 'draft' => $draft, 'updated_at' => $row['updated_at']]);
    }

    if ($method === 'POST') {
        $body = json_body();
        $draft = $body['draft'] ?? null;
        if (!is_array($draft)) {
            respond(['error' => 'Dữ liệu bản nháp không hợp lệ.'], 422);
        }

        $draftJson = json_encode($draft, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        if ($draftJson === false) {
            respond(['error' => 'Không thể mã hóa dữ liệu bản nháp.'], 422);
        }

        $statement = $pdo->prepare('INSERT INTO user_phuluc_drafts (user_id, mon_hoc, lop, nam_hoc, draft_data) VALUES (?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE mon_hoc = VALUES(mon_hoc), lop = VALUES(lop), nam_hoc = VALUES(nam_hoc), draft_data = VALUES(draft_data), updated_at = CURRENT_TIMESTAMP');
        $statement->execute([
            $userId,
            draft_config_value($draft, 'monHoc'),
            draft_config_value($draft, 'lop'),
            draft_config_value($draft, 'namHoc'),
            $draftJson,
        ]);

        $updated = $pdo->prepare('SELECT updated_at FROM user_phuluc_drafts WHERE user_id = ? LIMIT 1');
        $updated->execute([$userId]);
        $row = $updated->fetch() ?: [];
        respond(['ok' => true, 'updated_at' => $row['updated_at'] ?? null]);
    }

    respond(['error' => 'Method not allowed.'], 405);
} catch (Throwable $e) {
    respond(['error' => 'Không thể lưu hoặc tải bản nháp.'], 500);
}
