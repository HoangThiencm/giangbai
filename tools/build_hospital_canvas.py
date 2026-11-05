# -*- coding: utf-8 -*-
"""
Builder script to generate canvas_taobaocao_benhvien.html
Dedicated Hospital Administrative, Clinical, Planning & Regulation Assistant for Gemini Canvas.
"""
import os
import re

def build_hospital_canvas():
    source_path = os.path.join("backupcode viettailieu", "taobaocao.html")
    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"Read source taobaocao.html ({len(content)} chars)")

    # 1. Clean huge base64 signatures to make the file fast, lightweight (~400KB lighter)
    content = re.sub(
        r'<script id="embeddedSignatureAssets" type="application/json">\s*\{[\s\S]*?\}\s*</script>',
        r'<script id="embeddedSignatureAssets" type="application/json">\n{\n  "draftSignature": "",\n  "partyStamp": "",\n  "agencyStamp": ""\n}\n</script>',
        content
    )

    # 2. Update Title, Header Branding & Theme Meta
    content = content.replace(
        "<title>Trợ lý Hành Chính AI</title>",
        "<title>Trợ lý Soạn thảo Văn bản & Kế hoạch Bệnh viện (Gemini Canvas)</title>"
    )

    content = content.replace(
        "Đã kết nối Gemini Canvas – Môi trường mở rộng toàn màn hình",
        "Đã kết nối Gemini Canvas – Môi trường Soạn thảo Văn bản, Kế hoạch & Quy chế Bệnh viện (Y tế Chuyên sâu)"
    )

    content = content.replace(
        "Trợ lý Hành Chính AI",
        "Trợ lý Văn bản & Kế hoạch Bệnh viện"
    )

    # 3. Update preview and placeholders for Hospital
    content = content.replace(
        '<div class="org-name" id="setupPrevUnit">TRƯỜNG THCS TRẦN PHÚ</div>',
        '<div class="org-name" id="setupPrevUnit">BỆNH VIỆN ĐA KHOA TỈNH LÂM ĐỒNG</div>'
    )

    content = content.replace(
        '<div style="font-weight:bold; text-transform:uppercase;" id="setupPrevAuthority">HIỆU TRƯỞNG TRƯỜNG THCS TRẦN PHÚ</div>',
        '<div style="font-weight:bold; text-transform:uppercase;" id="setupPrevAuthority">GIÁM ĐỐC BỆNH VIỆN ĐA KHOA TỈNH LÂM ĐỒNG</div>'
    )

    content = content.replace(
        'placeholder="Cơ quan ban hành" value="TRƯỜNG THCS TRẦN PHÚ"',
        'placeholder="Cơ quan ban hành (VD: BỆNH VIỆN ĐA KHOA TỈNH...)" value="BỆNH VIỆN ĐA KHOA TỈNH LÂM ĐỒNG"'
    )

    content = content.replace(
        'placeholder="Cơ quan cấp trên" value="UBND XÃ XUÂN ĐÔNG"',
        'placeholder="Cơ quan cấp trên (VD: SỞ Y TẾ TỈNH...)" value="SỞ Y TẾ TỈNH LÂM ĐỒNG"'
    )

    content = content.replace(
        'placeholder="VD: HIỆU TRƯỞNG TRƯỜNG THCS TRẦN PHÚ"',
        'placeholder="VD: GIÁM ĐỐC BỆNH VIỆN ĐA KHOA TỈNH LÂM ĐỒNG"'
    )

    content = content.replace(
        'placeholder="VD: HIỆU TRƯỞNG"',
        'placeholder="VD: GIÁM ĐỐC BỆNH VIỆN"'
    )

    content = content.replace(
        'placeholder="VD: Bùi Ngọc Nam"',
        'placeholder="VD: BSCKII. Nguyễn Văn A"'
    )

    # 4. Update Account setup modal inputs & labels
    content = content.replace(
        'placeholder="VD: TRƯỜNG THCS TRẦN PHÚ"',
        'placeholder="VD: BỆNH VIỆN ĐA KHOA TỈNH LÂM ĐỒNG"'
    )

    content = content.replace(
        'placeholder="VD: CHI BỘ TRƯỜNG THCS TRẦN PHÚ"',
        'placeholder="VD: ĐẢNG BỘ BỆNH VIỆN ĐA KHOA TỈNH"'
    )

    content = content.replace(
        'placeholder="VD: UBND XÃ XUÂN ĐÔNG"',
        'placeholder="VD: SỞ Y TẾ TỈNH LÂM ĐỒNG"'
    )

    content = content.replace(
        'placeholder="VD: ĐẢNG ỦY XÃ XUÂN ĐÔNG"',
        'placeholder="VD: ĐẢNG ỦY KHỐI CÁC CƠ QUAN TỈNH"'
    )

    content = content.replace(
        'placeholder="VD: CHI BỘ THCS TRẦN PHÚ"',
        'placeholder="VD: ĐẢNG BỘ BỆNH VIỆN ĐA KHOA TỈNH"'
    )

    content = content.replace(
        '<label class="block text-sm font-semibold text-gray-700 mb-1">Số lớp</label>',
        '<label class="block text-sm font-semibold text-gray-700 mb-1">Số giường bệnh kế hoạch</label>'
    )
    content = content.replace('placeholder="VD: 15"', 'placeholder="VD: 500"')
    content = content.replace('placeholder="VD: 24"', 'placeholder="VD: 500"')

    content = content.replace(
        '<label class="block text-sm font-semibold text-gray-700 mb-1">Số học sinh</label>',
        '<label class="block text-sm font-semibold text-gray-700 mb-1">Giường thực kê / Lượt khám</label>'
    )
    content = content.replace('placeholder="VD: 615"', 'placeholder="VD: 580 thực kê (650 lượt khám/ngày)"')
    content = content.replace('placeholder="VD: 945"', 'placeholder="VD: 580 thực kê (650 lượt khám/ngày)"')

    content = content.replace(
        'Username / Tài khoản giáo viên (trên hoangthiencm.id.vn)',
        'Tài khoản cán bộ / nhân viên bệnh viện (hoặc chế độ Gemini Canvas tự do)'
    )

    content = content.replace(
        'Tài khoản giáo viên là <code>username</code> đăng ký trên hệ thống hoangthiencm.id.vn.',
        'Hệ thống tối ưu hóa hoàn toàn cho cán bộ, nhân viên, y bác sĩ và điều dưỡng Bệnh viện trên Gemini Canvas.'
    )

    content = content.replace(
        'placeholder="Nhập username đăng nhập (VD: tranphu_gv1)"',
        'placeholder="Nhập username đăng nhập (VD: bvdakhoa_cb1)"'
    )

    content = content.replace(
        '<h3 class="text-base font-bold text-slate-800">Tổ chuyên môn & Giáo viên</h3>',
        '<h3 class="text-base font-bold text-slate-800">Khoa / Phòng & Nhân lực Y tế</h3>'
    )

    content = content.replace(
        '<p class="text-xs text-slate-500 mb-2">Excel gợi ý: cột `Tên tổ`, `Giáo viên`.</p>',
        '<p class="text-xs text-slate-500 mb-2">Excel gợi ý: cột `Tên Khoa/Phòng`, `Bác sĩ / Nhân viên y tế`.</p>'
    )

    content = content.replace(
        'Sheet gợi ý: `BanGiamHieu`, `ToChuyenMon`, `NhanVien`, `DangVien`.',
        'Sheet gợi ý: `BanGiamDoc`, `KhoaPhong`, `NhanVien`, `DangVien`.'
    )

    content = content.replace(
        '<h3 class="text-base font-bold text-slate-800">Ban Giám hiệu</h3>',
        '<h3 class="text-base font-bold text-slate-800">Ban Giám đốc Bệnh viện</h3>'
    )

    content = content.replace(
        '<h3 class="text-base font-bold text-slate-800">Nhân viên & Vị trí</h3>',
        '<h3 class="text-base font-bold text-slate-800">Vị trí then chốt & Hội đồng chuyên môn</h3>'
    )

    content = content.replace(
        '<label class="block text-sm font-semibold text-gray-700 mb-1">Bí thư Đoàn trường</label>',
        '<label class="block text-sm font-semibold text-gray-700 mb-1">Bí thư Đoàn Thanh niên BV</label>'
    )

    content = content.replace(
        '<label class="block text-sm font-semibold text-gray-700 mb-1">Tổng phụ trách Đội</label>',
        '<label class="block text-sm font-semibold text-gray-700 mb-1">Điều dưỡng trưởng Bệnh viện</label>'
    )

    content = content.replace(
        'placeholder="VD: Lập kế hoạch tuần tra ATGT của trường..."',
        'placeholder="VD: Kế hoạch triển khai kiểm soát nhiễm khuẩn và vệ sinh tay toàn viện năm 2026..."'
    )

    content = content.replace(
        'placeholder="VD: Quyết định chuyển đổi số mẫu của trường A để tham khảo cấu trúc và nội dung..."',
        'placeholder="VD: Quyết định ban hành Quy chế chuyên môn thường trực 24/24 và quy trình Báo động đỏ cấp cứu mẫu..."'
    )

    content = content.replace(
        'setAccountSettingsStatus("Hãy nhập username tài khoản giáo viên trước khi kiểm tra Hosting.", "error");',
        'setAccountSettingsStatus("Hãy nhập username tài khoản bệnh viện trước khi kiểm tra Hosting.", "error");'
    )

    # 5. Update Scheme dropdown in Step 1
    old_scheme_select = """<select id="docSchemeSelect"
                    class="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-purple-500 font-bold text-blue-700"
                    onchange="handleDocSchemeChange()">
                    <option value="HANH_CHINH" selected>Hành chính</option>
                    <option value="HOANG_THIEN">HOÀNG THIÊN</option>
                    <option value="DANG">Đảng</option>
                    <option value="DOAN">Đoàn</option>
                    <option value="MATTRAN">Mặt trận</option>
                    <option value="HOP_DONG">Hợp đồng</option>
                </select>"""
    new_scheme_select = """<select id="docSchemeSelect"
                    class="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-teal-500 font-bold text-teal-800 bg-teal-50/50"
                    onchange="handleDocSchemeChange()">
                    <option value="BENH_VIEN" selected>🏥 Bệnh viện & Chuyên môn Y tế</option>
                    <option value="HANH_CHINH">🏛️ Hành chính - Văn thư Bệnh viện</option>
                    <option value="DANG">⭐ Đảng bộ Bệnh viện</option>
                    <option value="CONG_DOAN">🤝 Công đoàn ngành Y tế</option>
                    <option value="DOAN_TN">🌱 Đoàn Thanh niên Bệnh viện</option>
                    <option value="HOP_DONG">📑 Hợp đồng & Mua sắm Y tế</option>
                </select>"""
    content = content.replace(old_scheme_select, new_scheme_select)

    # 6. Add Quick Hospital Presets in Step 1
    quick_presets = """
        <!-- THANH PHÍM TẮT MẪU BỆNH VIỆN NHANH -->
        <div class="mb-5 p-3.5 bg-gradient-to-r from-teal-900/90 via-cyan-900/80 to-blue-900/90 rounded-2xl border border-teal-500/30 text-white shadow-lg">
            <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                    <span class="flex h-7 w-7 items-center justify-center rounded-lg bg-teal-500 text-white text-sm shadow"><i class="fas fa-notes-medical"></i></span>
                    <span class="text-xs font-bold uppercase tracking-wider text-teal-200">Mẫu nghiệp vụ Bệnh viện (Nạp nhanh 1-Click):</span>
                </div>
                <span class="text-[11px] text-teal-300/80 italic hidden sm:inline">* Tự động điền trích yếu, thể thức & cấu hình chuẩn</span>
            </div>
            <div class="flex flex-wrap gap-2 pt-1">
                <button type="button" onclick="applyHospitalPreset('KH_CHAT_LUONG')" class="px-2.5 py-1.5 bg-white/10 hover:bg-teal-500 hover:text-white text-teal-100 rounded-lg text-xs font-semibold border border-white/10 transition flex items-center gap-1.5 shadow-sm">
                    <i class="fas fa-award text-yellow-400"></i> Kế hoạch 83 Tiêu chí Chất lượng
                </button>
                <button type="button" onclick="applyHospitalPreset('KH_KSNK')" class="px-2.5 py-1.5 bg-white/10 hover:bg-teal-500 hover:text-white text-teal-100 rounded-lg text-xs font-semibold border border-white/10 transition flex items-center gap-1.5 shadow-sm">
                    <i class="fas fa-shield-virus text-emerald-400"></i> Kế hoạch Kiểm soát nhiễm khuẩn (TT 16)
                </button>
                <button type="button" onclick="applyHospitalPreset('QC_TRUC')" class="px-2.5 py-1.5 bg-white/10 hover:bg-teal-500 hover:text-white text-teal-100 rounded-lg text-xs font-semibold border border-white/10 transition flex items-center gap-1.5 shadow-sm">
                    <i class="fas fa-clock text-blue-400"></i> Quy chế Thường trực 24/24 & Báo động đỏ
                </button>
                <button type="button" onclick="applyHospitalPreset('KH_EMR')" class="px-2.5 py-1.5 bg-white/10 hover:bg-teal-500 hover:text-white text-teal-100 rounded-lg text-xs font-semibold border border-white/10 transition flex items-center gap-1.5 shadow-sm">
                    <i class="fas fa-laptop-medical text-cyan-400"></i> Kế hoạch Bệnh án điện tử (EMR)
                </button>
                <button type="button" onclick="applyHospitalPreset('QD_HOI_DONG')" class="px-2.5 py-1.5 bg-white/10 hover:bg-teal-500 hover:text-white text-teal-100 rounded-lg text-xs font-semibold border border-white/10 transition flex items-center gap-1.5 shadow-sm">
                    <i class="fas fa-users-gear text-amber-400"></i> QĐ Kiện toàn Hội đồng Thuốc & ĐT
                </button>
                <button type="button" onclick="applyHospitalPreset('BC_SU_CO')" class="px-2.5 py-1.5 bg-white/10 hover:bg-teal-500 hover:text-white text-teal-100 rounded-lg text-xs font-semibold border border-white/10 transition flex items-center gap-1.5 shadow-sm">
                    <i class="fas fa-triangle-exclamation text-rose-400"></i> Báo cáo Sự cố y khoa (TT 43)
                </button>
                <button type="button" onclick="applyHospitalPreset('BB_HOI_CHAN')" class="px-2.5 py-1.5 bg-white/10 hover:bg-teal-500 hover:text-white text-teal-100 rounded-lg text-xs font-semibold border border-white/10 transition flex items-center gap-1.5 shadow-sm">
                    <i class="fas fa-stethoscope text-indigo-400"></i> Biên bản Hội chẩn ca bệnh nặng
                </button>
                <button type="button" onclick="applyHospitalPreset('TTR_MUA_SAM')" class="px-2.5 py-1.5 bg-white/10 hover:bg-teal-500 hover:text-white text-teal-100 rounded-lg text-xs font-semibold border border-white/10 transition flex items-center gap-1.5 shadow-sm">
                    <i class="fas fa-file-invoice-dollar text-purple-400"></i> Tờ trình Mua sắm TBYT kỹ thuật cao
                </button>
            </div>
        </div>
    """
    content = content.replace(
        '<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">',
        quick_presets + '\n        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">',
        1
    )

    # 7. Add styleSelect option for BENH_VIEN
    old_style_radios = """<label class="flex-1 cursor-pointer">
                        <input type="radio" name="styleSelect" value="hanh_chinh" checked class="peer sr-only" />"""
    new_style_radios = """<label class="flex-1 cursor-pointer">
                        <input type="radio" name="styleSelect" value="benh_vien" checked class="peer sr-only" />
                        <div
                            class="p-3 border-2 border-teal-300 rounded-lg peer-checked:border-teal-600 peer-checked:bg-teal-50 transition-all hover:bg-gray-50">
                            <div class="flex items-center gap-2">
                                <span class="text-2xl">🏥</span>
                                <div>
                                    <div class="font-bold text-teal-900">Quản trị Y tế & Bệnh viện</div>
                                    <div class="text-xs text-teal-700">Chuẩn Bộ Y tế, 83 tiêu chí, an toàn người bệnh</div>
                                </div>
                            </div>
                        </div>
                    </label>

                    <label class="flex-1 cursor-pointer">
                        <input type="radio" name="styleSelect" value="hanh_chinh" class="peer sr-only" />"""
    content = content.replace(old_style_radios, new_style_radios)

    # 8. Replace DEFAULT_ACCOUNT_PROFILE_SEED with Comprehensive Hospital Seed
    old_seed_start = content.find("const DEFAULT_ACCOUNT_PROFILE_SEED = {")
    old_seed_end = content.find("};", old_seed_start)
    if old_seed_start != -1 and old_seed_end != -1:
        new_seed = """const DEFAULT_ACCOUNT_PROFILE_SEED = {
            unit_name: "BỆNH VIỆN ĐA KHOA TỈNH LÂM ĐỒNG",
            unit_parent: "SỞ Y TẾ TỈNH LÂM ĐỒNG",
            party_parent: "ĐẢNG ỦY KHỐI CÁC CƠ QUAN TỈNH",
            chi_bo: "ĐẢNG BỘ BỆNH VIỆN ĐA KHOA TỈNH",
            class_count: "500", // Số giường bệnh kế hoạch
            student_count: "580 giường thực kê (Công suất 108%, 650 lượt khám/ngày)",
            board_members: "",
            board_member_items: [
                { name: "BSCKII. Nguyễn Văn A", title: "Giám đốc Bệnh viện (Phụ trách chung, TCCB, TCKT)" },
                { name: "BSCKII. Trần Thị B", title: "Phó Giám đốc (Phụ trách Chuyên môn Khám chữa bệnh & KHTH)" },
                { name: "BSCKI. Lê Văn C", title: "Phó Giám đốc (Phụ trách Ngoại khoa, Dược & Trang thiết bị y tế)" },
                { name: "ThS. Phạm Hoàng D", title: "Phó Giám đốc (Phụ trách Hậu cần, Quản trị, EMR & PCCC)" }
            ],
            departments: "",
            department_teachers: "",
            department_items: [
                { name: "Phòng Kế hoạch tổng hợp", teachers: "BSCKI. Vũ Hoàng Minh (Trưởng phòng), BS. Trần Mai Linh, CN. Lê Thu Hà" },
                { name: "Phòng Quản lý chất lượng & ATNB", teachers: "ThS.BS. Đặng Quốc Huy (Trưởng phòng), CNĐD. Nguyễn Bích Ngọc, ThS. Hoàng Tuấn" },
                { name: "Phòng Điều dưỡng", teachers: "CNĐD. Phạm Thị Thanh Tâm (Trưởng phòng), CNĐD. Lê Thị Mai, ĐD. Vũ Hồng Nhung" },
                { name: "Phòng Tổ chức cán bộ", teachers: "ThS. Đỗ Quang Hưng (Trưởng phòng), CN. Trịnh Văn Nam, CN. Bùi Thị Huệ" },
                { name: "Phòng Tài chính - Kế toán", teachers: "Cử nhân KT. Nguyễn Thị Hương (Trưởng phòng), KTV. Phan Minh Đức, KTV. Lê Thùy Dung" },
                { name: "Phòng Hành chính quản trị", teachers: "KS. Hoàng Văn Thắng (Trưởng phòng), CN. Đinh Văn Toàn, NV. Nguyễn Văn Cường" },
                { name: "Phòng Vật tư - Thiết bị y tế", teachers: "KS. Trần Hữu Phúc (Trưởng phòng), KS. Đỗ Tuấn Anh, KTV. Mai Thanh Tùng" },
                { name: "Phòng Công nghệ thông tin", teachers: "KS. Vũ Thái Bình (Trưởng phòng), KS. Nguyễn Đức Long, CN. Đào Hải Yến" },
                { name: "Phòng Công tác xã hội", teachers: "CN. Lâm Mỹ Duyên (Trưởng phòng), CN. Phan Thị Hòa, NV. Lê Văn Quân" },
                { name: "Khoa Khám bệnh - Cấp cứu", teachers: "BSCKII. Phạm Minh Tuấn (Trưởng khoa), BSCKI. Lê Quốc Bảo, ĐDT. Trần Thị Thu" },
                { name: "Khoa Hồi sức tích cực - Chống độc (ICU)", teachers: "BSCKII. Nguyễn Hữu Trí (Trưởng khoa), BSCKI. Đỗ Hải Nam, ĐDT. Hoàng Mai Phương" },
                { name: "Khoa Nội tổng hợp", teachers: "BSCKI. Trần Đức Thắng (Trưởng khoa), ThS.BS. Nguyễn Thị Ngọc, ĐDT. Vũ Thị Duyên" },
                { name: "Khoa Ngoại tổng hợp", teachers: "BSCKII. Lê Đình Chiến (Trưởng khoa), BSCKI. Phạm Anh Dũng, ĐDT. Bùi Văn Hùng" },
                { name: "Khoa Phẫu thuật - Gây mê hồi sức", teachers: "BSCKI. Ngô Tiến Đạt (Trưởng khoa), BSCKI. Nguyễn Thanh Hằng, KTVT. Phan Văn Khải" },
                { name: "Khoa Phụ sản", teachers: "BSCKI. Dương Thị Lan (Trưởng khoa), BS. Đỗ Thúy Quỳnh, HST. Mai Thị Bích" },
                { name: "Khoa Nhi", teachers: "BSCKI. Vũ Thị Hà (Trưởng khoa), ThS.BS. Phạm Hồng Anh, ĐDT. Nguyễn Thị Trang" },
                { name: "Khoa Dược", teachers: "DSCKI. Nguyễn Tuấn Kiệt (Trưởng khoa), DSĐH. Lê Phương Thảo, DS. Trần Ngọc Sang" },
                { name: "Khoa Xét nghiệm", teachers: "ThS.BS. Hoàng Trung Kiên (Trưởng khoa), KTVT. Đặng Thị Nga, KTV. Lưu Hải Đăng" },
                { name: "Khoa Chẩn đoán hình ảnh", teachers: "BSCKI. Tạ Quang Vinh (Trưởng khoa), KTVT. Nguyễn Văn Bình, KTV. Lê Thị Thoa" },
                { name: "Khoa Kiểm soát nhiễm khuẩn", teachers: "BS. Đỗ Thị Minh Hòa (Trưởng khoa), CN. Bùi Quốc Việt, ĐD. Phạm Thu Hương" }
            ],
            youth_secretary: "BS. Nguyễn Văn Tùng (Bí thư Đoàn Thanh niên BV)",
            head_teacher: "CNĐD. Phạm Thị Thanh Tâm (Điều dưỡng trưởng Bệnh viện)",
            staff_list: "",
            staff_items: [
                { name: "Cử nhân KT. Nguyễn Thị Hương", position: "Kế toán trưởng Bệnh viện" },
                { name: "CNĐD. Phạm Thị Thanh Tâm", position: "Điều dưỡng trưởng Bệnh viện" },
                { name: "DSCKI. Nguyễn Tuấn Kiệt", position: "Phụ trách kho thuốc BHYT & Dược lâm sàng" },
                { name: "KS. Trần Hữu Phúc", position: "Phụ trách An toàn bức xạ & Thiết bị y tế kỹ thuật cao" },
                { name: "KS. Vũ Thái Bình", position: "Phụ trách An toàn thông tin mạng & EMR (Bệnh án điện tử)" },
                { name: "NV. Đinh Văn Toàn", position: "Đội trưởng Đội PCCC & An ninh trật tự BV" },
                { name: "Lái xe Nguyễn Văn Cường", position: "Tổ trưởng Tổ xe cấp cứu cứu thương 24/24" }
            ],
            party_members: "",
            party_member_items: [
                { name: "BSCKII. Nguyễn Văn A", role: "Bí thư Đảng ủy - Giám đốc Bệnh viện" },
                { name: "BSCKII. Trần Thị B", role: "Phó Bí thư Đảng ủy - Phó Giám đốc BV" },
                { name: "BSCKI. Vũ Hoàng Minh", role: "Đảng ủy viên - Trưởng phòng KHTH" },
                { name: "ThS.BS. Đặng Quốc Huy", role: "Bí thư Chi bộ Khối Phòng ban" },
                { name: "BSCKII. Phạm Minh Tuấn", role: "Bí thư Chi bộ Khối Cấp cứu - ICU" },
                { name: "BSCKII. Lê Đình Chiến", role: "Bí thư Chi bộ Khối Ngoại - Sản" },
                { name: "DSCKI. Nguyễn Tuấn Kiệt", role: "Bí thư Chi bộ Khối Dược - Cận lâm sàng" }
            ]
        };"""
        content = content[:old_seed_start] + new_seed + content[old_seed_end + 2:]
        print("Replaced DEFAULT_ACCOUNT_PROFILE_SEED with Hospital seed.")

    # 9. Replace DOC_TYPE_CATALOG
    old_cat_start = content.find("const DOC_TYPE_CATALOG = {")
    old_cat_end = content.find("const CONTRACT_BASE_PROFILE = {", old_cat_start)
    if old_cat_start != -1 and old_cat_end != -1:
        new_cat = """const DOC_TYPE_CATALOG = {
            BENH_VIEN: {
                badge: "BV",
                types: [
                    "KẾ HOẠCH BỆNH VIỆN",
                    "QUY CHẾ CHUYÊN MÔN",
                    "QUY TRÌNH KỸ THUẬT (SOP)",
                    "QUY ĐỊNH BỆNH VIỆN",
                    "QUYẾT ĐỊNH Y TẾ",
                    "BÁO CÁO KHÁM CHỮA BỆNH",
                    "BÁO CÁO SỰ CỐ Y KHOA",
                    "BÁO CÁO KIỂM SOÁT NHIỄM KHUẨN",
                    "TỜ TRÌNH Y TẾ",
                    "BIÊN BẢN HỘI CHẨN",
                    "BIÊN BẢN KIỂM THẢO TỬ VONG",
                    "DANH MỤC THUỐC - VẬT TƯ",
                    "LỊCH TRỰC CHUYÊN MÔN 24/24"
                ]
            },
            HANH_CHINH: {
                badge: "HC",
                types: [
                    "THÔNG BÁO",
                    "QUYẾT ĐỊNH",
                    "DANH SÁCH",
                    "DANH MỤC",
                    "CÔNG VĂN",
                    "TỜ TRÌNH",
                    "BÁO CÁO",
                    "ĐỀ CƯƠNG BÁO CÁO",
                    "KẾ HOẠCH",
                    "HƯỚNG DẪN",
                    "QUY CHẾ",
                    "QUY ĐỊNH",
                    "BIÊN BẢN",
                    "GIẤY MỜI",
                    "GIẤY GIỚI THIỆU",
                    "PHỤ LỤC",
                    "NGHỊ QUYẾT",
                    "BẢN CAM KẾT"
                ]
            },
            DANG: {
                badge: "Đ",
                types: ["NGHỊ QUYẾT", "CHỈ THỊ", "KẾ HOẠCH", "BÁO CÁO", "TỜ TRÌNH", "QUYẾT ĐỊNH", "BẢN CAM KẾT"]
            },
            CONG_DOAN: {
                badge: "CĐ",
                types: ["KẾ HOẠCH", "BÁO CÁO", "THÔNG BÁO", "TỜ TRÌNH", "QUYẾT ĐỊNH"]
            },
            DOAN_TN: {
                badge: "ĐT",
                types: ["KẾ HOẠCH", "THÔNG BÁO", "TỜ TRÌNH", "BIÊN BẢN", "BÁO CÁO", "BẢN CAM KẾT"]
            },
            HOP_DONG: {
                badge: "HĐ",
                types: [
                    "HỢP ĐỒNG CUNG CẤP THUỐC - VẬT TƯ",
                    "HỢP ĐỒNG BẢO TRÌ THIẾT BỊ Y TẾ",
                    "HỢP ĐỒNG DỊCH VỤ XỬ LÝ RÁC THẢI Y TẾ",
                    "HỢP ĐỒNG LAO ĐỘNG BÁC SĨ - ĐIỀU DƯỠNG",
                    "HỢP ĐỒNG THỬ VIỆC",
                    "HỢP ĐỒNG DỊCH VỤ GIẶT LÀ - SUẤT ĂN",
                    "HỢP ĐỒNG MUA BÁN",
                    "BIÊN BẢN NGHIỆM THU",
                    "THANH LÝ HỢP ĐỒNG"
                ]
            }
        };\n\n        """
        content = content[:old_cat_start] + new_cat + content[old_cat_end:]
        print("Replaced DOC_TYPE_CATALOG with Hospital catalog.")

    # 10. Add Hospital Profiles into DOCUMENT_PROFILES
    hospital_profiles = """
            "KẾ HOẠCH BỆNH VIỆN": {
                defaultMode: "strict_nd30", lengthMode: "long",
                questions: [
                    "Mục tiêu cụ thể của kế hoạch (chất lượng 83 tiêu chí, KSNK, an toàn người bệnh, CME, đấu thầu thuốc/vật tư, EMR, cấp cứu thảm họa...) là gì?",
                    "Chỉ tiêu chuyên môn lâm sàng/cận lâm sàng, phạm vi áp dụng tại các khoa/phòng và thời gian thực hiện ra sao?",
                    "Các hoạt động trọng tâm, giải pháp kỹ thuật và nguồn lực (kinh phí, nhân lực y tế, trang thiết bị) như thế nào?",
                    "Đơn vị chủ trì (KHTH, QLCL, Điều dưỡng, Dược, KSNK...), đơn vị phối hợp và tiêu chí nghiệm thu đánh giá kết quả là gì?"
                ],
                appendixCandidates: ["BẢNG PHÂN CÔNG", "TIẾN ĐỘ THỰC HIỆN", "DANH MỤC THUỐC - VẬT TƯ", "DANH SÁCH"],
                guide: `*** KHUNG RIÊNG CHO KẾ HOẠCH BỆNH VIỆN ***\\n- Bố cục chuẩn Bộ Y tế & NĐ 30: Căn cứ pháp lý (Luật Khám bệnh, chữa bệnh số 15/2023/QH15, Bộ tiêu chí chất lượng QĐ 6858, Thông tư chuyên môn) -> Mục đích, Yêu cầu -> Chỉ tiêu & Nhiệm vụ trọng tâm -> Giải pháp kỹ thuật, chuyên môn, nhân lực, cơ sở vật chất, tài chính -> Tiến độ & Phân công trách nhiệm các Khoa/Phòng -> Tổ chức thực hiện, chế độ báo cáo.\\n- Tuyệt đối không xuất bảng Markdown trong body kế hoạch; toàn bộ phân công, tiến độ hoặc định mức dài tách thành Phụ lục.\\n- Số liệu chỉ tiêu phải rõ ràng (công suất giường bệnh, tỷ lệ nhiễm khuẩn bệnh viện, tỷ lệ hài lòng người bệnh...); không bịa số liệu tùy tiện.`
            },
            "QUY CHẾ CHUYÊN MÔN": {
                defaultMode: "strict_nd30", lengthMode: "long",
                questions: [
                    "Quy chế chuyên môn điều chỉnh hoạt động nào (thường trực 24/24, cấp cứu & báo động đỏ, hội chẩn, chuyển tuyến, phẫu thuật - thủ thuật, kê đơn thuốc, quản lý hồ sơ bệnh án)?",
                    "Đối tượng áp dụng (Bác sĩ, Điều dưỡng, Dược sĩ, Kỹ thuật viên, Lãnh đạo khoa/phòng) là ai?",
                    "Quy trình, nguyên tắc bắt buộc, các hành vi nghiêm cấm và chế độ báo cáo xử lý khi có tình huống khẩn cấp/tai biến y khoa là gì?",
                    "Trách nhiệm của Trưởng khoa/phòng, Hội đồng chuyên môn và Giám đốc Bệnh viện trong giám sát thực hiện ra sao?"
                ],
                appendixCandidates: ["BIỂU MẪU", "DANH MỤC"],
                guide: `*** KHUNG RIÊNG CHO QUY CHẾ CHUYÊN MÔN BỆNH VIỆN ***\\n- Tổ chức theo Chương, Điều. Chương I: Quy định chung (phạm vi, đối tượng, nguyên tắc an toàn người bệnh); Chương II: Các quy định chuyên môn cụ thể (tiêu chuẩn, quy trình thao tác, thời gian đáp ứng cấp cứu, hồ sơ lưu trữ); Chương III: Trách nhiệm và quyền hạn của các chức danh; Chương IV: Tổ chức thực hiện, khen thưởng và xử lý vi phạm.\\n- Ngôn từ mang tính quy phạm nội bộ bệnh viện, chuẩn xác thuật ngữ y khoa, tuyệt đối không dùng lời văn vận động.`
            },
            "QUY TRÌNH KỸ THUẬT (SOP)": {
                defaultMode: "strict_nd30", lengthMode: "long",
                questions: [
                    "Tên quy trình kỹ thuật chuyên môn là gì (VD: Cấp cứu ngừng tuần hoàn, Thở máy xâm nhập, Lọc máu liên tục, An toàn phẫu thuật 3 bước, Tiệt khuẩn dụng cụ nội soi...)?",
                    "Chỉ định, chống chỉ định và đối tượng người bệnh áp dụng là gì?",
                    "Các bước chuẩn bị (nhân lực, trang thiết bị y tế, thuốc men, vật tư tiêu hao, người bệnh và hồ sơ bệnh án) gồm những gì?",
                    "Trình tự các bước thực hiện kỹ thuật và cách theo dõi, phát hiện, xử trí tai biến/biến chứng sau thủ thuật là gì?"
                ],
                appendixCandidates: ["BIỂU MẪU BẢNG KIỂM (CHECKLIST)", "DANH MỤC DỤNG CỤ"],
                guide: `*** KHUNG RIÊNG CHO QUY TRÌNH KỸ THUẬT (SOP) Y TẾ ***\\n- Bố cục chuẩn SOP Bộ Y tế: 1. Đại cương; 2. Chỉ định; 3. Chống chỉ định; 4. Chuẩn bị (người thực hiện, phương tiện/thuốc/vật tư, người bệnh, hồ sơ bệnh án); 5. Các bước tiến hành (thao tác chi tiết, định lượng thời gian, liều lượng chuẩn); 6. Theo dõi và chăm sóc sau thủ thuật; 7. Tai biến và cách xử trí.\\n- Trình bày mạch lạc, từng bước rõ ràng, dễ đối chiếu khi thực hành lâm sàng.`
            },
            "QUY ĐỊNH BỆNH VIỆN": {
                defaultMode: "strict_nd30", lengthMode: "long",
                questions: [
                    "Quy định điều chỉnh nội dung nào (văn hóa giao tiếp y đức QĐ 2151, quản lý thuốc gây nghiện - hướng thần, báo cáo sự cố y khoa không trừng phạt, phân loại rác thải y tế, chi tiêu nội bộ NĐ 60)?",
                    "Phạm vi, đối tượng áp dụng và các hành vi bắt buộc / nghiêm cấm là gì?",
                    "Quy trình kiểm tra, giám sát và chế tài xử lý khi vi phạm quy định ra sao?"
                ],
                appendixCandidates: ["BIỂU MẪU", "DANH MỤC"],
                guide: `*** KHUNG RIÊNG CHO QUY ĐỊNH BỆNH VIỆN ***\\n- Bố cục theo Chương/Điều. Nêu rõ trách nhiệm của cán bộ, nhân viên y tế, người bệnh và thân nhân người bệnh (nếu có liên quan).\\n- Lời văn pháp quy, chặt chẽ, gắn liền với đạo đức người thầy thuốc và quy định của ngành Y tế.`
            },
            "QUYẾT ĐỊNH Y TẾ": {
                defaultMode: "strict_nd30", lengthMode: "decision",
                questions: [
                    "Thẩm quyền ban hành: Giám đốc Bệnh viện (hoặc Chủ tịch Hội đồng)?",
                    "Nội dung quyết định: Thành lập/kiện toàn Hội đồng chuyên môn, Ban hành quy trình kỹ thuật SOP, Phê duyệt danh mục kỹ thuật/thuốc, Phân công trực 24/24, Khen thưởng cấp cứu?",
                    "Khoa, phòng, đơn vị và các cá nhân chịu trách nhiệm thi hành là ai?",
                    "Thời điểm có hiệu lực thi hành của Quyết định là khi nào?"
                ],
                appendixCandidates: ["DANH SÁCH THÀNH VIÊN", "DANH MỤC KỸ THUẬT/THUỐC", "BẢNG PHÂN CÔNG"],
                guide: `*** KHUNG RIÊNG CHO QUYẾT ĐỊNH Y TẾ ***\\n- Căn cứ pháp lý chuẩn: Luật Khám bệnh, chữa bệnh 15/2023/QH15, Quyết định thành lập bệnh viện, Quy chế tổ chức hoạt động và Nghị định 30/2020/NĐ-CP.\\n- Sau căn cứ là dòng QUYẾT ĐỊNH: in đậm, căn giữa.\\n- Điều 1: Nội dung quyết định chính thức; Điều 2: Quyền hạn, trách nhiệm chi tiết (hoặc ban hành kèm Quy chế/Danh mục); Điều 3: Hiệu lực và trách nhiệm thi hành (Trưởng phòng KHTH, TCCB, TCKT, các Trưởng khoa/phòng liên quan và các cá nhân chịu trách nhiệm).`
            },
            "BÁO CÁO KHÁM CHỮA BỆNH": {
                defaultMode: "strict_nd30", lengthMode: "long",
                questions: [
                    "Báo cáo khám chữa bệnh thuộc kỳ nào (tháng, quý, 6 tháng, năm) và phạm vi toàn viện hay khoa phòng?",
                    "Các số liệu lâm sàng chủ yếu (lượt khám ngoại trú, bệnh nhân nội trú, số ca cấp cứu, số ca phẫu thuật/thủ thuật, ngày điều trị trung bình, công suất giường bệnh) là bao nhiêu?",
                    "Kết quả hoạt động của cận lâm sàng, dược, kiểm soát nhiễm khuẩn, quản lý chất lượng và BHYT đạt mức nào?",
                    "Những ca bệnh khó, kỹ thuật mới triển khai thành công, các tồn tại hạn chế và đề xuất giải pháp phương hướng kỳ tới là gì?"
                ],
                appendixCandidates: ["BẢNG SỐ LIỆU CHI TIẾT", "DANH MỤC KỸ THUẬT MỚI", "KIẾN NGHỊ"],
                guide: `*** KHUNG RIÊNG CHO BÁO CÁO KHÁM CHỮA BỆNH ***\\n- Bố cục chuẩn: I. Tình hình chung & Quy mô hoạt động; II. Kết quả công tác khám chữa bệnh (Khối Khám bệnh - Cấp cứu, Khối Nội, Khối Ngoại - Sản, Cận lâm sàng & Dược, Triển khai kỹ thuật mới, Công tác BHYT, KSNK & QLCL); III. Đánh giá ưu điểm, khó khăn, tồn tại & Phân tích nguyên nhân; IV. Phương hướng, nhiệm vụ trọng tâm và chỉ tiêu chuyên môn kỳ tiếp theo.\\n- Mọi nhận định chuyên môn phải gắn với số liệu thực tế; không dùng mỹ từ chung chung.`
            },
            "BÁO CÁO SỰ CỐ Y KHOA": {
                defaultMode: "strict_nd30", lengthMode: "standard",
                questions: [
                    "Sự cố y khoa xảy ra tại khoa/phòng nào, vào thời điểm nào và mức độ tổn thương của người bệnh (NC0 đến NC6 theo Thông tư 43/2018/TT-BYT) là gì?",
                    "Mô tả ngắn gọn diễn biến sự cố và các biện pháp xử trí cấp cứu tức thì đã thực hiện?",
                    "Phân tích nguyên nhân gốc rễ (Root Cause Analysis - con người, quy trình, trang thiết bị, môi trường, thông tin liên lạc)?",
                    "Hành động khắc phục, phòng ngừa tái diễn và bài học kinh nghiệm toàn viện là gì?"
                ],
                appendixCandidates: ["BIÊN BẢN HỌP XỬ TRÍ", "BẢNG PHÂN TÍCH NGUYÊN NHÂN"],
                guide: `*** KHUNG RIÊNG CHO BÁO CÁO SỰ CỐ Y KHOA (TT 43/2018/TT-BYT) ***\\n- Tinh thần bắt buộc: Văn phong khách quan, trung thực, mang tính xây dựng cải tiến hệ thống theo nguyên tắc 'KHÔNG TRỪNG PHẠT' (No-blame culture).\\n- Bố cục: 1. Thông tin chung; 2. Tóm tắt diễn biến sự cố; 3. Xử trí tức thời; 4. Đánh giá mức độ tổn thương theo phân loại Bộ Y tế; 5. Phân tích nguyên nhân trực tiếp và nguyên nhân gốc rễ; 6. Kế hoạch hành động khắc phục và giải pháp phòng ngừa tái diễn.`
            },
            "BÁO CÁO KIỂM SOÁT NHIỄM KHUẨN": {
                defaultMode: "strict_nd30", lengthMode: "long",
                questions: [
                    "Kỳ báo cáo kiểm soát nhiễm khuẩn và phạm vi giám sát (toàn viện, ICU, Ngoại, Phòng mổ) là gì?",
                    "Kết quả giám sát vi sinh, tỷ lệ tuân thủ vệ sinh tay, tỷ lệ nhiễm khuẩn vết mổ, viêm phổi thở máy, nhiễm khuẩn huyết ra sao?",
                    "Tình hình khử khuẩn, tiệt khuẩn dụng cụ, giặt là đồ vải và thu gom xử lý chất thải y tế nguy hại đạt kết quả gì?",
                    "Tồn tại, nguy cơ bùng phát nhiễm khuẩn và kiến nghị biện pháp khắc phục là gì?"
                ],
                appendixCandidates: ["BẢNG THỐNG KÊ VI SINH", "BẢNG ĐÁNH GIÁ VỆ SINH TAY"],
                guide: `*** KHUNG RIÊNG CHO BÁO CÁO KIỂM SOÁT NHIỄM KHUẨN (TT 16/2018/TT-BYT) ***\\n- Nêu rõ các chỉ số định lượng: tỷ lệ tuân thủ vệ sinh tay của từng khoa, số mẫu cấy vi sinh đạt chuẩn, tỷ lệ nhiễm khuẩn bệnh viện (HCAI).\\n- Đánh giá quy trình tiệt trùng dụng cụ và phân loại rác thải y tế tại nguồn.`
            },
            "TỜ TRÌNH Y TẾ": {
                defaultMode: "strict_nd30", lengthMode: "standard",
                questions: [
                    "Kính gửi cơ quan nào (Sở Y tế, UBND tỉnh, Bảo hiểm xã hội tỉnh)?",
                    "Sự cần thiết và cơ sở thực tiễn y tế (nhu cầu khám chữa bệnh tăng cao, máy móc xuống cấp, kỹ thuật mới cứu sống người bệnh) là gì?",
                    "Nội dung trình cụ thể: Xin phê duyệt dự toán, mua sắm máy móc (CT, MRI, máy thở), mở rộng giường bệnh, bổ sung danh mục kỹ thuật?",
                    "Dự toán kinh phí, phương án nhân lực, hiệu quả kinh tế - xã hội và hồ sơ kèm theo gồm những gì?"
                ],
                appendixCandidates: ["BẢNG DỰ TOÁN KINH PHÍ", "DANH MỤC THIẾT BỊ / KỸ THUẬT", "THUYẾT MINH PHƯƠNG ÁN"],
                guide: `*** KHUNG RIÊNG CHO TỜ TRÌNH Y TẾ ***\\n- Dòng đầu body là Kính gửi.\\n- Bố cục: Sự cần thiết & Cơ sở thực tiễn y tế -> Căn cứ pháp lý -> Nội dung chi tiết xin phê duyệt (thông số kỹ thuật, số lượng, dự toán kinh phí, nguồn vốn tự chủ/ngân sách) -> Hiệu quả dự kiến mang lại cho người bệnh và bệnh viện -> Kiến nghị cấp có thẩm quyền xem xét, phê duyệt.\\n- Bảng dự toán hoặc cấu hình máy chi tiết đưa vào Phụ lục kèm theo.`
            },
            "BIÊN BẢN HỘI CHẨN": {
                defaultMode: "strict_nd30", lengthMode: "standard",
                questions: [
                    "Hội chẩn thuộc hình thức nào (hội chẩn toàn viện, liên khoa, hội chẩn chuyển tuyến, hội chẩn khẩn cấp)?",
                    "Thông tin người bệnh: Họ tên, tuổi, giới tính, số bệnh án, khoa điều trị, ngày giờ vào viện?",
                    "Chẩn đoán hiện tại, tóm tắt bệnh án, diễn biến triệu chứng lâm sàng và các kết quả xét nghiệm, CĐHA nổi bật?",
                    "Ý kiến của từng thành viên tham gia hội chẩn và Kết luận thống nhất của Chủ tọa (chẩn đoán xác định, phác đồ điều trị, phẫu thuật/thủ thuật, chế độ chăm sóc, tiên lượng)?"
                ],
                appendixCandidates: ["KẾT QUẢ CẬN LÂM SÀNG ĐÍNH KÈM"],
                guide: `*** KHUNG RIÊNG CHO BIÊN BẢN HỘI CHẨN (QĐ 1895/1997/QĐ-BYT) ***\\n- Mở đầu bắt buộc: Thời gian, địa điểm, Chủ tọa, Thư ký, các Bác sĩ chuyên khoa tham dự.\\n- Phần bệnh án: Tóm tắt tiền sử, bệnh sử, triệu chứng lâm sàng, cận lâm sàng, điều trị đã qua và đáp ứng.\\n- Ý kiến thảo luận của các bác sĩ chuyên khoa.\\n- Kết luận của Chủ tọa: Chẩn đoán xác định/phân biệt; Hướng điều trị tiếp theo; Chỉ định thuốc/phẫu thuật; Phân công bác sĩ theo dõi; Giải thích tình trạng bệnh cho người nhà.`
            },
            "BIÊN BẢN KIỂM THẢO TỬ VONG": {
                defaultMode: "strict_nd30", lengthMode: "standard",
                questions: [
                    "Thời gian tổ chức kiểm thảo tử vong, địa điểm, thành phần Chủ tọa, Thư ký và các thành viên tham dự?",
                    "Thông tin người bệnh tử vong, ngày giờ vào viện, ngày giờ tử vong, khoa điều trị?",
                    "Tóm tắt bệnh án: diễn biến bệnh lý, quá trình cấp cứu và hồi sức tích cực trước khi tử vong?",
                    "Ý kiến đánh giá về: Tiếp đón người bệnh, Chẩn đoán, Phác đồ điều trị, Chăm sóc điều dưỡng, Tinh thần thái độ phục vụ; và Kết luận rút kinh nghiệm chuyên môn toàn viện?"
                ],
                appendixCandidates: ["BẢN TÓM TẮT HỒ SƠ BỆNH ÁN"],
                guide: `*** KHUNG RIÊNG CHO BIÊN BẢN KIỂM THẢO TỬ VONG (QĐ 1895/1997/QĐ-BYT) ***\\n- Nghiêm túc, khoa học, khách quan, mang tính xây dựng chuyên môn sâu sắc.\\n- Bố cục: 1. Thành phần họp; 2. Tóm tắt diễn biến bệnh án và quá trình cấp cứu hồi sức; 3. Thảo luận đánh giá toàn diện: chẩn đoán, điều trị, chăm sóc, phối hợp liên khoa, thuốc men, trang thiết bị; 4. Xác định nguyên nhân tử vong chính và bệnh kèm theo; 5. Kết luận của Chủ tọa và bài học kinh nghiệm chuyên môn rút ra cho toàn viện.`
            },
            "DANH MỤC THUỐC - VẬT TƯ": {
                defaultMode: "strict_nd30", lengthMode: "table",
                questions: [
                    "Danh mục thuộc nhóm nào (thuốc BHYT, vật tư y tế tiêu hao, hóa chất xét nghiệm, trang thiết bị y tế)?",
                    "Các trường/cột bắt buộc cần có (STT, Tên hoạt chất/thương mại, Nồng độ/hàm lượng, Đường dùng, ĐVT, Số lượng, Đơn giá dự toán, Ghi chú)?",
                    "Nguồn căn cứ để lập danh mục (nhu cầu điều trị các khoa lâm sàng, kết quả đấu thầu kỳ trước) là gì?"
                ],
                appendixCandidates: [],
                guide: `*** KHUNG RIÊNG CHO DANH MỤC THUỐC - VẬT TƯ Y TẾ ***\\n- Bắt buộc xuất bảng Markdown kín 4 cạnh.\\n- Cột chuẩn: STT | Tên thuốc/Vật tư/Hoạt chất | Hàm lượng/Quy cách | ĐVT | Số lượng | Đơn giá dự kiến (VNĐ) | Thành tiền (VNĐ) | Nhóm BHYT / Ghi chú.\\n- Không tự tạo dòng giả; nếu thiếu thông tin thì ghi [...].`
            },
            "LỊCH TRỰC CHUYÊN MÔN 24/24": {
                defaultMode: "strict_nd30", lengthMode: "table",
                questions: [
                    "Giai đoạn trực (tuần, tháng, kỳ nghỉ lễ/Tết) là từ ngày nào đến ngày nào?",
                    "Các vị trí trực bắt buộc (Trực lãnh đạo, Trực lâm sàng/cấp cứu, Trực ngoại khoa, Trực cận lâm sàng, Trực điều dưỡng, Trực xe cứu thương, Trực bảo vệ PCCC)?",
                    "Danh sách nhân sự phân công và số điện thoại liên lạc khẩn cấp (Hotline) là gì?"
                ],
                appendixCandidates: [],
                guide: `*** KHUNG RIÊNG CHO LỊCH TRỰC CHUYÊN MÔN 24/24 ***\\n- Bắt buộc xuất bảng Markdown kín viền.\\n- Cột chuẩn: Thứ/Ngày | Trực Lãnh đạo | Trực Cấp cứu/ICU | Trực Khối Ngoại - Sản | Trực Cận lâm sàng/Dược | Trực Điều dưỡng viện | Lái xe cấp cứu | Ghi chú.\\n- Nêu rõ nguyên tắc thường trực 24/24: không rời vị trí trực, sẵn sàng kích hoạt Báo động đỏ khi có ca cấp cứu nặng hàng loạt.`
            },"""

    doc_prof_marker = "const DOCUMENT_PROFILES = Object.freeze({"
    if doc_prof_marker in content:
        content = content.replace(
            doc_prof_marker,
            doc_prof_marker + "\n" + hospital_profiles
        )
        print("Inserted Hospital Profiles into DOCUMENT_PROFILES.")

    # 11. Update SCHEME_WRITING_GUIDES
    old_scheme_marker = "const SCHEME_WRITING_GUIDES = Object.freeze({"
    new_scheme_guides = """const SCHEME_WRITING_GUIDES = Object.freeze({
            BENH_VIEN: "Dùng văn phong quản trị bệnh viện và y tế chuyên nghiệp, chuẩn mực y khoa, tuyệt đối chính xác về thuật ngữ lâm sàng, bảo đảm an toàn người bệnh và bám sát Luật Khám bệnh, chữa bệnh số 15/2023/QH15, Bộ 83 tiêu chí chất lượng bệnh viện.",
            HANH_CHINH: "Dùng văn phong hành chính trung tính, chuẩn mực theo Nghị định 30/2020/NĐ-CP, chính xác, tiết chế, rõ ràng nhiệm vụ và trách nhiệm.",
            DANG: "Dùng thuật ngữ và giọng văn của tổ chức Đảng bộ Bệnh viện, gắn kết chặt chẽ với y đức, tinh thần trách nhiệm của người thầy thuốc và phục vụ nhân dân.",
            CONG_DOAN: "Dùng giọng văn công đoàn ngành y tế, động viên chăm lo bảo vệ quyền lợi hợp pháp, an toàn lao động và đời sống y bác sĩ, nhân viên y tế.",
            DOAN_TN: "Dùng giọng văn xung kích của Đoàn thanh niên Bệnh viện: y đức, nghiên cứu khoa học, hiến máu tình nguyện, khám chữa bệnh thiện nguyện vì cộng đồng.",
            HOP_DONG: "Dùng ngôn ngữ hợp đồng y tế chặt chẽ, làm rõ tiêu chuẩn chất lượng thuốc/thiết bị (GMP, ISO, CE), thời hạn giao hàng, bảo hành bảo trì, nghiệm thu và giải quyết tranh chấp."
        };"""
    old_scheme_end = content.find("});", content.find(old_scheme_marker))
    if old_scheme_end != -1:
        content = content[:content.find(old_scheme_marker)] + new_scheme_guides + content[old_scheme_end + 3:]
        print("Updated SCHEME_WRITING_GUIDES.")

    # 12. Add STYLE_BENH_VIEN and hospital helpers
    style_benh_vien_def = """
        const STYLE_BENH_VIEN = `
**QUẢN TRỊ BỆNH VIỆN & Y TẾ CHUYÊN SÂU** - Văn bản quản trị, quy chế chuyên môn, kế hoạch, SOP và báo cáo bệnh viện
NGUYÊN TẮC CỐT LÕI:
- Tuân thủ Luật Khám bệnh, chữa bệnh số 15/2023/QH15, Bộ 83 Tiêu chí Chất lượng Bệnh viện (QĐ 6858/QĐ-BYT).
- An toàn người bệnh là ưu tiên tối thượng: mọi quy định, kế hoạch, quy trình kỹ thuật phải hướng tới phòng ngừa sai sót chuyên môn và giảm thiểu tai biến y khoa.
- Văn phong chuẩn xác y khoa, chặt chẽ, trang trọng, minh bạch và khoa học.
- Báo cáo sự cố y khoa theo Thông tư 43/2018/TT-BYT tuân thủ nghiêm ngặt văn hóa 'Không trừng phạt' (No-blame culture) nhằm cải tiến quy trình liên tục.
- Tuân thủ thể thức hành chính chuẩn Nghị định 30/2020/NĐ-CP (Font Times New Roman 13pt, lùi đầu dòng 1.27cm, dãn dòng 1.2, bảng kín 4 cạnh viền ngoài và các đường kẻ trong).
- Thẩm quyền ban hành rõ ràng: Giám đốc Bệnh viện, các Phó Giám đốc theo lĩnh vực phụ trách, Hội đồng chuyên môn (Thuốc & ĐT, KSNK, QLCL...).
`;
    """
    content = content.replace("const STYLE_HANH_CHINH = `", style_benh_vien_def + "\n        const STYLE_HANH_CHINH = `")

    # Replace school rule block in STYLE_HANH_CHINH
    idx_rule_start = content.find("**QUY TẮC CHÍNH QUYỀN 2 CẤP")
    if idx_rule_start != -1:
        idx_rule_end = content.find("const STYLE_DANG =", idx_rule_start)
        if idx_rule_end != -1:
            hospital_rule_text = """**QUY TẮC PHÁP LÝ & QUẢN TRỊ BỆNH VIỆN (BẮT BUỘC)**:
Hệ thống này chuyên phục vụ công tác xây dựng Kế hoạch, Quy chế, Quyết định, Báo cáo và Quy trình chuyên môn của BỆNH VIỆN theo quy chuẩn Bộ Y tế và Nghị định 30/2020/NĐ-CP:
- **Cơ quan cấp trên:** Sử dụng "Sở Y tế tỉnh/thành phố" (hoặc "Bộ Y tế", "UBND tỉnh/thành phố").
- **Cơ quan ban hành:** Tên Bệnh viện (VD: BỆNH VIỆN ĐA KHOA TỈNH LÂM ĐỒNG, TRUNG TÂM Y TẾ...).
- **Căn cứ pháp lý nền tảng:**
  + Luật Khám bệnh, chữa bệnh số 15/2023/QH15 và Nghị định số 96/2023/NĐ-CP.
  + Luật Dược số 105/2016/QH13 và Luật Bảo hiểm y tế.
  + Nghị định số 60/2021/NĐ-CP về cơ chế tự chủ tài chính đơn vị sự nghiệp y tế công lập.
  + Nghị định số 30/2020/NĐ-CP về công tác văn thư (Times New Roman 13pt, lùi đầu dòng 1.27cm, dãn dòng 1.2, bảng kín 4 cạnh).
  + Quyết định số 1895/1997/QĐ-BYT về Quy chế Bệnh viện.
  + Quyết định số 6858/QĐ-BYT ban hành Bộ 83 Tiêu chí Chất lượng Bệnh viện Việt Nam.
  + Thông tư số 43/2018/TT-BYT về phòng ngừa sự cố y khoa trong cơ sở khám bệnh, chữa bệnh.
  + Thông tư số 16/2018/TT-BYT về kiểm soát nhiễm khuẩn trong cơ sở khám chữa bệnh.
  + Thông tư số 31/2021/TT-BYT về hoạt động điều dưỡng trong bệnh viện.
  + Thông tư số 46/2018/TT-BYT về hồ sơ bệnh án điện tử (EMR).
  + Quyết định số 2151/QĐ-BYT về đổi mới phong cách, thái độ phục vụ hướng tới sự hài lòng của người bệnh.
- **Thuật ngữ chuyên môn:** Sử dụng đúng chức danh: Giám đốc Bệnh viện, Phó Giám đốc, Bác sĩ CKI/CKII, Thạc sĩ y khoa, Cử nhân Điều dưỡng, Dược sĩ, Kỹ thuật viên, Hộ sinh...
- **Phân định rõ thẩm quyền:** Ban Giám đốc, Phòng Kế hoạch tổng hợp, Phòng Quản lý chất lượng, Hội đồng Thuốc và Điều trị, Hội đồng KSNK.
`;

        """
            content = content[:idx_rule_start] + hospital_rule_text + content[idx_rule_end:]
            print("Replaced school rule block with hospital legal rule block.")

    # 13. Replace buildHoangThien functions completely
    idx_ht_start = content.find("function buildHoangThienAnalyzeGuide")
    if idx_ht_start != -1:
        idx_ht_end = content.find("// PHONG CÁCH VĂN BẢN", idx_ht_start)
        if idx_ht_end != -1:
            hospital_guides_func = """function buildHospitalAnalyzeGuide(docType = "") {
            const type = String(docType || "").toUpperCase().trim();
            return `
YÊU CẦU RIÊNG CHO HỆ THỐNG VĂN BẢN BỆNH VIỆN (${type}):
- Người dùng là Lãnh đạo Bệnh viện (Giám đốc, Phó Giám đốc) hoặc Trưởng các Phòng chức năng (KHTH, QLCL, Điều dưỡng, Dược, TCCB, TCKT) và Khoa lâm sàng/cận lâm sàng.
- Tài liệu nguồn thường là: Công văn/Chỉ thị của Sở Y tế, Bộ Y tế; Báo cáo số liệu chuyên môn các khoa phòng; Biên bản sự cố/hội chẩn; Hồ sơ thầu thuốc/vật tư; Kết quả đánh giá chất lượng 83 tiêu chí.
- Trích dẫn chính xác các căn cứ pháp lý cốt lõi ngành Y tế: Luật Khám bệnh, chữa bệnh 15/2023/QH15; Nghị định 96/2023/NĐ-CP; Thông tư 43/2018/TT-BYT (sự cố y khoa); Thông tư 16/2018/TT-BYT (KSNK); Quyết định 6858/QĐ-BYT (83 tiêu chí); Nghị định 30/2020/NĐ-CP (thể thức).
- Đảm bảo thuật ngữ y khoa chuẩn xác, tôn trọng nguyên tắc an toàn người bệnh tuyệt đối.
`;
        }

        function buildHospitalWriteGuide(docType = "", useWebSearch = false) {
            const type = String(docType || "").toUpperCase().trim();
            return `
*** HƯỚNG DẪN SOẠN THẢO VĂN BẢN BỆNH VIỆN (${type}) ***
- Vai trò: Chuyên viên quản trị bệnh viện & Thư ký y khoa cao cấp soạn thảo văn bản cho Ban Giám đốc Bệnh viện.
- Thể thức: Tuân thủ 100% Nghị định 30/2020/NĐ-CP (Font Times New Roman, cỡ 13pt, thụt đầu dòng 1.27cm, dãn dòng 1.2, bảng kín 4 cạnh viền).
- Thuật ngữ: Sử dụng danh từ, thuật ngữ lâm sàng, cận lâm sàng, dược khoa chính thức của Bộ Y tế.
- Với Kế hoạch: Nêu rõ mục tiêu, chỉ tiêu, hoạt động, thời gian, kinh phí và phân công Khoa/Phòng (KHTH, QLCL, Điều dưỡng, Dược...).
- Với Quy chế: Phân định rõ trách nhiệm của Bác sĩ điều trị, Bác sĩ trực, Điều dưỡng, Dược sĩ, Trưởng khoa và Ban Giám đốc.
- Với Báo cáo sự cố y khoa: Giữ vững nguyên tắc 'Không trừng phạt', phân tích nguyên nhân gốc rễ (RCA) để phòng ngừa tái diễn.
${useWebSearch ? "- Cho phép tra cứu các hướng dẫn chẩn đoán, phác đồ điều trị và thông tư mới nhất của Bộ Y tế khi cần." : "- Bám sát dữ liệu thực tế của bệnh viện; không bịa số liệu người bệnh, giường bệnh hay tai biến."}
`;
        }

        """
            content = content[:idx_ht_start] + hospital_guides_func + content[idx_ht_end:]
            print("Replaced buildHoangThien functions with buildHospital functions.")

    content = content.replace("buildHoangThienAnalyzeGuide", "buildHospitalAnalyzeGuide")
    content = content.replace("buildHoangThienWriteGuide", "buildHospitalWriteGuide")
    content = content.replace("HOANG_THIEN", "BENH_VIEN")

    # Update helpers for plans, decisions, totrinh
    helpers_def = """
        function isKeHoachDocType(docType = "") {
            const t = String(docType || "").toUpperCase().trim();
            return t === "KẾ HOẠCH" || t === "KẾ HOẠCH BỆNH VIỆN";
        }

        function isDecisionDocType(docType = "") {
            const t = String(docType || "").toUpperCase().trim();
            return t === "QUYẾT ĐỊNH" || t === "QUYẾT ĐỊNH Y TẾ";
        }

        function isToTrinhDocType(docType = "") {
            const t = String(docType || "").toUpperCase().trim();
            return t === "TỜ TRÌNH" || t === "TỜ TRÌNH Y TẾ";
        }

        function isTableDocType(docType = "") {
            const t = String(docType || "").toUpperCase().trim();
            return t === "DANH SÁCH" || t === "DANH MỤC" || t === "DANH MỤC THUỐC - VẬT TƯ" || t === "LỊCH TRỰC CHUYÊN MÔN 24/24";
        }
    """
    content = content.replace(
        "function isKeHoachDocType(docType = \"\") {",
        helpers_def + "\n        function isKeHoachDocType_Old(docType = \"\") {"
    )

    content = content.replace(
        'if (decisionDiv) decisionDiv.classList.toggle("hidden", docType !== "QUYẾT ĐỊNH");',
        'if (decisionDiv) decisionDiv.classList.toggle("hidden", !isDecisionDocType(docType));'
    )
    content = content.replace(
        'if (toTrinhDiv) toTrinhDiv.classList.toggle("hidden", docType !== "TỜ TRÌNH");',
        'if (toTrinhDiv) toTrinhDiv.classList.toggle("hidden", !isToTrinhDocType(docType));'
    )

    # 14. Update Excel templates & sample tables for Hospital
    content = content.replace(
        '{ key: "teachers", placeholder: "Danh sách giáo viên, ngăn cách bằng dấu phẩy", aliases: ["giao vien", "danh sach", "thanh vien"] }',
        '{ key: "teachers", placeholder: "Danh sách y bác sĩ / nhân viên y tế, ngăn cách bằng dấu phẩy", aliases: ["bac si", "dieu duong", "nhan vien", "giao vien", "danh sach", "thanh vien"] }'
    )
    content = content.replace('["Nguyễn Văn A", "Hiệu trưởng"]', '["BSCKII. Nguyễn Văn A", "Giám đốc Bệnh viện"]')
    content = content.replace('["Trần Thị B", "Phó Hiệu trưởng"]', '["BSCKII. Trần Thị B", "Phó Giám đốc"]')
    content = content.replace('headers: ["Tên tổ", "Giáo viên"]', 'headers: ["Tên Khoa/Phòng", "Bác sĩ / Nhân viên y tế"]')
    content = content.replace(
        '["Tổ Toán - Tin", "Nguyễn Văn C, Trần Thị D"]',
        '["Khoa Hồi sức tích cực (ICU)", "BSCKII. Nguyễn Hữu Trí, BSCKI. Đỗ Hải Nam"]'
    )

    # 15. Update buildAccountProfilePromptBlock for Hospital
    content = content.replace('pushField("Số học sinh", p.student_count, 50);', 'pushField("Giường bệnh / Lượt khám", p.student_count, 50);')
    content = content.replace('pushList("Ban giám hiệu", p.board_members, 6, 360);', 'pushList("Ban Giám đốc", p.board_members, 6, 360);')
    content = content.replace('pushList("Tổ chuyên môn", p.departments, 10, 420);', 'pushList("Khoa / Phòng chuyên môn", p.departments, 12, 500);')
    content = content.replace('pushList("GV theo tổ", p.department_teachers, 10, 460);', 'pushList("Y bác sĩ theo Khoa/Phòng", p.department_teachers, 12, 600);')
    content = content.replace('pushField("Bí thư đoàn", p.youth_secretary);', 'pushField("Bí thư Đoàn Thanh niên BV", p.youth_secretary);')
    content = content.replace('pushField("Tổng phụ trách", p.head_teacher);', 'pushField("Điều dưỡng trưởng Bệnh viện", p.head_teacher);')
    content = content.replace('pushList("Danh sách nhân viên", p.staff_list, 10, 460);', 'pushList("Vị trí then chốt", p.staff_list, 10, 460);')
    content = content.replace('pushList("Danh sách đảng viên", p.party_members, 12, 460);', 'pushList("Đảng viên", p.party_members, 12, 460);')

    # 16. Update buildDanhSachSeedRowsFromAccountProfile for Hospital
    content = content.replace(
        'const wantsBoard = /(ban giam hieu|bgh|lanh dao|quan ly|hieu truong|pho hieu truong)/.test(intent);',
        'const wantsBoard = /(ban giam doc|bgd|lanh dao|quan ly|giam doc|pho giam doc|hieu truong|pho hieu truong)/.test(intent);'
    )
    content = content.replace(
        'const wantsTeachers = /(giao vien|gv|to chuyen mon|to tu nhien|to xa hoi|tap huan|chuyen de|boi duong|chuyen doi so|tri tue nhan tao|ai)/.test(intent);',
        'const wantsTeachers = /(bac si|dieu duong|y si|duoc si|ky thuat vien|nhan vien y te|giao vien|gv|khoa|phong|lam sang|can lam sang|tap huan|cme|nghien cuu khoa hoc)/.test(intent);'
    )
    content = content.replace(
        'const wantsDepartmentsOnly = /(to chuyen mon|danh sach to|cac to|to tu nhien|to xa hoi)/.test(intent) && !wantsTeachers;',
        'const wantsDepartmentsOnly = /(khoa phong|danh sach khoa|danh sach phong|cac khoa|to chuyen mon)/.test(intent) && !wantsTeachers;'
    )
    content = content.replace('addRow(item.name, "Tổ chuyên môn", "Chưa tách được giáo viên từ hồ sơ tài khoản");', 'addRow(item.name, "Khoa / Phòng", "Chưa tách được nhân viên y tế từ hồ sơ tài khoản");')
    content = content.replace('names.forEach((teacherName) => addRow(teacherName, `Giáo viên ${item.name}`, "Hồ sơ tài khoản"));', 'names.forEach((staffName) => addRow(staffName, `Cán bộ ${item.name}`, "Hồ sơ tài khoản"));')

    # 17. Add Hospital Presets click function in JS
    preset_js = """
        function applyHospitalPreset(presetKey) {
            const presets = {
                'KH_CHAT_LUONG': {
                    scheme: 'BENH_VIEN',
                    type: 'KẾ HOẠCH BỆNH VIỆN',
                    subject: 'Kế hoạch Cải tiến chất lượng Bệnh viện năm 2026 theo Bộ 83 Tiêu chí của Bộ Y tế',
                    note: 'Bám sát Quyết định 6858/QĐ-BYT; Đặt mục tiêu đạt điểm trung bình chung toàn viện từ 3.85 trở lên; Ưu tiên cải tiến tiêu chí an toàn người bệnh (Phần C) và nâng cao năng lực chuyên môn lâm sàng (Phần D); Phân công Phòng QLCL làm đầu mối giám sát hàng tháng.'
                },
                'KH_KSNK': {
                    scheme: 'BENH_VIEN',
                    type: 'KẾ HOẠCH BỆNH VIỆN',
                    subject: 'Kế hoạch Kiểm soát nhiễm khuẩn và Giám sát vi sinh bệnh viện năm 2026',
                    note: 'Tuân thủ Thông tư 16/2018/TT-BYT; Nâng tỷ lệ tuân thủ vệ sinh tay của nhân viên y tế lên trên 85%; Giảm tỷ lệ nhiễm khuẩn vết mổ và viêm phổi thở máy; Tăng cường tiệt khuẩn dụng cụ phòng mổ và phân loại rác thải y tế tại nguồn theo Thông tư 20/2021/TT-BYT.'
                },
                'QC_TRUC': {
                    scheme: 'BENH_VIEN',
                    type: 'QUY CHẾ CHUYÊN MÔN',
                    subject: 'Quy chế Thường trực 24/24 và Quy trình kích hoạt Báo động đỏ cấp cứu toàn viện',
                    note: 'Quy định rõ 4 cấp trực: Trực lãnh đạo, Trực lâm sàng/cấp cứu, Trực cận lâm sàng & Dược, Trực bảo vệ - xe cứu thương; Quy định thời gian có mặt xử trí ca bệnh khẩn cấp trong vòng 3 phút; Phân định rõ trách nhiệm của Bác sĩ trưởng kíp trực và Điều dưỡng ca trực.'
                },
                'KH_EMR': {
                    scheme: 'BENH_VIEN',
                    type: 'KẾ HOẠCH BỆNH VIỆN',
                    subject: 'Kế hoạch Triển khai Bệnh án điện tử (EMR) và Chuyển đổi số Y tế giai đoạn 2026-2027',
                    note: 'Căn cứ Thông tư 46/2018/TT-BYT; Nâng cấp hệ thống phần mềm quản lý bệnh viện (HIS), hệ thống thông tin xét nghiệm (LIS), truyền tải lưu trữ hình ảnh (PACS/RIS); Thay thế hoàn toàn hồ sơ bệnh án giấy sang bệnh án điện tử, bảo đảm an toàn thông tin mức độ 3.'
                },
                'QD_HOI_DONG': {
                    scheme: 'BENH_VIEN',
                    type: 'QUYẾT ĐỊNH Y TẾ',
                    subject: 'Về việc Kiện toàn Hội đồng Thuốc và Điều trị Bệnh viện Đa khoa tỉnh',
                    note: 'Căn cứ Thông tư 21/2013/TT-BYT; Thành phần: Giám đốc Bệnh viện làm Chủ tịch Hội đồng, Trưởng khoa Dược làm Phó Chủ tịch thường trực, Trưởng phòng KHTH làm Thư ký, các Trưởng khoa lâm sàng làm Ủy viên; Nhiệm vụ xây dựng danh mục thuốc BHYT, theo dõi ADR và giám sát sử dụng kháng sinh hợp lý.'
                },
                'BC_SU_CO': {
                    scheme: 'BENH_VIEN',
                    type: 'BÁO CÁO SỰ CỐ Y KHOA',
                    subject: 'Báo cáo Phân tích và Xử lý Sự cố y khoa quý I/2026',
                    note: 'Theo Thông tư 43/2018/TT-BYT; Tổng hợp số lượng sự cố tự nguyện và bắt buộc; Phân loại theo mức độ tổn thương NC0-NC6; Phân tích nguyên nhân gốc rễ (RCA) về con người, quy trình, trang thiết bị; Đề xuất giải pháp khắc phục phòng ngừa tái diễn theo nguyên tắc không trừng phạt.'
                },
                'BB_HOI_CHAN': {
                    scheme: 'BENH_VIEN',
                    type: 'BIÊN BẢN HỘI CHẨN',
                    subject: 'Biên bản Hội chẩn chuyên môn toàn viện ca bệnh đa chấn thương nặng kèm sốc mất máu',
                    note: 'Bệnh nhân nam 45 tuổi, vào viện cấp cứu giờ thứ 2 sau tai nạn giao thông; Chẩn đoán sơ bộ: Đa chấn thương, dập phổi, vỡ lách độ IV, gãy hở xương đùi; Thành phần hội chẩn: Ban Giám đốc, Ngoại tổng hợp, Phẫu thuật - GMHS, Hồi sức tích cực (ICU), Chẩn đoán hình ảnh, Huyết học truyền máu; Thống nhất mổ cấp cứu cầm máu khẩn cấp.'
                },
                'TTR_MUA_SAM': {
                    scheme: 'BENH_VIEN',
                    type: 'TỜ TRÌNH Y TẾ',
                    subject: 'Tờ trình Sở Y tế xin phê duyệt Dự toán và Kế hoạch lựa chọn nhà thầu mua sắm Hệ thống Chụp cắt lớp vi tính (CT-Scanner 128 lát cắt)',
                    note: 'Căn cứ nhu cầu cấp bách trong chẩn đoán cấp cứu đột quỵ não và đa chấn thương; Máy CT hiện tại đã hoạt động 12 năm xuống cấp nghiêm trọng; Dự toán kinh phí 25 tỷ đồng từ nguồn Quỹ phát triển hoạt động sự nghiệp và vốn vay ưu đãi; Hồ sơ đính kèm thuyết minh kỹ thuật và 3 báo giá hợp lệ.'
                }
            };

            const p = presets[presetKey];
            if (!p) return;

            const schemeSelect = document.getElementById("docSchemeSelect");
            if (schemeSelect) {
                schemeSelect.value = p.scheme;
                handleDocSchemeChange();
            }

            const typeSelect = document.getElementById("docTypeSelect");
            if (typeSelect) {
                typeSelect.value = p.type;
                onDocTypeChange();
            }

            const subjectInput = document.getElementById("docSubject");
            if (subjectInput) subjectInput.value = p.subject;

            const noteInput = document.getElementById("userContext");
            if (noteInput) noteInput.value = p.note;

            const styleRadio = document.querySelector('input[name="styleSelect"][value="benh_vien"]');
            if (styleRadio) styleRadio.checked = true;

            if (window.customAlert) {
                window.customAlert("Đã nạp mẫu: " + p.subject);
            }
        }
    """
    content = content.replace("function handleDocSchemeChange() {", preset_js + "\n        function handleDocSchemeChange() {")

    # 18. Update forbidden terms to catch stray school words
    forbidden_terms_def = """
        const FORBIDDEN_TERMS = [
            { term: "Phòng Giáo dục và Đào tạo", alternatives: ["Sở Y tế", "Bệnh viện"] },
            { term: "Phòng Giáo dục", alternatives: ["Sở Y tế", "Bệnh viện"] },
            { term: "Phòng GD&ĐT", alternatives: ["Sở Y tế", "Bệnh viện"] },
            { term: "Phòng GDĐT", alternatives: ["Sở Y tế", "Bệnh viện"] },
            { term: "Sở Giáo dục và Đào tạo", alternatives: ["Sở Y tế", "Bộ Y tế"] },
            { term: "Sở GD&ĐT", alternatives: ["Sở Y tế"] },
            { term: "Hiệu trưởng", alternatives: ["Giám đốc Bệnh viện", "Trưởng khoa"] },
            { term: "Hiệu phó", alternatives: ["Phó Giám đốc Bệnh viện", "Phó Trưởng khoa"] },
            { term: "Giáo viên", alternatives: ["Bác sĩ", "Điều dưỡng", "Nhân viên y tế"] },
            { term: "Học sinh", alternatives: ["Người bệnh", "Bệnh nhân"] }
        ];
    """
    content = re.sub(
        r'const FORBIDDEN_TERMS = \[[\s\S]*?\];',
        forbidden_terms_def.strip(),
        content
    )

    # 19. Add Copy Prompt Button
    copy_prompt_btn = """
                    <button type="button" id="copyPromptBtn" class="px-3 py-2 bg-teal-600 hover:bg-teal-700 text-white text-xs font-bold rounded-lg shadow transition flex items-center gap-1.5" title="Sao chép toàn bộ Prompt hoàn chỉnh để dán vào Gemini Web Chat">
                        <i class="fas fa-clipboard-list text-sm"></i>
                        <span>Copy Prompt cho Gemini</span>
                    </button>
    """
    if 'id="copyPromptBtn"' not in content:
        content = content.replace(
            '<div class="flex items-center gap-2">',
            '<div class="flex items-center gap-2">\n' + copy_prompt_btn,
            1
        )
        copy_handler = """
        document.getElementById("copyPromptBtn")?.addEventListener("click", () => {
            const docType = document.getElementById("docTypeSelect")?.value || "VĂN BẢN";
            const subject = document.getElementById("docSubject")?.value || "";
            const note = document.getElementById("userContext")?.value || "";
            const samplePrompt = `BẠN LÀ CHUYÊN VIÊN SOẠN THẢO VĂN BẢN VÀ QUẢN TRỊ BỆNH VIỆN CHUYÊN NGHIỆP.
HÃY SOẠN THẢO HOÀN CHỈNH VĂN BẢN SAU THEO ĐÚNG NGHỊ ĐỊNH 30/2020/NĐ-CP VÀ QUY ĐỊNH BỘ Y TẾ:

- LOẠI VĂN BẢN: ${docType}
- CƠ QUAN BAN HÀNH: ${document.getElementById("unitName")?.value || "BỆNH VIỆN ĐA KHOA TỈNH LÂM ĐỒNG"}
- CƠ QUAN CẤP TRÊN: ${document.getElementById("unitParent")?.value || "SỞ Y TẾ TỈNH LÂM ĐỒNG"}
- TRÍCH YẾU NỘI DUNG: ${subject}
- GHI CHÚ YÊU CẦU: ${note}

QUY CHUẨN TRÌNH BÀY (NGHỊ ĐỊNH 30/2020/NĐ-CP):
1. Font Times New Roman, cỡ chữ đồng nhất 13pt.
2. Thụt đầu dòng tất cả các đoạn văn 1.27cm (0.5 inch).
3. Dãn dòng 1.2, căn đều hai bên (Justify).
4. Các căn cứ pháp lý: Luật Khám bệnh, chữa bệnh 15/2023/QH15, Nghị định 96/2023/NĐ-CP, Bộ 83 tiêu chí chất lượng bệnh viện (QĐ 6858/QĐ-BYT), Thông tư chuyên ngành.
5. Nếu có bảng biểu thì đóng khung kín 4 cạnh viền ngoài và các đường kẻ bên trong.
6. Chỉ xuất duy nhất phần NỘI DUNG BODY VĂN BẢN (Markdown), không viết lời giải thích thừa.`;
            navigator.clipboard.writeText(samplePrompt).then(() => {
                if (window.customAlert) window.customAlert("Đã sao chép Prompt chuyên sâu Bệnh viện vào Clipboard! Bạn có thể dán trực tiếp vào Gemini để chạy.");
                else alert("Đã sao chép Prompt Bệnh viện vào Clipboard!");
            }).catch(() => {
                alert("Không thể sao chép tự động, vui lòng chọn văn bản thủ công.");
            });
        });
        """
        content = content.replace(
            'document.addEventListener("DOMContentLoaded", () => {',
            'document.addEventListener("DOMContentLoaded", () => {\n' + copy_handler
        )

    # 20. Save to canvas_taobaocao_benhvien.html and backupcode viettailieu/
    target_root = "canvas_taobaocao_benhvien.html"
    target_backup = os.path.join("backupcode viettailieu", "canvas_taobaocao_benhvien.html")

    with open(target_root, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written {target_root} ({len(content)} chars)")

    with open(target_backup, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written {target_backup} ({len(content)} chars)")

if __name__ == "__main__":
    build_hospital_canvas()
