import os
import re
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

BOARD_CSS = """
    /* ==========================================================================
       BẢNG VIẾT TOÀN MÀN HÌNH VỚI ẢNH TỰ DO KÉO THẢ / CO GIÃN / XOÁ
       ========================================================================== */
    .blackboard-overlay, #blackboardOverlay {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 10000;
      background-color: #14532d;
      background-image: 
        linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px);
      background-size: 32px 32px;
    }
    .blackboard-overlay.active, #blackboardOverlay.active { display: block; }
    .blackboard-overlay.theme-white, #blackboardOverlay.theme-white {
      background-color: #f8fafc;
      background-image: 
        linear-gradient(rgba(0,0,0,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,0,0,0.06) 1px, transparent 1px);
    }
    .blackboard-overlay.theme-dark, #blackboardOverlay.theme-dark {
      background-color: #0f172a;
      background-image: 
        linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
    }

    /* Hộp ảnh nổi tương tác tự do trên bảng viết */
    .board-floating-image-box {
      position: absolute;
      top: 80px;
      left: 40px;
      z-index: 10005;
      display: none;
      background: rgba(255,255,255,0.95);
      border: 2px solid #38bdf8;
      border-radius: 8px;
      box-shadow: 0 12px 35px rgba(0,0,0,0.5);
      user-select: none;
      touch-action: none;
      min-width: 140px;
      min-height: 100px;
    }
    .board-floating-image-box.active { display: inline-flex; flex-direction: column; }
    .board-img-header {
      background: #1e293b;
      color: #38bdf8;
      padding: 4px 8px;
      font-size: 11px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: move;
      border-top-left-radius: 6px;
      border-top-right-radius: 6px;
    }
    .float-photo-bar {
      display: flex;
      align-items: center;
      gap: 4px;
      background: #0f172a;
      color: #e2e8f0;
      padding: 4px 6px;
      cursor: grab;
      border-radius: 8px 8px 0 0;
      touch-action: none;
      user-select: none;
    }
    .float-photo-bar span { font-size: 12px; font-weight: 700; margin-right: 4px; }
    .float-photo-btn {
      min-width: 32px;
      min-height: 32px;
      border: 1px solid #475569;
      background: #1e293b;
      color: #f8fafc;
      border-radius: 6px;
      font-size: 15px;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
    .float-photo-btn:hover { background: #334155; }
    .float-photo-btn.danger { background: #b91c1c; border-color: #ef4444; }
    .float-photo-btn.danger:hover { background: #991b1b; }
    .board-img-body {
      padding: 6px;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .board-img-body img, #boardInsertedImg {
      display: block;
      width: 320px;
      height: auto;
      max-width: 48vw;
      max-height: 70vh;
      object-fit: contain;
      border-radius: 4px;
      pointer-events: none;
      transform-origin: center center;
    }
    /* Chốt kéo co giãn ảnh (Resize handle) */
    .resize-handle-br {
      position: absolute;
      right: 0;
      bottom: 0;
      width: 18px;
      height: 18px;
      cursor: nwse-resize;
      background: linear-gradient(135deg, transparent 50%, #0284c7 50%);
      border-bottom-right-radius: 6px;
    }

    .blackboard-canvas, #blackboardCanvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      touch-action: none;
      cursor: crosshair;
      z-index: 10002;
    }
    .blackboard-tools {
      position: absolute;
      top: 14px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 8px;
      z-index: 10008;
      background: rgba(15, 23, 42, 0.94);
      border: 1px solid #475569;
      border-radius: 999px;
      padding: 8px 18px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
      align-items: center;
      flex-wrap: wrap;
      justify-content: center;
    }
    .chalk-dot {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      cursor: pointer;
      border: 2px solid white;
      transition: transform 0.15s;
    }
    .chalk-dot:hover { transform: scale(1.2); }
    .chalk-dot.is-active { box-shadow: 0 0 0 2px #38bdf8; }
    .board-btn {
      background: #334155;
      color: white;
      border: 1px solid #64748b;
      border-radius: 999px;
      padding: 5px 12px;
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .board-btn:hover { background: #475569; }
    .board-btn.close { background: #b91c1c; border-color: #ef4444; }
    .board-btn.close:hover { background: #991b1b; }
    .board-btn.img-btn { background: #7c3aed; border-color: #a78bfa; }
    .board-btn.img-btn:hover { background: #6d28d9; }
"""

BOARD_HTML = """<div id="blackboardOverlay" class="blackboard-overlay surface-green" aria-hidden="true">
  <!-- Hộp ảnh nổi tương tác tự do trên bảng viết -->
  <div id="boardImageBox" class="board-floating-image-box">
    <div class="float-photo-bar" id="boardImgHeader">
      <span>Kéo ảnh</span>
      <button type="button" class="float-photo-btn" onclick="zoomBoardImg(0.2); event.stopPropagation();" title="Phóng to">+</button>
      <button type="button" class="float-photo-btn" onclick="zoomBoardImg(-0.2); event.stopPropagation();" title="Thu nhỏ">−</button>
      <button type="button" class="float-photo-btn" onclick="rotateBoardImg(); event.stopPropagation();" title="Xoay 90 độ">↻</button>
      <button type="button" class="float-photo-btn" onclick="resetBoardImg(); event.stopPropagation();" title="Đặt lại kích thước">↺</button>
      <button type="button" class="float-photo-btn danger" onclick="removeBoardImage(); event.stopPropagation();" title="Xóa ảnh">🗑️</button>
    </div>
    <div class="board-img-body" id="boardImgBody">
      <img id="boardInsertedImg" src="" alt="Ảnh trên bảng">
      <div class="resize-handle-br" id="boardImgResizeHandle" title="Kéo góc này để phóng to/thu nhỏ ảnh"></div>
    </div>
  </div>

  <!-- Thanh công cụ phấn & bảng -->
  <div class="blackboard-tools">
    <span style="color:#e2e8f0; font-size:13px; font-weight:700;">PHẤN:</span>
    <div class="chalk-dot" style="background:#ffffff;" onclick="setChalk('#ffffff', 3.5)" title="Phấn trắng"></div>
    <div class="chalk-dot" style="background:#fde047;" onclick="setChalk('#fde047', 3.5)" title="Phấn vàng"></div>
    <div class="chalk-dot" style="background:#f472b6;" onclick="setChalk('#f472b6', 3.5)" title="Phấn hồng"></div>
    <div class="chalk-dot" style="background:#38bdf8;" onclick="setChalk('#38bdf8', 3.5)" title="Phấn xanh"></div>
    <button type="button" class="board-btn" onclick="setChalk(chalkColor, 2.5)">Mảnh</button>
    <button type="button" class="board-btn" onclick="setChalk(chalkColor, 6)">Đậm</button>
    
    <!-- Chèn ảnh vào bảng -->
    <label class="board-btn img-btn" title="Tải ảnh từ máy chèn vào bảng">
      📁 Chèn Ảnh
      <input type="file" id="boardFileInput" accept="image/*" style="display:none" onchange="handleBoardImageUpload(event)">
    </label>
    <button type="button" class="board-btn img-btn" onclick="alert('Thầy hãy chụp màn hình (Win + Shift + S) rồi bấm Ctrl + V trên bàn phím để dán ảnh vào bảng!')" title="Dán ảnh từ Clipboard (Ctrl+V)">📋 Dán (Ctrl+V)</button>
    
    <button type="button" class="board-btn" onclick="toggleBoardTheme()" title="Đổi Bảng xanh / Bảng trắng / Bảng đen">🎨 Đổi Bảng</button>
    <button type="button" class="board-btn" onclick="clearBlackboard()" title="Xoá sạch nét phấn">🗑️ Xoá Phấn</button>
    <button type="button" class="board-btn close" onclick="toggleBlackboard(false)" title="Đóng bảng (Phím W hoặc Esc)">❌ Đóng Bảng (W)</button>
    <span style="color:#94a3b8; font-size:12px; margin-left:4px;">💡 Giữ Shift để kẻ đường thẳng</span>
  </div>
  
  <canvas id="blackboardCanvas" class="blackboard-canvas"></canvas>
</div>"""

PEDAGOGY_GROUP = """  <div class="ctrl-group ctrl-group-pedagogy">
    <button class="btn-ctrl" id="btnBoard" onclick="toggleBlackboard()" title="Bảng viết vẽ toàn màn hình & Chèn ảnh (Phím W)">📋 Bảng viết</button>
    <button class="btn-ctrl" id="btnTimer" onclick="toggleTimerModal()" title="Đồng hồ đếm ngược thảo luận/làm bài (Phím T)">⏱️ Bấm giờ</button>
    <button class="btn-ctrl" id="btnCalc" onclick="toggleCalculator()" title="Máy tính Casio fx-580VN X (Phím C)">🔢 Máy tính</button>
  </div>"""

CONTEXT_MENU = """<div id="contextMenu" class="context-menu" style="display:none;" aria-hidden="true">
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
  <div class="ctx-item" onclick="handleCtxAction('blankScreen')">
    <span class="ctx-icon">⬛</span>
    <span class="ctx-label">Màn hình đen</span>
    <span class="ctx-key">Phím B</span>
  </div>
</div>"""

BOARD_JS = """
  /* === BẢNG VIẾT TOÀN MÀN HÌNH VỚI ẢNH TỰ DO KÉO THẢ / CO GIÃN / XOÁ === */
  let chalkDrawing = false;
  let chalkColor = '#ffffff';
  let chalkWidth = 3.5;
  let chalkStart = null;
  let chalkSnap = null;
  const boardThemes = ['', 'theme-white', 'theme-dark'];
  let boardThemeIdx = 0;
  let boardImgAngle = 0;

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
    const btn = document.getElementById('btnBoard') || document.getElementById('btnBlackboard');
    if (btn) btn.classList.toggle('is-on', on);
    if (on) {
      resizeBlackboard();
      if (typeof togglePenMode === 'function') togglePenMode(false);
      if (typeof toggleLaserMode === 'function') toggleLaserMode(false);
    }
  }

  function setChalk(col, w) {
    chalkColor = col;
    chalkWidth = w || 3.5;
  }

  function toggleBoardTheme() {
    const overlay = document.getElementById('blackboardOverlay');
    if (!overlay) return;
    boardThemes.forEach(t => t && overlay.classList.remove(t));
    boardThemeIdx = (boardThemeIdx + 1) % boardThemes.length;
    if (boardThemes[boardThemeIdx]) overlay.classList.add(boardThemes[boardThemeIdx]);
    if (boardThemeIdx === 1) chalkColor = '#0f172a';
    else chalkColor = '#ffffff';
  }

  function clearBlackboard() {
    const canvas = document.getElementById('blackboardCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.restore();
  }

  // XỬ LÝ ẢNH TRÊN BẢNG VIẾT (KÉO THẢ, CO GIÃN, XOÁ, XOAY)
  function handleBoardImageUpload(e) {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = function(evt) {
        setBoardImage(evt.target.result);
      };
      reader.readAsDataURL(file);
    }
  }

  function setBoardImage(dataUrl) {
    const box = document.getElementById('boardImageBox');
    const img = document.getElementById('boardInsertedImg');
    if (!box || !img) return;
    img.src = dataUrl;
    box.style.left = '40px';
    box.style.top = '80px';
    boardImgAngle = 0;
    img.style.width = '320px';
    img.style.height = 'auto';
    applyBoardImgVisual();
    box.classList.add('active');
    initBoardImageInteractions();
  }

  function removeBoardImage() {
    const box = document.getElementById('boardImageBox');
    const img = document.getElementById('boardInsertedImg');
    if (!box || !img) return;
    img.src = '';
    box.classList.remove('active');
  }

  function zoomBoardImg(delta) {
    const img = document.getElementById('boardInsertedImg');
    if (!img) return;
    const currentW = img.clientWidth;
    img.style.width = Math.max(100, currentW * (1 + delta)) + 'px';
    img.style.height = 'auto';
  }

  function applyBoardImgVisual() {
    const img = document.getElementById('boardInsertedImg');
    if (img) img.style.transform = 'rotate(' + boardImgAngle + 'deg)';
  }

  function rotateBoardImg() {
    boardImgAngle = (boardImgAngle + 90) % 360;
    applyBoardImgVisual();
  }

  function resetBoardImg() {
    const box = document.getElementById('boardImageBox');
    const img = document.getElementById('boardInsertedImg');
    boardImgAngle = 0;
    if (img) {
      img.style.width = '320px';
      img.style.height = 'auto';
      applyBoardImgVisual();
    }
    if (box) {
      box.style.left = '40px';
      box.style.top = '80px';
    }
  }

  function initBoardImageInteractions() {
    const box = document.getElementById('boardImageBox');
    const header = document.getElementById('boardImgHeader');
    const body = document.getElementById('boardImgBody');
    const handle = document.getElementById('boardImgResizeHandle');
    const img = document.getElementById('boardInsertedImg');
    if (!box || !header || !handle || !img || box.dataset.interactBound) return;
    box.dataset.interactBound = '1';

    function bindDrag(surface) {
      let drag = null;
      surface.addEventListener('pointerdown', function (e) {
        if (e.target.closest('button') || e.target.closest('.resize-handle-br')) return;
        e.preventDefault();
        e.stopPropagation();
        drag = { x: e.clientX, y: e.clientY, l: box.offsetLeft, t: box.offsetTop };
        surface.setPointerCapture(e.pointerId);
      });
      surface.addEventListener('pointermove', function (e) {
        if (!drag) return;
        box.style.left = Math.max(0, drag.l + e.clientX - drag.x) + 'px';
        box.style.top = Math.max(0, drag.t + e.clientY - drag.y) + 'px';
      });
      surface.addEventListener('pointerup', function () { drag = null; });
      surface.addEventListener('pointercancel', function () { drag = null; });
    }
    bindDrag(header);
    if (body) bindDrag(body);

    let resize = null;
    handle.addEventListener('pointerdown', function (e) {
      e.preventDefault();
      e.stopPropagation();
      resize = { x: e.clientX, w: img.getBoundingClientRect().width || 240 };
      handle.setPointerCapture(e.pointerId);
    });
    handle.addEventListener('pointermove', function (e) {
      if (!resize) return;
      img.style.width = Math.max(80, resize.w + e.clientX - resize.x) + 'px';
      img.style.height = 'auto';
    });
    handle.addEventListener('pointerup', function () { resize = null; });
    handle.addEventListener('pointercancel', function () { resize = null; });

    box.addEventListener('wheel', function (e) {
      e.preventDefault();
      e.stopPropagation();
      zoomBoardImg(e.deltaY < 0 ? 0.15 : -0.15);
    }, { passive: false });
  }

  function bindBlackboard() {
    const canvas = document.getElementById('blackboardCanvas');
    if (!canvas || canvas.dataset.bound) return;
    canvas.dataset.bound = '1';
    const ctx = canvas.getContext('2d');

    function bPoint(e) {
      const r = canvas.getBoundingClientRect();
      const src = (e.touches && e.touches[0]) || e;
      return { x: src.clientX - r.left, y: src.clientY - r.top };
    }

    function start(e) {
      const overlay = document.getElementById('blackboardOverlay');
      if (!overlay || !overlay.classList.contains('active')) return;
      // Bỏ qua nếu thao tác trên hộp ảnh hoặc thanh công cụ
      if (e.target.closest('#boardImageBox') || e.target.closest('.blackboard-tools')) return;
      e.preventDefault();
      chalkDrawing = true;
      chalkStart = bPoint(e);
      chalkSnap = ctx.getImageData(0, 0, canvas.width, canvas.height);
      ctx.beginPath();
      ctx.moveTo(chalkStart.x, chalkStart.y);
    }

    function move(e) {
      if (!chalkDrawing) return;
      e.preventDefault();
      const p = bPoint(e);
      if (e.shiftKey) {
        ctx.putImageData(chalkSnap, 0, 0);
        ctx.beginPath();
        ctx.moveTo(chalkStart.x, chalkStart.y);
        ctx.lineTo(p.x, p.y);
        ctx.strokeStyle = chalkColor;
        ctx.lineWidth = chalkWidth;
        ctx.lineCap = 'round';
        ctx.stroke();
        return;
      }
      ctx.strokeStyle = chalkColor;
      ctx.lineWidth = chalkWidth;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.lineTo(p.x, p.y);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
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

  // Lắng nghe dán ảnh từ clipboard (Ctrl + V)
  window.addEventListener('paste', function(e) {
    const overlay = document.getElementById('blackboardOverlay');
    if (!overlay || !overlay.classList.contains('active')) return;
    const items = (e.clipboardData || e.originalEvent.clipboardData).items;
    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf('image') !== -1) {
        const blob = items[i].getAsFile();
        const reader = new FileReader();
        reader.onload = function(evt) { setBoardImage(evt.target.result); };
        reader.readAsDataURL(blob);
        e.preventDefault();
        break;
      }
    }
  });
"""

def upgrade_file(filepath):
    print(f"=== Processing: {filepath} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_len = len(content)

    # 1. Update CSS
    # Find '/* BẢNG VIẾT PHẤN NÂNG CẤP: THANH CHỌN BỀ MẶT BẢNG VÀ MÀU PHẤN */'
    c_start = content.find('/* BẢNG VIẾT PHẤN NÂNG CẤP: THANH CHỌN BỀ MẶT BẢNG VÀ MÀU PHẤN */')
    if c_start != -1:
        c_end = content.find('/* Accordion Toggle Answer */', c_start)
        if c_end == -1:
            c_end = content.find('</style>', c_start)
        if c_end != -1:
            content = content[:c_start] + BOARD_CSS.strip() + "\n\n    " + content[c_end:]
            print("  [1] Replaced blackboard CSS block")
        else:
            print("  [!] Could not find end of CSS block")
    else:
        print("  [!] Could not find start of blackboard CSS block")

    # Also remove duplicate old #blackboardOverlay { ... } if exists
    dup_re = re.compile(r'#blackboardOverlay\s*\{\s*display:\s*none;[\s\S]*?\.blackboard-tools\s*button\s*\{[^}]*\}\s*', re.MULTILINE)
    if dup_re.search(content):
        content = dup_re.sub('', content)
        print("  [1b] Removed duplicate old blackboard CSS block")

    # 2. Update HTML
    # Replace <div id="blackboardOverlay" ... up to <canvas id="blackboardCanvas"></canvas>(\s*</div>)?
    h_re = re.compile(r'<div id="blackboardOverlay"[\s\S]*?<canvas id="blackboardCanvas"></canvas>(\s*</div>)?', re.MULTILINE)
    if h_re.search(content):
        content = h_re.sub(BOARD_HTML.strip(), content, count=1)
        print("  [2] Replaced blackboard HTML block")
    else:
        print("  [!] Could not find blackboard HTML block")

    # 3. Update Toolbar Pedagogy Group
    tb_re = re.compile(r'<div class="ctrl-group ctrl-group-pedagogy">[\s\S]*?</div>', re.MULTILINE)
    if tb_re.search(content):
        content = tb_re.sub(PEDAGOGY_GROUP.strip(), content, count=1)
        print("  [3] Replaced ctrl-group-pedagogy on toolbar")
    else:
        print("  [!] Could not find ctrl-group-pedagogy")

    # 4. Update Context Menu
    ctx_re = re.compile(r'<div id="contextMenu"[\s\S]*?</div>\s*</div>', re.MULTILINE)
    if ctx_re.search(content):
        content = ctx_re.sub(CONTEXT_MENU.strip(), content, count=1)
        print("  [4] Replaced contextMenu")
    else:
        print("  [!] Could not find contextMenu")

    # 5. Update Blackboard JS
    # Replace from chalkColor / chalkDrawing up to document.addEventListener('DOMContentLoaded', bindBlackboard);
    js_re = re.compile(r'(/\* === BẢNG VIẾT PHẤN ĐA BỀ MẶT[\s\S]*?document\.addEventListener\(\'DOMContentLoaded\', bindBlackboard\);|let chalkColor = \'#f8fafc\'[\s\S]*?document\.addEventListener\(\'DOMContentLoaded\', bindBlackboard\);)', re.MULTILINE)
    if js_re.search(content):
        content = js_re.sub(BOARD_JS.strip(), content, count=1)
        print("  [5] Replaced blackboard JS")
    else:
        print("  [!] Could not find blackboard JS block")

    # 6. Ensure key W / B handling
    # Fix 'w' / 'b' conflict in keyboard handler:
    # 'w' -> toggleBlackboard(), 'b' -> toggleBlankScreen()
    old_key_wb = "if (e.key === 'w' || e.key === 'W' || e.key === 'b' || e.key === 'B') {\n      e.preventDefault();\n      toggleBlackboard();\n      return;\n    }"
    new_key_wb = """if (e.key === 'w' || e.key === 'W') {
      e.preventDefault();
      toggleBlackboard();
      return;
    }
    if (e.key === 'b' || e.key === 'B') {
      e.preventDefault();
      toggleBlankScreen();
      return;
    }"""
    if old_key_wb in content:
        content = content.replace(old_key_wb, new_key_wb)
        print("  [6] Separated Key W (Blackboard) and Key B (Blank Screen)")

    # 7. Specific fixes for Bai_12: restore corrupted tab characters and remove teacher heading
    if 'Bai_12_' in filepath:
        # replace corrupted tabs
        content = content.replace('\tan', '\\tan')
        content = content.replace('\text', '\\text')
        content = content.replace('\times', '\\times')
        # fix HƯỚNG DẪN TƯ DUY
        content = content.replace('data-title-vi="HƯỚNG DẪN TƯ DUY"', 'data-title-vi="✍️ BIỂU THỨC LIÊN HỆ"')
        content = content.replace('<span class="badge-role">💡 Hướng dẫn</span>', '<span class="badge-role">✍️ Liên hệ</span>')
        print("  [7] Restored corrupted LaTeX commands & sanitized teacher title in Bai 12")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Done. Size changed from {orig_len} to {len(content)} bytes.\n")

if __name__ == '__main__':
    targets = [
        'TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html',
        'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html',
        'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html'
    ]

    for t in targets:
        if os.path.exists(t):
            upgrade_file(t)
        else:
            print(f"Skipping non-existent file: {t}")

    print("All files upgraded successfully!")

