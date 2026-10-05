import subprocess
import sys
import re
import os

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    master_tpl = f.read()

# Lấy các khối chuẩn từ master template
# 1. Blackboard DOM
m_bb_dom = re.search(r'(<div id="blackboardOverlay"[\s\S]*?</div>\s*<canvas id="blackboardCanvas"[\s\S]*?</div>)', master_tpl)
assert m_bb_dom, "Blackboard DOM not found in master template!"
CANONICAL_BB_DOM = m_bb_dom.group(1)

# 2. Blackboard JS
CANONICAL_BB_JS = """  let chalkColor = '#ffffff';
  let chalkWidth = 3.5;
  let chalkDrawing = false;
  let chalkStart = null;
  let chalkSnap = null;
  let boardThemeIdx = 0;
  const boardThemes = ['', 'surface-white', 'surface-dark'];
  let boardImgAngle = 0;

  function resizeBlackboard() {
    const canvas = document.getElementById('blackboardCanvas');
    if (!canvas) return;
    const ratio = window.devicePixelRatio || 1;
    const w = window.innerWidth;
    const h = window.innerHeight;
    const ctx = canvas.getContext('2d');
    const prev = ctx.getImageData(0, 0, canvas.width, canvas.height);
    canvas.width = Math.floor(w * ratio);
    canvas.height = Math.floor(h * ratio);
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    if (prev.width > 1) ctx.putImageData(prev, 0, 0);
  }

  function toggleBlackboard(force) {
    const overlay = document.getElementById('blackboardOverlay');
    if (!overlay) return;
    const on = typeof force === 'boolean' ? force : !overlay.classList.contains('active');
    overlay.classList.toggle('active', on);
    overlay.style.display = on ? 'block' : 'none';
    overlay.setAttribute('aria-hidden', on ? 'false' : 'true');
    const btn = document.getElementById('btnBoard');
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
  });"""

MODAL_CSS = """
    /* ==========================================================================
       BẢNG VIẾT TOÀN MÀN HÌNH (BLACKBOARD FULLSCREEN)
       ========================================================================== */
    #blackboardOverlay, .blackboard-overlay {
      display: none;
      position: fixed !important;
      inset: 0 !important;
      width: 100vw !important;
      height: 100vh !important;
      z-index: 10000 !important;
      background-color: #14532d;
      background-image: linear-gradient(rgba(255,255,255,.08) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.08) 1px, transparent 1px);
      background-size: 28px 28px;
    }
    #blackboardOverlay.active, .blackboard-overlay.active {
      display: block !important;
    }
    #blackboardOverlay.surface-green { background-color: #14532d !important; }
    #blackboardOverlay.surface-black { background-color: #09090b !important; }
    #blackboardOverlay.surface-white { background-color: #f8fafc !important; }
    #blackboardOverlay.surface-grid {
      background-color: #14532d !important;
      background-image: linear-gradient(rgba(255,255,255,0.12) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(255,255,255,0.12) 1px, transparent 1px) !important;
      background-size: 28px 28px !important;
    }
    #blackboardCanvas, .blackboard-canvas {
      position: absolute;
      inset: 0;
      width: 100% !important;
      height: 100% !important;
      touch-action: none;
      cursor: crosshair;
      z-index: 10001;
    }
    .blackboard-tools {
      position: absolute;
      top: 14px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 8px 16px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      z-index: 10003;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .chalk-dot {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      cursor: pointer;
      border: 2px solid rgba(255, 255, 255, 0.4);
      transition: transform 0.15s ease, border-color 0.15s ease;
      display: inline-block;
      flex-shrink: 0;
    }
    .chalk-dot:hover {
      transform: scale(1.25);
      border-color: #ffffff;
    }
    .board-btn {
      background: rgba(255, 255, 255, 0.15);
      color: #ffffff;
      border: 1px solid rgba(255, 255, 255, 0.25);
      border-radius: 999px;
      padding: 6px 12px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s ease;
      user-select: none;
      white-space: nowrap;
    }
    .board-btn:hover {
      background: rgba(255, 255, 255, 0.3);
      color: #ffffff;
    }
    .board-btn.close {
      background: #dc2626;
      border-color: #ef4444;
    }
    .board-btn.close:hover {
      background: #b91c1c;
    }
    .board-btn.img-btn {
      background: #0284c7;
      border-color: #38bdf8;
    }
    .board-btn.img-btn:hover {
      background: #0369a1;
    }

    .ctx-item:hover, .ctx-item.is-focused {
      background: #4f46e5 !important;
      color: #ffffff !important;
      outline: 2px solid #a5b4fc !important;
      outline-offset: -2px;
      transform: translateX(4px);
    }

    /* Điểm sáng Laser ảo & Tiêu điểm trình chiếu */
    .laser-pointer {
      position: fixed;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: radial-gradient(circle, #ff2a2a 0%, #dc2626 65%, rgba(220, 38, 38, 0.2) 100%);
      box-shadow: 0 0 10px 3px rgba(239, 68, 68, 0.9), 0 0 24px 8px rgba(239, 68, 68, 0.5);
      pointer-events: none;
      z-index: 999999;
      transform: translate(-50%, -50%);
      display: none;
    }
    body.laser-mode .laser-pointer,
    .laser-pointer.active {
      display: block !important;
    }
    body.laser-mode {
      cursor: crosshair;
    }

    /* Hiệu ứng tia sáng nhẹ khi khối nội dung mới xuất hiện theo bước */
    @keyframes block-focus-glow {
      0% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.5); }
      40% { box-shadow: 0 0 0 6px rgba(99, 102, 241, 0.35), 0 6px 20px rgba(99, 102, 241, 0.2); }
      100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }
    }
    .content-block.step-just-revealed {
      animation: block-focus-glow 1.2s ease-out;
    }

    /* ==========================================================================
       MODAL SOẠN THẢO & CHỈNH SỬA KHỐI NỘI DUNG (RICH EDITOR MODAL)
       ========================================================================== */
    .edit-modal-backdrop {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.75);
      z-index: 99999;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(4px);
    }
    .edit-modal-backdrop.active {
      display: flex;
    }
    .edit-modal {
      background: #ffffff;
      border-radius: 14px;
      width: 92%;
      max-width: 680px;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.45);
      border: 1px solid #cbd5e1;
      display: flex;
      flex-direction: column;
    }
    .edit-modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 14px 20px;
      border-bottom: 1px solid #e2e8f0;
      background: #f8fafc;
      border-top-left-radius: 14px;
      border-top-right-radius: 14px;
    }
    .edit-modal-title {
      font-size: 17px;
      font-weight: 700;
      color: #0f172a;
    }
    .btn-modal-close {
      background: transparent;
      border: none;
      font-size: 20px;
      cursor: pointer;
      color: #64748b;
      padding: 4px 8px;
      border-radius: 6px;
    }
    .btn-modal-close:hover {
      background: #e2e8f0;
      color: #0f172a;
    }
    .edit-modal-body {
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      overflow-y: auto;
    }
    .edit-field {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .edit-field label {
      font-size: 13px;
      font-weight: 700;
      color: #334155;
    }
    .edit-field input[type="text"],
    .edit-field input[type="number"],
    .edit-field textarea {
      padding: 8px 12px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-size: 14px;
      font-family: inherit;
      color: #0f172a;
      outline: none;
    }
    .edit-field input:focus,
    .edit-field textarea:focus {
      border-color: #2563eb;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
    }
    .edit-field textarea {
      min-height: 120px;
      resize: vertical;
      line-height: 1.5;
    }
    .edit-toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      background: #f1f5f9;
      padding: 6px;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
    }
    .btn-tool {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 4px 8px;
      font-size: 12px;
      cursor: pointer;
      font-weight: 600;
      color: #334155;
    }
    .btn-tool:hover {
      background: #e2e8f0;
      color: #0f172a;
    }
    .btn-tool-math {
      background: #eff6ff;
      border-color: #bfdbfe;
      color: #1d4ed8;
      font-family: 'Times New Roman', serif;
      font-style: italic;
    }
    .btn-tool-math:hover {
      background: #dbeafe;
    }
    .edit-preview {
      min-height: 60px;
      max-height: 160px;
      overflow-y: auto;
      padding: 10px 12px;
      background: #f8fafc;
      border: 1px dashed #cbd5e1;
      border-radius: 8px;
      font-size: 14px;
      line-height: 1.5;
      color: #1e293b;
    }
    .edit-modal-footer {
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      padding: 14px 20px;
      border-top: 1px solid #e2e8f0;
      background: #f8fafc;
      border-bottom-left-radius: 14px;
      border-bottom-right-radius: 14px;
    }

    /* ==========================================================================
       TOOLTIP NỔI BÔI ĐEN VĂN BẢN (SELECTION TOOLTIP)
       ========================================================================== */
    .selection-tooltip {
      position: absolute;
      display: none;
      z-index: 99999;
      background: #1e293b;
      color: #ffffff;
      padding: 6px 10px;
      border-radius: 8px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
      font-size: 12px;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
    }
    .selection-tooltip.active {
      display: flex;
    }
    .selection-tooltip .tooltip-title {
      font-weight: 700;
      color: #94a3b8;
      margin-right: 2px;
    }
    .btn-tip-action {
      background: #334155;
      color: #ffffff;
      border: 1px solid #475569;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 11.5px;
      cursor: pointer;
      font-weight: 600;
      transition: background 0.15s;
    }
    .btn-tip-action:hover {
      background: #2563eb;
      border-color: #3b82f6;
    }
    .btn-tip-cancel {
      background: transparent;
      color: #94a3b8;
      border: none;
      font-size: 14px;
      cursor: pointer;
      padding: 2px 6px;
    }
    .btn-tip-cancel:hover {
      color: #ffffff;
    }

    /* ==========================================================================
       MODAL PHÓNG TO HÌNH VẼ & BẢNG MINH HỌA (LIGHTBOX)
       ========================================================================== */
    .image-lightbox-backdrop {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.92);
      z-index: 15000;
      backdrop-filter: blur(4px);
      align-items: center;
      justify-content: center;
    }
    .image-lightbox-backdrop.active {
      display: flex;
    }
    .image-lightbox-dialog {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 16px;
      width: 90vw;
      max-width: 1100px;
      height: 88vh;
      display: flex;
      flex-direction: column;
      position: relative;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
      overflow: hidden;
    }
    .image-lightbox-close {
      position: absolute;
      top: 12px;
      right: 16px;
      background: #ef4444;
      border: none;
      color: #ffffff;
      font-size: 16px;
      font-weight: 800;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      cursor: pointer;
      z-index: 15005;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .image-lightbox-close:hover {
      background: #dc2626;
    }
    .image-lightbox-header {
      padding: 14px 20px;
      border-bottom: 1px solid #334155;
      background: #0f172a;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .image-lightbox-title {
      font-size: 17px;
      font-weight: 800;
      color: #38bdf8;
    }
    .image-lightbox-hint {
      font-size: 12px;
      color: #94a3b8;
    }
    .image-lightbox-viewport {
      flex: 1;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #090d16;
      cursor: grab;
      position: relative;
    }
    .image-lightbox-canvas {
      display: flex;
      align-items: center;
      justify-content: center;
      max-width: 100%;
      max-height: 100%;
      transition: transform 0.08s ease-out;
      transform-origin: center center;
    }
    .image-lightbox-canvas svg {
      max-width: 82vw;
      max-height: 68vh;
      height: auto;
    }
    .image-lightbox-canvas img {
      max-width: 82vw;
      max-height: 68vh;
      object-fit: contain;
    }
    .image-lightbox-toolbar {
      padding: 10px 20px;
      background: #0f172a;
      border-top: 1px solid #334155;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
    }
    .image-lightbox-toolbar button {
      background: #1e293b;
      color: #f1f5f9;
      border: 1px solid #475569;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
    }
    .image-lightbox-toolbar button:hover {
      background: #334155;
    }
    .image-lightbox-toolbar .btn-lightbox-exit {
      background: #475569;
    }
    .lightbox-zoom-level {
      color: #38bdf8;
      font-weight: 800;
      font-size: 13px;
      min-width: 48px;
      text-align: center;
    }

    /* ==========================================================================
       HỘP ẢNH NỔI TRÊN BẢNG VIẾT (BOARD FLOATING IMAGE BOX)
       ========================================================================== */
    .board-floating-image-box {
      position: absolute;
      top: 80px;
      left: 40px;
      z-index: 10005;
      display: none;
      background: rgba(255, 255, 255, 0.95);
      border: 2px solid #38bdf8;
      border-radius: 8px;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5);
      user-select: none;
      touch-action: none;
      min-width: 140px;
      min-height: 100px;
    }
    .board-floating-image-box.active {
      display: inline-flex;
      flex-direction: column;
    }
    .float-photo-bar {
      background: #1e293b;
      color: #38bdf8;
      padding: 4px 8px;
      font-size: 11px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 4px;
      cursor: move;
      border-top-left-radius: 6px;
      border-top-right-radius: 6px;
    }
    .float-photo-btn {
      background: #334155;
      color: white;
      border: 1px solid #475569;
      border-radius: 4px;
      padding: 2px 6px;
      font-size: 11px;
      cursor: pointer;
    }
    .float-photo-btn:hover {
      background: #475569;
    }
    .float-photo-btn.danger {
      background: #b91c1c;
      border-color: #ef4444;
    }
    .float-photo-btn.danger:hover {
      background: #dc2626;
    }
    .board-img-body {
      padding: 6px;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .board-img-body img {
      max-width: 48vw;
      max-height: 70vh;
      object-fit: contain;
      border-radius: 4px;
      pointer-events: none;
    }
    .resize-handle-br {
      position: absolute;
      right: 0;
      bottom: 0;
      width: 16px;
      height: 16px;
      cursor: nwse-resize;
      background: linear-gradient(135deg, transparent 50%, #0284c7 50%);
      border-bottom-right-radius: 6px;
    }
"""

TITLE_MAPPINGS = {
    # Hướng dẫn & lời giải
    "HƯỚNG DẪN GIẢI TỪNG BƯỚC": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT (CHUẨN GDPT 2018)": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT (CHUẨN SGK)": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT": "HƯỚNG DẪN",
    "HƯỚNG DẪN THỰC HIỆN CÂU A": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT (2 CÁCH TÍNH CẠNH BC)": "HƯỚNG DẪN",
    "HƯỚNG DẪN TỰ HỌC Ở NHÀ & DẶN DÒ": "DẶN DÒ",

    # Đề bài & Hoạt động
    "HOẠT ĐỘNG 1 (SGK TR.74)": "HOẠT ĐỘNG 1",
    "HOẠT ĐỘNG 2 (SGK TR.75)": "HOẠT ĐỘNG 2",
    "HOẠT ĐỘNG KHỞI ĐỘNG (SGK TR.6)": "KHỞI ĐỘNG",
    "HOẠT ĐỘNG KHÁM PHÁ 1 (SGK TR.6)": "HOẠT ĐỘNG 1",
    "HOẠT ĐỘNG KHÁM PHÁ 2 (SGK TR.7)": "HOẠT ĐỘNG 2",

    # Ví dụ & Luyện tập
    "LUYỆN TẬP 4 (SGK TR.77)": "LUYỆN TẬP 4",
    "BÀI TẬP VẬN DỤNG NHANH TẠI LỚP (30 GIÂY)": "VẬN DỤNG",

    # Câu hỏi & đáp án
    "CÂU HỎI TRẮC NGHIỆM 1": "TRẮC NGHIỆM 1",
    "CÂU HỎI TRẮC NGHIỆM 2": "TRẮC NGHIỆM 2",

    # Tình huống & hình
    "TÌNH HUỐNG MỞ ĐẦU (SGK TR.74)": "TÌNH HUỐNG",
    "HÌNH 4.11 — MÔ HÌNH QUAN SÁT THỰC ĐỊA": "HÌNH 4.11",
    "HÌNH 4.11 — MÔ HÌNH TOÁN HỌC": "HÌNH 4.11",
    "HÌNH 4.12 — TAM GIÁC VUÔNG ABC": "HÌNH 4.12",
    "HÌNH 4.13 — MÔ HÌNH HÌNH HỌC": "HÌNH 4.13",
    "HÌNH 4.14 — CHIẾC THANG GÓC 65°": "HÌNH 4.14",
    "HÌNH 4.15 — CON ĐÒ QUA KHÚC SÔNG": "HÌNH 4.15",
    "HÌNH 4.16 — TAM GIÁC VUÔNG VỚI HAI CẠNH GÓC VUÔNG": "HÌNH 4.16",
    "HÌNH 4.17 — TÒA THÁP VÀ BÓNG NẮNG 8,6 M": "HÌNH 4.17",
    "HÌNH 4.18 — BÓNG CÂY 25 M DƯỚI GÓC 40°": "HÌNH 4.18",
    "HÌNH 4.19 — TAM GIÁC ABC CÓ AB = 5, AC = 8": "HÌNH 4.19",
    "HÌNH 4.20 — TAM GIÁC ABC CÓ AB = 3 VÀ GÓC B = 42°": "HÌNH 4.20",
    "HÌNH 4.22 — XE CHỞ RÁC NÂNG THÙNG BEN": "HÌNH 4.22",
    "HÌNH 4.23 — MÔ HÌNH MÁI DỐC NHÀ KHO": "HÌNH 4.23",
    "HÌNH VẼ MINH HỌA CHO A = 10, B = 6": "HÌNH VẼ",
    "HÌNH VẼ MINH HỌA HÌNH THOI": "HÌNH VẼ",

    # Lý thuyết & phương pháp
    "MỤC TIÊU BÀI HỌC (3 TIẾT)": "MỤC TIÊU",
    "MỤC TIÊU BÀI HỌC (2 TIẾT)": "MỤC TIÊU",
    "MỤC TIÊU BÀI HỌC": "MỤC TIÊU",
    "SƠ ĐỒ TƯ DUY PHÂN TÍCH ĐI LÊN": "PHÂN TÍCH",
    "NHẬN XÉT SƯ PHẠM VỀ VỊ TRÍ GÓC": "NHẬN XÉT",
    "ĐỊNH HƯỚNG CHUYỂN THÀNH ĐỊNH LÍ PHÁT BIỂU BẰNG LỜI": "KẾT LUẬN",
    "ĐỊNH HƯỚNG PHÁT BIỂU ĐỊNH LÍ 2": "KẾT LUẬN",
    "MẸO GHI NHỚ SƯ PHẠM ĐỘC QUYỀN": "GHI NHỚ",
    "BẢNG CHUYỂN ĐỔI KHI ĐỔI TÊN ĐỈNH TAM GIÁC": "BẢNG CHUYỂN ĐỔI",
    "TỈ SỐ TANG & CÔTANG TRONG TAM GIÁC ABC": "TỈ SỐ LƯỢNG GIÁC",
    "BIỂU DIỄN CẠNH GÓC VUÔNG QUA CẠNH GÓC VUÔNG KIA": "BIỂU DIỄN CẠNH",
    "PHÂN TÍCH VỊ TRÍ GÓC ĐỐI VÀ GÓC KỀ": "VỊ TRÍ GÓC",
    "CÔNG THỨC TÍNH CÔTANG TRÊN MÁY TÍNH CẦM TAY": "TÍNH CÔTANG",
    "BẢNG ĐỐI CHIẾU HỆ THỨC LƯỢNG": "BẢNG ĐỐI CHIẾU",
    "SƠ ĐỒ CÂY QUYẾT ĐỊNH CHỌN ĐỊNH LÍ": "SƠ ĐỒ QUYẾT ĐỊNH",
    "GIẢI TAM GIÁC VUÔNG LÀ GÌ? (SGK TR.77)": "ĐỊNH NGHĨA",
    "HAI TRƯỜNG HỢP CƠ BẢN": "HAI TRƯỜNG HỢP",
    "CÔNG CỤ TOÁN HỌC CẦN SỬ DỤNG KHI GIẢI": "CÔNG CỤ",
    "CÁC TRỤ CỘT KIẾN THỨC CỐT LÕI": "TRỌNG TÂM",

    # Casio
    "MẸO BẤM MÁY FX-580VN X & CẢNH BÁO": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & AN TOÀN LAO ĐỘNG": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & CẢNH BÁO": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & NGUYÊN LÝ ĐO BÓNG NẮNG": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & CẢNH BÁO LÀM TRÒN": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & BỘ BA SỐ PYTHAGORE": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & CẢNH BÁO DÂY CHUYỀN": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & LƯU Ý LÀM TRÒN .0": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & CẢNH BÁO GIÁC KẾ": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & KỸ THUẬT XE BEN": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & NGUYÊN LÝ THOÁT NƯỚC": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & CẢNH BÁO NHÂN ĐÔI GÓC": "HƯỚNG DẪN CASIO",

    # Dặn dò & tổng kết
    "TỔNG KẾT TIẾT 1 & DẶN DÒ": "DẶN DÒ",
    "TỔNG KẾT TIẾT 2 & CHUẨN BỊ TIẾT 3": "DẶN DÒ",
    "NHIỆM VỤ TỰ HỌC TẠI NHÀ": "DẶN DÒ",
    "SƠ ĐỒ TƯ DUY HỆ THỨC LƯỢNG TRONG TAM GIÁC VUÔNG": "TỔNG KẾT",
    "GỢI Ý BÀI TẬP VỀ NHÀ 4.13 (SGK TR.78)": "GỢI Ý 4.13"
}

def update_block_step(txt, block_id, new_step):
    block_pattern = rf'(<div\s+class="content-block[^"]*"\s+id="{block_id}"[^>]*>)([\s\S]*?)(<button class="btn-block-speak")'
    m = re.search(block_pattern, txt)
    if not m:
        block_pattern2 = rf'(<div\s+[^>]*id="{block_id}"[^>]*>)([\s\S]*?)(<button class="btn-block-speak")'
        m = re.search(block_pattern2, txt)
        if not m:
            print(f"  [WARN] Block {block_id} not found!")
            return txt

    start_tag = m.group(1)
    overlay = m.group(2)
    rest = m.group(3)

    if 'data-step="' in start_tag:
        new_start_tag = re.sub(r'data-step="[^"]*"', f'data-step="{new_step}"', start_tag)
    else:
        new_start_tag = start_tag.replace('id="', f'data-step="{new_step}" id="')

    badge_pattern = rf'(<span\s+class="badge-step-num"\s+onclick="setBlockStepDirect\(\'{block_id}\'\)"[^>]*>)([^<]*)(</span>)'
    new_overlay = re.sub(badge_pattern, rf'\g<1>{new_step}\g<3>', overlay)

    new_full = new_start_tag + new_overlay + rest
    txt = txt[:m.start()] + new_full + txt[m.end():]
    return txt

def common_patch(content):
    # 1. Thêm CSS vào trước </style>
    if '.edit-modal-backdrop' not in content:
        content = content.replace('</style>', MODAL_CSS + '\n</style>', 1)
        print("  Added modal/floating CSS into <style>.")

    # 2. Đảm bảo inline style="display:none;" trên selectionTooltip
    content = re.sub(
        r'<div\s+id="selectionTooltip"\s+class="selection-tooltip"[^>]*>',
        '<div id="selectionTooltip" class="selection-tooltip" style="display:none;" onmousedown="event.stopPropagation()">',
        content
    )

    # 3. Đồng bộ editModal / editModalBackdrop
    if '<div class="edit-modal-backdrop"' not in content:
        # Trong Bai 4, <div id="editModal"> đứng một mình
        old_m = re.search(r'<div id="editModal">[\s\S]*?</div>\s*</div>\s*(?:<!--|$)', content)
        if old_m:
            # Wrap into editModalBackdrop
            new_edit_modal_wrap = """<div class="edit-modal-backdrop" id="editModalBackdrop" style="display:none;" onclick="handleBackdropClick(event)">
  <div class="edit-modal" id="editModal">
    <div class="edit-modal-header">
      <span class="edit-modal-title" id="editModalHeaderTitle">✏️ Soạn Thảo Khối Nội Dung</span>
      <button class="btn-modal-close" onclick="closeEditModal()">✕</button>
    </div>
    <div class="edit-modal-body">
      <div class="edit-field">
        <label for="editTitleInput">Tiêu đề khối:</label>
        <input type="text" id="editTitleInput" placeholder="Ví dụ: ĐỊNH LÍ 1, VÍ DỤ 1...">
      </div>

      <div class="edit-field">
        <label for="editBlockStep">Số thứ tự bước xuất hiện:</label>
        <input type="number" id="editBlockStep" min="0" max="20" value="1">
      </div>

      <div class="edit-field">
        <label>Thanh công cụ định dạng & Công thức nhanh:</label>
        <div class="edit-toolbar">
          <button type="button" class="btn-tool" onclick="insertTag('<b>', '</b>')" title="In đậm"><b>B</b></button>
          <button type="button" class="btn-tool" onclick="insertTag('<i>', '</i>')" title="In nghiêng"><i>I</i></button>
          <button type="button" class="btn-tool" onclick="insertTag('<u>', '</u>')" title="Gạch chân"><u>U</u></button>
          <button type="button" class="btn-tool" onclick="insertTag('<mark>', '</mark>')" title="Tô sáng"><mark>Highlight</mark></button>
          <button type="button" class="btn-tool" onclick="insertText('<br>')" title="Xuống dòng">&para; Xuống dòng</button>
          <button type="button" class="btn-tool" onclick="insertText('• ')" title="Dấu gạch đầu dòng">&bull; Danh sách</button>

          <span style="border-left:1px solid #cbd5e1;margin:0 4px;"></span>

          <button type="button" class="btn-tool btn-tool-math" onclick="insertMath('$')" title="Công thức nội dòng">$...$</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertMath('$$')" title="Công thức khối">$$...$$</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\frac{a}{b}')" title="Phân số">\\frac{a}{b}</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\sqrt{x}')" title="Căn bậc hai">\\sqrt{x}</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('x^2')" title="Mũ hai">x&sup2;</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\sin B')" title="Sin">\\sin</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\cos B')" title="Cos">\\cos</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\tan B')" title="Tan">\\tan</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\cot B')" title="Cot">\\cot</button>
        </div>
      </div>

      <div class="edit-field">
        <label for="editTextarea">Nội dung khối (hỗ trợ HTML & LaTeX):</label>
        <textarea id="editTextarea" placeholder="Nhập nội dung, công thức toán học..." oninput="updateLivePreview()"></textarea>
      </div>

      <div class="edit-field">
        <label>Khung xem trước trực tiếp (Live Preview):</label>
        <div class="edit-preview" id="editPreviewBox"></div>
      </div>
    </div>
    <div class="edit-modal-footer">
      <button class="btn-ctrl" onclick="closeEditModal()">Hủy bỏ</button>
      <button class="btn-ctrl btn-ctrl-primary" onclick="saveEditContent()">Lưu thay đổi</button>
    </div>
  </div>
</div>"""
            content = content[:old_m.start()] + new_edit_modal_wrap + '\n' + content[old_m.end():]
            print("  Replaced standalone editModal with canonical editModalBackdrop wrap.")
    else:
        content = re.sub(
            r'<div\s+class="edit-modal-backdrop"\s+id="editModalBackdrop"[^>]*>',
            '<div class="edit-modal-backdrop" id="editModalBackdrop" style="display:none;" onclick="handleBackdropClick(event)">',
            content
        )
        new_modal_html = """<div class="edit-modal" id="editModal">
    <div class="edit-modal-header">
      <span class="edit-modal-title" id="editModalHeaderTitle">✏️ Soạn Thảo Khối Nội Dung</span>
      <button class="btn-modal-close" onclick="closeEditModal()">✕</button>
    </div>
    <div class="edit-modal-body">
      <div class="edit-field">
        <label for="editTitleInput">Tiêu đề khối:</label>
        <input type="text" id="editTitleInput" placeholder="Ví dụ: ĐỊNH LÍ 1, VÍ DỤ 1...">
      </div>

      <div class="edit-field">
        <label for="editBlockStep">Số thứ tự bước xuất hiện:</label>
        <input type="number" id="editBlockStep" min="0" max="20" value="1">
      </div>

      <div class="edit-field">
        <label>Thanh công cụ định dạng & Công thức nhanh:</label>
        <div class="edit-toolbar">
          <button type="button" class="btn-tool" onclick="insertTag('<b>', '</b>')" title="In đậm"><b>B</b></button>
          <button type="button" class="btn-tool" onclick="insertTag('<i>', '</i>')" title="In nghiêng"><i>I</i></button>
          <button type="button" class="btn-tool" onclick="insertTag('<u>', '</u>')" title="Gạch chân"><u>U</u></button>
          <button type="button" class="btn-tool" onclick="insertTag('<mark>', '</mark>')" title="Tô sáng"><mark>Highlight</mark></button>
          <button type="button" class="btn-tool" onclick="insertText('<br>')" title="Xuống dòng">&para; Xuống dòng</button>
          <button type="button" class="btn-tool" onclick="insertText('• ')" title="Dấu gạch đầu dòng">&bull; Danh sách</button>

          <span style="border-left:1px solid #cbd5e1;margin:0 4px;"></span>

          <button type="button" class="btn-tool btn-tool-math" onclick="insertMath('$')" title="Công thức nội dòng">$...$</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertMath('$$')" title="Công thức khối">$$...$$</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\frac{a}{b}')" title="Phân số">\\frac{a}{b}</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\sqrt{x}')" title="Căn bậc hai">\\sqrt{x}</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('x^2')" title="Mũ hai">x&sup2;</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\sin B')" title="Sin">\\sin</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\cos B')" title="Cos">\\cos</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\tan B')" title="Tan">\\tan</button>
          <button type="button" class="btn-tool btn-tool-math" onclick="insertText('\\\\cot B')" title="Cot">\\cot</button>
        </div>
      </div>

      <div class="edit-field">
        <label for="editTextarea">Nội dung khối (hỗ trợ HTML & LaTeX):</label>
        <textarea id="editTextarea" placeholder="Nhập nội dung, công thức toán học..." oninput="updateLivePreview()"></textarea>
      </div>

      <div class="edit-field">
        <label>Khung xem trước trực tiếp (Live Preview):</label>
        <div class="edit-preview" id="editPreviewBox"></div>
      </div>
    </div>
    <div class="edit-modal-footer">
      <button class="btn-ctrl" onclick="closeEditModal()">Hủy bỏ</button>
      <button class="btn-ctrl btn-ctrl-primary" onclick="saveEditContent()">Lưu thay đổi</button>
    </div>
  </div>"""
        if '<div class="edit-modal" id="editModal">' in content:
            content = re.sub(r'<div class="edit-modal" id="editModal">[\s\S]*?</div>\s*</div>\s*</div>', lambda m: new_modal_html + '\n</div>', content)
            print("  Synchronized editModal HTML markup and IDs.")

    # 4. Đảm bảo inline style="display:none;" trên imageLightboxBackdrop
    content = re.sub(
        r'<div\s+class="image-lightbox-backdrop"\s+id="imageLightboxBackdrop"[^>]*>',
        '<div class="image-lightbox-backdrop" id="imageLightboxBackdrop" style="display:none;" onclick="handleLightboxBackdropClick(event)">',
        content
    )

    # 5. Thay thế / Bổ sung Blackboard DOM chuẩn
    if 'id="boardImageBox"' not in content:
        # Thay thế <div id="blackboardOverlay" ...>...</div> cũ bằng CANONICAL_BB_DOM
        content = re.sub(
            r'<div id="blackboardOverlay"[\s\S]*?</div>\s*</div>(?=\s*(?:<!--|$|<div))',
            lambda m: CANONICAL_BB_DOM,
            content
        )
        if 'id="boardImageBox"' not in content:
            # Thử pattern đơn giản hơn
            content = re.sub(
                r'<div id="blackboardOverlay"[^>]*>[\s\S]*?</div>\s*(?:<!-- THANH ĐIỀU KHIỂN|<!-- MODAL MÁY TÍNH)',
                lambda m: CANONICAL_BB_DOM + '\n\n',
                content
            )
        print("  Injected canonical blackboard DOM with boardImageBox and floating image tools.")

    # 6. Thay thế / Bổ sung Blackboard JS chuẩn
    if 'function handleBoardImageUpload' not in content:
        # Tìm chỗ có function toggleBlackboard cũ và thay thế bằng CANONICAL_BB_JS
        if 'function toggleBlackboard' in content:
            content = re.sub(
                r'let chalkColor[\s\S]*?canvas\.addEventListener\(\'touchend\',\s*end\);\s*\}\s*document\.addEventListener\(\'DOMContentLoaded\',\s*bindBlackboard\);',
                lambda m: CANONICAL_BB_JS,
                content
            )
        else:
            # Chèn trước function jumpToPeriod hoặc cuối script
            idx = content.find('function jumpToPeriod')
            if idx != -1:
                content = content[:idx] + CANONICAL_BB_JS + '\n\n  ' + content[idx:]
        print("  Injected canonical blackboard JS functions and paste listener.")

    # 7. Thêm hàm insertMath & aliases vào JS
    if 'function insertMath' not in content:
        target_fn = 'function insertTag(openTag, closeTag) {'
        if target_fn in content:
            helper_code = """function insertMath(delim) {
    insertTag(delim, delim);
  }
  const insertFormat = insertTag;
  const saveEditModal = saveEditContent;

  """
            content = content.replace(target_fn, helper_code + target_fn)
            print("  Added insertMath and aliases (insertFormat, saveEditModal).")

    # 8. Cập nhật openEditModal & closeEditModal
    open_edit_pat = r'function openEditModal\(blockId\)\s*\{[\s\S]*?document\.getElementById\(\'editModal\'\)\.classList\.add\(\'active\'\);\s*\}'
    new_open_edit = """function openEditModal(blockId) {
    const el = document.getElementById(blockId);
    if (!el) return;
    activeEditBlockId = blockId;
    activeCreateSlideId = null;
    activeCreateColType = null;

    const titleEl = document.getElementById('editModalHeaderTitle') || document.getElementById('editModalTitle');
    if (titleEl) titleEl.textContent = '✏️ Chỉnh sửa nội dung khối';
    const strong = el.querySelector('strong');
    const titleInput = document.getElementById('editTitleInput') || document.getElementById('editBlockTitle');
    if (titleInput) titleInput.value = strong ? strong.textContent.trim() : '';

    const raw = el.getAttribute('data-raw') || cleanLatexInHtml(el.querySelector('.block-body')) || '';
    const textarea = document.getElementById('editTextarea') || document.getElementById('editBlockBody');
    if (textarea) textarea.value = cleanLatexInHtml(raw);

    const stepInput = document.getElementById('editBlockStep');
    if (stepInput) {
      stepInput.value = el.getAttribute('data-step') || '1';
    }

    updateLivePreview();
    const backdrop = document.getElementById('editModalBackdrop');
    if (backdrop) {
      backdrop.style.display = 'flex';
      backdrop.classList.add('active');
    }
    const modal = document.getElementById('editModal');
    if (modal) modal.classList.add('active');
  }"""
    if re.search(open_edit_pat, content):
        content = re.sub(open_edit_pat, lambda m: new_open_edit, content)
        print("  Updated openEditModal function.")

    close_edit_pat = r'function closeEditModal\(\)\s*\{[\s\S]*?activeCreateColType = null;\s*\}'
    new_close_edit = """function closeEditModal() {
    const backdrop = document.getElementById('editModalBackdrop');
    if (backdrop) {
      backdrop.style.display = 'none';
      backdrop.classList.remove('active');
    }
    const modal = document.getElementById('editModal');
    if (modal) modal.classList.remove('active');
    activeEditBlockId = null;
    activeCreateSlideId = null;
    activeCreateColType = null;
  }"""
    if re.search(close_edit_pat, content):
        content = re.sub(close_edit_pat, lambda m: new_close_edit, content)
        print("  Updated closeEditModal function.")

    # 9. Cập nhật openImageLightbox & closeImageLightbox
    if "backdrop.style.display = 'flex';" not in content:
        content = content.replace("backdrop.classList.add('active');", "backdrop.style.display = 'flex';\n    backdrop.classList.add('active');")
        content = content.replace("backdrop.classList.remove('active');", "backdrop.style.display = 'none';\n      backdrop.classList.remove('active');")
        print("  Updated openImageLightbox and closeImageLightbox display toggles.")

    # 10. Sửa lỗi corrupted tab/formfeed escapes
    TAB_REPLACEMENTS = [
        ('\tan', r'\tan'),
        ('\text', r'\text'),
        ('\times', r'\times'),
        ('\theta', r'\theta'),
        ('\tau', r'\tau'),
        ('\frac', r'\frac')
    ]
    for bad, good in TAB_REPLACEMENTS:
        if bad in content:
            cnt = content.count(bad)
            content = content.replace(bad, good)
            print(f"  Fixed {cnt} corrupted escapes for {repr(good)}")

    # 11. Đảm bảo CSS khóa cuộn khi vẽ bút
    if 'body.pen-mode, body.pen-mode .slide-deck' not in content:
        target = '.pen-palette.active { display: flex; }'
        if target in content:
            content = content.replace(target, target + '\n    body.pen-mode, body.pen-mode .slide-deck { overflow: hidden !important; }\n')
            print("  Added pen-mode scroll lock CSS.")

    # 12. Đảm bảo Bảng viết, Timer, Calc nằm trên thanh công cụ
    # GỠ BỎ HOÀN TOÀN #btnBlackboard ("📋 Bảng vẽ"), CHỈ GIỮ LẠI 1 NÚT "📋 Bảng viết" (#btnBoard)
    content = re.sub(r'<button[^>]*id="btnBlackboard"[^>]*>[\s\S]*?</button>\s*', '', content)

    if 'id="btnBoard"' not in content:
        btn_board_html = '<button class="btn-ctrl" id="btnBoard" onclick="toggleBlackboard()" title="Bảng viết vẽ toàn màn hình & Chèn ảnh (Phím W)">📋 Bảng viết</button>'
        if '<button class="btn-ctrl" id="btnTimer"' in content:
            content = content.replace(
                '<button class="btn-ctrl" id="btnTimer"',
                btn_board_html + '\n    <button class="btn-ctrl" id="btnTimer"'
            )
        elif '<button class="btn-ctrl" id="btnCalc"' in content:
            content = content.replace(
                '<button class="btn-ctrl" id="btnCalc"',
                btn_board_html + '\n    <button class="btn-ctrl" id="btnTimer" onclick="toggleTimerModal()" title="Đồng hồ đếm ngược thảo luận/làm bài">⏱️ Đếm ngược</button>\n    <button class="btn-ctrl" id="btnCalc"'
            )
        print("  Added btnBoard/btnTimer to control bar.")

    if 'id="btnTimer"' not in content:
        if '<button class="btn-ctrl" id="btnCalc"' in content:
            content = content.replace(
                '<button class="btn-ctrl" id="btnCalc"',
                '<button class="btn-ctrl" id="btnTimer" onclick="toggleTimerModal()" title="Đồng hồ đếm ngược thảo luận/làm bài">⏱️ Đếm ngược</button>\n    <button class="btn-ctrl" id="btnCalc"'
            )
            print("  Added btnTimer to control bar.")

    # Đảm bảo contextMenu có mục Bảng viết
    if "handleCtxAction('blackboard')" not in content:
        bb_ctx_item = """  <div class="ctx-item" onclick="handleCtxAction('blackboard')">
    <span class="ctx-icon">📋</span>
    <span class="ctx-label">Bảng viết</span>
    <span class="ctx-key">Phím W</span>
  </div>"""
        target_calc = '<div class="ctx-item" onclick="handleCtxAction(\'calc\')">'
        if target_calc in content:
            content = content.replace(target_calc, bb_ctx_item + '\n  ' + target_calc, 1)

    # 13. Áp dụng TITLE_MAPPINGS
    for old_t, new_t in TITLE_MAPPINGS.items():
        old_attr = f'data-title-vi="{old_t}"'
        new_attr = f'data-title-vi="{new_t}"'
        if old_attr in content:
            content = content.replace(old_attr, new_attr)

        old_strong = f'<strong>{old_t}</strong>'
        new_strong = f'<strong>{new_t}</strong>'
        if old_strong in content:
            content = content.replace(old_strong, new_strong)

        old_h4 = f'<h4 class="block-title">{old_t}</h4>'
        new_h4 = f'<h4 class="block-title">{new_t}</h4>'
        if old_h4 in content:
            content = content.replace(old_h4, new_h4)

    # 14. Bút trình chiếu - Pointer tracking + Edge Scrolling + KeyUp Volume Prevention
    ptr_code = """  /* Tọa độ con trỏ và Tự động cuộn theo mép màn hình (Edge Scrolling) */
  let lastPointerX = window.innerWidth / 2;
  let lastPointerY = window.innerHeight / 2;
  let edgeScrollAnimId = null;

  function handleEdgeScroll(e) {
    if (isDesignMode) return;
    const y = e.clientY;
    const x = e.clientX;
    const topZone = 70;
    const bottomZone = window.innerHeight - 75;

    if (edgeScrollAnimId) {
      cancelAnimationFrame(edgeScrollAnimId);
      edgeScrollAnimId = null;
    }

    if (y > bottomZone || y < topZone) {
      const el = document.elementFromPoint(x, y);
      const col = el ? el.closest('.col-board, .col-task') : null;
      if (!col) return;

      const isDown = y > bottomZone;
      const speed = isDown ? Math.min(16, Math.max(3, Math.round((y - bottomZone) / 3)))
                           : Math.min(16, Math.max(3, Math.round((topZone - y) / 3)));

      function step() {
        if (isDown) {
          col.scrollTop += speed;
        } else {
          col.scrollTop -= speed;
        }
        edgeScrollAnimId = requestAnimationFrame(step);
      }
      edgeScrollAnimId = requestAnimationFrame(step);
    }
  }

  window.addEventListener('mousemove', function(e) {
    lastPointerX = e.clientX;
    lastPointerY = e.clientY;
    const y = e.clientY;
    if (y >= 70 && y <= window.innerHeight - 75) {
      if (edgeScrollAnimId) {
        cancelAnimationFrame(edgeScrollAnimId);
        edgeScrollAnimId = null;
      }
    } else {
      handleEdgeScroll(e);
    }
  });

  window.addEventListener('pointermove', function(e) {
    lastPointerX = e.clientX;
    lastPointerY = e.clientY;
  });

  window.addEventListener('mouseleave', function() {
    if (edgeScrollAnimId) {
      cancelAnimationFrame(edgeScrollAnimId);
      edgeScrollAnimId = null;
    }
  });

  /* Ngăn chặn Windows chiếm phím âm lượng ở sự kiện keyup */
  function preventVolumeKeyUp(e) {
    if (e.key === 'AudioVolumeUp' || e.key === 'VolumeUp' || e.code === 'AudioVolumeUp' || e.keyCode === 175 ||
        e.key === 'AudioVolumeDown' || e.key === 'VolumeDown' || e.code === 'AudioVolumeDown' || e.keyCode === 174) {
      e.preventDefault();
      e.stopPropagation();
      if (typeof e.stopImmediatePropagation === 'function') e.stopImmediatePropagation();
    }
  }
  window.addEventListener('keyup', preventVolumeKeyUp, { capture: true, passive: false });
  document.addEventListener('keyup', preventVolumeKeyUp, { capture: true, passive: false });
"""
    if "edgeScrollAnimId" not in content:
        old_ptr_pattern = r'/\*[\s\S]*?Tọa độ con trỏ[\s\S]*?window\.addEventListener\(\'pointermove\'[\s\S]*?\}\);\s*'
        if re.search(old_ptr_pattern, content):
            content = re.sub(old_ptr_pattern, ptr_code + '\n\n', content, count=1)
        else:
            target = "/* Phím tắt điều hướng"
            if target in content:
                content = content.replace(target, ptr_code + '\n  ' + target, 1)
        print("  Upgraded pointer tracking with edge scrolling & volume keyup prevention.")

    # Chuyển listener keydown sang window với capture phase true và xử lý Volume Up/Down + Menu Navigation
    vol_nav_code = """window.addEventListener('keydown', function(e) {
    if (e.target.closest('input, textarea, [contenteditable="true"]')) return;

    const ctx = document.getElementById('contextMenu');
    const isMenuOpen = ctx && ctx.style.display !== 'none' && ctx.getAttribute('aria-hidden') !== 'true';

    const isVolUp = e.key === 'AudioVolumeUp' || e.key === 'VolumeUp' || e.code === 'AudioVolumeUp' || e.keyCode === 175 || e.which === 175 || (e.key && e.key.toLowerCase().includes('volumeup'));
    const isVolDown = e.key === 'AudioVolumeDown' || e.key === 'VolumeDown' || e.code === 'AudioVolumeDown' || e.keyCode === 174 || e.which === 174 || (e.key && e.key.toLowerCase().includes('volumedown'));

    // 1. TĂNG ÂM LƯỢNG = CHUỘT TRÁI (Chọn mục menu hoặc click tại vị trí con trỏ)
    if (isVolUp) {
      e.preventDefault();
      e.stopPropagation();
      if (typeof e.stopImmediatePropagation === 'function') e.stopImmediatePropagation();
      simulateLeftClickAt(lastPointerX, lastPointerY);
      return;
    }

    // 2. GIẢM ÂM LƯỢNG = CHUỘT PHẢI (Mở/tắt Menu Chuột Phải Sư phạm)
    if (isVolDown) {
      e.preventDefault();
      e.stopPropagation();
      if (typeof e.stopImmediatePropagation === 'function') e.stopImmediatePropagation();
      toggleContextMenuAt(lastPointerX, lastPointerY);
      return;
    }

    // 3. KHI MENU CHUỘT PHẢI ĐANG MỞ -> BÚT VÀ PHÍM MŨI TÊN DI CHUYỂN & CHỌN MỤC
    if (isMenuOpen) {
      if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === 'ArrowRight' || e.key === '>') {
        e.preventDefault();
        e.stopPropagation();
        updateContextMenuFocus(ctxFocusedIdx + 1);
        return;
      }
      if (e.key === 'ArrowUp' || e.key === 'PageUp' || e.key === 'ArrowLeft' || e.key === '<') {
        e.preventDefault();
        e.stopPropagation();
        updateContextMenuFocus(ctxFocusedIdx - 1);
        return;
      }
      if (e.key === 'Tab') {
        e.preventDefault();
        e.stopPropagation();
        updateContextMenuFocus(ctxFocusedIdx + 1);
        return;
      }
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'b' || e.key === 'B' || e.key === '.') {
        e.preventDefault();
        e.stopPropagation();
        simulateLeftClickAt(lastPointerX, lastPointerY);
        return;
      }
      if (e.key === 'Escape') {
        e.preventDefault();
        e.stopPropagation();
        hideContextMenu();
        return;
      }
      if (e.key === 'Meta' || e.code === 'MetaLeft' || e.code === 'MetaRight' || e.key === 'OS' || e.keyCode === 91 || e.keyCode === 92 ||
          e.key === 'ContextMenu' || e.code === 'ContextMenu' || e.keyCode === 93 ||
          e.key === 't' || e.key === 'T' || e.code === 'KeyT') {
        e.preventDefault();
        e.stopPropagation();
        // Nhấn nút Đỏ lại khi menu mở: KÍCH HOẠT MỤC ĐANG SÁNG!
        simulateLeftClickAt(lastPointerX, lastPointerY);
        return;
      }
    }"""
    if "const isVolUp" not in content:
        old_vol_pattern = r'window\.addEventListener\(\'keydown\',\s*function\(e\)\s*\{[\s\S]*?//\s*3\.\s*KHI MENU CHUỘT PHẢI ĐANG MỞ[\s\S]*?\}\s*\}'
        if re.search(old_vol_pattern, content):
            content = re.sub(old_vol_pattern, vol_nav_code, content, count=1)
        else:
            content = content.replace("document.addEventListener('keydown', function(e) {", vol_nav_code, 1)
        content = re.sub(
            r'(prevStep\(\);\s*\}\s*\}\s*)\);',
            r'\1, true);',
            content,
            count=1
        )

    # 15. Phím Meta (Windows) / Tab / T / ContextMenu gọi toggleContextMenuAt (Hỗ trợ nút trên bút trình chiếu)
    key_check_code = """if (e.key === 'Meta' || e.code === 'MetaLeft' || e.code === 'MetaRight' || e.key === 'OS' || e.keyCode === 91 || e.keyCode === 92 ||
        e.key === 'Tab' || e.code === 'Tab' || e.keyCode === 9 ||
        e.key === 'ContextMenu' || e.code === 'ContextMenu' || e.keyCode === 93 ||
        e.key === 't' || e.key === 'T' || e.code === 'KeyT') {
      e.preventDefault();
      e.stopPropagation();
      toggleContextMenuAt(lastPointerX, lastPointerY);
      return;
    }"""
    if "e.key === 'Meta'" not in content:
        if "toggleContextMenuAt(lastPointerX, lastPointerY)" in content:
            content = re.sub(
                r"if\s*\(\s*e\.key\s*===\s*'Tab'[\s\S]*?toggleContextMenuAt\(lastPointerX,\s*lastPointerY\);\s*return;\s*\}",
                key_check_code,
                content
            )
        elif "e.key === 't'" in content:
            content = re.sub(
                r"if\s*\(\s*e\.key\s*===\s*'t'\s*\|\|\s*e\.key\s*===\s*'T'\s*\)\s*\{\s*e\.preventDefault\(\);\s*toggleTimerModal\(\);\s*return;\s*\}",
                key_check_code,
                content
            )
        else:
            target_esc = "togglePenMode(false);\n      }\n      return;\n    }"
            if target_esc in content:
                content = content.replace(target_esc, target_esc + "\n\n    " + key_check_code, 1)
        print("  Mapped key Meta/Tab/T/ContextMenu to toggleContextMenuAt.")

    # 16. Định nghĩa showContextMenuAt & toggleContextMenuAt & simulateLeftClickAt
    new_sim_click = """  function simulateLeftClickAt(x, y) {
    const ctx = document.getElementById('contextMenu');
    const isMenuOpen = ctx && ctx.style.display !== 'none' && ctx.getAttribute('aria-hidden') !== 'true';
    if (isMenuOpen) {
      const items = Array.from(ctx.querySelectorAll('.ctx-item'));
      const targetItem = items[ctxFocusedIdx] || items[0];
      if (targetItem) {
        targetItem.style.background = '#10b981';
        targetItem.style.color = '#ffffff';
        setTimeout(() => {
          targetItem.click();
        }, 60);
        return;
      }
    }

    const cx = (typeof x === 'number' && !isNaN(x) && x > 0) ? x : (window.innerWidth / 2);
    const cy = (typeof y === 'number' && !isNaN(y) && y > 0) ? y : (window.innerHeight / 2);
    const el = document.elementFromPoint(cx, cy);
    if (el) {
      const clickable = el.closest('button, a, [role="button"], .ctx-item, .quiz-btn, [onclick]');
      if (clickable) {
        clickable.click();
      } else {
        nextStep();
      }
    } else {
      nextStep();
    }
  }"""
    if "targetItem.style.background = '#10b981'" not in content:
        content = re.sub(
            r'function\s+simulateLeftClickAt\(x,\s*y\)\s*\{[\s\S]*?\n  \}',
            new_sim_click.strip(),
            content,
            count=1
        )
        print("  Upgraded simulateLeftClickAt in lecture content.")

    if "function toggleContextMenuAt" not in content:
        ctx_helpers = """  let ctxFocusedIdx = 0;

  function updateContextMenuFocus(idx) {
    const ctx = document.getElementById('contextMenu');
    if (!ctx) return;
    const items = Array.from(ctx.querySelectorAll('.ctx-item'));
    if (!items.length) return;
    if (idx < 0) idx = items.length - 1;
    if (idx >= items.length) idx = 0;
    ctxFocusedIdx = idx;
    items.forEach((it, i) => {
      it.classList.toggle('is-focused', i === idx);
    });
  }

""" + new_sim_click + """

  function refreshContextMenuState(ctx) {
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
  }

  function showContextMenuAt(x, y) {
    const ctx = document.getElementById('contextMenu');
    if (!ctx) return;
    refreshContextMenuState(ctx);
    const menuWidth = 240;
    const menuHeight = 440;
    let left = (typeof x === 'number' && !isNaN(x) && x > 0) ? x : (window.innerWidth / 2 - 120);
    let top = (typeof y === 'number' && !isNaN(y) && y > 0) ? y : (window.innerHeight / 2 - 200);
    if (left + menuWidth > window.innerWidth) left = window.innerWidth - menuWidth - 8;
    if (top + menuHeight > window.innerHeight) top = window.innerHeight - menuHeight - 8;
    ctx.style.left = Math.max(8, Math.round(left)) + 'px';
    ctx.style.top = Math.max(8, Math.round(top)) + 'px';
    ctx.style.display = 'flex';
    ctx.style.visibility = 'visible';
    ctx.style.opacity = '1';
    ctx.style.zIndex = '99999';
    ctx.setAttribute('aria-hidden', 'false');
    updateContextMenuFocus(0);
  }

  function toggleContextMenuAt(x, y) {
    const ctx = document.getElementById('contextMenu');
    if (!ctx) return;
    if (ctx.style.display === 'flex' && ctx.getAttribute('aria-hidden') === 'false') {
      hideContextMenu();
      return;
    }
    showContextMenuAt(x, y);
  }

"""
        target = "function initContextMenu() {"
        if target in content:
            content = content.replace(target, ctx_helpers + "  " + target, 1)
            content = re.sub(
                r"window\.addEventListener\('contextmenu',\s*function\(e\)\s*\{[\s\S]*?ctx\.style\.display\s*=\s*'flex';\s*\}\);",
                "window.addEventListener('contextmenu', function(e) {\n      if (e.target.closest('input, textarea, [contenteditable=\"true\"]')) return;\n      e.preventDefault();\n      e.stopPropagation();\n      showContextMenuAt(e.clientX, e.clientY);\n    }, true);",
                content
            )
        print("  Injected showContextMenuAt and toggleContextMenuAt before initContextMenu.")

    # Thêm hover focus listener vào initContextMenu
    init_focus_hook = """    ctx.querySelectorAll('.ctx-item').forEach((item, idx) => {
      item.addEventListener('mouseenter', () => updateContextMenuFocus(idx));
    });

"""
    if "updateContextMenuFocus(idx)" not in content:
        target_hide = "function hideContextMenu() {"
        if target_hide in content:
            content = content.replace(target_hide, init_focus_hook + "  " + target_hide, 1)

    # Đảm bảo action 'calc' mở máy tính trong handleCtxAction
    if "action === 'calc'" not in content:
        content = content.replace(
            "else if (action === 'blackboard') {",
            "else if (action === 'calc') {\n      if (typeof toggleCalculator === 'function') toggleCalculator();\n    } else if (action === 'blackboard') {"
        )

    # 17. Nâng cấp applyStepsToSlide & updateSlideDisplay để cuộn tự động và di chuyển con trỏ theo khối mới
    if "step-just-revealed" not in content:
        step_scroll_block = """    // 3. Tự động cuộn và di chuyển con trỏ chuột/laser theo khối mới xuất hiện
    if (currentStep > 0) {
      const target = slideEl.querySelector(`.content-block.is-revealed[data-step="${currentStep}"]`) ||
                     slideEl.querySelector(`.inline-anim.is-revealed[data-step="${currentStep}"]`);
      if (target) {
        target.classList.add('step-just-revealed');
        setTimeout(() => target.classList.remove('step-just-revealed'), 1300);

        setTimeout(function() {
          if (!target.isConnected) return;
          const col = target.closest('.col-board, .col-task') || target.closest('.slide-item');
          if (col) {
            const cRect = col.getBoundingClientRect();
            const tRect = target.getBoundingClientRect();
            const bottomLimit = Math.min(window.innerHeight - 90, cRect.bottom - 20);
            if (tRect.bottom > bottomLimit) {
              const scrollDiff = (tRect.bottom - bottomLimit) + 32;
              col.scrollBy({ top: scrollDiff, behavior: 'smooth' });
            } else if (tRect.top < cRect.top + 10) {
              const scrollDiff = tRect.top - cRect.top - 20;
              col.scrollBy({ top: scrollDiff, behavior: 'smooth' });
            }
          } else {
            try { target.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); } catch(e) {}
          }

          // Cập nhật vị trí con trỏ chuột ảo và laser pointer chạy theo
          setTimeout(function() {
            if (!target.isConnected) return;
            const freshRect = target.getBoundingClientRect();
            const targetX = Math.round(Math.min(window.innerWidth - 30, Math.max(30, freshRect.left + 35)));
            const targetY = Math.round(Math.min(window.innerHeight - 40, Math.max(40, freshRect.top + 28)));
            lastPointerX = targetX;
            lastPointerY = targetY;

            const laser = document.getElementById('laserPointer');
            if (laser) {
              laser.style.transition = 'left 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), top 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)';
              laser.style.left = targetX + 'px';
              laser.style.top = targetY + 'px';
              setTimeout(function() {
                if (laser) laser.style.transition = '';
              }, 450);
            }
          }, 120);
        }, 60);
      }
    } else if (currentStep === 0) {
      slideEl.querySelectorAll('.col-board, .col-task').forEach(c => {
        c.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }

"""
        target_mjx = "if (window.MathJax && window.MathJax.typesetPromise) {"
        if target_mjx in content:
            content = content.replace(target_mjx, step_scroll_block + '    ' + target_mjx, 1)
            print("  Upgraded applyStepsToSlide with auto-scroll and laser tracking.")

        target_usd = "const cur = getCurrentSlide();\n    if (cur) {\n      cur.classList.add('active');"
        repl_usd = "const cur = getCurrentSlide();\n    if (cur) {\n      cur.querySelectorAll('.col-board, .col-task').forEach(c => { c.scrollTop = 0; });\n      cur.classList.add('active');"
        if target_usd in content:
            content = content.replace(target_usd, repl_usd, 1)

    return content

print("================ RECREATING BAI 12 ================")
path_bai12 = 'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html'
c12 = subprocess.check_output(['git', 'show', f'HEAD:{path_bai12}'], encoding='utf-8')
c12 = common_patch(c12)

# Sửa Slide 1 của Bài 12:
# s1_b1 (MỤC TIÊU): step 0 (permanent on open!)
# s1_t1 (TÌNH HUỐNG) + s1_t2 (HÌNH 4.11): step 1
# s1_t3 (ĐỊNH HƯỚNG TƯ DUY): step 2
# s1_b2 (ĐẶT VẤN ĐỀ): step 3
# data-max-steps="3"
c12 = update_block_step(c12, 's1_b1', '0')
c12 = update_block_step(c12, 's1_t1', '1')
c12 = update_block_step(c12, 's1_t2', '1')
c12 = update_block_step(c12, 's1_t3', '2')
c12 = update_block_step(c12, 's1_b2', '3')

c12 = re.sub(
    r'(<section\s+class="slide-item[^"]*"[^>]*id="s1"[^>]*data-max-steps=")\d+(")',
    r'\g<1>3\g<2>',
    c12
)
print("  Slide 1 Bai 12 fixed: s1_b1=0, s1_t1=1, s1_t2=1, s1_t3=2, s1_b2=3 (max-steps=3).")

# Slide 16 Bai 12: s16_b1=1, s16_b2=2, s16_t1=3
c12 = update_block_step(c12, 's16_b1', '1')
c12 = update_block_step(c12, 's16_b2', '2')
c12 = update_block_step(c12, 's16_t1', '3')
c12 = re.sub(
    r'(<section\s+class="slide-item[^"]*"[^>]*id="s16"[^>]*data-max-steps=")\d+(")',
    r'\g<1>3\g<2>',
    c12
)
print("  Slide 16 Bai 12 fixed: s16_b1=1, s16_b2=2, s16_t1=3 (max-steps=3).")

with open(path_bai12, 'w', encoding='utf-8') as f:
    f.write(c12)
print("SAVED BAI 12 SUCCESSFULLY!")


print("\n================ RECREATING BAI 4 ================")
path_bai4 = 'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
c4 = subprocess.check_output(['git', 'show', f'HEAD:{path_bai4}'], encoding='utf-8')
c4 = common_patch(c4)

# Sửa Slide 1 của Bài 4:
# s1_b1 (MỤC TIÊU BÀI HỌC): step 0 (permanent on open!)
# s1_t1 (KHỞI ĐỘNG VƯỜN HOA) + s1_t2 (HÌNH 2.1 SVG): step 1 (đồng hành đề bài - hình vẽ)
# s1_t3 (CÂU HỎI THẢO LUẬN): step 2
# data-max-steps="2"
c4 = update_block_step(c4, 's1_b1', '0')
c4 = update_block_step(c4, 's1_t1', '1')
c4 = update_block_step(c4, 's1_t2', '1')
c4 = update_block_step(c4, 's1_t3', '2')

c4 = re.sub(
    r'(<section\s+class="slide-item[^"]*"[^>]*id="s1"[^>]*data-max-steps=")\d+(")',
    r'\g<1>2\g<2>',
    c4
)
print("  Slide 1 Bai 4 fixed: s1_b1=0, s1_t1=1, s1_t2=1, s1_t3=2 (max-steps=2).")

# Thêm nút chuyển 3 tiết học vào thanh điều khiển Bài 4 (Tiết 1: Slide 1, Tiết 2: Slide 10, Tiết 3: Slide 19)
if '.btn-ctrl.btn-period' not in c4:
    c4 = c4.replace(
        '.btn-ctrl:hover {',
        '.btn-ctrl.btn-period { font-size: 0.78rem; padding: 4px 8px; }\n    .btn-ctrl.btn-period:hover { background: #3b82f6; color: #fff; }\n    .btn-ctrl:hover {',
        1
    )

if 'ctrl-group-periods' not in c4:
    periods_html = """
  <!-- Nhóm 2: Chuyển tiết học -->
  <div class="ctrl-group ctrl-group-periods">
    <button class="btn-ctrl btn-period" onclick="jumpToPeriod(1)" title="Tiết 1: Phương trình tích (Slide 1–9)">Tiết 1</button>
    <button class="btn-ctrl btn-period" onclick="jumpToPeriod(2)" title="Tiết 2: Phương trình chứa ẩn ở mẫu (Slide 10–18)">Tiết 2</button>
    <button class="btn-ctrl btn-period" onclick="jumpToPeriod(3)" title="Tiết 3: Luyện tập & Vận dụng (Slide 19–26)">Tiết 3</button>
  </div>"""
    c4 = re.sub(
        r'(<div class="ctrl-group ctrl-group-nav">[\s\S]*?</div>)',
        r'\1' + periods_html,
        c4,
        1
    )
    print("  Added 3-period navigation buttons to Bai 4 control bar.")

if 'function jumpToPeriod' not in c4:
    jump_fn = """  function jumpToPeriod(n) {
    const map = { 1: 1, 2: 10, 3: 19 };
    const target = map[n];
    if (!target || target > totalSlides) return;
    currentSlideIndex = target;
    currentStep = 0;
    updateSlideDisplay();
  }

"""
    target_zoom = 'function zoomableFigure(target) {'
    if target_zoom in c4:
        c4 = c4.replace(target_zoom, jump_fn + target_zoom, 1)
        print("  Added jumpToPeriod function to Bai 4 JS.")

with open(path_bai4, 'w', encoding='utf-8') as f:
    f.write(c4)
print("SAVED BAI 4 SUCCESSFULLY!")

