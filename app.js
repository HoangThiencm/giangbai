// js/app.js - Tích hợp hệ thống & Model Priority

const defaultProps = {
    selectable: true, hasControls: true, hasBorders: true, originX: 'center', originY: 'center', strokeWidth: 2, padding: 5,
};

const chartPatterns = [];
function createPatterns() {
    const patternSize = 10;
    const patternCanvas = new fabric.StaticCanvas(null, { width: patternSize, height: patternSize });
    const patterns = [
        (ctx) => { ctx.strokeStyle = '#333'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, patternSize / 2); ctx.lineTo(patternSize, patternSize / 2); ctx.stroke(); },
        (ctx) => { ctx.strokeStyle = '#333'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(patternSize / 2, 0); ctx.lineTo(patternSize / 2, patternSize); ctx.stroke(); },
        (ctx) => { ctx.strokeStyle = '#333'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(patternSize, patternSize); ctx.moveTo(-patternSize, 0); ctx.lineTo(0, patternSize); ctx.moveTo(patternSize, 0); ctx.lineTo(0, -patternSize); ctx.stroke(); },
        (ctx) => { ctx.strokeStyle = '#555'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(0, patternSize / 2); ctx.lineTo(patternSize, patternSize / 2); ctx.moveTo(patternSize / 2, 0); ctx.lineTo(patternSize / 2, patternSize); ctx.stroke(); },
        (ctx) => { ctx.fillStyle = '#333'; ctx.beginPath(); ctx.arc(patternSize / 2, patternSize / 2, 2, 0, Math.PI * 2); ctx.fill(); }
    ];
    patterns.forEach(pFunc => {
        patternCanvas.clear(); pFunc(patternCanvas.getContext('2d'));
        chartPatterns.push(new fabric.Pattern({ source: patternCanvas.getElement(), repeat: 'repeat' }));
    });
}
createPatterns();
const chartColors = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#6366f1', '#8b5cf6'];

let pointLabelCounter = 0;
function addPoint(canvas, x, y, color) {
    const label = String.fromCharCode(65 + pointLabelCounter++);
    const point = new fabric.Circle({ ...defaultProps, left: x, top: y, radius: 4, fill: color, stroke: color, strokeWidth: 1, source: 'user', type: 'point' });
    const text = new fabric.IText(label, { ...defaultProps, left: x + 10, top: y + 10, fontFamily: 'Inter', fontSize: 18, fill: color, source: 'user', type: 'point_label' });
    const group = new fabric.Group([point, text], { ...defaultProps, left: x, top: y, source: 'user', subTargetCheck: true, type: 'point_group' });
    canvas.add(group);
}

function addText(canvas, x, y, color, textContent = 'Tên') {
    const fontSize = parseInt(document.getElementById('font-size').value, 10) || 18;
    const isBold = document.getElementById('font-bold').classList.contains('active');
    const isItalic = document.getElementById('font-italic').classList.contains('active');
    const isUnderline = document.getElementById('font-underline').classList.contains('active');
    const text = new fabric.IText(textContent, { ...defaultProps, left: x, top: y, fontFamily: 'Inter', fontSize: fontSize, fontWeight: isBold ? 'bold' : 'normal', fontStyle: isItalic ? 'italic' : 'normal', underline: isUnderline, fill: color, stroke: null, source: 'user' });
    canvas.add(text); text.bringToFront(); canvas.setActiveObject(text);
    if (textContent === 'Tên') { text.enterEditing(); text.selectAll(); }
}

function addRightAngleSymbol(canvas, p1, vertex, p2, color, size = 15) {
    const v1 = { x: p1.x - vertex.x, y: p1.y - vertex.y }; const v2 = { x: p2.x - vertex.x, y: p2.y - vertex.y };
    const dist1 = Math.sqrt(v1.x * v1.x + v1.y * v1.y); const dist2 = Math.sqrt(v2.x * v2.x + v2.y * v2.y);
    if (dist1 === 0 || dist2 === 0) return;
    const unitV1 = { x: v1.x / dist1, y: v1.y / dist1 }; const unitV2 = { x: v2.x / dist2, y: v2.y / dist2 };
    const pA = { x: vertex.x + unitV1.x * size, y: vertex.y + unitV1.y * size }; const pB = { x: vertex.x + unitV2.x * size, y: vertex.y + unitV2.y * size };
    const pC = { x: pA.x + unitV2.x * size, y: pA.y + unitV2.y * size };
    const symbol = new fabric.Polyline([pA, pC, pB], { ...defaultProps, stroke: color, fill: 'transparent', strokeWidth: 1.5, selectable: false, evented: false, source: 'ai_primitive' });
    canvas.add(symbol);
}

function addEqualityTick(canvas, p1, p2, color, numTicks = 1, size = 10, spacing = 4) {
    const midPoint = { x: (p1.x + p2.x) / 2, y: (p1.y + p2.y) / 2 };
    const dx = p2.x - p1.x; const dy = p2.y - p1.y; const angle = Math.atan2(dy, dx); const perpAngle = angle + Math.PI / 2;
    const tickDx = Math.cos(perpAngle) * size / 2; const tickDy = Math.sin(perpAngle) * size / 2;
    const segmentLen = Math.sqrt(dx * dx + dy * dy); if (segmentLen === 0) return;
    const unitSegmentVec = { x: dx / segmentLen, y: dy / segmentLen };
    for (let i = 0; i < numTicks; i++) {
        const offset = (i - (numTicks - 1) / 2) * spacing;
        const center = { x: midPoint.x + unitSegmentVec.x * offset, y: midPoint.y + unitSegmentVec.y * offset };
        const tick = new fabric.Line([center.x - tickDx, center.y - tickDy, center.x + tickDx, center.y + tickDy], { ...defaultProps, stroke: color, strokeWidth: 2, selectable: false, evented: false, originX: 'center', originY: 'center', source: 'ai_primitive' });
        canvas.add(tick);
    }
}

function addAngleArc(canvas, p1, vertex, p2, color, radius = 25, label = '') {
    const v1 = { x: p1.x - vertex.x, y: p1.y - vertex.y }; const v2 = { x: p2.x - vertex.x, y: p2.y - vertex.y };
    const startAngle = Math.atan2(v1.y, v1.x) * 180 / Math.PI; const endAngle = Math.atan2(v2.y, v2.x) * 180 / Math.PI;
    let angleDiff = endAngle - startAngle; if (angleDiff > 180) angleDiff -= 360; if (angleDiff < -180) angleDiff += 360;
    const finalEndAngle = startAngle + angleDiff;
    const arc = new fabric.Circle({ ...defaultProps, left: vertex.x, top: vertex.y, radius: radius, startAngle: startAngle, endAngle: finalEndAngle, stroke: color, strokeWidth: 1.5, fill: '', selectable: false, evented: false, source: 'ai_primitive' });
    canvas.add(arc);
    if (label) {
        const midAngleRad = (arc.startAngle + angleDiff / 2) * Math.PI / 180; const labelRadius = radius * 0.7;
        const textLabel = new fabric.IText(label, { ...defaultProps, left: vertex.x + labelRadius * Math.cos(midAngleRad), top: vertex.y + labelRadius * Math.sin(midAngleRad), fontSize: 14, fill: color, selectable: false, evented: false, source: 'ai_primitive' });
        canvas.add(textLabel);
    }
}

function drawBarChart(canvas, data, options = {}) {
    const { title = "Biểu đồ cột", usePatterns = false, x = 100, y = 400, width = 400, height = 300 } = options;
    const chartGroup = []; const maxValue = Math.max(...data.map(d => d.value)); const barWidth = width / (data.length * 1.5);
    const axisLine = new fabric.Polyline([{ x: x, y: y - height }, { x: x, y: y }, { x: x + width, y: y }], { ...defaultProps, stroke: '#333', fill: 'transparent', selectable: false, source: 'ai_primitive' });
    chartGroup.push(axisLine);
    data.forEach((d, i) => {
        const barHeight = (d.value / maxValue) * height; const barX = x + (i + 0.5) * (width / data.length);
        const fill = usePatterns ? chartPatterns[i % chartPatterns.length] : chartColors[i % chartColors.length];
        const bar = new fabric.Rect({ ...defaultProps, left: barX, top: y, width: barWidth, height: barHeight, fill: fill, stroke: '#333', strokeWidth: 1, originX: 'center', originY: 'bottom', selectable: false, source: 'ai_primitive' });
        const label = new fabric.IText(d.label, { ...defaultProps, left: barX, top: y + 10, fontSize: 14, originX: 'center', originY: 'top', selectable: false, source: 'ai_primitive' });
        chartGroup.push(bar, label);
    });
    const titleText = new fabric.IText(title, { ...defaultProps, left: x + width / 2, top: y - height - 30, fontSize: 20, fontWeight: 'bold', originX: 'center', originY: 'bottom', selectable: false, source: 'ai_primitive' });
    chartGroup.push(titleText);
    const group = new fabric.Group(chartGroup, { source: 'ai', ...defaultProps }); canvas.add(group);
}

function drawPieChart(canvas, data, options = {}) {
    const { title = "Biểu đồ tròn", usePatterns = false, cx = 300, cy = 250, radius = 150 } = options;
    const chartGroup = []; const total = data.reduce((sum, d) => sum + d.value, 0); let startAngle = 0;
    data.forEach((d, i) => {
        const sliceAngle = (d.value / total) * 360; const endAngle = startAngle + sliceAngle;
        const fill = usePatterns ? chartPatterns[i % chartPatterns.length] : chartColors[i % chartColors.length];
        const largeArcFlag = sliceAngle > 180 ? 1 : 0;
        const startRad = fabric.util.degreesToRadians(startAngle - 90); const endRad = fabric.util.degreesToRadians(endAngle - 90);
        const startPoint = { x: cx + radius * Math.cos(startRad), y: cy + radius * Math.sin(startRad) };
        const endPoint = { x: cx + radius * Math.cos(endRad), y: cy + radius * Math.sin(endRad) };
        const pathData = `M ${cx} ${cy} L ${startPoint.x} ${startPoint.y} A ${radius} ${radius} 0 ${largeArcFlag} 1 ${endPoint.x} ${endPoint.y} z`;
        const slice = new fabric.Path(pathData, { ...defaultProps, fill: fill, stroke: '#333', strokeWidth: 1, selectable: false, source: 'ai_primitive' });
        chartGroup.push(slice);
        const legendColorBox = new fabric.Rect({ ...defaultProps, left: cx + radius + 20, top: cy - radius + i * 25, width: 20, height: 20, fill: fill, stroke: '#333', strokeWidth: 1, selectable: false, source: 'ai_primitive' });
        const legendText = new fabric.IText(`${d.label} (${d.value})`, { ...defaultProps, left: cx + radius + 50, top: cy - radius + i * 25 + 10, fontSize: 14, originY: 'center', selectable: false, source: 'ai_primitive' });
        chartGroup.push(legendColorBox, legendText);
        startAngle = endAngle;
    });
    const titleText = new fabric.IText(title, { ...defaultProps, left: cx, top: cy - radius - 30, fontSize: 20, fontWeight: 'bold', originX: 'center', originY: 'bottom', selectable: false, source: 'ai_primitive' });
    chartGroup.push(titleText);
    const group = new fabric.Group(chartGroup, { source: 'ai', ...defaultProps }); canvas.add(group);
}

function activatePointTool(canvas, colorPicker) {
    const handleMouseDown = (options) => { if (!options.target) { const p = canvas.getPointer(options.e); addPoint(canvas, p.x, p.y, colorPicker.value); } };
    canvas.on('mouse:down', handleMouseDown); return () => canvas.off('mouse:down', handleMouseDown);
}
function activateTextTool(canvas, colorPicker) {
    const handleMouseDown = (options) => { if (!options.target) { const p = canvas.getPointer(options.e); addText(canvas, p.x, p.y, colorPicker.value); } };
    canvas.on('mouse:down', handleMouseDown); return () => canvas.off('mouse:down', handleMouseDown);
}
function activateLineTool(canvas, colorPicker) {
    let line, isDown;
    const handleMouseDown = (o) => { isDown = true; const pointer = canvas.getPointer(o.e); line = new fabric.Line([pointer.x, pointer.y, pointer.x, pointer.y], { ...defaultProps, objectCaching: false, stroke: colorPicker.value, source: 'user' }); canvas.add(line); };
    const handleMouseMove = (o) => { if (!isDown) return; const pointer = canvas.getPointer(o.e); line.set({ x2: pointer.x, y2: pointer.y }); canvas.renderAll(); };
    const handleMouseUp = () => { isDown = false; };
    canvas.on('mouse:down', handleMouseDown); canvas.on('mouse:move', handleMouseMove); canvas.on('mouse:up', handleMouseUp);
    return () => { canvas.off('mouse:down', handleMouseDown); canvas.off('mouse:move', handleMouseMove); canvas.off('mouse:up', handleMouseUp); };
}
function activateCircleTool(canvas, colorPicker) {
    let circle, origX, origY;
    const handleMouseDown = (o) => { const pointer = canvas.getPointer(o.e); origX = pointer.x; origY = pointer.y; circle = new fabric.Circle({ ...defaultProps, left: origX, top: origY, radius: 0, fill: 'transparent', stroke: colorPicker.value, source: 'user' }); canvas.add(circle); };
    const handleMouseMove = (o) => { if (!circle) return; const pointer = canvas.getPointer(o.e); const radius = Math.sqrt(Math.pow(origX - pointer.x, 2) + Math.pow(origY - pointer.y, 2)); circle.set({ radius: radius }); canvas.renderAll(); };
    const handleMouseUp = () => { circle = null; };
    canvas.on('mouse:down', handleMouseDown); canvas.on('mouse:move', handleMouseMove); canvas.on('mouse:up', handleMouseUp);
    return () => { canvas.off('mouse:down', handleMouseDown); canvas.off('mouse:move', handleMouseMove); canvas.off('mouse:up', handleMouseUp); };
}

document.addEventListener('DOMContentLoaded', function () {
    const canvasContainer = document.querySelector('#geometry-canvas').parentElement;
    const canvas = new fabric.Canvas('geometry-canvas', { width: canvasContainer.clientWidth, height: canvasContainer.clientHeight, backgroundColor: '#fff', selection: true, renderOnAddRemove: true });

    const ZOOM_VIEWER_SCALE = 3; const ZOOM_VIEWER_SIZE = 200;
    const zoomCanvasElement = document.getElementById('zoom-canvas');
    let zoomViewerCanvas = null;
    if (zoomCanvasElement) {
        zoomCanvasElement.width = ZOOM_VIEWER_SIZE; zoomCanvasElement.height = ZOOM_VIEWER_SIZE;
        zoomViewerCanvas = new fabric.Canvas('zoom-canvas', { width: ZOOM_VIEWER_SIZE, height: ZOOM_VIEWER_SIZE, selection: false, hoverCursor: 'default', backgroundColor: '#f0f0f0' });
    }

    let currentTool = 'select', apiKeysFromFile = [], activeImageFile = null, activeToolCleanup = null;
    let isAiLocked = false, _clipboard = null, history = [], historyIndex = -1, isRestoring = false, isAiDrawing = false, isPanning = false, lastPanX, lastPanY;
    const HISTORY_LIMIT = 100; let isGridVisible = false, gridGroup = null; const GRID_SIZE = 25, GRID_COLOR = '#e0e0e0'; let mathField = null; let isSnapEnabled = false;

    const allDOMElements = {
        generateBtn: document.getElementById('generate-btn'), regenerateBtn: document.getElementById('regenerate-btn'), promptInput: document.getElementById('prompt-input'), imageUpload: document.getElementById('image-upload'), imagePreview: document.getElementById('image-preview'), analysisOutput: document.getElementById('analysis-output'), loader: document.getElementById('loader'), toolbar: document.getElementById('toolbar'), colorPicker: document.getElementById('color-picker'), deleteBtn: document.getElementById('delete-btn'), apiKeyFile: document.getElementById('api-key-file'), apiKeyFilename: document.getElementById('api-key-filename'), modelSelect: document.getElementById('model-select'), lockAiBtn: document.getElementById('lock-ai-btn'), undoBtn: document.getElementById('undo-btn'), redoBtn: document.getElementById('redo-btn'), copyBtn: document.getElementById('copy-btn'), pasteBtn: document.getElementById('paste-btn'), zoomInBtn: document.getElementById('zoom-in-btn'), zoomOutBtn: document.getElementById('zoom-out-btn'), resetZoomBtn: document.getElementById('reset-zoom-btn'), accordionHeaders: document.querySelectorAll('.accordion-header'), geogebraToggle: document.getElementById('geogebra-toggle'), geogebraContainer: document.getElementById('geogebra-container'), latexToolBtn: document.getElementById('latex-tool-btn'), insertImageBtn: document.getElementById('insert-image-btn'), imageInserter: document.getElementById('image-inserter'), latexModal: document.getElementById('latex-modal'), latexModalBackdrop: document.getElementById('latex-modal-backdrop'), mathInput: document.getElementById('math-input'), latexPreview: document.getElementById('latex-preview'), cancelLatexBtn: document.getElementById('cancel-latex-btn'), insertLatexBtn: document.getElementById('insert-latex-btn'), toggleGridBtn: document.getElementById('toggle-grid-btn'), zoomViewer: document.getElementById('zoom-viewer'), textControls: document.getElementById('text-controls'), fontSize: document.getElementById('font-size'), fontBold: document.getElementById('font-bold'), fontItalic: document.getElementById('font-italic'), fontUnderline: document.getElementById('font-underline'), promptSuggestions: document.getElementById('prompt-suggestions'), toggleSnapBtn: document.getElementById('toggle-snap-btn'), alignControls: document.getElementById('align-controls'), darkModeToggle: document.getElementById('dark-mode-toggle'), miniToolbar: document.getElementById('mini-toolbar'), miniColorPicker: document.getElementById('mini-color-picker'), miniDeleteBtn: document.getElementById('mini-delete-btn'),
    };
    allDOMElements.aiProviderSelect = document.getElementById('ai-provider-select');
    allDOMElements.aiModelSelect = document.getElementById('ai-model-select');
    allDOMElements.aiModelSummary = document.getElementById('ai-model-summary');
    let drawingAiConfig = null;
    const VEHINH_PROVIDER_STORAGE_KEY = 'vehinh_ai_provider';
    const VEHINH_MODEL_STORAGE_PREFIX = 'vehinh_ai_model_';

    function getDrawingProviderConfig(provider) {
        return drawingAiConfig?.providers?.[provider] || null;
    }

    function getSavedDrawingModel(provider) {
        return localStorage.getItem(`${VEHINH_MODEL_STORAGE_PREFIX}${provider}`) || '';
    }

    function getCurrentDrawingModel(provider) {
        const providerConfig = getDrawingProviderConfig(provider);
        if (!providerConfig) return '';
        const models = Array.isArray(providerConfig.models) ? providerConfig.models : [];
        const savedModel = getSavedDrawingModel(provider);
        if (savedModel && models.includes(savedModel)) return savedModel;
        if (providerConfig.model && models.includes(providerConfig.model)) return providerConfig.model;
        return providerConfig.model || models[0] || '';
    }

    function syncDrawingModelSelect() {
        const provider = allDOMElements.aiProviderSelect?.value || drawingAiConfig?.default_provider || 'ds2api';
        const providerConfig = getDrawingProviderConfig(provider);
        const select = allDOMElements.aiModelSelect;
        if (!select) return;

        select.innerHTML = '';
        const models = Array.isArray(providerConfig?.models) ? providerConfig.models : [];
        if (!models.length) {
            const option = document.createElement('option');
            option.value = providerConfig?.model || '';
            option.textContent = providerConfig?.model || 'Chưa có model';
            select.appendChild(option);
            select.disabled = true;
            return;
        }

        models.forEach((model) => {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = model;
            select.appendChild(option);
        });
        select.disabled = false;
        select.value = getCurrentDrawingModel(provider);
    }

    function serializeCanvas() { return canvas.toJSON(['source', 'type']); }
    function saveHistory() { if (isRestoring) return; const json = serializeCanvas(); if (historyIndex < history.length - 1) { history = history.slice(0, historyIndex + 1); } history.push(json); if (history.length > HISTORY_LIMIT) history.shift(); historyIndex = history.length - 1; updateUndoRedoButtons(); }
    function updateUndoRedoButtons() { allDOMElements.undoBtn.disabled = historyIndex <= 0; allDOMElements.redoBtn.disabled = historyIndex >= history.length - 1; }
    function loadFrom(json) { return new Promise((resolve) => { isRestoring = true; canvas.loadFromJSON(json, () => { applyAiLockState(); sendPointsToFront(); isRestoring = false; resolve(); }); }); }
    async function undo() { if (historyIndex > 0) { historyIndex--; await loadFrom(history[historyIndex]); canvas.renderAll(); updateUndoRedoButtons(); } }
    async function redo() { if (historyIndex < history.length - 1) { historyIndex++; await loadFrom(history[historyIndex]); canvas.renderAll(); updateUndoRedoButtons(); } }

    function applyAiLockState() { canvas.getObjects().forEach(obj => { if (obj.source === 'ai' || obj.source === 'ai_primitive') { obj.set({ selectable: !isAiLocked, hasControls: !isAiLocked, hasBorders: !isAiLocked, hoverCursor: isAiLocked ? 'default' : 'move' }); } }); const lockIcon = document.getElementById('lock-icon-locked'), unlockIcon = document.getElementById('lock-icon-unlocked'); if (isAiLocked) { unlockIcon.classList.add('hidden'); lockIcon.classList.remove('hidden'); allDOMElements.lockAiBtn.classList.add('active'); } else { unlockIcon.classList.remove('hidden'); lockIcon.classList.add('hidden'); allDOMElements.lockAiBtn.classList.remove('active'); } canvas.discardActiveObject().renderAll(); }
    function sendPointsToFront() { canvas.getObjects().forEach(obj => { if (obj.type === 'circle' || obj.type === 'i-text' || obj.type === 'text' || obj.type === 'point_group') { obj.bringToFront(); } }); canvas.renderAll(); }
    saveHistory();

    function showMiniToolbar(target) { if (!target) return; const toolbar = allDOMElements.miniToolbar; const objCoords = target.getBoundingRect(); const zoom = canvas.getZoom(); const panX = canvas.viewportTransform[4]; const panY = canvas.viewportTransform[5]; const top = objCoords.top * zoom + panY - 45; const left = objCoords.left * zoom + panX + (objCoords.width * zoom / 2) - (toolbar.offsetWidth / 2); toolbar.style.top = `${top}px`; toolbar.style.left = `${left}px`; toolbar.classList.remove('hidden'); allDOMElements.miniColorPicker.value = target.fill || target.stroke || '#000000'; }
    function hideMiniToolbar() { allDOMElements.miniToolbar.classList.add('hidden'); }
    allDOMElements.miniDeleteBtn.addEventListener('click', () => { allDOMElements.deleteBtn.click(); hideMiniToolbar(); });
    allDOMElements.miniColorPicker.addEventListener('input', (e) => { const color = e.target.value; const activeObj = canvas.getActiveObject(); if (activeObj) { if (activeObj.type === 'activeSelection') { activeObj.forEachObject(obj => setColorForObject(obj, color)); } else { setColorForObject(activeObj, color); } canvas.renderAll(); saveHistory(); } });
    function setColorForObject(obj, color) { if (obj.type === 'i-text' || obj.type === 'text' || obj.type === 'point_group' || obj.type === 'point_label') { obj.set('fill', color); } else if (obj.type === 'point') { obj.set('fill', color); obj.set('stroke', color); } else if (obj.type === 'circle' && obj.fill !== 'transparent') { obj.set('fill', color); } else { obj.set('stroke', color); } }

    canvas.on({
        'object:added': () => { if (!isRestoring && !isAiDrawing) saveHistory(); sendPointsToFront(); },
        'object:modified': () => { if (!isRestoring && !isAiDrawing) saveHistory(); sendPointsToFront(); },
        'object:removed': () => { if (!isRestoring && !isAiDrawing) saveHistory(); },
        'selection:created': (e) => { updateContextualToolbars(); showMiniToolbar(e.target); },
        'selection:updated': (e) => { updateContextualToolbars(); showMiniToolbar(e.target); },
        'selection:cleared': () => { updateContextualToolbars(); hideMiniToolbar(); },
        'object:moving': (e) => { updateZoomViewer(e); if (isSnapEnabled) snapObject(e.target); showMiniToolbar(e.target); },
        'object:scaling': (e) => { updateZoomViewer(e); showMiniToolbar(e.target); },
        'object:rotating': (e) => { updateZoomViewer(e); showMiniToolbar(e.target); },
        'mouse:move': updateZoomViewer, 'object:moved': hideZoomViewer, 'mouse:up': hideZoomViewer,
    });

    let zoomViewerTarget = null;

    function isZoomViewerTarget(obj, target) {
        if (!target) return false;
        if (obj === target) return true;
        if (target.type === 'activeSelection' && typeof target.contains === 'function') {
            return target.contains(obj);
        }
        return false;
    }

    function updateZoomViewer(options) {
        if (!options?.e) return;
        const isMouseMove = !options.target && options.e.type === 'mousemove';
        if (isMouseMove && !zoomViewerTarget) return;

        const targetObject = options.target || zoomViewerTarget;
        if (!targetObject) return;

        if (options.action === 'drag' || options.transform) {
            zoomViewerTarget = targetObject;
        }
        if (!zoomViewerTarget || !zoomViewerCanvas) return;

        allDOMElements.zoomViewer.style.display = 'block';

        const rect = targetObject.getBoundingRect(true, true);
        const zoomCenterX = rect.left + rect.width / 2;
        const zoomCenterY = rect.top + rect.height / 2;
        zoomViewerCanvas.setViewportTransform([
            ZOOM_VIEWER_SCALE, 0, 0, ZOOM_VIEWER_SCALE,
            -zoomCenterX * ZOOM_VIEWER_SCALE + ZOOM_VIEWER_SIZE / 2,
            -zoomCenterY * ZOOM_VIEWER_SCALE + ZOOM_VIEWER_SIZE / 2,
        ]);

        const objects = canvas.getObjects().filter(obj => obj !== gridGroup && obj.visible !== false);
        zoomViewerCanvas.clear();
        if (!objects.length) {
            zoomViewerCanvas.requestRenderAll();
            return;
        }

        let pending = objects.length;
        objects.forEach(obj => {
            obj.clone((cloned) => {
                const isTarget = isZoomViewerTarget(obj, targetObject);
                cloned.set({
                    hasControls: isTarget,
                    hasBorders: isTarget,
                    selectable: false,
                    evented: false,
                    opacity: isTarget ? 0.85 : 1,
                });
                cloned.setCoords();
                zoomViewerCanvas.add(cloned);
                pending -= 1;
                if (pending === 0) zoomViewerCanvas.requestRenderAll();
            }, ['source', 'type']);
        });
    }

    function showZoomViewer(e) { if (zoomViewerTarget) { allDOMElements.zoomViewer.style.display = 'block'; } }
    function hideZoomViewer() { allDOMElements.zoomViewer.style.display = 'none'; zoomViewerTarget = null; }

    allDOMElements.undoBtn.addEventListener('click', undo); allDOMElements.redoBtn.addEventListener('click', redo); allDOMElements.copyBtn.addEventListener('click', copy); allDOMElements.pasteBtn.addEventListener('click', paste); allDOMElements.zoomInBtn.addEventListener('click', () => zoom(1.1)); allDOMElements.zoomOutBtn.addEventListener('click', () => zoom(1 / 1.1)); allDOMElements.resetZoomBtn.addEventListener('click', () => { canvas.setViewportTransform([1, 0, 0, 1, 0, 0]); canvas.renderAll(); });
    function zoom(factor) { const center = canvas.getCenter(); canvas.zoomToPoint(new fabric.Point(center.left, center.top), canvas.getZoom() * factor); canvas.renderAll(); }

    function updateContextualToolbars() { const activeObj = canvas.getActiveObject(); if (activeObj && activeObj.type === 'i-text' && !activeObj.isEditing) { allDOMElements.textControls.classList.remove('hidden'); allDOMElements.textControls.classList.add('flex'); allDOMElements.fontSize.value = activeObj.get('fontSize'); allDOMElements.fontBold.classList.toggle('active', activeObj.get('fontWeight') === 'bold'); allDOMElements.fontItalic.classList.toggle('active', activeObj.get('fontStyle') === 'italic'); allDOMElements.fontUnderline.classList.toggle('active', activeObj.get('underline')); } else { allDOMElements.textControls.classList.add('hidden'); allDOMElements.textControls.classList.remove('flex'); } if (activeObj && activeObj.type === 'activeSelection' && activeObj._objects.length > 1) { allDOMElements.alignControls.classList.remove('hidden'); allDOMElements.alignControls.classList.add('flex'); } else { allDOMElements.alignControls.classList.add('hidden'); allDOMElements.alignControls.classList.remove('flex'); } }
    function applyStyleToSelection(style, value) { const activeObj = canvas.getActiveObject(); if (activeObj && activeObj.type === 'i-text') { activeObj.set(style, value); canvas.renderAll(); saveHistory(); } }
    allDOMElements.fontSize.addEventListener('input', (e) => applyStyleToSelection('fontSize', parseInt(e.target.value, 10))); allDOMElements.fontBold.addEventListener('click', () => { const a = canvas.getActiveObject(); if (a && a.type === 'i-text') { applyStyleToSelection('fontWeight', a.get('fontWeight') === 'bold' ? 'normal' : 'bold'); updateContextualToolbars(); } }); allDOMElements.fontItalic.addEventListener('click', () => { const a = canvas.getActiveObject(); if (a && a.type === 'i-text') { applyStyleToSelection('fontStyle', a.get('fontStyle') === 'italic' ? 'normal' : 'italic'); updateContextualToolbars(); } }); allDOMElements.fontUnderline.addEventListener('click', () => { const a = canvas.getActiveObject(); if (a && a.type === 'i-text') { applyStyleToSelection('underline', !a.get('underline')); updateContextualToolbars(); } });

    // --- API Key Management (UPDATED) ---
    async function loadDrawingAiConfig() {
        try {
            const res = await fetch('api/vehinh_ai.php?action=config', {
                credentials: 'same-origin',
                cache: 'no-store'
            });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(data.error || 'Không đọc được cấu hình AI vẽ hình.');
            if (!data || typeof data !== 'object' || !data.providers?.ds2api || !data.providers?.gemini) {
                throw new Error('Cáº¥u hÃ¬nh AI váº½ hÃ¬nh tráº£ vá» khÃ´ng Ä‘á»§ dá»¯ liá»‡u.');
            }
            drawingAiConfig = data;
            const savedProvider = localStorage.getItem(VEHINH_PROVIDER_STORAGE_KEY);
            const defaultProvider = savedProvider || data.default_provider || 'ds2api';
            if (allDOMElements.aiProviderSelect) {
                allDOMElements.aiProviderSelect.value = defaultProvider;
            }
            syncDrawingModelSelect();
            updateDrawingAiSummary();
        } catch (error) {
            drawingAiConfig = {
                default_provider: 'gemini',
                providers: {
                    ds2api: {
                        label: 'DeepSeek / DS2API',
                        configured: false,
                        model: localStorage.getItem('default_ds2api_module') || 'deepseek-v4-flash',
                        models: ['deepseek-v4-flash', 'deepseek-v4-flash-nothinking', 'deepseek-v4-pro', 'deepseek-v4-pro-nothinking']
                    },
                    gemini: {
                        label: 'Google Gemini',
                        configured: false,
                        model: localStorage.getItem('default_gemini_module') || 'gemini-2.5-flash',
                        models: ['gemini-3-flash-preview', 'gemini-2.5-flash', 'gemini-2.0-flash-exp'],
                        keys_count: 0
                    }
                }
            };
            syncDrawingModelSelect();
            if (allDOMElements.aiModelSummary) {
                allDOMElements.aiModelSummary.innerHTML = `<span class="text-amber-300">Không đọc được cấu hình server:</span> ${error.message}`;
            }
        }
    }

    function updateDrawingAiSummary() {
        const provider = allDOMElements.aiProviderSelect?.value || drawingAiConfig?.default_provider || 'ds2api';
        const ds2 = drawingAiConfig?.providers?.ds2api || {};
        const gemini = drawingAiConfig?.providers?.gemini || {};
        const currentModel = getCurrentDrawingModel(provider);
        if (allDOMElements.aiProviderSelect) {
            const ds2Option = allDOMElements.aiProviderSelect.querySelector('option[value="ds2api"]');
            const geminiOption = allDOMElements.aiProviderSelect.querySelector('option[value="gemini"]');
            if (ds2Option) ds2Option.textContent = `DeepSeek / DS2API · ${ds2.model || 'deepseek-v4-flash'}${ds2.configured ? '' : ' (chưa cấu hình)'}`;
            if (geminiOption) geminiOption.textContent = `Google Gemini · ${gemini.model || 'gemini-2.5-flash'}${gemini.configured ? '' : ' (chưa cấu hình)'}`;
        }
        if (!allDOMElements.aiModelSummary) return;
        const selected = provider === 'gemini' ? gemini : ds2;
        const supportsImage = selected.supports_image ? 'có hỗ trợ ảnh' : 'chỉ mô tả chữ';
        const readyText = selected.configured ? 'Đã cấu hình' : 'Chưa cấu hình';
        const extra = provider === 'gemini'
            ? ` · ${gemini.keys_count || 0} key`
            : ' · dùng Client Key DS2API trên server';
        allDOMElements.aiModelSummary.innerHTML = `
            <div><strong>${selected.label || provider}</strong>: <code>${currentModel || selected.model || '---'}</code></div>
            <div>${readyText}${extra} · ${supportsImage}</div>
        `;
    }

    function loadApiKeys() {
        // Prioritize System Keys
        const systemKeys = localStorage.getItem('global_gemini_keys');
        if (systemKeys) {
            try {
                const keys = JSON.parse(systemKeys);
                if (keys.length > 0) {
                    apiKeysFromFile = keys;
                    allDOMElements.apiKeyFilename.textContent = `Đã tải ${keys.length} khóa từ Hệ thống.`;
                    allDOMElements.apiKeyFilename.classList.remove('text-red-400');
                    allDOMElements.apiKeyFilename.classList.add('text-green-400');
                }
            } catch (e) { console.error("Error parsing system keys", e); }
        } else {
            // Fallback to local keys (from file upload)
            const storedKeys = localStorage.getItem('geometryAiApiKeys');
            if (storedKeys) {
                apiKeysFromFile = JSON.parse(storedKeys);
                if (apiKeysFromFile.length > 0) {
                    allDOMElements.apiKeyFilename.textContent = `Đã tải ${apiKeysFromFile.length} khóa (Local).`;
                    allDOMElements.apiKeyFilename.classList.add('text-green-400');
                }
            }
        }
    }
    loadDrawingAiConfig().finally(loadApiKeys);

    allDOMElements.aiProviderSelect?.addEventListener('change', () => {
        localStorage.setItem(VEHINH_PROVIDER_STORAGE_KEY, allDOMElements.aiProviderSelect.value);
        syncDrawingModelSelect();
        updateDrawingAiSummary();
    });
    allDOMElements.aiModelSelect?.addEventListener('change', () => {
        const provider = allDOMElements.aiProviderSelect?.value || drawingAiConfig?.default_provider || 'ds2api';
        localStorage.setItem(`${VEHINH_MODEL_STORAGE_PREFIX}${provider}`, allDOMElements.aiModelSelect.value || '');
        updateDrawingAiSummary();
    });

    allDOMElements.apiKeyFile.addEventListener('change', (e) => { const file = e.target.files[0]; if (file) { const reader = new FileReader(); reader.onload = (event) => { const keys = event.target.result.trim().split('\n').filter(key => key.trim() !== ''); apiKeysFromFile = keys; allDOMElements.apiKeyFilename.classList.remove('text-green-400', 'text-red-400'); if (keys.length > 0) { localStorage.setItem('geometryAiApiKeys', JSON.stringify(keys)); allDOMElements.apiKeyFilename.textContent = `Đã lưu ${keys.length} khóa.`; allDOMElements.apiKeyFilename.classList.add('text-green-400'); } else { allDOMElements.apiKeyFilename.textContent = `Tệp không hợp lệ.`; allDOMElements.apiKeyFilename.classList.add('text-red-400'); } }; reader.readAsText(file); } });
    allDOMElements.promptInput.addEventListener('paste', handlePaste);
    window.addEventListener('resize', () => { canvas.setWidth(canvasContainer.clientWidth); canvas.setHeight(canvasContainer.clientHeight); if (isGridVisible) drawGrid(); canvas.renderAll(); });
    allDOMElements.imageUpload.addEventListener('change', (e) => { const file = e.target.files[0]; if (file) { activeImageFile = file; const reader = new FileReader(); reader.onload = (event) => { allDOMElements.imagePreview.src = event.target.result; allDOMElements.imagePreview.classList.remove('hidden'); }; reader.readAsDataURL(file); } });
    allDOMElements.generateBtn.addEventListener('click', () => handleGenerateClick(false));
    allDOMElements.regenerateBtn.addEventListener('click', () => handleGenerateClick(true));
    allDOMElements.deleteBtn.addEventListener('click', () => { const activeObjects = canvas.getActiveObjects(); if (activeObjects.length) { activeObjects.forEach(obj => { if (!isAiLocked || (obj.source !== 'ai' && obj.source !== 'ai_primitive')) { canvas.remove(obj); } }); canvas.discardActiveObject().renderAll(); } });
    allDOMElements.lockAiBtn.addEventListener('click', () => { isAiLocked = !isAiLocked; applyAiLockState(); });
    allDOMElements.accordionHeaders.forEach(header => { header.addEventListener('click', () => { const content = header.nextElementSibling; header.classList.toggle('active'); content.classList.toggle('active'); }); });
    allDOMElements.geogebraToggle.addEventListener('click', () => { allDOMElements.geogebraContainer.classList.toggle('hidden'); allDOMElements.geogebraToggle.querySelector('i').classList.toggle('rotate-180'); });

    async function copy() { const activeObject = canvas.getActiveObject(); if (!activeObject) return; activeObject.clone(cloned => _clipboard = cloned, ['source']); try { const dataUrl = activeObject.toDataURL({ format: 'png', quality: 1, multiplier: 2 }); const blob = await (await fetch(dataUrl)).blob(); await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]); } catch (err) { console.error('Sao chép ảnh thất bại.', err); } }
    function paste() { if (!_clipboard) return; _clipboard.clone(clonedObj => { canvas.discardActiveObject(); clonedObj.set({ left: clonedObj.left + 15, top: clonedObj.top + 15, evented: true, source: 'user' }); if (clonedObj.type === 'activeSelection') { clonedObj.canvas = canvas; clonedObj.forEachObject(obj => canvas.add(obj)); clonedObj.setCoords(); } else { canvas.add(clonedObj); } _clipboard.top += 15; _clipboard.left += 15; canvas.setActiveObject(clonedObj); canvas.requestRenderAll(); }); }
    function handlePaste(e) { const items = e.clipboardData.items; for (let i = 0; i < items.length; i++) { if (items[i].kind === 'file' && items[i].type.startsWith('image/')) { e.preventDefault(); const imageFile = items[i].getAsFile(); activeImageFile = imageFile; allDOMElements.imageUpload.value = ''; const reader = new FileReader(); reader.onload = (event) => { allDOMElements.imagePreview.src = event.target.result; allDOMElements.imagePreview.classList.remove('hidden'); }; reader.readAsDataURL(imageFile); break; } } }
    document.addEventListener('keydown', (e) => { const activeEl = document.activeElement; const isInputFocused = activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA' || (canvas.getActiveObject() && canvas.getActiveObject().isEditing); const activeObj = canvas.getActiveObject(); if ((e.ctrlKey || e.metaKey) && activeObj && activeObj.type === 'i-text' && !isInputFocused) { switch (e.key.toLowerCase()) { case 'b': e.preventDefault(); allDOMElements.fontBold.click(); break; case 'i': e.preventDefault(); allDOMElements.fontItalic.click(); break; case 'u': e.preventDefault(); allDOMElements.fontUnderline.click(); break; } } if (isInputFocused) return; if (e.key === 'Delete' || e.key === 'Backspace') allDOMElements.deleteBtn.click(); if (e.key === 'Escape') { e.preventDefault(); canvas.discardActiveObject().renderAll(); resetDrawingState(); } if (e.ctrlKey || e.metaKey) { switch (e.key.toLowerCase()) { case 'a': e.preventDefault(); selectAll(); break; case 'c': e.preventDefault(); copy(); break; case 'v': e.preventDefault(); paste(); break; case 'x': e.preventDefault(); if (canvas.getActiveObject()) { copy(); allDOMElements.deleteBtn.click(); } break; case 'z': e.preventDefault(); e.shiftKey ? redo() : undo(); break; case 'y': e.preventDefault(); redo(); break; case 'q': e.preventDefault(); allDOMElements.generateBtn.click(); break; } } });
    function selectAll() { const allObjects = canvas.getObjects().filter(obj => obj.selectable); if (allObjects.length) { const sel = new fabric.ActiveSelection(allObjects, { canvas: canvas }); canvas.setActiveObject(sel).requestRenderAll(); } }
    canvas.on('mouse:wheel', function (opt) { const delta = opt.e.deltaY; let zoom = canvas.getZoom(); zoom *= 0.999 ** delta; if (zoom > 20) zoom = 20; if (zoom < 0.01) zoom = 0.01; canvas.zoomToPoint({ x: opt.e.offsetX, y: opt.e.offsetY }, zoom); opt.e.preventDefault(); opt.e.stopPropagation(); });
    canvas.on('mouse:down', function (opt) { if (opt.e.altKey === true || opt.e.button === 1) { isPanning = true; this.selection = false; lastPanX = opt.e.clientX; lastPanY = opt.e.clientY; hideMiniToolbar(); } });
    canvas.on('mouse:move', function (opt) { if (isPanning) { const vpt = this.viewportTransform; vpt[4] += opt.e.clientX - lastPanX; vpt[5] += opt.e.clientY - lastPanY; this.requestRenderAll(); lastPanX = opt.e.clientX; lastPanY = opt.e.clientY; } });
    canvas.on('mouse:up', function () { if (isPanning) { this.setViewportTransform(this.viewportTransform); isPanning = false; this.selection = true; } });

    const AI_THROTTLE_STORAGE_KEY = 'giangbai_ai_last_request_at';

    async function waitForAiThrottle(minMs = 2000, maxMs = 3000) {
        const required = minMs + Math.floor(Math.random() * (maxMs - minMs + 1));
        const last = Number(localStorage.getItem(AI_THROTTLE_STORAGE_KEY) || 0);
        const elapsed = Date.now() - last;
        if (last > 0 && elapsed < required) {
            await new Promise(resolve => setTimeout(resolve, required - elapsed));
        }
        localStorage.setItem(AI_THROTTLE_STORAGE_KEY, String(Date.now()));
    }

    // === AI GENERATION LOGIC (UPDATED WITH PRIORITY & FALLBACK) ===
    async function handleGenerateClick(isRegenerating = false) {
        const userPrompt = allDOMElements.promptInput.value;
        const imageFile = activeImageFile;
        if (!userPrompt && !imageFile) { allDOMElements.analysisOutput.innerHTML = '<span class="text-red-400">Lỗi: Vui lòng nhập đề bài hoặc tải ảnh.</span>'; return; }
        const selectedProvider = allDOMElements.aiProviderSelect?.value || drawingAiConfig?.default_provider || 'ds2api';
        const selectedModel = allDOMElements.aiModelSelect?.value || getCurrentDrawingModel(selectedProvider) || '';
        if (selectedProvider === 'ds2api' && imageFile) {
            allDOMElements.analysisOutput.innerHTML = '<span class="text-amber-300">DeepSeek/DS2API hiện chỉ dùng cho mô tả chữ trên trang này. Nếu muốn AI đọc ảnh, hãy chọn Google Gemini.</span>';
            return;
        }

        allDOMElements.loader.classList.remove('hidden');
        allDOMElements.generateBtn.disabled = true; allDOMElements.regenerateBtn.disabled = true;
        allDOMElements.analysisOutput.innerHTML = `AI đang phân tích bằng ${selectedProvider === 'gemini' ? 'Gemini' : 'DeepSeek/DS2API'}${selectedModel ? ` · ${selectedModel}` : ''}...`;

        canvas.getObjects().slice().forEach(obj => { if (obj.source === 'ai' || obj.source === 'ai_primitive') { canvas.remove(obj); } });
        canvas.renderAll();

        const systemPrompt = `Bạn là một chuyên gia phân tích hình học, thống kê và lập trình viên JavaScript. Nhiệm vụ của bạn là nhận một mô tả hoặc hình ảnh và tạo ra mã JavaScript để vẽ lại hình học hoặc biểu đồ một cách SẠCH SẼ, RÕ NÉT, và CHÍNH XÁC bằng thư viện Fabric.js. PHẢN HỒI CỦA BẠN PHẢI CÓ 2 PHẦN: PHẦN 1: PHÂN TÍCH trong thẻ <analysis>...</analysis>. PHẦN 2: MÃ JAVASCRIPT trong thẻ <javascript>...</javascript>. A. QUY TẮC HÌNH HỌC: 1. Khai báo điểm trước: const diemA = {x: 150, y: 100}; 2. Dùng trực tiếp Fabric.js: new fabric.Circle(...). 3. Mọi đối tượng phải có selectable, hasControls, hasBorders, originX/Y 'center'. 4. Dùng hàm vẽ ký hiệu: addRightAngleSymbol(), addEqualityTick(), addAngleArc(). B. QUY TẮC BIỂU ĐỒ: 1. Dùng hàm chuyên dụng: drawBarChart(), drawPieChart(). 2. Định dạng data: [{ label: 'Tổ 1', value: 50 }, ...]. 3. ĐỂ IN ĐEN TRẮNG, LUÔN LUÔN đặt usePatterns: true trong options. Môi trường thực thi: KHÔNG khai báo lại biến 'canvas'. Cuối cùng phải gọi canvas.renderAll();`;
        let userInstruction = `Phân tích và vẽ hình cho yêu cầu sau: ${userPrompt}`;
        if (isRegenerating) { userInstruction += " Vui lòng vẽ lại hình này nhưng sử dụng các tọa độ và tỷ lệ khác với lần trước."; }
        try {
            await waitForAiThrottle();
            const imagePayload = imageFile
                ? { mime_type: imageFile.type, data: await imageToBase64(imageFile) }
                : null;
            const response = await fetch('api/vehinh_ai.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    provider: selectedProvider,
                    model: selectedModel,
                    system_prompt: systemPrompt,
                    user_instruction: userInstruction,
                    image: imagePayload,
                }),
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
                const err = new Error(data.error || 'AI vẽ hình không phản hồi.');
                err.code = data.code || '';
                throw err;
            }
            const fullResponseText = data.text || '';
            allDOMElements.analysisOutput.innerHTML = fullResponseText.replace(/\n/g, '<br>');
            executeAiCode(fullResponseText);
        } catch (error) {
            console.error('Lỗi AI vẽ hình:', error);
            allDOMElements.analysisOutput.innerHTML = `<span class="text-red-400">Lỗi AI vẽ hình:</span> ${error.message}`;
            allDOMElements.loader.classList.add('hidden');
            allDOMElements.generateBtn.disabled = false;
            allDOMElements.regenerateBtn.disabled = false;
        }
    }

    function executeAiCode(fullText) {
        const codeMatch = fullText.match(/<javascript>([\s\S]*?)<\/javascript>/); const codeText = codeMatch ? codeMatch[1].trim() : null;
        if (codeText) {
            try {
                isAiDrawing = true; canvas.renderOnAddRemove = false;
                const drawFunction = new Function('canvas', 'fabric', 'addRightAngleSymbol', 'addEqualityTick', 'addAngleArc', 'drawBarChart', 'drawPieChart', codeText);
                drawFunction(canvas, fabric, (...args) => addRightAngleSymbol(canvas, ...args), (...args) => addEqualityTick(canvas, ...args), (...args) => addAngleArc(canvas, ...args), (...args) => drawBarChart(canvas, ...args), (...args) => drawPieChart(canvas, ...args));
                canvas.getObjects().forEach(obj => { if (!obj.source) obj.set({ source: 'ai_primitive' }); if (obj.type === 'line' || obj.type === 'polyline' || obj.type === 'path') { obj.set({ objectCaching: false }); } });
                applyAiLockState(); sendPointsToFront();
            } catch (e) { const errorHtml = `<br><br><strong class="text-red-400">Lỗi thực thi mã vẽ:</strong> ${e.message}`; if (!allDOMElements.analysisOutput.innerHTML.includes(errorHtml)) { allDOMElements.analysisOutput.innerHTML += errorHtml; } } finally { canvas.renderOnAddRemove = true; canvas.renderAll(); isAiDrawing = false; saveHistory(); allDOMElements.loader.classList.add('hidden'); allDOMElements.generateBtn.disabled = false; allDOMElements.regenerateBtn.disabled = false; }
        } else { const warningHtml = `<br><br><strong class="text-yellow-400">Cảnh báo:</strong> Không tìm thấy mã JavaScript trong phản hồi của AI.`; if (!allDOMElements.analysisOutput.innerHTML.includes(warningHtml)) { allDOMElements.analysisOutput.innerHTML += warningHtml; } allDOMElements.loader.classList.add('hidden'); allDOMElements.generateBtn.disabled = false; allDOMElements.regenerateBtn.disabled = false; }
    }

    function resetDrawingState() { if (activeToolCleanup) { activeToolCleanup(); activeToolCleanup = null; } canvas.isDrawingMode = false; canvas.selection = true; canvas.defaultCursor = 'default'; document.querySelectorAll('.tool-btn').forEach(btn => btn.classList.remove('active')); document.querySelector('button[data-tool="select"]').classList.add('active'); }
    allDOMElements.toolbar.addEventListener('click', (e) => { const toolItem = e.target.closest('[data-tool]'); if (!toolItem) return; const tool = toolItem.dataset.tool; resetDrawingState(); currentTool = tool; toolItem.classList.add('active'); canvas.selection = (tool === 'select'); if (tool === 'pencil') { canvas.isDrawingMode = true; canvas.freeDrawingBrush.width = 2; canvas.freeDrawingBrush.color = allDOMElements.colorPicker.value; } else if (tool !== 'select') { canvas.defaultCursor = 'crosshair'; if (tool === 'line') activeToolCleanup = activateLineTool(canvas, allDOMElements.colorPicker); else if (tool === 'circle') activeToolCleanup = activateCircleTool(canvas, allDOMElements.colorPicker); else if (tool === 'text') activeToolCleanup = activateTextTool(canvas, allDOMElements.colorPicker); else if (tool === 'point') activeToolCleanup = activatePointTool(canvas, allDOMElements.colorPicker); } });
    allDOMElements.colorPicker.addEventListener('change', () => { const color = allDOMElements.colorPicker.value; if (canvas.isDrawingMode) canvas.freeDrawingBrush.color = color; const activeObj = canvas.getActiveObject(); if (activeObj) { if (activeObj.type === 'activeSelection') { activeObj.forEachObject(obj => setColorForObject(obj, color)); } else { setColorForObject(activeObj, color); } canvas.renderAll(); saveHistory(); } });

    function drawGrid() { if (gridGroup) canvas.remove(gridGroup); const lines = []; const zoom = canvas.getZoom(); const canvasWidth = canvas.getWidth() / zoom; const canvasHeight = canvas.getHeight() / zoom; const left = -(canvas.viewportTransform[4] / zoom); const top = -(canvas.viewportTransform[5] / zoom); for (let i = Math.floor(left / GRID_SIZE); i <= Math.ceil((left + canvasWidth) / GRID_SIZE); i++) { lines.push(new fabric.Line([i * GRID_SIZE, top, i * GRID_SIZE, top + canvasHeight], { stroke: GRID_COLOR, selectable: false, evented: false })); } for (let i = Math.floor(top / GRID_SIZE); i <= Math.ceil((top + canvasHeight) / GRID_SIZE); i++) { lines.push(new fabric.Line([left, i * GRID_SIZE, left + canvasWidth, i * GRID_SIZE], { stroke: GRID_COLOR, selectable: false, evented: false })); } gridGroup = new fabric.Group(lines, { selectable: false, evented: false, source: 'grid', excludeFromExport: true }); canvas.add(gridGroup); gridGroup.moveTo(-1); }
    allDOMElements.toggleGridBtn.addEventListener('click', () => { if (isGridVisible) { if (gridGroup) canvas.remove(gridGroup); gridGroup = null; allDOMElements.toggleGridBtn.classList.remove('active'); } else { drawGrid(); allDOMElements.toggleGridBtn.classList.add('active'); } isGridVisible = !isGridVisible; canvas.renderAll(); });
    canvas.on('viewport:transformed', () => { if (isGridVisible) drawGrid(); hideMiniToolbar(); });

    allDOMElements.insertImageBtn.addEventListener('click', () => allDOMElements.imageInserter.click());
    allDOMElements.imageInserter.addEventListener('change', (e) => { const file = e.target.files[0]; if (!file) return; const reader = new FileReader(); reader.onload = (f) => { fabric.Image.fromURL(f.target.result, (img) => { img.set({ left: canvas.getCenter().left, top: canvas.getCenter().top, originX: 'center', originY: 'center', source: 'user' }); img.scaleToWidth(canvas.getWidth() * 0.5); canvas.add(img); canvas.setActiveObject(img); canvas.renderAll(); sendPointsToFront(); }); }; reader.readAsDataURL(file); e.target.value = ''; });
    function openLatexModal() { allDOMElements.latexModal.classList.remove('hidden'); allDOMElements.latexModalBackdrop.classList.remove('hidden'); if (!mathField) { const MQ = MathQuill.getInterface(2); mathField = MQ.MathField(allDOMElements.mathInput, { spaceBehavavesLikeTab: true, handlers: { edit: () => updateLatexPreview() } }); } mathField.focus(); updateLatexPreview(); }
    function closeLatexModal() { allDOMElements.latexModal.classList.add('hidden'); allDOMElements.latexModalBackdrop.classList.add('hidden'); }
    function updateLatexPreview() { const latexString = mathField ? mathField.latex() : ''; try { katex.render(latexString, allDOMElements.latexPreview, { throwOnError: false, displayMode: true, output: 'html' }); } catch (e) { allDOMElements.latexPreview.textContent = e.message; } }
    allDOMElements.latexToolBtn.addEventListener('click', openLatexModal); allDOMElements.cancelLatexBtn.addEventListener('click', closeLatexModal); allDOMElements.latexModalBackdrop.addEventListener('click', closeLatexModal);
    allDOMElements.insertLatexBtn.addEventListener('click', async () => { if (!mathField || mathField.latex().trim() === '') { closeLatexModal(); return; } const originalColor = allDOMElements.latexPreview.style.color; allDOMElements.latexPreview.style.color = allDOMElements.colorPicker.value; try { const formulaCanvas = await html2canvas(allDOMElements.latexPreview, { backgroundColor: null, scale: 3 }); fabric.Image.fromURL(formulaCanvas.toDataURL('image/png'), (img) => { img.set({ left: canvas.getCenter().left, top: canvas.getCenter().top, originX: 'center', originY: 'center', source: 'user' }); canvas.add(img); canvas.setActiveObject(img); canvas.renderAll(); sendPointsToFront(); closeLatexModal(); }); } catch (error) { console.error('Error generating image from LaTeX:', error); } finally { allDOMElements.latexPreview.style.color = originalColor; } });
    function imageToBase64(file) { return new Promise((resolve, reject) => { const reader = new FileReader(); reader.readAsDataURL(file); reader.onload = () => resolve(reader.result.split(',')[1]); reader.onerror = error => reject(error); }); }

    const suggestionMap = { "Tam giác ABC vuông tại A": "Vẽ tam giác ABC vuông tại A, có đường cao AH. Ký hiệu góc vuông và đánh dấu hai đoạn BH và HC bằng nhau.", "Hình thang ABCD": "Vẽ hình thang ABCD (AB song song CD) có hai đường chéo AC và BD cắt nhau tại O.", "Biểu đồ tròn 3 loại": "Vẽ biểu đồ hình tròn thể hiện tỉ lệ học sinh Giỏi, Khá, Trung bình lần lượt là 20, 50, 30.", "Biểu đồ cột có pattern": "Vẽ biểu đồ cột so sánh sản lượng lúa của 3 miền Bắc, Trung, Nam lần lượt là 300, 250, 500 tấn. Dùng pattern để dễ in đen trắng." };
    allDOMElements.promptSuggestions.addEventListener('click', (e) => { if (e.target.classList.contains('suggestion-btn')) { const key = e.target.textContent; allDOMElements.promptInput.value = suggestionMap[key] || key; allDOMElements.promptInput.focus(); } });
    allDOMElements.toggleSnapBtn.addEventListener('click', () => { isSnapEnabled = !isSnapEnabled; allDOMElements.toggleSnapBtn.classList.toggle('active', isSnapEnabled); });
    function snapObject(target) { if (!target) return; target.set({ left: Math.round(target.left / GRID_SIZE) * GRID_SIZE, top: Math.round(target.top / GRID_SIZE) * GRID_SIZE }); }
    function alignObjects(direction) { const activeSelection = canvas.getActiveObject(); if (!activeSelection || activeSelection.type !== 'activeSelection') return; const selectionBox = activeSelection.getBoundingRect(); const objects = activeSelection.getObjects(); objects.forEach(obj => { const objBox = obj.getBoundingRect(); switch (direction) { case 'left': obj.set({ left: selectionBox.left + objBox.width / 2 }); break; case 'center-h': obj.set({ left: selectionBox.left + selectionBox.width / 2 }); break; case 'right': obj.set({ left: selectionBox.left + selectionBox.width - objBox.width / 2 }); break; case 'top': obj.set({ top: selectionBox.top + objBox.height / 2 }); break; case 'center-v': obj.set({ top: selectionBox.top + selectionBox.height / 2 }); break; case 'bottom': obj.set({ top: selectionBox.top + selectionBox.height - objBox.height / 2 }); break; } obj.setCoords(); }); canvas.renderAll(); saveHistory(); }
    document.getElementById('align-left').addEventListener('click', () => alignObjects('left')); document.getElementById('align-center-h').addEventListener('click', () => alignObjects('center-h')); document.getElementById('align-right').addEventListener('click', () => alignObjects('right')); document.getElementById('align-top').addEventListener('click', () => alignObjects('top')); document.getElementById('align-center-v').addEventListener('click', () => alignObjects('center-v')); document.getElementById('align-bottom').addEventListener('click', () => alignObjects('bottom'));
    function applyDarkMode(isDark) { const html = document.documentElement; const moonIcon = allDOMElements.darkModeToggle.querySelector('[data-lucide="moon"]'); const sunIcon = allDOMElements.darkModeToggle.querySelector('[data-lucide="sun"]'); if (isDark) { html.classList.add('dark'); moonIcon.classList.add('hidden'); sunIcon.classList.remove('hidden'); canvas.backgroundColor = '#374151'; } else { html.classList.remove('dark'); moonIcon.classList.remove('hidden'); sunIcon.classList.add('hidden'); canvas.backgroundColor = '#fff'; } canvas.renderAll(); }
    allDOMElements.darkModeToggle.addEventListener('click', () => { const isDark = !document.documentElement.classList.contains('dark'); localStorage.setItem('darkMode', isDark); applyDarkMode(isDark); });
    if (localStorage.getItem('darkMode') === 'true' || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches && localStorage.getItem('darkMode') === null)) { applyDarkMode(true); }
});
