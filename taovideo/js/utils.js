/**
 * Utility functions for AI Video Studio
 */

const Utils = {
    /**
     * Format seconds to MM:SS or MM:SS.m format
     */
    formatTime(seconds) {
        if (isNaN(seconds) || seconds < 0) seconds = 0;
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },

    /**
     * Convert File or Blob to Data URL
     */
    fileToDataURL(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    },

    /**
     * Convert File to ArrayBuffer
     */
    fileToArrayBuffer(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsArrayBuffer(file);
        });
    },

    /**
     * Load an image from URL or DataURL and return HTMLImageElement
     */
    loadImage(src) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.crossOrigin = 'anonymous';
            img.onload = () => resolve(img);
            img.onerror = (err) => reject(new Error('Failed to load image: ' + err));
            img.src = src;
        });
    },

    /**
     * Easing functions for smooth animations
     */
    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    },

    easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    },

    easeOutBack(t) {
        const c1 = 1.70158;
        const c3 = c1 + 1;
        return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
    },

    easeOutBounce(t) {
        const n1 = 7.5625;
        const d1 = 2.75;
        let x = t;
        if (x < 1 / d1) {
            return n1 * x * x;
        } else if (x < 2 / d1) {
            return n1 * (x -= 1.5 / d1) * x + 0.75;
        } else if (x < 2.5 / d1) {
            return n1 * (x -= 2.25 / d1) * x + 0.9375;
        } else {
            return n1 * (x -= 2.625 / d1) * x + 0.984375;
        }
    },

    /**
     * Draw image fitted/covered inside canvas rectangle
     */
    drawImageCover(ctx, img, x, y, w, h, scale = 1, offsetX = 0, offsetY = 0) {
        if (!img || !img.width) return;
        const imgRatio = img.width / img.height;
        const targetRatio = w / h;
        let sWidth, sHeight, sx, sy;

        if (imgRatio > targetRatio) {
            sHeight = img.height;
            sWidth = img.height * targetRatio;
            sx = (img.width - sWidth) / 2;
            sy = 0;
        } else {
            sWidth = img.width;
            sHeight = img.width / targetRatio;
            sx = 0;
            sy = (img.height - sHeight) / 2;
        }

        ctx.save();
        // Center zoom transform
        ctx.translate(x + w / 2 + offsetX, y + h / 2 + offsetY);
        ctx.scale(scale, scale);
        ctx.drawImage(img, sx, sy, sWidth, sHeight, -w / 2, -h / 2, w, h);
        ctx.restore();
    },

    /**
     * Draw Ken Burns Motion effect
     * @param {CanvasRenderingContext2D} ctx
     * @param {HTMLImageElement} img
     * @param {number} progress 0.0 to 1.0
     * @param {number} canvasW
     * @param {number} canvasH
     * @param {string} motion 'zoom-in', 'zoom-out', 'pan-left', 'pan-right'
     */
    drawKenBurns(ctx, img, progress, canvasW, canvasH, motion = 'kenburns') {
        let scale = 1.0;
        let offX = 0;
        let offY = 0;
        let rotation = 0;
        let alpha = 1;

        const p = this.easeInOutQuad(progress);

        switch (motion) {
            case 'zoom-in':
            case 'kenburns':
                scale = 1.0 + p * 0.12; // 1.0 -> 1.12
                offX = Math.sin(p * Math.PI) * (canvasW * 0.015);
                offY = p * (canvasH * 0.02);
                break;
            case 'zoom-out':
                scale = 1.12 - p * 0.12;
                offX = Math.cos(p * Math.PI) * (canvasW * 0.015);
                break;
            case 'pan-left':
                scale = 1.08;
                offX = (1 - p * 2) * (canvasW * 0.04);
                break;
            case 'pan-right':
                scale = 1.08;
                offX = (p * 2 - 1) * (canvasW * 0.04);
                break;
            case 'pan-up': scale = 1.08; offY = (1 - p * 2) * canvasH * 0.04; break;
            case 'pan-down': scale = 1.08; offY = (p * 2 - 1) * canvasH * 0.04; break;
            case 'diagonal-tl': scale = 1.11; offX = (1 - p * 2) * canvasW * 0.04; offY = (1 - p * 2) * canvasH * 0.04; break;
            case 'diagonal-tr': scale = 1.11; offX = (p * 2 - 1) * canvasW * 0.04; offY = (1 - p * 2) * canvasH * 0.04; break;
            case 'diagonal-bl': scale = 1.11; offX = (1 - p * 2) * canvasW * 0.04; offY = (p * 2 - 1) * canvasH * 0.04; break;
            case 'diagonal-br': scale = 1.11; offX = (p * 2 - 1) * canvasW * 0.04; offY = (p * 2 - 1) * canvasH * 0.04; break;
            case 'zoom-pan-left': scale = 1.04 + p * 0.14; offX = (1 - p * 2) * canvasW * 0.035; break;
            case 'zoom-pan-right': scale = 1.04 + p * 0.14; offX = (p * 2 - 1) * canvasW * 0.035; break;
            case 'zoom-pan-up': scale = 1.04 + p * 0.14; offY = (1 - p * 2) * canvasH * 0.035; break;
            case 'zoom-pan-down': scale = 1.04 + p * 0.14; offY = (p * 2 - 1) * canvasH * 0.035; break;
            case 'drift-left': scale = 1.13; offX = Math.sin(p * Math.PI) * canvasW * 0.055 - canvasW * 0.025; offY = Math.cos(p * Math.PI) * canvasH * 0.018; break;
            case 'drift-right': scale = 1.13; offX = canvasW * 0.025 - Math.sin(p * Math.PI) * canvasW * 0.055; offY = -Math.cos(p * Math.PI) * canvasH * 0.018; break;
            case 'drift-up': scale = 1.13; offY = Math.sin(p * Math.PI) * canvasH * 0.055 - canvasH * 0.025; offX = Math.cos(p * Math.PI) * canvasW * 0.018; break;
            case 'drift-down': scale = 1.13; offY = canvasH * 0.025 - Math.sin(p * Math.PI) * canvasH * 0.055; offX = -Math.cos(p * Math.PI) * canvasW * 0.018; break;
            case 'pulse': scale = 1.05 + Math.sin(p * Math.PI) * 0.07; break;
            case 'breathe': scale = 1.09 + Math.sin(p * Math.PI * 2) * 0.025; break;
            case 'rotate-left': scale = 1.16; rotation = -0.018 + p * 0.036; break;
            case 'rotate-right': scale = 1.16; rotation = 0.018 - p * 0.036; break;
            case 'tilt-left': scale = 1.16; rotation = -0.03 * p; offX = -p * canvasW * 0.025; break;
            case 'tilt-right': scale = 1.16; rotation = 0.03 * p; offX = p * canvasW * 0.025; break;
            case 'orbit-left': scale = 1.13; offX = Math.cos(p * Math.PI) * canvasW * 0.035; offY = Math.sin(p * Math.PI) * canvasH * 0.03; rotation = -0.012; break;
            case 'orbit-right': scale = 1.13; offX = -Math.cos(p * Math.PI) * canvasW * 0.035; offY = Math.sin(p * Math.PI) * canvasH * 0.03; rotation = 0.012; break;
            case 'push-in': scale = 1.0 + p * 0.2; alpha = 0.92 + p * 0.08; break;
            case 'pull-back': scale = 1.2 - p * 0.2; alpha = 1 - p * 0.08; break;
            case 'cinematic-left': scale = 1.15; offX = (1 - p * 2) * canvasW * 0.05; offY = p * canvasH * 0.018; break;
            case 'cinematic-right': scale = 1.15; offX = (p * 2 - 1) * canvasW * 0.05; offY = -p * canvasH * 0.018; break;
            case 'sweep-top': scale = 1.14; offY = (1 - p * 2) * canvasH * 0.055; rotation = 0.012; break;
            case 'sweep-bottom': scale = 1.14; offY = (p * 2 - 1) * canvasH * 0.055; rotation = -0.012; break;
            case 'none':
            default:
                scale = 1.0;
                offX = 0;
                offY = 0;
                break;
        }

        ctx.save();
        ctx.globalAlpha = alpha;
        if (rotation) {
            ctx.translate(canvasW / 2, canvasH / 2);
            ctx.rotate(rotation);
            ctx.translate(-canvasW / 2, -canvasH / 2);
        }
        this.drawImageCover(ctx, img, 0, 0, canvasW, canvasH, scale, offX, offY);
        ctx.restore();
    },

    /**
     * Render seamless transition between two slides
     * Supports: crossfade, fade-black, fade-white, slide-left, slide-right, slide-up, slide-down, wipe-left, wipe-right, circle-reveal, zoom-cross
     */
    drawTransition(ctx, slide1, slide2, slide1Progress, transProgress, w, h, transitionType = 'crossfade') {
        if (!slide1 || !slide1.imageElement) return;
        const p = this.easeInOutCubic(Math.max(0, Math.min(1, transProgress)));
        const type = transitionType || 'crossfade';
        const motion1 = slide1.motion || slide1.transition || 'none';
        const motion2 = slide2?.motion || slide2?.transition || 'none';

        if (!slide2 || !slide2.imageElement || type === 'none') {
            this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, motion1);
            return;
        }

        switch (type) {
            case 'fade-black': {
                if (p < 0.5) {
                    const alpha = 1 - (p * 2);
                    ctx.save();
                    ctx.globalAlpha = alpha;
                    this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, motion1);
                    ctx.restore();
                } else {
                    const alpha = (p - 0.5) * 2;
                    ctx.save();
                    ctx.globalAlpha = alpha;
                    this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, motion2);
                    ctx.restore();
                }
                break;
            }
            case 'fade-white': {
                if (p < 0.5) {
                    this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, motion1);
                    ctx.fillStyle = `rgba(255, 255, 255, ${p * 2})`;
                    ctx.fillRect(0, 0, w, h);
                } else {
                    this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, motion2);
                    ctx.fillStyle = `rgba(255, 255, 255, ${(1 - p) * 2})`;
                    ctx.fillRect(0, 0, w, h);
                }
                break;
            }
            case 'slide-left':
            case 'slide': {
                ctx.save();
                ctx.translate(-p * w, 0);
                this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, 'none');
                ctx.restore();

                ctx.save();
                ctx.translate((1 - p) * w, 0);
                this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, 'none');
                ctx.restore();
                break;
            }
            case 'slide-right': {
                ctx.save();
                ctx.translate(p * w, 0);
                this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, 'none');
                ctx.restore();

                ctx.save();
                ctx.translate(-(1 - p) * w, 0);
                this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, 'none');
                ctx.restore();
                break;
            }
            case 'slide-up': {
                ctx.save();
                ctx.translate(0, -p * h);
                this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, 'none');
                ctx.restore();

                ctx.save();
                ctx.translate(0, (1 - p) * h);
                this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, 'none');
                ctx.restore();
                break;
            }
            case 'slide-down': {
                ctx.save();
                ctx.translate(0, p * h);
                this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, 'none');
                ctx.restore();

                ctx.save();
                ctx.translate(0, -(1 - p) * h);
                this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, 'none');
                ctx.restore();
                break;
            }
            case 'wipe-left': {
                this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, motion1);
                ctx.save();
                ctx.beginPath();
                ctx.rect(w * (1 - p), 0, w * p, h);
                ctx.clip();
                this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, motion2);
                ctx.restore();
                break;
            }
            case 'wipe-right': {
                this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, motion1);
                ctx.save();
                ctx.beginPath();
                ctx.rect(0, 0, w * p, h);
                ctx.clip();
                this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, motion2);
                ctx.restore();
                break;
            }
            case 'circle-reveal': {
                this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, motion1);
                ctx.save();
                ctx.beginPath();
                const maxRadius = Math.hypot(w / 2, h / 2);
                ctx.arc(w / 2, h / 2, p * maxRadius, 0, Math.PI * 2);
                ctx.clip();
                this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, motion2);
                ctx.restore();
                break;
            }
            case 'zoom-cross': {
                ctx.save();
                ctx.globalAlpha = 1 - p;
                const scale1 = 1.0 + p * 0.25;
                ctx.translate(w / 2, h / 2);
                ctx.scale(scale1, scale1);
                ctx.translate(-w / 2, -h / 2);
                this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, 'none');
                ctx.restore();

                ctx.save();
                ctx.globalAlpha = p;
                const scale2 = 0.75 + p * 0.25;
                ctx.translate(w / 2, h / 2);
                ctx.scale(scale2, scale2);
                ctx.translate(-w / 2, -h / 2);
                this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, 'none');
                ctx.restore();
                break;
            }
            case 'crossfade':
            default: {
                this.drawKenBurns(ctx, slide1.imageElement, slide1Progress, w, h, motion1);
                ctx.save();
                ctx.globalAlpha = p;
                this.drawKenBurns(ctx, slide2.imageElement, 0, w, h, motion2);
                ctx.restore();
                break;
            }
        }
    },

    /**
     * Render rich text / captions / overlays on a slide
     * Completely deterministic based on localTime & duration
     */
    drawTextOverlay(ctx, overlay, defaultText, localTime, duration, canvasW, canvasH) {
        if (!overlay && !defaultText) return;
        if (overlay && overlay.enabled === false) return;

        const text = (overlay && overlay.text !== undefined && overlay.text !== null) ? overlay.text : (defaultText || '');
        if (!text || !text.trim()) return;

        const scale = canvasH / 1080;
        const fontFamily = overlay?.fontFamily || 'Be Vietnam Pro';
        const rawFontSize = overlay?.fontSize || 46;
        const fontSize = Math.max(16, Math.round(rawFontSize * scale));
        const textColor = overlay?.color || '#ffffff';
        const bgStyle = overlay?.bgStyle || 'pill'; // none, pill, shadow, neon, highlight, gradient-banner, boxed-border
        const bgColor = overlay?.bgColor || '#000000';
        const animation = overlay?.animation || 'fade';
        const position = overlay?.position || 'bottom-center';
        const customX = overlay?.customX ?? 50;
        const customY = overlay?.customY ?? 85;

        let textAlign = overlay?.textAlign;
        if (!textAlign) {
            if (position.includes('left')) textAlign = 'left';
            else if (position.includes('right')) textAlign = 'right';
            else textAlign = 'center';
        }

        // Target coordinates
        let targetX = canvasW * 0.5;
        let targetY = canvasH * 0.85;

        if (position === 'custom') {
            targetX = canvasW * (customX / 100);
            targetY = canvasH * (customY / 100);
        } else {
            switch (position) {
                case 'top-left': targetX = canvasW * 0.08; targetY = canvasH * 0.12; break;
                case 'top-center':
                case 'top': targetX = canvasW * 0.5; targetY = canvasH * 0.12; break;
                case 'top-right': targetX = canvasW * 0.92; targetY = canvasH * 0.12; break;
                case 'mid-left': targetX = canvasW * 0.08; targetY = canvasH * 0.5; break;
                case 'center': targetX = canvasW * 0.5; targetY = canvasH * 0.5; break;
                case 'mid-right': targetX = canvasW * 0.92; targetY = canvasH * 0.5; break;
                case 'bottom-left': targetX = canvasW * 0.08; targetY = canvasH * 0.85; break;
                case 'bottom-center':
                case 'bottom': targetX = canvasW * 0.5; targetY = canvasH * 0.85; break;
                case 'bottom-right': targetX = canvasW * 0.92; targetY = canvasH * 0.85; break;
            }
        }

        // Font & Wrapping
        ctx.save();
        ctx.font = `600 ${fontSize}px "${fontFamily}", "Be Vietnam Pro", sans-serif`;

        const maxLineW = Math.min(canvasW * 0.84, 1600 * scale);
        const hardLines = text.split('\n');
        const lines = [];

        for (const hLine of hardLines) {
            const trimmed = hLine.trim();
            if (!trimmed) {
                lines.push('');
                continue;
            }
            const words = trimmed.split(/\s+/);
            let cur = '';
            for (let i = 0; i < words.length; i++) {
                const test = cur ? cur + ' ' + words[i] : words[i];
                const w = ctx.measureText(test).width;
                if (w > maxLineW && cur) {
                    lines.push(cur);
                    cur = words[i];
                } else {
                    cur = test;
                }
            }
            if (cur) lines.push(cur);
        }

        if (lines.length === 0) {
            ctx.restore();
            return;
        }

        // Animation timing calculations
        const dur = Math.max(0.1, duration);
        const t = Math.max(0, Math.min(dur, localTime));
        const inDur = Math.min(0.65, dur * 0.35);
        const inProg = Math.max(0, Math.min(1, t / inDur));

        let exitAlpha = 1;
        if (dur - t < 0.22) {
            exitAlpha = Math.max(0, (dur - t) / 0.22);
        }

        let animAlpha = 1;
        let animOffsetX = 0;
        let animOffsetY = 0;
        let animScale = 1;
        let animCharCount = Infinity;
        let animGlowBlur = 0;
        let isKaraoke = (animation === 'karaoke');
        let karaokeProgress = Math.max(0, Math.min(1, t / (dur * 0.88)));

        switch (animation) {
            case 'static':
                animAlpha = 1;
                break;
            case 'fade':
                animAlpha = this.easeInOutQuad(inProg);
                break;
            case 'slide-up':
                animAlpha = inProg;
                animOffsetY = (1 - this.easeInOutQuad(inProg)) * 45 * scale;
                break;
            case 'slide-down':
                animAlpha = inProg;
                animOffsetY = -(1 - this.easeInOutQuad(inProg)) * 45 * scale;
                break;
            case 'slide-left':
                animAlpha = inProg;
                animOffsetX = (1 - this.easeInOutQuad(inProg)) * 60 * scale;
                break;
            case 'typewriter':
                animAlpha = 1;
                const totalCleanChars = text.replace(/\n/g, '').length;
                const typeProg = Math.max(0, Math.min(1, t / (dur * 0.7)));
                animCharCount = Math.floor(typeProg * totalCleanChars);
                break;
            case 'pop':
                animScale = 0.2 + 0.8 * this.easeOutBack(inProg);
                animAlpha = Math.min(1, inProg * 2);
                break;
            case 'bounce':
                animOffsetY = -(1 - this.easeOutBounce(inProg)) * 75 * scale;
                animAlpha = Math.min(1, inProg * 2);
                break;
            case 'glow':
                animAlpha = inProg;
                animGlowBlur = 12 + Math.sin(t * 6) * 8;
                break;
            case 'karaoke':
                animAlpha = this.easeInOutQuad(inProg);
                break;
        }

        animAlpha *= exitAlpha;
        if (animAlpha <= 0) {
            ctx.restore();
            return;
        }

        const lineHeight = fontSize * 1.35;
        const totalHeight = lines.length * lineHeight;

        ctx.globalAlpha = animAlpha;
        ctx.translate(targetX + animOffsetX, targetY + animOffsetY);
        if (animScale !== 1) {
            ctx.scale(animScale, animScale);
        }

        // Measure line metrics
        let maxLineWidth = 0;
        const measuredLines = lines.map(line => {
            const width = ctx.measureText(line).width;
            if (width > maxLineWidth) maxLineWidth = width;
            return { text: line, width };
        });

        // Determine starting Y offset
        const startY = -totalHeight / 2 + lineHeight / 2;

        // Render Background Styles
        if (bgStyle === 'gradient-banner') {
            const bannerH = totalHeight + fontSize * 1.2;
            const grad = ctx.createLinearGradient(-canvasW / 2, 0, canvasW / 2, 0);
            grad.addColorStop(0, 'rgba(15, 23, 42, 0)');
            grad.addColorStop(0.15, 'rgba(15, 23, 42, 0.88)');
            grad.addColorStop(0.5, 'rgba(15, 23, 42, 0.95)');
            grad.addColorStop(0.85, 'rgba(15, 23, 42, 0.88)');
            grad.addColorStop(1, 'rgba(15, 23, 42, 0)');
            ctx.fillStyle = grad;
            ctx.fillRect(-canvasW / 2, -bannerH / 2, canvasW, bannerH);

            ctx.fillStyle = 'rgba(139, 92, 246, 0.5)';
            ctx.fillRect(-canvasW * 0.4, -bannerH / 2, canvasW * 0.8, 2 * scale);
            ctx.fillRect(-canvasW * 0.4, bannerH / 2 - 2 * scale, canvasW * 0.8, 2 * scale);
        } else if (bgStyle === 'boxed-border') {
            const padX = fontSize * 0.8;
            const padY = fontSize * 0.4;
            const boxW = maxLineWidth + padX * 2;
            const boxH = totalHeight + padY * 2;

            let boxX = -boxW / 2;
            if (textAlign === 'left') boxX = -padX;
            else if (textAlign === 'right') boxX = -maxLineWidth - padX;

            ctx.fillStyle = 'rgba(15, 23, 42, 0.82)';
            ctx.beginPath();
            ctx.roundRect(boxX, -boxH / 2, boxW, boxH, fontSize * 0.3);
            ctx.fill();

            ctx.strokeStyle = textColor || '#8b5cf6';
            ctx.lineWidth = 2.5 * scale;
            ctx.stroke();

            ctx.fillStyle = textColor || '#8b5cf6';
            const cornerSize = 8 * scale;
            ctx.fillRect(boxX, -boxH / 2, cornerSize, cornerSize);
            ctx.fillRect(boxX + boxW - cornerSize, -boxH / 2, cornerSize, cornerSize);
            ctx.fillRect(boxX, -boxH / 2 + boxH - cornerSize, cornerSize, cornerSize);
            ctx.fillRect(boxX + boxW - cornerSize, -boxH / 2 + boxH - cornerSize, cornerSize, cornerSize);
        }

        // Render each line
        let charsRenderedSoFar = 0;
        const totalWords = measuredLines.reduce((acc, l) => acc + (l.text.trim() ? l.text.trim().split(/\s+/).length : 0), 0);
        let wordsProcessedSoFar = 0;

        measuredLines.forEach((mLine, idx) => {
            const y = startY + idx * lineHeight;
            let lineX = 0;
            if (textAlign === 'left') lineX = 0;
            else if (textAlign === 'right') lineX = 0;
            else lineX = 0;

            let lineText = mLine.text;

            if (animation === 'typewriter') {
                const remaining = animCharCount - charsRenderedSoFar;
                if (remaining <= 0) {
                    return;
                }
                if (remaining < lineText.length) {
                    const isBlink = Math.floor(t * 4) % 2 === 0;
                    lineText = lineText.slice(0, remaining) + (isBlink ? '|' : '');
                }
                charsRenderedSoFar += mLine.text.length;
            }

            const currentMetrics = ctx.measureText(lineText);
            const curWidth = currentMetrics.width;

            if (bgStyle === 'pill') {
                const padX = fontSize * 0.55;
                const padY = fontSize * 0.22;
                let bgX = -curWidth / 2 - padX;
                if (textAlign === 'left') bgX = -padX;
                else if (textAlign === 'right') bgX = -curWidth - padX;

                ctx.fillStyle = bgColor ? (bgColor.startsWith('#') ? bgColor + 'cc' : bgColor) : 'rgba(0, 0, 0, 0.78)';
                ctx.beginPath();
                ctx.roundRect(bgX, y - lineHeight / 2 + padY / 2, curWidth + padX * 2, lineHeight - padY, fontSize * 0.35);
                ctx.fill();
            } else if (bgStyle === 'highlight') {
                const padX = fontSize * 0.35;
                let bgX = -curWidth / 2 - padX;
                if (textAlign === 'left') bgX = -padX;
                else if (textAlign === 'right') bgX = -curWidth - padX;

                ctx.fillStyle = bgColor || '#fde047';
                ctx.globalAlpha = animAlpha * 0.88;
                ctx.fillRect(bgX, y - lineHeight * 0.05, curWidth + padX * 2, lineHeight * 0.55);
                ctx.globalAlpha = animAlpha;
            }

            ctx.textAlign = textAlign;
            ctx.textBaseline = 'middle';

            if (bgStyle === 'shadow') {
                ctx.shadowColor = 'rgba(0, 0, 0, 0.95)';
                ctx.shadowBlur = 10 * scale;
                ctx.shadowOffsetX = 3 * scale;
                ctx.shadowOffsetY = 3 * scale;

                ctx.lineWidth = fontSize * 0.16;
                ctx.strokeStyle = '#000000';
                ctx.strokeText(lineText, lineX, y);
            } else if (bgStyle === 'neon') {
                const glowColor = bgColor !== '#000000' ? bgColor : '#38bdf8';
                ctx.shadowColor = glowColor;
                ctx.shadowBlur = (animGlowBlur || 14) * scale;
                ctx.shadowOffsetX = 0;
                ctx.shadowOffsetY = 0;

                ctx.lineWidth = fontSize * 0.14;
                ctx.strokeStyle = glowColor;
                ctx.strokeText(lineText, lineX, y);
            } else if (bgStyle === 'none' || bgStyle === 'pill') {
                ctx.shadowColor = 'rgba(0, 0, 0, 0.6)';
                ctx.shadowBlur = 4 * scale;
                ctx.shadowOffsetX = 1 * scale;
                ctx.shadowOffsetY = 1 * scale;

                ctx.lineWidth = fontSize * 0.1;
                ctx.strokeStyle = 'rgba(0, 0, 0, 0.8)';
                ctx.strokeText(lineText, lineX, y);
            }

            if (isKaraoke && totalWords > 0) {
                ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
                ctx.fillText(lineText, lineX, y);

                const words = lineText.trim().split(/\s+/);
                let wordStartX = (textAlign === 'center') ? -curWidth / 2 : (textAlign === 'right') ? -curWidth : 0;

                words.forEach(w => {
                    const wordMetrics = ctx.measureText(w + ' ');
                    const wordIdx = wordsProcessedSoFar;
                    const wordProgress = (wordIdx + 1) / totalWords;

                    if (karaokeProgress >= wordProgress) {
                        ctx.fillStyle = '#fde047';
                        ctx.shadowColor = '#f59e0b';
                        ctx.shadowBlur = 8 * scale;
                        ctx.textAlign = 'left';
                        ctx.fillText(w, wordStartX, y);
                    }
                    wordStartX += wordMetrics.width;
                    wordsProcessedSoFar++;
                });

                ctx.textAlign = textAlign;
            } else {
                ctx.fillStyle = textColor;
                ctx.fillText(lineText, lineX, y);
            }
        });

        ctx.restore();
    },

    /**
     * Wrap and render text lines with backdrop for subtitles
     */
    drawSubtitles(ctx, text, canvasW, canvasH, options = {}) {
        if (!text || !text.trim()) return;

        const position = options.position || 'bottom'; // top, center, bottom
        const style = options.style || 'pill'; // pill, shadow, yellow
        const sizeOption = options.size || 'medium';

        // Calculate font size responsive to canvas height
        let baseFontSize = canvasH * 0.045; // ~48px for 1080p
        if (sizeOption === 'small') baseFontSize = canvasH * 0.035;
        if (sizeOption === 'large') baseFontSize = canvasH * 0.06;

        ctx.save();
        ctx.font = `600 ${Math.round(baseFontSize)}px 'Be Vietnam Pro', 'Inter', sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        // Word wrapping
        const maxWidth = canvasW * 0.85;
        const words = text.trim().split(/\s+/);
        const lines = [];
        let currentLine = '';

        for (let i = 0; i < words.length; i++) {
            const testLine = currentLine ? currentLine + ' ' + words[i] : words[i];
            const metrics = ctx.measureText(testLine);
            if (metrics.width > maxWidth && currentLine) {
                lines.push(currentLine);
                currentLine = words[i];
            } else {
                currentLine = testLine;
            }
        }
        if (currentLine) lines.push(currentLine);

        const lineHeight = baseFontSize * 1.35;
        const totalHeight = lines.length * lineHeight;

        let startY = canvasH * 0.82; // bottom
        if (position === 'center') startY = canvasH * 0.5 - totalHeight / 2 + lineHeight / 2;
        if (position === 'top') startY = canvasH * 0.15;

        // Render based on style
        lines.forEach((line, idx) => {
            const y = startY + idx * lineHeight;
            const lineMetrics = ctx.measureText(line);
            const lineWidth = lineMetrics.width;

            if (style === 'pill') {
                // Dark rounded background pill
                const paddingX = baseFontSize * 0.6;
                const paddingY = baseFontSize * 0.25;
                ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
                ctx.beginPath();
                ctx.roundRect(
                    canvasW / 2 - lineWidth / 2 - paddingX,
                    y - lineHeight / 2 + paddingY / 2,
                    lineWidth + paddingX * 2,
                    lineHeight - paddingY,
                    baseFontSize * 0.3
                );
                ctx.fill();

                ctx.fillStyle = '#ffffff';
                ctx.fillText(line, canvasW / 2, y);
            } else if (style === 'yellow') {
                // Yellow bold text with strong black stroke
                ctx.lineWidth = baseFontSize * 0.18;
                ctx.strokeStyle = '#000000';
                ctx.strokeText(line, canvasW / 2, y);

                ctx.fillStyle = '#fde047'; // Amber yellow
                ctx.fillText(line, canvasW / 2, y);
            } else {
                // Shadow style
                ctx.shadowColor = 'rgba(0, 0, 0, 0.9)';
                ctx.shadowBlur = 10;
                ctx.shadowOffsetX = 2;
                ctx.shadowOffsetY = 2;

                ctx.lineWidth = baseFontSize * 0.15;
                ctx.strokeStyle = '#000000';
                ctx.strokeText(line, canvasW / 2, y);

                ctx.fillStyle = '#ffffff';
                ctx.fillText(line, canvasW / 2, y);
            }
        });

        ctx.restore();
    },

    /**
     * Generate procedural demo images with beautiful gradients and patterns
     */
    generateSampleImage(title, subtitle, colorA, colorB, iconType = 'sun') {
        const c = document.createElement('canvas');
        c.width = 1920;
        c.height = 1080;
        const ctx = c.getContext('2d');

        // Background Gradient
        const grad = ctx.createLinearGradient(0, 0, 1920, 1080);
        grad.addColorStop(0, colorA);
        grad.addColorStop(1, colorB);
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, 1920, 1080);

        // Abstract decorative geometric circles
        ctx.fillStyle = 'rgba(255, 255, 255, 0.06)';
        ctx.beginPath();
        ctx.arc(1600, 300, 450, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(300, 900, 350, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(960, 540, 600, 0, Math.PI * 2);
        ctx.lineWidth = 2;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
        ctx.stroke();

        // Inner glowing card
        ctx.fillStyle = 'rgba(15, 23, 42, 0.55)';
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.roundRect(240, 200, 1440, 680, 40);
        ctx.fill();
        ctx.stroke();

        // Text
        ctx.textAlign = 'center';
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 76px "Be Vietnam Pro", sans-serif';
        ctx.shadowColor = 'rgba(0, 0, 0, 0.4)';
        ctx.shadowBlur = 20;
        ctx.fillText(title, 960, 500);

        ctx.font = '500 36px "Be Vietnam Pro", sans-serif';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
        ctx.fillText(subtitle, 960, 600);

        return c.toDataURL('image/jpeg', 0.92);
    }
};

window.Utils = Utils;
