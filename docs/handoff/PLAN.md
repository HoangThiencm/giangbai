# PLAN: Tích Hợp Lấy Danh Sách Học Sinh Từ Lớp Học CSDL Cho Game Đua Vịt (trochoi.html)

## 1. Hiện Trạng & Phân Tích Khả Thi

### Yêu cầu người dùng:
> *"Game đua vịt này có thể lấy danh sách từ lớp học của thitructuyen.html không? bổ sung thêm nút nạp từ lớp dạy CSDL"* (Kèm ảnh giao diện Đua Vịt `media_1790003283887.png`)

### Đánh giá tính khả thi:
- **Khả thi 100% và rất thuận tiện:**
  Hệ thống backend `api/exam.php` đã có sẵn 2 API chuẩn được chia sẻ dùng chung giữa `thitructuyen.html` và `sodiem.html`:
  1. `GET api/exam.php?route=student-classes`: Lấy danh sách tên các lớp học có học sinh hoạt động trong cơ sở dữ liệu (`users.class_name`).
  2. `GET api/exam.php?route=class-students&class_name={TÊN_LỚP}`: Lấy danh sách học sinh thuộc lớp đó (`student_id`, `full_name`, `username`, `sbd`, `class_name`).
- Hiện tại ở màn hình cấu hình Game Đua Vịt (`renderDuckSection` trong `trochoi.compiled.js`), hệ thống chỉ mới có 2 nút:
  * `[ ⌨️ Nhập tay ]`: Người dùng tự gõ/dán danh sách học sinh.
  * `[ 📊 Import Excel ]`: Người dùng tải file Excel danh sách lớp lên.
- Chưa có nút liên thông trực tiếp với CSDL lớp học như của `thitructuyen.html`.

---

## 2. Thiết Kế Giao Diện & Tính Năng

### 1. Bổ sung nút chuyển chế độ thứ 3: `[ 👥 Từ lớp học (CSDL) ]`
Tại khối chuyển đổi chế độ (`participantMode`), bổ sung nút thứ 3 bên cạnh "Nhập tay" và "Import Excel":
- Nút 1: `[ ⌨️ Nhập tay ]` (`participantMode === 'manual'`)
- Nút 2: `[ 📊 Import Excel ]` (`participantMode === 'excel'`)
- Nút 3: `[ 👥 Từ lớp dạy (CSDL) ]` (`participantMode === 'database'`)

### 2. Giao diện khi chọn `Từ lớp dạy (CSDL)` (`participantMode === 'database'`)
Hiển thị:
1. **Dropdown chọn lớp học:**
   - Khi chuyển sang chế độ này, tự động gọi API `api/exam.php?route=student-classes` (hoặc `api/sodiem.php?action=classes`).
   - Dropdown: `<select>` chứa danh sách các lớp đã tạo trong CSDL (ví dụ: `-- Chọn lớp dạy --`, `Lớp 6A`, `Lớp 6B`, `Lớp 9A`...).
   - Nút `🔄 Tải lại` kế bên để làm mới danh sách lớp nếu vừa thêm mới ở trang Admin/Sổ điểm.
2. **Trạng thái nạp học sinh:**
   - Khi giáo viên chọn 1 lớp (ví dụ `Lớp 6A`):
     - Gọi `api/exam.php?route=class-students&class_name=Lớp 6A` với `{ credentials: 'include' }`.
     - Nhận về danh sách `roster` gồm các học sinh của lớp.
     - Tự động đóng gói danh sách vịt:
       ```javascript
       const duckList = roster.map((st, idx) => ({
           id: `p${idx + 1}`,
           name: st.full_name || st.name,
           className: className
       }));
       setParticipants(duckList);
       setManualParticipantText(duckList.map(p => p.name).join('\n'));
       setParticipantClassHint(`Đã nạp ${duckList.length} học sinh từ ${className}.`);
       ```
     - Hiển thị thông báo màu xanh nhạt: *✅ Đã nạp thành công 35 học sinh từ Lớp 6A.*
3. **Tính linh hoạt:**
   - Sau khi nạp từ CSDL, tên học sinh tự động được đồng bộ vào `manualParticipantText`.
   - Nếu buổi học hôm đó có học sinh vắng hoặc thêm học sinh mới, giáo viên có thể bấm lại tab "Nhập tay" để sửa nhanh mà không làm mất danh sách đã nạp.

---

## 3. Các Bước Triển Khai Cho Coder

### Bước 1: Khai báo State và Hàm tải dữ liệu lớp học trong `trochoi.compiled.js`
- Thêm state:
  ```javascript
  const [dbClasses, setDbClasses] = useState([]);
  const [selectedDbClass, setSelectedDbClass] = useState('');
  const [loadingDbClasses, setLoadingDbClasses] = useState(false);
  const [participantClassHint, setParticipantClassHint] = useState('');
  ```
- Hàm nạp danh sách lớp:
  ```javascript
  const loadDbClasses = async () => {
      setLoadingDbClasses(true);
      try {
          const res = await fetch('api/exam.php?route=student-classes', { credentials: 'include' });
          if (!res.ok) throw new Error('Không thể tải danh sách lớp');
          const data = await res.json();
          const classes = Array.isArray(data.classes) ? data.classes : [];
          setDbClasses(classes);
          if (classes.length && !selectedDbClass) {
              // Có thể giữ trống để giáo viên chọn
          }
      } catch (err) {
          console.warn('Lỗi tải lớp từ CSDL:', err);
      } finally {
          setLoadingDbClasses(false);
      }
  };
  ```
- Hàm nạp học sinh theo lớp:
  ```javascript
  const handleSelectClass = async (className) => {
      setSelectedDbClass(className);
      if (!className) {
          setParticipantClassHint('');
          return;
      }
      setLoadingDbClasses(true);
      try {
          const res = await fetch(`api/exam.php?route=class-students&class_name=${encodeURIComponent(className)}`, { credentials: 'include' });
          if (!res.ok) throw new Error('Không thể tải danh sách học sinh của lớp');
          const data = await res.json();
          const roster = Array.isArray(data.roster) ? data.roster : [];
          if (!roster.length) {
              setParticipantClassHint(`Lớp ${className} chưa có học sinh trong CSDL.`);
              return;
          }
          const duckList = roster.map((st, idx) => ({
              id: `p${idx + 1}`,
              name: st.full_name || st.name,
              className: className
          }));
          setParticipants(duckList);
          setManualParticipantText(duckList.map(p => p.name).join('\n'));
          setParticipantClassHint(`Đã nạp ${duckList.length} học sinh từ ${className}.`);
      } catch (err) {
          alert('Lỗi nạp học sinh: ' + (err.message || err));
      } finally {
          setLoadingDbClasses(false);
      }
  };
  ```

### Bước 2: Cập nhật hàm `renderDuckSection` trong `trochoi.compiled.js`
- Thêm nút thứ 3:
  ```jsx
  <button
      type="button"
      onClick={() => { setParticipantMode('database'); if (!dbClasses.length) loadDbClasses(); }}
      className={`px-4 py-2 rounded-lg text-sm font-bold transition ${participantMode === 'database' ? 'bg-cyan-600 text-white' : 'bg-white text-cyan-800 border border-cyan-200'}`}
  >
      <i className="fas fa-database mr-1"></i>Từ lớp dạy (CSDL)
  </button>
  ```
- Render khối chọn lớp khi `participantMode === 'database'`:
  ```jsx
  participantMode === 'database' ? (
      <div className="space-y-3">
          <label className="block font-bold text-gray-700">Chọn lớp học từ cơ sở dữ liệu</label>
          <div className="flex gap-2 items-center">
              <select
                  value={selectedDbClass}
                  onChange={(e) => handleSelectClass(e.target.value)}
                  disabled={loadingDbClasses}
                  className="flex-1 p-2.5 border-2 border-gray-200 rounded-xl focus:border-cyan-500 outline-none bg-white text-sm font-medium"
              >
                  <option value="">-- Chọn lớp học ({dbClasses.length} lớp) --</option>
                  {dbClasses.map(cls => <option key={cls} value={cls}>{cls}</option>)}
              </select>
              <button
                  type="button"
                  onClick={loadDbClasses}
                  disabled={loadingDbClasses}
                  className="px-3 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl text-sm font-bold transition"
                  title="Tải lại danh sách lớp"
              >
                  <i className={`fas fa-sync-alt ${loadingDbClasses ? 'fa-spin' : ''}`}></i>
              </button>
          </div>
          {participantClassHint && (
              <p className="text-sm font-semibold text-cyan-800">{participantClassHint}</p>
          )}
          <p className="text-xs text-gray-500">
              Dữ liệu học sinh được đồng bộ từ danh sách lớp đã tạo ở phần Thi trực tuyến và Admin.
          </p>
      </div>
  ) : ...
  ```

---

## 4. Kế Hoạch Kiểm Thử (Verification Plan)
1. **Kiểm tra tải danh sách lớp:**
   - Mở `trochoi.html` $\rightarrow$ Chọn game "Đua Vịt Kiến Thức" $\rightarrow$ Xuất hiện khối "Danh sách học sinh đua vịt".
   - Bấm vào nút **"Từ lớp dạy (CSDL)"**.
   - Kiểm tra dropdown tự động nạp danh sách các lớp trong hệ thống (vd: 6A, 6B...).
2. **Kiểm tra nạp học sinh:**
   - Chọn 1 lớp bất kỳ trong dropdown.
   - Kiểm tra danh sách học sinh hiển thị ngay bên dưới (số lượng học sinh, tên học sinh `1. Nguyễn Văn An...`).
   - Bấm nút "Nhập tay" $\rightarrow$ Kiểm tra danh sách tên vẫn được lưu giữ trọn vẹn trong ô textarea.
3. **Kiểm tra bắt đầu game:**
   - Bấm "Tạo trò chơi ngay" hoặc chuyển sang xem trước $\rightarrow$ Game đua vịt khởi tạo thành công với đúng số lượng vịt tương ứng danh sách học sinh của lớp đã chọn.
