<?php
require_once __DIR__ . '/helpers.php';
require_admin_key();

function hs_format_bytes(int $bytes): string
{
    if ($bytes < 1024) {
        return $bytes . ' B';
    }
    $units = ['KB', 'MB', 'GB', 'TB'];
    $value = (float) $bytes;
    foreach ($units as $unit) {
        $value /= 1024;
        if ($value < 1024) {
            return round($value, 2) . ' ' . $unit;
        }
    }
    return round($value, 2) . ' PB';
}

function hs_directory_size(string $path, int $maxDepth = 5, int $depth = 0): int
{
    if (!is_dir($path) || $depth > $maxDepth) {
        return 0;
    }

    $size = 0;
    $items = @scandir($path);
    if (!$items) {
        return 0;
    }

    $skipDirs = ['.git', 'node_modules', 'vendor', '.cursor'];
    foreach ($items as $item) {
        if ($item === '.' || $item === '..') {
            continue;
        }
        $full = $path . DIRECTORY_SEPARATOR . $item;
        if (is_link($full)) {
            continue;
        }
        if (is_file($full)) {
            $size += (int) @filesize($full);
            continue;
        }
        if (!is_dir($full)) {
            continue;
        }
        if ($depth === 0 || !in_array($item, $skipDirs, true)) {
            $size += hs_directory_size($full, $maxDepth, $depth + 1);
        }
    }

    return $size;
}

function hs_count_files(string $path, int $maxDepth = 5, int $depth = 0): int
{
    if (!is_dir($path) || $depth > $maxDepth) {
        return 0;
    }

    $count = 0;
    $items = @scandir($path);
    if (!$items) {
        return 0;
    }

    foreach ($items as $item) {
        if ($item === '.' || $item === '..') {
            continue;
        }
        $full = $path . DIRECTORY_SEPARATOR . $item;
        if (is_file($full)) {
            $count++;
            continue;
        }
        if (is_dir($full) && !is_link($full)) {
            $count += hs_count_files($full, $maxDepth, $depth + 1);
        }
    }

    return $count;
}

$projectRoot = realpath(__DIR__ . '/..') ?: dirname(__DIR__);
$diskPath = $projectRoot;

$diskTotal = @disk_total_space($diskPath);
$diskFree = @disk_free_space($diskPath);
$diskTotal = is_numeric($diskTotal) ? (int) $diskTotal : null;
$diskFree = is_numeric($diskFree) ? (int) $diskFree : null;
$diskUsed = ($diskTotal !== null && $diskFree !== null) ? max(0, $diskTotal - $diskFree) : null;

$folderDefs = [
    ['key' => 'project', 'label' => 'Toàn bộ dự án (giangbai)', 'path' => $projectRoot],
    ['key' => 'api', 'label' => 'Thư mục API', 'path' => $projectRoot . DIRECTORY_SEPARATOR . 'api'],
    ['key' => 'templates', 'label' => 'Mẫu Excel / templates', 'path' => $projectRoot . DIRECTORY_SEPARATOR . 'templates'],
    ['key' => 'uploads', 'label' => 'Uploads cục bộ', 'path' => $projectRoot . DIRECTORY_SEPARATOR . 'uploads'],
];

$folders = [];
foreach ($folderDefs as $def) {
    $exists = is_dir($def['path']);
    $bytes = $exists ? hs_directory_size($def['path']) : 0;
    $folders[] = [
        'key' => $def['key'],
        'label' => $def['label'],
        'path' => $def['path'],
        'exists' => $exists,
        'bytes' => $bytes,
        'human' => hs_format_bytes($bytes),
        'files' => $exists ? hs_count_files($def['path']) : 0,
    ];
}

$projectBytes = $folders[0]['bytes'] ?? 0;

$dbName = defined('DB_NAME') ? (string) DB_NAME : '';
$tables = [];
$dbBytes = 0;

if ($dbName !== '') {
    $tableStmt = $pdo->prepare("
        SELECT
            table_name,
            table_rows,
            data_length,
            index_length,
            (data_length + index_length) AS size_bytes,
            update_time
        FROM information_schema.tables
        WHERE table_schema = ?
        ORDER BY size_bytes DESC, table_name ASC
    ");
    $tableStmt->execute([$dbName]);
    foreach ($tableStmt->fetchAll() as $row) {
        $sizeBytes = (int) ($row['size_bytes'] ?? 0);
        $dbBytes += $sizeBytes;
        $tables[] = [
            'name' => (string) $row['table_name'],
            'rows' => (int) ($row['table_rows'] ?? 0),
            'bytes' => $sizeBytes,
            'human' => hs_format_bytes($sizeBytes),
            'updated_at' => $row['update_time'] ?? null,
        ];
    }
}

$counts = [];
$countQueries = [
    'users' => "SELECT COUNT(*) FROM users",
    'lessons' => "SELECT COUNT(*) FROM lessons",
    'student_lesson_progress' => "SELECT COUNT(*) FROM student_lesson_progress",
    'exams' => "SELECT COUNT(*) FROM exams",
    'exam_submissions' => "SELECT COUNT(*) FROM exam_submissions",
    'short_links' => "SELECT COUNT(*) FROM short_links",
];
foreach ($countQueries as $key => $sql) {
    try {
        $counts[$key] = (int) $pdo->query($sql)->fetchColumn();
    } catch (Throwable $e) {
        $counts[$key] = null;
    }
}

respond([
    'ok' => true,
    'generated_at' => date('c'),
    'project_root' => $projectRoot,
    'disk' => [
        'path' => $diskPath,
        'total_bytes' => $diskTotal,
        'free_bytes' => $diskFree,
        'used_bytes' => $diskUsed,
        'total_human' => $diskTotal !== null ? hs_format_bytes($diskTotal) : null,
        'free_human' => $diskFree !== null ? hs_format_bytes($diskFree) : null,
        'used_human' => $diskUsed !== null ? hs_format_bytes($diskUsed) : null,
        'used_percent' => ($diskTotal && $diskUsed !== null) ? round(($diskUsed / $diskTotal) * 100, 1) : null,
        'available' => $diskTotal !== null,
    ],
    'project' => [
        'bytes' => $projectBytes,
        'human' => hs_format_bytes($projectBytes),
        'folders' => $folders,
    ],
    'database' => [
        'name' => $dbName,
        'bytes' => $dbBytes,
        'human' => hs_format_bytes($dbBytes),
        'tables' => $tables,
        'counts' => $counts,
    ],
    'notes' => [
        'Dung lượng ổ đĩa là của partition hosting chứa thư mục dự án — có thể dùng chung với site khác trên cùng gói.',
        'File nộp bài qua Google Drive không tính vào dung lượng hosting này.',
        'Số dòng bảng MySQL (table_rows) là ước lượng, có thể lệch vài % so với thực tế.',
    ],
]);