<?php
// ==================== IMPORT KẾT QUẢ THI TỪ SUPABASE → MYSQL ====================
require_once 'config.php'; // hoặc file kết nối DB của bạn

header('Content-Type: text/html; charset=utf-8');

echo "<h2>Import kết quả thi từ file CSV</h2>";

// Kết nối DB
$pdo = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8mb4", $db_user, $db_pass);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['csv_file'])) {
    $file = $_FILES['csv_file']['tmp_name'];
    $exam_id = $_POST['exam_id'] ?? 'db776d2b'; // thay bằng exam_id thật nếu khác

    if (empty($file)) {
        die("Vui lòng chọn file CSV");
    }

    $row = 0;
    $imported = 0;
    if (($handle = fopen($file, "r")) !== FALSE) {
        while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
            $row++;
            if ($row == 1) continue; // bỏ header

            // Điều chỉnh thứ tự cột tùy theo file CSV của bạn
            $student_name = trim($data[0] ?? '');
            $student_sbd   = trim($data[1] ?? '');
            $student_class = trim($data[2] ?? '');
            $score         = floatval($data[3] ?? 0);
            $details_json  = $data[4] ?? '{}';   // cột details_json

            if (empty($student_name) || empty($student_sbd)) continue;

            $sql = "INSERT INTO exam_submissions 
                    (exam_id, student_name, student_sbd, student_class, score, details_json, submitted_at) 
                    VALUES (?, ?, ?, ?, ?, ?, NOW())";

            $stmt = $pdo->prepare($sql);
            $stmt->execute([
                $exam_id,
                $student_name,
                $student_sbd,
                $student_class,
                $score,
                $details_json
            ]);

            $imported++;
        }
        fclose($handle);
    }

    echo "<h3>Hoàn tất! Đã import $imported bản ghi.</h3>";
    echo "<a href='thitructuyen.html'>← Quay lại trang Thi trực tuyến</a>";
} else {
    // Form upload
    echo '
    <form method="post" enctype="multipart/form-data">
        <p>Chọn file CSV export từ Supabase:</p>
        <input type="file" name="csv_file" accept=".csv" required><br><br>
        
        <label>Exam ID (mặc định db776d2b):</label><br>
        <input type="text" name="exam_id" value="db776d2b" style="width:300px"><br><br>
        
        <button type="submit" style="padding:10px 20px; font-size:16px;">Import ngay</button>
    </form>
    <hr>
    <p><strong>Hướng dẫn:</strong></p>
    <ol>
        <li>Export bảng submissions từ Supabase ra CSV (UTF-8)</li>
        <li>Upload file CSV ở trên</li>
        <li>Chạy import</li>
    </ol>
    ';
}
?>