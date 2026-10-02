import os
import glob
import re

html_files = glob.glob(r'TROLYTHIEN\10_BAI_GIANG_HTML\Ket_qua\*.html')

grouped_css = """
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

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Cập nhật CSS nếu chưa có .ctrl-group
    if '.ctrl-group' not in content:
        # Thay thế CSS của .control-bar
        content = re.sub(
            r'/\*\s*Thanh điều khiển nổi\s*\*/\s*\.control-bar\s*\{[^}]*\}',
            grouped_css.strip(),
            content
        )

    # 2. Cập nhật HTML của nav#controlBar
    m = re.search(r'<nav class="control-bar" id="controlBar">([\s\S]*?)</nav>', content)
    if m and 'ctrl-group' not in m.group(1):
        inner = m.group(1)
        
        # Trích xuất các nút bấm hiện có
        has_caption = 'showCaptionHelp' in inner
        
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
        
        content = content[:m.start()] + new_nav_html + content[m.end():]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {os.path.basename(file_path)}")
    else:
        print(f"Already grouped: {os.path.basename(file_path)}")
