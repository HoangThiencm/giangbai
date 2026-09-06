# IMPLEMENT: Nạp phân công TKB toàn tổ + ảnh thông báo dạy thay (AI)

**Ngày implement**: 2026-09-06
**Coder**: Grok (xAI)
**Trạng thái**: DONE

## Tóm tắt

1. **Nạp phân công từ TKB toàn tổ (1-click)** trên Tab 1 và Tab 2; AI nhận diện TKB xong tự phiên lớp sang phân công khi checkbox bật (mặc định `checked`).
2. **Sổ Dạy Thay**: nút `Tạo ảnh thông báo (AI)` mở modal card sư phạm, soạn lời dặn dò bằng Gemini 2.5 Flash, copy ảnh / tải PNG / copy tin Zalo.

## Files

| File | Thay đổi |
|------|----------|
| `phancongtochuyenmon.html` | Nút nạp TKB toàn tổ, auto-apply, bóc ô/alias môn, html2canvas, modal `#substitute-announcement-modal`, JS tạo ảnh & AI |
| `docs/handoff/IMPLEMENT.md` | Ghi nhận implement |
| `docs/handoff/.lock` | Khóa lại |

Không sửa `api/phancong.php` / `api/khbd_gemini.php`. Không đổi cấu trúc JSON (`assignments`, `timetable`, `substitutes`).

## Chi tiết

### Phần 1
- Tab 1 `.live-stats-banner`: nút `⚡ Nạp phân công từ TKB toàn tổ`.
- Tab 2 `#tt-right-panel`: nút `⚡ Dịch TKB toàn tổ sang Phân công`; nhãn đơn lẻ `Dịch GV này sang Phân công`.
- Tab 2 `#tt-left-panel`: nút `⚡ Nạp phân công toàn tổ` dưới `#tt-progress`.
- `#tt-auto-apply-assign` mặc định `checked`.
- `applyAiTimetableResult`: nếu checkbox bật thì gọi `applyTimetableToAssignments(..., { silent: true, skipRender: true })` rồi toast phiên lớp.
- `syncAllAssignmentsFromTimetables`: `confirm()` theo tên đợt, đếm GV + lượt lớp, `rebuildUnassignedForSubject` toàn bộ môn, snapshot + `saveToLocal` + `render()`.
- `parseTimetableCell` / `splitSubjectAndClass`: `Toán 95`, `Toán 9A1`, `Toán/95`.
- `matchSubjectFromTimetableLabel`: alias `tin`→Tin học, `toan`→Toán, `hdtn`→HĐTN, `shl`/`sinh hoạt lớp`→Chủ nhiệm khi có lớp.

### Phần 2
- `html2canvas` 1.4.1 trên `<head>` (cùng CDN với `vehinh.html`).
- Toolbar Sổ Dạy Thay: `✨ Tạo ảnh thông báo (AI)`.
- Modal `#substitute-announcement-modal` + card `#dt-announcement-card`.
- Hàm: `openDayThayAnnouncementModal`, `closeDayThayAnnouncementModal`, `renderAnnouncementCard`, `generateDayThayAnnouncementAI` (`api/khbd_gemini.php`, `gemini-2.5-flash`), `copyAnnouncementImage` (clipboard PNG, fallback tải file), `downloadAnnouncementImage` (`Thong_Bao_Day_Thay_YYYYMMDD.png`), `copyAnnouncementZaloText`.

## Kiểm thử Coder

1. `node tests/smartquiz-smoke.js` → PASS.
2. 140 HTML ID, 0 trùng; JS parse (`vm.Script`) OK.
3. Unit `parseTimetableCell` / `matchSubjectFromTimetableLabel`: `Toán 95`/`9A1`/`Toán/95`; alias tin/toan/hdtn/shl.

Chưa chạy được trên trình duyệt thật (cần đăng nhập + Gemini + dữ liệu tổ). `/verify` theo *Cách kiểm thử* trong `PLAN.md`.
