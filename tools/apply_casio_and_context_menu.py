import re
import os
import subprocess

# 1. Đọc dữ liệu Casio từ master_bai_day_html_template.html
source_template = r'TROLYTHIEN\2_TAO_BAI_TAP\templates\master_bai_day_html_template.html'
with open(source_template, 'r', encoding='utf-8') as f:
    src_lines = f.readlines()
src_text = "".join(src_lines)

# CSS Casio
c1 = src_text.find('4. MÁY TÍNH CẦM TAY CASIO fx-580VN X CLASSWIZ')
c2 = src_text.find('MODAL PHÓNG TO HÌNH ẢNH (LIGHTBOX)')
casio_css = src_text[src_text.rfind('/*', 0, c1):src_text.rfind('/*', 0, c2)].strip()

# HTML Casio
h1 = src_text.find('MÁY TÍNH CẦM TAY CASIO fx-580VN X CLASSWIZ', c2)
h2 = src_text.find('MODAL SỬA BÀI "SAI ĐÂU SỬA ĐÓ"', h1)
casio_html = src_text[src_text.rfind('<!--', 0, h1):src_text.rfind('<!--', 0, h2)].strip()

# JS Casio PURE (Chỉ lấy phần core engine của Casio, LOẠI BỎ hoàn toàn pen/laser/blackboard/duplicate vars)
# Part A: lines 1587 to 2139 (1-indexed -> 1586:2139)
casio_js_part_a = "".join(src_lines[1586:2139])
# Part B: lines 2543 to 3186 (1-indexed -> 2542:3186)
casio_js_part_b = "".join(src_lines[2542:3186])

casio_pure_js = f"""
/* ==========================================================================
   MÁY TÍNH CẦM TAY CASIO fx-580VN X CLASSWIZ - CORE SIMULATOR ENGINE
   ========================================================================== */
{casio_js_part_a}

{casio_js_part_b}
"""

# Context Menu CSS (Menu chuột phải sư phạm)
context_menu_css = """
    /* MENU CHUỘT PHẢI SƯ PHẠM (QUICK CONTEXT MENU) */
    .context-menu {
      position: fixed;
      z-index: 2000;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 12px;
      padding: 6px;
      min-width: 210px;
      box-shadow: 0 14px 40px rgba(0, 0, 0, 0.7);
      display: flex;
      flex-direction: column;
      gap: 2px;
      user-select: none;
      animation: ctxFadeIn 0.12s ease-out;
    }
    @keyframes ctxFadeIn {
      from { opacity: 0; transform: scale(0.95); }
      to { opacity: 1; transform: scale(1); }
    }
    .ctx-item {
      display: flex;
      align-items: center;
      padding: 8px 12px;
      border-radius: 8px;
      color: #f1f5f9;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.12s ease;
    }
    .ctx-item:hover {
      background: rgba(99, 102, 241, 0.35);
      color: #ffffff;
    }
    .ctx-item.is-active {
      background: rgba(239, 68, 68, 0.28);
      color: #fca5a5;
    }
    .ctx-icon {
      width: 22px;
      display: inline-flex;
      align-items: center;
      font-size: 1.05rem;
      margin-right: 6px;
    }
    .ctx-label {
      flex: 1;
    }
    .ctx-key {
      font-size: 0.72rem;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.08);
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .ctx-divider {
      height: 1px;
      background: rgba(255, 255, 255, 0.12);
      margin: 4px 0;
    }
"""

context_menu_html = """
<!-- MENU CHUỘT PHẢI SƯ PHẠM (QUICK CONTEXT MENU) -->
<div id="contextMenu" class="context-menu" style="display:none;" aria-hidden="true">
  <div class="ctx-item" onclick="handleCtxAction('laser')">
    <span class="ctx-icon">🔴</span>
    <span class="ctx-label">Con trỏ Laser</span>
    <span class="ctx-key">Phím L</span>
  </div>
  <div class="ctx-item" onclick="handleCtxAction('pen')">
    <span class="ctx-icon">✏️</span>
    <span class="ctx-label">Bút vẽ màn hình</span>
    <span class="ctx-key">Phím P</span>
  </div>
  <div class="ctx-item" onclick="handleCtxAction('highlighter')">
    <span class="ctx-icon">🟡</span>
    <span class="ctx-label">Bút dạ quang vàng</span>
    <span class="ctx-key">Dạ quang</span>
  </div>
  <div class="ctx-item" onclick="handleCtxAction('clearPen')">
    <span class="ctx-icon">🗑️</span>
    <span class="ctx-label">Xóa nét vẽ</span>
    <span class="ctx-key">Xóa nét</span>
  </div>
  <div class="ctx-divider"></div>
  <div class="ctx-item" onclick="handleCtxAction('calc')">
    <span class="ctx-icon">🔢</span>
    <span class="ctx-label">Máy tính Casio fx-580</span>
    <span class="ctx-key">Phím C</span>
  </div>
  <div class="ctx-item" onclick="handleCtxAction('blankScreen')">
    <span class="ctx-icon">⬛</span>
    <span class="ctx-label">Màn hình đen</span>
    <span class="ctx-key">Phím B</span>
  </div>
  <div class="ctx-divider"></div>
  <div class="ctx-item" onclick="handleCtxAction('readSlideEn')">
    <span class="ctx-icon">🔊</span>
    <span class="ctx-label">Đọc bài giảng EN</span>
    <span class="ctx-key">Song ngữ</span>
  </div>
  <div class="ctx-item" onclick="handleCtxAction('nextStep')">
    <span class="ctx-icon">↪️</span>
    <span class="ctx-label">Tiến 1 bước</span>
    <span class="ctx-key">Phím Phải</span>
  </div>
  <div class="ctx-item" onclick="handleCtxAction('prevStep')">
    <span class="ctx-icon">↩️</span>
    <span class="ctx-label">Lùi 1 bước</span>
    <span class="ctx-key">Phím Trái</span>
  </div>
</div>
"""

context_menu_js = """
  /* MENU CHUỘT PHẢI SƯ PHẠM (QUICK CONTEXT MENU) */
  function initContextMenu() {
    const ctx = document.getElementById('contextMenu');
    if (!ctx) return;

    window.addEventListener('contextmenu', function(e) {
      if (e.target.closest('input, textarea, [contenteditable="true"]')) return;
      e.preventDefault();
      e.stopPropagation();

      const isLaser = document.body.classList.contains('laser-mode');
      const isPen = document.body.classList.contains('pen-mode');
      const items = ctx.querySelectorAll('.ctx-item');
      if (items[0]) {
        items[0].classList.toggle('is-active', isLaser);
        const lbl = items[0].querySelector('.ctx-label');
        if (lbl) lbl.textContent = isLaser ? 'Tắt Laser' : 'Con trỏ Laser';
      }
      if (items[1]) {
        items[1].classList.toggle('is-active', isPen);
        const lbl = items[1].querySelector('.ctx-label');
        if (lbl) lbl.textContent = isPen ? 'Tắt Bút vẽ' : 'Bút vẽ màn hình';
      }

      const menuWidth = 240;
      const menuHeight = 360;
      let x = e.clientX;
      let y = e.clientY;
      if (x + menuWidth > window.innerWidth) x = window.innerWidth - menuWidth - 8;
      if (y + menuHeight > window.innerHeight) y = window.innerHeight - menuHeight - 8;

      ctx.style.left = Math.max(8, x) + 'px';
      ctx.style.top = Math.max(8, y) + 'px';
      ctx.style.display = 'flex';
    });

    window.addEventListener('click', function(e) {
      if (!e.target.closest('#contextMenu')) {
        hideContextMenu();
      }
    });

    window.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        hideContextMenu();
      }
    });
  }

  function hideContextMenu() {
    const ctx = document.getElementById('contextMenu');
    if (ctx) ctx.style.display = 'none';
  }

  function handleCtxAction(action) {
    hideContextMenu();
    if (action === 'laser') {
      toggleLaserMode();
    } else if (action === 'pen') {
      togglePenMode();
    } else if (action === 'highlighter') {
      if (!document.body.classList.contains('pen-mode')) togglePenMode(true);
      if (typeof setPenColor === 'function') setPenColor('rgba(250, 204, 21, 0.45)', 14, true);
    } else if (action === 'clearPen') {
      if (typeof clearDrawCanvas === 'function') clearDrawCanvas();
    } else if (action === 'calc') {
      toggleCalculator();
    } else if (action === 'blankScreen') {
      if (typeof toggleBlankScreen === 'function') toggleBlankScreen();
    } else if (action === 'readSlideEn') {
      if (typeof toggleReadSlideEn === 'function') toggleReadSlideEn();
    } else if (action === 'nextStep') {
      if (typeof nextStep === 'function') nextStep();
    } else if (action === 'prevStep') {
      if (typeof prevStep === 'function') prevStep();
    }
  }

  document.addEventListener('DOMContentLoaded', initContextMenu);
"""

# Toolbar CSS cho floating pill islands
grouped_toolbar_css = """
    /* Thanh điều khiển nổi gom nhóm độc lập (Floating Pill Islands) */
    .control-bar {
      position: fixed;
      bottom: 8px;
      left: 50%;
      transform: translateX(-50%);
      background: transparent !important;
      backdrop-filter: none !important;
      -webkit-backdrop-filter: none !important;
      border: none !important;
      box-shadow: none !important;
      padding: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      z-index: 1000;
      max-width: calc(100vw - 16px);
      overflow-x: auto;
      scrollbar-width: none;
      pointer-events: none;
    }
    .control-bar::-webkit-scrollbar {
      display: none;
    }
    .ctrl-group {
      pointer-events: auto;
      display: inline-flex;
      align-items: center;
      gap: 3px;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      padding: 4px 6px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.16);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
      flex-shrink: 0;
      transition: all 0.2s ease;
    }
    .ctrl-group:hover {
      border-color: rgba(255, 255, 255, 0.32);
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.6);
    }
    .ctrl-group-pedagogy {
      background: rgba(30, 27, 75, 0.94);
      border-color: rgba(129, 140, 248, 0.35);
    }
    .ctrl-group-pedagogy:hover {
      border-color: rgba(129, 140, 248, 0.65);
    }
    .ctrl-group-speech {
      background: rgba(15, 30, 42, 0.94);
      border-color: rgba(56, 189, 248, 0.35);
    }
    .ctrl-group-speech:hover {
      border-color: rgba(56, 189, 248, 0.65);
    }
"""

def upgrade_file(file_path):
    print(f"\n--- Upgrading: {file_path} ---")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Thêm Toolbar CSS nếu chưa có
    if '.ctrl-group' not in content:
        content = re.sub(
            r'/\*\s*Thanh điều khiển nổi\s*\*/\s*\.control-bar\s*\{[^}]*\}',
            grouped_toolbar_css.strip(),
            content
        )
        if '.ctrl-group' not in content:
            content = content.replace('</style>', f"\n{grouped_toolbar_css}\n</style>", 1)

    # 2. Thêm Context Menu CSS
    if '.context-menu' not in content:
        content = content.replace('</style>', f"\n{context_menu_css}\n</style>", 1)

    # 3. Thêm Casio CSS
    if '.casio-widget' not in content:
        content = content.replace('</style>', f"\n{casio_css}\n</style>", 1)

    # 4. Cập nhật HTML control-bar thành dạng 4 cụm pills
    if '<div class="ctrl-group ctrl-group-nav">' not in content:
        has_caption = 'showCaptionHelp' in content
        new_nav_html = """<nav class="control-bar" id="controlBar">
  <!-- Nhóm 1: Điều hướng Slide & Bước -->
  <div class="ctrl-group ctrl-group-nav">
    <button class="btn-ctrl" onclick="prevSlide()" title="Phím mũi tên Trái">◀ Trước</button>
    <button class="btn-ctrl" onclick="prevStep()" title="Lùi 1 bước">↩ Lùi</button>
    <button class="btn-ctrl btn-ctrl-primary" onclick="nextStep()" title="Phím mũi tên Phải hoặc chạm vùng trống">↪ Tiến bước</button>
    <button class="btn-ctrl" onclick="nextSlide()" title="Phím mũi tên Phải">Sau ▶</button>
  </div>

  <!-- Nhóm 2: Công cụ Sư phạm & Tương tác -->
  <div class="ctrl-group ctrl-group-pedagogy">
    <button class="btn-ctrl" id="btnLaser" onclick="toggleLaserMode()" title="Con trỏ laser (phím L)">🔴 Laser</button>
    <button class="btn-ctrl" id="btnPen" onclick="togglePenMode()" title="Bút vẽ & Dạ quang (phím P)">✏️ Vẽ</button>
    <button class="btn-ctrl" id="btnCalc" onclick="toggleCalculator()" title="Máy tính Casio fx-580VN X (phím C)">🔢 Máy tính</button>
  </div>

  <!-- Nhóm 3: Âm thanh & Song ngữ -->
  <div class="ctrl-group ctrl-group-speech">
    <button class="btn-ctrl" id="btnToggleLang" onclick="toggleLanguage()" title="Chuyển đổi song ngữ Việt / Anh">🌐 Song ngữ</button>
    <button class="btn-ctrl btn-speech" id="btnReadSlideEn" onclick="toggleReadSlideEn()" title="Trợ giảng AI đọc tiếng Anh">🔊 Đọc EN</button>
    <button class="btn-ctrl" id="btnSpeechRate" onclick="cycleSpeechRate()" title="Đổi tốc độ đọc: 0.85x ⇄ 0.75x ⇄ 0.5x ⇄ 1.0x">⚡ 0.85x</button>""" + ("""
    <button class="btn-ctrl" id="btnHelpCaption" onclick="showCaptionHelp()" title="Cách tắt phụ đề tự động (Live Caption)">💬 Phụ đề</button>""" if has_caption else "") + """
  </div>

  <!-- Nhóm 4: Cài đặt hiển thị & Lưu bài -->
  <div class="ctrl-group ctrl-group-settings">
    <button class="btn-ctrl" onclick="toggleFullscreen()" title="Toàn màn hình (F11)">⛶ Toàn màn hình</button>
    <button class="btn-ctrl" id="btnFontSize" onclick="cycleFontSize()" title="Đổi cỡ chữ TV: 28px ⇄ 30px ⇄ 22px">🔤 TV 28px</button>
    <button class="btn-ctrl" id="btnSaveLecture" onclick="saveLecture()" title="Lưu trực tiếp đè vào file">💾 Lưu</button>
    <button class="btn-ctrl btn-ctrl-mode" id="btnToggleMode" onclick="toggleMode()">⚙ Thiết kế</button>
  </div>
</nav>"""
        m_bar = re.search(r'<nav class="control-bar" id="controlBar">[\s\S]*?</nav>', content)
        if m_bar:
            content = content[:m_bar.start()] + new_nav_html + content[m_bar.end():]
    else:
        # Nếu đã có ctrl-group nhưng chưa có btnCalc trong pedagogy
        if 'id="btnCalc"' not in content:
            m_ped = re.search(r'(<div class="ctrl-group ctrl-group-pedagogy">[\s\S]*?)(</div>)', content)
            if m_ped:
                calc_btn = '\n    <button class="btn-ctrl" id="btnCalc" onclick="toggleCalculator()" title="Máy tính Casio fx-580VN X (phím C)">🔢 Máy tính</button>\n  '
                content = content[:m_ped.start()] + m_ped.group(1) + calc_btn + m_ped.group(2) + content[m_ped.end():]

    # 5. Thêm HTML Casio Widget
    if 'id="casioWidget"' not in content:
        if '<nav class="control-bar"' in content:
            content = content.replace('<nav class="control-bar"', f"{casio_html}\n\n<nav class=\"control-bar\"", 1)
        else:
            content = content.replace('</body>', f"{casio_html}\n</body>", 1)

    # 6. Thêm HTML Context Menu nếu chưa có
    if 'id="contextMenu"' not in content:
        if 'id="casioWidget"' in content:
            content = content.replace('<div id="casioWidget"', f"{context_menu_html}\n\n<div id=\"casioWidget\"", 1)
        elif '<nav class="control-bar"' in content:
            content = content.replace('<nav class="control-bar"', f"{context_menu_html}\n\n<nav class=\"control-bar\"", 1)
        else:
            content = content.replace('</body>', f"{context_menu_html}\n</body>", 1)
    else:
        # Đã có contextMenu, kiểm tra xem đã có nút Casio trong menu chưa
        if "handleCtxAction('calc')" not in content:
            calc_ctx_item = """  <div class="ctx-item" onclick="handleCtxAction('calc')">
    <span class="ctx-icon">🔢</span>
    <span class="ctx-label">Máy tính Casio fx-580</span>
    <span class="ctx-key">Phím C</span>
  </div>\n"""
            content = content.replace("<div class=\"ctx-divider\"></div>", calc_ctx_item + "  <div class=\"ctx-divider\"></div>", 1)

    # 7. Thêm Context Menu JS nếu chưa có
    if 'function initContextMenu' not in content:
        last_script = content.rfind('</script>')
        if last_script != -1:
            content = content[:last_script] + f"\n{context_menu_js}\n" + content[last_script:]
    else:
        # Nếu đã có initContextMenu, đảm bảo handleCtxAction xử lý 'calc'
        if "action === 'calc'" not in content:
            content = content.replace(
                "if (action === 'laser')",
                "if (action === 'calc') {\n      toggleCalculator();\n    } else if (action === 'laser')"
            )

    # 8. Cập nhật phím tắt keydown trong slide: Phím C (vẽ nét thì xóa nét, bình thường thì mở máy tính)
    # Tìm đoạn phím C trong keydown
    content = re.sub(
        r"if\s*\(\s*e\.key\s*===\s*['\"]c['\"]\s*\|\|\s*e\.key\s*===\s*['\"]C['\"]\s*\)\s*\{[\s\S]*?clearDrawCanvas\(\);[\s\S]*?return;\s*\}",
        """if (e.key === 'c' || e.key === 'C') {
      e.preventDefault();
      if (document.body.classList.contains('pen-mode')) {
        clearDrawCanvas();
      } else {
        toggleCalculator();
      }
      return;
    }""",
        content
    )

    # Cập nhật Escape: đóng máy tính nếu đang mở
    if "toggleCalculator(false);" not in content:
        content = re.sub(
            r"(if\s*\(\s*e\.key\s*===\s*['\"]Escape['\"]\s*\)\s*\{)",
            r"\1\n      toggleCalculator(false);",
            content
        )

    # 9. Thêm PURE Casio JS vào trước </script>
    if 'function solveFmt' not in content:
        last_script = content.rfind('</script>')
        if last_script != -1:
            content = content[:last_script] + f"\n{casio_pure_js}\n" + content[last_script:]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully updated {file_path}")

targets = [
    r'TROLYTHIEN\10_BAI_GIANG_HTML\templates\master_lecture_template.html',
    r'TROLYTHIEN\10_BAI_GIANG_HTML\Ket_qua\Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
]

for t in targets:
    upgrade_file(t)
