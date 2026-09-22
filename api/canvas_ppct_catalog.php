<?php
/** Canvas PPCT catalog: same table as soankhbd, teacher resolved like Canvas drafts. */
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-User-Account');
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') { http_response_code(204); exit; }
require_once __DIR__ . '/helpers.php';
if (session_status() === PHP_SESSION_NONE) session_start();

function canvas_ppct_reply(array $data, int $code = 200): void {
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

function canvas_ppct_teacher(PDO $pdo): array {
    $id = (int)($_SESSION['user_id'] ?? 0);
    if ($id > 0) {
        $q = $pdo->prepare("SELECT id FROM users WHERE id=? AND role='teacher' AND is_active=1 LIMIT 1");
        $q->execute([$id]);
        $u = $q->fetch();
        if ($u) return $u;
    }
    $body = in_array($_SERVER['REQUEST_METHOD'] ?? '', ['PUT', 'POST'], true) ? json_body() : [];
    $accountValue = $_SERVER['HTTP_X_USER_ACCOUNT'] ?? $_GET['user_account'] ?? ($body['user_account'] ?? '');
    $account = is_string($accountValue) ? trim($accountValue) : '';
    if (strpos($account, '%') !== false) $account = rawurldecode($account);
    if ($account === '') $account = 'hoangthiencm@gmail.com';
    $alt = strpos($account, '@') !== false ? explode('@', $account)[0] : $account;
    $q = $pdo->prepare("SELECT id FROM users WHERE (username=? OR username=?) AND role='teacher' AND is_active=1 LIMIT 1");
    $q->execute([$account, $alt]);
    $u = $q->fetch();
    if (!$u) canvas_ppct_reply(['error' => "Tài khoản '$account' chưa đăng ký giáo viên trên hosting."], 401);
    return $u;
}

function canvas_ppct_table(PDO $pdo): void { $pdo->exec("CREATE TABLE IF NOT EXISTS teacher_ppct_catalogs (id INT AUTO_INCREMENT PRIMARY KEY, owner_user_id INT NOT NULL, subject VARCHAR(80) NOT NULL, grade VARCHAR(20) NOT NULL, academic_year VARCHAR(30) NOT NULL DEFAULT '', school_name VARCHAR(150) NOT NULL DEFAULT '', rows_json LONGTEXT NOT NULL, source_json TEXT NOT NULL, created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, UNIQUE KEY uq_teacher_ppct_catalog (owner_user_id,subject,grade,academic_year,school_name), INDEX idx_teacher_ppct_owner (owner_user_id), CONSTRAINT fk_teacher_ppct_owner FOREIGN KEY (owner_user_id) REFERENCES users(id) ON DELETE CASCADE) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"); $column=$pdo->query("SHOW COLUMNS FROM teacher_ppct_catalogs LIKE 'school_name'")->fetch();if(!$column)$pdo->exec("ALTER TABLE teacher_ppct_catalogs ADD COLUMN school_name VARCHAR(150) NOT NULL DEFAULT '' AFTER academic_year");$indexes=$pdo->query("SHOW INDEX FROM teacher_ppct_catalogs")->fetchAll();$keyParts=0;foreach($indexes as $index)if(($index['Key_name']??'')==='uq_teacher_ppct_catalog')$keyParts++;if($keyParts&&$keyParts!==5)$pdo->exec("ALTER TABLE teacher_ppct_catalogs DROP INDEX uq_teacher_ppct_catalog");if($keyParts!==5)$pdo->exec("ALTER TABLE teacher_ppct_catalogs ADD UNIQUE KEY uq_teacher_ppct_catalog (owner_user_id,subject,grade,academic_year,school_name)"); }
function canvas_ppct_school($value): string { return mb_substr(trim((string)$value),0,150); }
function canvas_ppct_catalog_row(array $row): array { $row['rows']=json_decode($row['rows_json'],true)?:[];$row['source']=json_decode($row['source_json'],true)?:[];unset($row['rows_json'],$row['source_json']);return $row; }

try {
    $teacher = canvas_ppct_teacher($pdo);
    canvas_ppct_table($pdo);
    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
    if ($method === 'GET') {
        $subject = trim((string)($_GET['subject'] ?? ''));
        $grade = trim((string)($_GET['grade'] ?? ''));
        $year = trim((string)($_GET['academic_year'] ?? '')); $schoolProvided=array_key_exists('school_name',$_GET); $school=canvas_ppct_school($_GET['school_name']??'');
        if ($subject === '' || $grade === '') canvas_ppct_reply(['error' => 'Thiếu môn hoặc khối lớp.'], 422);
        if (!$schoolProvided) { $sql='SELECT id,subject,grade,academic_year,school_name,updated_at FROM teacher_ppct_catalogs WHERE owner_user_id=? AND subject=? AND grade=?'.($year!==''?' AND academic_year=?':'').' ORDER BY updated_at DESC,id DESC';$q=$pdo->prepare($sql);$q->execute($year!==''?[(int)$teacher['id'],$subject,$grade,$year]:[(int)$teacher['id'],$subject,$grade]);canvas_ppct_reply(['ok'=>true,'profiles'=>$q->fetchAll()]); }
        $sql='SELECT * FROM teacher_ppct_catalogs WHERE owner_user_id=? AND subject=? AND grade=? AND school_name=?'.($year!==''?' AND academic_year=?':'').' ORDER BY updated_at DESC,id DESC LIMIT 1';$q=$pdo->prepare($sql);$q->execute($year!==''?[(int)$teacher['id'],$subject,$grade,$school,$year]:[(int)$teacher['id'],$subject,$grade,$school]);$row=$q->fetch();canvas_ppct_reply(['ok'=>true,'catalog'=>$row?canvas_ppct_catalog_row($row):null]);
    }
    if ($method === 'DELETE') { $subject=trim((string)($_GET['subject']??''));$grade=trim((string)($_GET['grade']??''));$year=trim((string)($_GET['academic_year']??''));$school=canvas_ppct_school($_GET['school_name']??'');if($subject===''||$grade===''||$year==='')canvas_ppct_reply(['error'=>'Thiếu môn, khối hoặc năm học.'],422);$q=$pdo->prepare('DELETE FROM teacher_ppct_catalogs WHERE owner_user_id=? AND subject=? AND grade=? AND academic_year=? AND school_name=?');$q->execute([(int)$teacher['id'],$subject,$grade,$year,$school]);canvas_ppct_reply(['ok'=>true,'deleted'=>$q->rowCount()]); }
    if ($method !== 'PUT') canvas_ppct_reply(['error' => 'Method not allowed.'], 405);
    $body = json_body();
    $subject = trim((string)($body['subject'] ?? ''));
    $grade = trim((string)($body['grade'] ?? ''));
    $year = trim((string)($body['academic_year'] ?? ''));
    $school = canvas_ppct_school($body['school_name'] ?? '');
    $rows = $body['rows'] ?? null;
    $source = $body['source'] ?? [];
    if ($subject === '' || $grade === '' || !is_array($rows)) canvas_ppct_reply(['error' => 'Dữ liệu PPCT không hợp lệ.'], 422);
    if (count($rows) > 1000) canvas_ppct_reply(['error' => 'Danh mục PPCT vượt giới hạn.'], 422);
    foreach ($rows as $row) if (!is_array($row) || empty($row['id']) || empty($row['title'])) canvas_ppct_reply(['error' => 'Mỗi dòng PPCT cần mã ổn định và tên bài.'], 422);
    $rj = json_encode(array_values($rows), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    $sj = json_encode(is_array($source) ? $source : [], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    $q = $pdo->prepare('INSERT INTO teacher_ppct_catalogs (owner_user_id,subject,grade,academic_year,school_name,rows_json,source_json) VALUES (?,?,?,?,?,?,?) ON DUPLICATE KEY UPDATE rows_json=VALUES(rows_json),source_json=VALUES(source_json),updated_at=CURRENT_TIMESTAMP');
    $q->execute([(int)$teacher['id'], $subject, $grade, $year, $school, $rj, $sj]);
    $q = $pdo->prepare('SELECT id,subject,grade,academic_year,school_name,updated_at FROM teacher_ppct_catalogs WHERE owner_user_id=? AND subject=? AND grade=? AND academic_year=? AND school_name=?');
    $q->execute([(int)$teacher['id'], $subject, $grade, $year, $school]);
    canvas_ppct_reply(['ok' => true, 'catalog' => $q->fetch()]);
} catch (Throwable $e) {
    canvas_ppct_reply(['error' => 'Không thể lưu danh mục PPCT.'], 500);
}
