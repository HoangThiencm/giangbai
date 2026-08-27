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
            case 'none':
            default:
                scale = 1.0;
                offX = 0;
                offY = 0;
                break;
        }

        this.drawImageCover(ctx, img, 0, 0, canvasW, canvasH, scale, offX, offY);
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
