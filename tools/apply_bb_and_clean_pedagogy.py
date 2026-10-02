import re
import sys
import os
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

# Đọc mã Bảng viết phấn từ master_lecture_template.html
with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    tmpl_text = f.read()

# 1. Trích xuất Blackboard CSS
c_start = tmpl_text.find('/* BẢNG VIẾT PHẤN NÂNG CẤP: THANH CHỌN BỀ MẶT BẢNG VÀ MÀU PHẤN */')
c_end = tmpl_text.find('/* Accordion Toggle Answer */', c_start)
bb_css = tmpl_text[c_start:c_end].strip()

# 2. Trích xuất Blackboard HTML
h_start = tmpl_text.find('<div id="blackboardOverlay"')
h_end = tmpl_text.find('</div>\n\n<!-- THANH ĐIỀU KHIỂN', h_start)
if h_end == -1:
    h_end = tmpl_text.find('</div>\n<!-- THANH ĐIỀU KHIỂN', h_start)
bb_html = tmpl_text[h_start:h_end].strip()

# 3. Trích xuất Blackboard JS
bb_js = """
  /* === BẢNG VIẾT PHẤN ĐA BỀ MẶT (MULTI-SURFACE CHALKBOARD) === */
  let chalkColor = '#f8fafc', chalkWidth = 4, chalkDrawing = false, chalkShift = false, chalkStart = null, chalkSnap = null;
  function resizeBlackboard() {
    const canvas = document.getElementById('blackboardCanvas');
    const overlay = document.getElementById('blackboardOverlay');
    if (!canvas || !overlay) return;
    const ratio = window.devicePixelRatio || 1;
    const w = overlay.clientWidth || window.innerWidth;
    const h = overlay.clientHeight || window.innerHeight;
    const prev = canvas.getContext('2d').getImageData(0, 0, canvas.width || 1, canvas.height || 1);
    canvas.width = Math.floor(w * ratio);
    canvas.height = Math.floor(h * ratio);
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    const ctx = canvas.getContext('2d');
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    if (prev.width > 1) ctx.putImageData(prev, 0, 0);
  }
  function toggleBlackboard(force) {
    const overlay = document.getElementById('blackboardOverlay');
    if (!overlay) return;
    const on = typeof force === 'boolean' ? force : !overlay.classList.contains('active');
    overlay.classList.toggle('active', on);
    overlay.setAttribute('aria-hidden', on ? 'false' : 'true');
    const btn = document.getElementById('btnBlackboard');
    if (btn) btn.classList.toggle('is-on', on);
    if (on) resizeBlackboard();
  }
  function setChalk(color, width) { chalkColor = color; chalkWidth = width; }
  function clearBlackboard() {
    const canvas = document.getElementById('blackboardCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.restore();
  }
  function bindBlackboard() {
    const canvas = document.getElementById('blackboardCanvas');
    if (!canvas || canvas.dataset.bound) return;
    canvas.dataset.bound = '1';
    const ctx = canvas.getContext('2d');
    function point(e) {
      const r = canvas.getBoundingClientRect();
      const src = (e.touches && e.touches[0]) || e;
      return { x: src.clientX - r.left, y: src.clientY - r.top };
    }
    function start(e) {
      if (!document.getElementById('blackboardOverlay').classList.contains('active')) return;
      e.preventDefault();
      chalkDrawing = true;
      chalkShift = !!(e.shiftKey);
      chalkStart = point(e);
      chalkSnap = ctx.getImageData(0, 0, canvas.width, canvas.height);
      ctx.beginPath(); ctx.moveTo(chalkStart.x, chalkStart.y);
    }
    function move(e) {
      if (!chalkDrawing) return;
      e.preventDefault();
      const p = point(e);
      if (e.shiftKey || chalkShift) {
        ctx.putImageData(chalkSnap, 0, 0);
        ctx.beginPath();
        ctx.moveTo(chalkStart.x, chalkStart.y);
        ctx.lineTo(p.x, p.y);
        ctx.strokeStyle = chalkColor; ctx.lineWidth = chalkWidth; ctx.lineCap = 'round';
        ctx.stroke();
        return;
      }
      ctx.strokeStyle = chalkColor; ctx.lineWidth = chalkWidth; ctx.lineCap = 'round';
      ctx.lineTo(p.x, p.y); ctx.stroke(); ctx.beginPath(); ctx.moveTo(p.x, p.y);
    }
    function end() { chalkDrawing = false; chalkSnap = null; }
    canvas.addEventListener('mousedown', start);
    canvas.addEventListener('mousemove', move);
    window.addEventListener('mouseup', end);
    canvas.addEventListener('touchstart', start, { passive: false });
    canvas.addEventListener('touchmove', move, { passive: false });
    canvas.addEventListener('touchend', end);
  }
  document.addEventListener('DOMContentLoaded', bindBlackboard);
  window.addEventListener('resize', resizeBlackboard);

  function setBoardSurface(type) {
    const bb = document.getElementById('blackboardOverlay');
    if (!bb) return;
    bb.classList.remove('surface-green', 'surface-white', 'surface-grid', 'surface-black');
    bb.classList.add('surface-' + type);
    document.querySelectorAll('.bb-surfaces .btn-bb').forEach(btn => {
      btn.classList.toggle('is-active', btn.onclick && btn.onclick.toString().includes("'" + type + "'"));
    });
    if (type === 'white') {
      setChalkColor('#0f172a', 3);
    } else {
      setChalkColor('#ffffff', 3);
    }
  }

  function setChalkColor(color, size) {
    chalkColor = color;
    chalkWidth = size || 3;
    document.querySelectorAll('.bb-chalks .btn-bb-color').forEach(btn => {
      const oc = (btn.getAttribute('style') || '');
      btn.classList.toggle('is-active', oc.includes(color));
    });
  }

  function clearBlackboardCanvas() {
    clearBlackboard();
  }
"""

def update_lecture_bai_4():
    path = r'TROLYTHIEN\10_BAI_GIANG_HTML\Ket_qua\Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # A. XÓA BỎ CÁC KHỐI GHI CHÚ SƯ PHẠM CỦA GIÁO VIÊN
    # 1. Xóa khối s7_t1: HƯỚNG DẪN TƯ DUY SƯ PHẠM
    content = re.sub(
        r'<div class="content-block"[^>]*id="s7_t1"[\s\S]*?<strong>HƯỚNG DẪN TƯ DUY SƯ PHẠM</strong>[\s\S]*?</div>\s*</div>',
        '',
        content
    )
    # 2. Xóa khối s26_t2: THÔNG ĐIỆP SƯ PHẠM
    content = re.sub(
        r'<div class="content-block[^"]*"[^>]*id="s26_t2"[\s\S]*?<strong>THÔNG ĐIỆP SƯ PHẠM</strong>[\s\S]*?</div>\s*</div>',
        '',
        content
    )

    # B. THÊM BẢNG VIẾT PHẤN / BẢNG VẼ
    # 1. Thêm CSS
    if '.blackboard-top-bar' not in content:
        content = content.replace('</style>', f"\n{bb_css}\n</style>", 1)

    # 2. Thêm HTML
    if 'id="blackboardOverlay"' not in content:
        # Chèn trước #casioWidget hoặc trước <nav class="control-bar"
        if '<div id="casioWidget"' in content:
            content = content.replace('<div id="casioWidget"', f"{bb_html}\n\n<div id=\"casioWidget\"", 1)
        elif '<nav class="control-bar"' in content:
            content = content.replace('<nav class="control-bar"', f"{bb_html}\n\n<nav class=\"control-bar\"", 1)

    # 3. Thêm nút Bảng vẽ vào .ctrl-group-pedagogy
    if 'id="btnBlackboard"' not in content:
        btn_bb_html = '<button class="btn-ctrl" id="btnBlackboard" onclick="toggleBlackboard()" title="Bảng viết vẽ toàn màn hình (phím W / Chuột phải)">📋 Bảng vẽ</button>'
        # Chèn sau btnPen hoặc trước btnCalc
        if '<button class="btn-ctrl" id="btnPen"' in content:
            content = re.sub(
                r'(<button class="btn-ctrl" id="btnPen"[^>]*>.*?</button>)',
                r'\1\n    ' + btn_bb_html,
                content
            )
        elif '<button class="btn-ctrl" id="btnCalc"' in content:
            content = content.replace(
                '<button class="btn-ctrl" id="btnCalc"',
                f"{btn_bb_html}\n    <button class=\"btn-ctrl\" id=\"btnCalc\""
            )

    # 4. Thêm JS Bảng viết phấn
    if 'function resizeBlackboard' not in content:
        last_script = content.rfind('</script>')
        if last_script != -1:
            content = content[:last_script] + f"\n{bb_js}\n" + content[last_script:]

    # 5. Phím tắt W và Escape cho Bảng viết
    # Kiểm tra keydown cho phím W
    if "e.key === 'w' || e.key === 'W'" not in content:
        # Chèn vào keydown listener
        content = re.sub(
            r"(if\s*\(\s*e\.key\s*===\s*['\"]c['\"]\s*\|\|\s*e\.key\s*===\s*['\"]C['\"]\s*\)\s*\{)",
            r"if (e.key === 'w' || e.key === 'W') {\n      e.preventDefault();\n      toggleBlackboard();\n      return;\n    }\n    \1",
            content
        )

    # Escape đóng cả bảng viết nếu đang mở
    if "toggleBlackboard(false);" not in content:
        content = re.sub(
            r"(if\s*\(\s*e\.key\s*===\s*['\"]Escape['\"]\s*\)\s*\{)",
            r"\1\n      toggleBlackboard(false);",
            content
        )

    # Menu chuột phải có mục Bảng viết
    if "handleCtxAction('blackboard')" not in content:
        bb_ctx_item = """  <div class="ctx-item" onclick="handleCtxAction('blackboard')">
    <span class="ctx-icon">📋</span>
    <span class="ctx-label">Bảng viết vẽ đa năng</span>
    <span class="ctx-key">Phím W</span>
  </div>\n"""
        content = content.replace(
            '<div class="ctx-item" onclick="handleCtxAction(\'calc\')">',
            bb_ctx_item + '  <div class="ctx-item" onclick="handleCtxAction(\'calc\')">'
        )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated Bai_4 successfully!")

def update_master_template():
    path = r'TROLYTHIEN\10_BAI_GIANG_HTML\templates\master_lecture_template.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Đảm bảo nhóm sư phạm trong template có đầy đủ: Laser, Vẽ, Bảng vẽ, Máy tính, Bấm giờ
    ped_full = """  <!-- Nhóm 4: Công cụ Sư phạm & Tương tác -->
  <div class="ctrl-group ctrl-group-pedagogy">
    <button class="btn-ctrl" id="btnLaser" onclick="toggleLaserMode()" title="Con trỏ laser (phím L)">🔴 Laser</button>
    <button class="btn-ctrl" id="btnPen" onclick="togglePenMode()" title="Bút vẽ màn hình (phím P)">✏️ Vẽ</button>
    <button class="btn-ctrl" id="btnBlackboard" onclick="toggleBlackboard()" title="Bảng viết vẽ toàn màn hình (phím W / Chuột phải)">📋 Bảng vẽ</button>
    <button class="btn-ctrl" id="btnCalc" onclick="toggleCalculator()" title="Máy tính Casio fx-580VN X (phím C)">🔢 Máy tính</button>
    <button class="btn-ctrl" id="btnTimer" onclick="toggleTimerModal()" title="Đồng hồ đếm ngược thảo luận (phím T)">⏱️ Bấm giờ</button>
  </div>"""

    content = re.sub(
        r'<!-- Nhóm 4: Công cụ Sư phạm -->\s*<div class="ctrl-group ctrl-group-pedagogy">[\s\S]*?</div>',
        ped_full,
        content
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated master_lecture_template successfully!")

update_lecture_bai_4()
update_master_template()
