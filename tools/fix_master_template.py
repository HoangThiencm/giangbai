import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

MODAL_CSS = """
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

def patch_html(content):
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

    # 3. Đảm bảo inline style="display:none;" trên editModalBackdrop
    content = re.sub(
        r'<div\s+class="edit-modal-backdrop"\s+id="editModalBackdrop"[^>]*>',
        '<div class="edit-modal-backdrop" id="editModalBackdrop" style="display:none;" onclick="handleBackdropClick(event)">',
        content
    )

    # 4. Đảm bảo inline style="display:none;" trên imageLightboxBackdrop
    content = re.sub(
        r'<div\s+class="image-lightbox-backdrop"\s+id="imageLightboxBackdrop"[^>]*>',
        '<div class="image-lightbox-backdrop" id="imageLightboxBackdrop" style="display:none;" onclick="handleLightboxBackdropClick(event)">',
        content
    )

    # 5. Sửa form Edit Modal cho đồng bộ ID và hỗ trợ math
    old_modal_pat = r'<div class="edit-modal" id="editModal">[\s\S]*?</div>\s*</div>'
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

    # 6. Thêm hàm insertMath & aliases vào JS
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

    # 7. Cập nhật openEditModal & closeEditModal để toggle backdrop display flex/none
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

    # 8. Cập nhật openImageLightbox & closeImageLightbox
    if "backdrop.style.display = 'flex';" not in content:
        content = content.replace("backdrop.classList.add('active');", "backdrop.style.display = 'flex';\n    backdrop.classList.add('active');")
        content = content.replace("backdrop.classList.remove('active');", "backdrop.style.display = 'none';\n      backdrop.classList.remove('active');")
        print("  Updated openImageLightbox and closeImageLightbox display toggles.")

    # 9. Sửa lỗi corrupted tab/formfeed escapes
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

    return content

p = 'TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

fixed = patch_html(text)
with open(p, 'w', encoding='utf-8') as f:
    f.write(fixed)
print("SUCCESSFULLY PATCHED master_lecture_template.html!")
