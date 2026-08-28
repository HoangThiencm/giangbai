/**
 * Video Renderer - Canvas rendering, Ken Burns animations, and Video Export
 */

class VideoRenderer {
    constructor(canvas, audioMixer) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d', { alpha: false });
        this.audioMixer = audioMixer;

        // Settings
        this.aspectRatio = '16:9'; // '16:9', '9:16', '1:1'
        this.resolutionHeight = 1080;
        this.transitionDuration = 0.8; // transition time in seconds
        this.defaultTransition = 'kenburns';

        this.enableSubtitles = true;
        this.subtitleOptions = {
            position: 'bottom',
            size: 'medium',
            style: 'pill'
        };

        // State
        this.slides = [];
        this.currentTime = 0;
        this.totalDuration = 0;
        this.isPlaying = false;
        this.animationFrameId = null;
        this.lastFrameTimestamp = 0;
        this.activeSlideIndex = -1;

        // Export state
        this.isExporting = false;
        this.mediaRecorder = null;
        this.recordedChunks = [];

        this.updateCanvasDimensions();
    }

    /**
     * Update Canvas Width & Height based on resolution and aspect ratio
     */
    updateCanvasDimensions() {
        let width = 1920;
        let height = 1080;

        if (this.aspectRatio === '16:9') {
            height = this.resolutionHeight;
            width = Math.round(height * (16 / 9));
        } else if (this.aspectRatio === '9:16') {
            width = this.resolutionHeight;
            height = Math.round(width * (16 / 9));
            if (height > 1920) {
                height = 1920;
                width = 1080;
            }
        } else if (this.aspectRatio === '1:1') {
            width = this.resolutionHeight;
            height = this.resolutionHeight;
        }

        this.canvas.width = width;
        this.canvas.height = height;

        // Update container aspect ratio style
        const container = document.getElementById('canvas-container');
        if (container) {
            if (this.aspectRatio === '16:9') container.style.aspectRatio = '16/9';
            else if (this.aspectRatio === '9:16') container.style.aspectRatio = '9/16';
            else if (this.aspectRatio === '1:1') container.style.aspectRatio = '1/1';
        }
    }

    setAspectRatio(ratio) {
        this.aspectRatio = ratio;
        this.updateCanvasDimensions();
        this.renderFrame(this.currentTime);
    }

    setResolution(height) {
        this.resolutionHeight = parseInt(height, 10);
        this.updateCanvasDimensions();
        this.renderFrame(this.currentTime);
    }

    setSlides(slides) {
        this.slides = slides;
        this.calculateTotalDuration();
        this.renderFrame(this.currentTime);
    }

    calculateTotalDuration() {
        this.totalDuration = this.slides.reduce((acc, s) => acc + (s.duration || 3.5), 0);
        return this.totalDuration;
    }

    /**
     * Find active slide index and relative time inside slide
     */
    getSlideAtTime(timeSec) {
        let accum = 0;
        for (let i = 0; i < this.slides.length; i++) {
            const dur = this.slides[i].duration || 3.5;
            if (timeSec >= accum && timeSec < accum + dur) {
                return {
                    index: i,
                    slide: this.slides[i],
                    slideStart: accum,
                    slideEnd: accum + dur,
                    localTime: timeSec - accum,
                    progress: (timeSec - accum) / dur,
                    duration: dur
                };
            }
            accum += dur;
        }

        // If at the end or empty
        if (this.slides.length > 0) {
            const lastIdx = this.slides.length - 1;
            const lastSlide = this.slides[lastIdx];
            const dur = lastSlide.duration || 3.5;
            return {
                index: lastIdx,
                slide: lastSlide,
                slideStart: accum - dur,
                slideEnd: accum,
                localTime: dur,
                progress: 1.0,
                duration: dur
            };
        }

        return null;
    }

    /**
     * Render a single frame at a specific timestamp
     */
    renderFrame(timeSec) {
        const w = this.canvas.width;
        const h = this.canvas.height;
        const ctx = this.ctx;

        // Clear canvas
        ctx.fillStyle = '#05070d';
        ctx.fillRect(0, 0, w, h);

        if (!this.slides || this.slides.length === 0) {
            return;
        }

        const current = this.getSlideAtTime(timeSec);
        if (!current || !current.slide || !current.slide.imageElement) return;

        // Trigger slide enter callback if playing
        if (this.isPlaying && current.index !== this.activeSlideIndex) {
            this.activeSlideIndex = current.index;
            if (this.onSlideEnter) {
                this.onSlideEnter(current.slide, current.index);
            }
        }

        const currentSlide = current.slide;
        const nextSlide = this.slides[current.index + 1] || null;
        const timeRemaining = current.slideEnd - timeSec;
        const transition = currentSlide.transition || this.defaultTransition;

        // Check if we are in transition zone to next slide
        if (nextSlide && nextSlide.imageElement && timeRemaining <= this.transitionDuration && transition !== 'none') {
            const transProgress = 1 - (timeRemaining / this.transitionDuration);
            Utils.drawTransition(ctx, currentSlide, nextSlide, current.progress, transProgress, w, h, transition);
        } else {
            // Normal slide rendering with slide's intra-motion
            const motion = currentSlide.motion || currentSlide.transition || this.defaultTransition;
            this.renderSingleSlide(ctx, currentSlide, current.progress, w, h, motion);
        }

        // Render Text Overlay (Per-slide customizable overlay or fallback to subtitles)
        if (currentSlide.overlay) {
            Utils.drawTextOverlay(ctx, currentSlide.overlay, currentSlide.text, current.localTime, current.duration, w, h);
        } else if (this.enableSubtitles && currentSlide.text) {
            Utils.drawSubtitles(ctx, currentSlide.text, w, h, this.subtitleOptions);
        }

        // Update badge index if callback provided
        if (this.onSlideChange) {
            this.onSlideChange(current.index + 1, this.slides.length);
        }
    }

    /**
     * Render single slide with Ken Burns motion
     */
    renderSingleSlide(ctx, slide, progress, w, h, transitionType) {
        if (!slide || !slide.imageElement) return;
        Utils.drawKenBurns(ctx, slide.imageElement, progress, w, h, transitionType);
    }

    /**
     * Render transition between two slides
     */
    renderTransition(ctx, slide1, slide2, slide1Progress, transProgress, w, h, type) {
        Utils.drawTransition(ctx, slide1, slide2, slide1Progress, transProgress, w, h, type);
    }

    /**
     * Player Play / Pause controls
     */
    play() {
        if (this.isPlaying) return;
        if (this.slides.length === 0) return;

        if (this.currentTime >= this.totalDuration) {
            this.currentTime = 0;
        }

        this.isPlaying = true;
        this.activeSlideIndex = -1;
        this.lastFrameTimestamp = performance.now();

        // Start Audio Mixer
        if (this.audioMixer) {
            this.audioMixer.playTimeline(this.slides, this.currentTime);
        }

        // Trigger slide enter for current timestamp
        const current = this.getSlideAtTime(this.currentTime);
        if (current) {
            this.activeSlideIndex = current.index;
            if (this.onSlideEnter) {
                this.onSlideEnter(current.slide, current.index);
            }
        }

        this.loop();
    }

    pause() {
        this.isPlaying = false;
        this.activeSlideIndex = -1;
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
        if (this.audioMixer) {
            this.audioMixer.stopAll();
        }
        if (this.onPlaybackPaused) {
            this.onPlaybackPaused();
        }
    }

    seek(targetTime) {
        this.currentTime = Math.max(0, Math.min(this.totalDuration, targetTime));
        this.activeSlideIndex = -1;
        this.renderFrame(this.currentTime);

        if (this.isPlaying) {
            if (this.audioMixer) {
                this.audioMixer.playTimeline(this.slides, this.currentTime);
            }
            const current = this.getSlideAtTime(this.currentTime);
            if (current) {
                this.activeSlideIndex = current.index;
                if (this.onSlideEnter) {
                    this.onSlideEnter(current.slide, current.index);
                }
            }
        } else {
            if (this.onPlaybackPaused) {
                this.onPlaybackPaused();
            }
        }

        if (this.onTimeUpdate) {
            this.onTimeUpdate(this.currentTime, this.totalDuration);
        }
    }

    loop(timestamp) {
        if (!this.isPlaying) return;

        const now = performance.now();
        const delta = (now - this.lastFrameTimestamp) / 1000;
        this.lastFrameTimestamp = now;

        this.currentTime += delta;

        if (this.currentTime >= this.totalDuration) {
            this.currentTime = this.totalDuration;
            this.renderFrame(this.currentTime);
            this.pause();
            if (this.onTimeUpdate) this.onTimeUpdate(this.currentTime, this.totalDuration);
            if (this.onPlaybackEnded) this.onPlaybackEnded();
            return;
        }

        this.renderFrame(this.currentTime);

        if (this.onTimeUpdate) {
            this.onTimeUpdate(this.currentTime, this.totalDuration);
        }

        this.animationFrameId = requestAnimationFrame(this.loop.bind(this));
    }

    /**
     * Export Video to MP4 / WebM using MediaRecorder and synchronized audio
     */
    async exportVideo(options = {}, onProgress = null) {
        if (this.isExporting) return;
        this.isExporting = true;
        this.pause();

        // Ensure all fonts are ready
        if (document.fonts && document.fonts.ready) {
            try {
                await document.fonts.ready;
            } catch (e) {
                console.warn('Fonts ready wait warning:', e);
            }
        }

        const format = options.format || 'mp4';
        const fps = 30;
        const totalFrames = Math.ceil(this.totalDuration * fps);
        const frameInterval = 1 / fps;

        // Create recording stream from canvas + audio mixer stream
        const canvasStream = this.canvas.captureStream(fps);
        const audioStream = this.audioMixer ? this.audioMixer.getStream() : null;

        const combinedStream = new MediaStream();
        canvasStream.getVideoTracks().forEach(track => combinedStream.addTrack(track));
        if (audioStream && audioStream.getAudioTracks().length > 0) {
            audioStream.getAudioTracks().forEach(track => combinedStream.addTrack(track));
        }

        // Determine supported mimeType
        let mimeType = 'video/webm;codecs=vp9,opus';
        if (format === 'mp4') {
            if (MediaRecorder.isTypeSupported('video/mp4;codecs=avc1,mp4a.40.2')) {
                mimeType = 'video/mp4;codecs=avc1,mp4a.40.2';
            } else if (MediaRecorder.isTypeSupported('video/mp4')) {
                mimeType = 'video/mp4';
            } else {
                mimeType = 'video/webm;codecs=vp8,opus';
            }
        } else {
            if (!MediaRecorder.isTypeSupported(mimeType)) {
                mimeType = 'video/webm';
            }
        }

        this.recordedChunks = [];
        const recorder = new MediaRecorder(combinedStream, {
            mimeType: mimeType,
            videoBitsPerSecond: 6000000 // 6 Mbps
        });

        recorder.ondataavailable = (e) => {
            if (e.data && e.data.size > 0) {
                this.recordedChunks.push(e.data);
            }
        };

        // Start Audio Playback for mixer
        if (this.audioMixer) {
            this.audioMixer.playTimeline(this.slides, 0);
        }

        recorder.start(100);

        // Render frames in realtime sync with audio recorder
        let currentExportTime = 0;

        return new Promise((resolve, reject) => {
            const processFrame = () => {
                if (!this.isExporting) {
                    recorder.stop();
                    reject(new Error('Export cancelled'));
                    return;
                }

                this.renderFrame(currentExportTime);
                currentExportTime += frameInterval;

                const progress = Math.min(1.0, currentExportTime / this.totalDuration);
                const currentFrame = Math.min(totalFrames, Math.round(progress * totalFrames));

                if (onProgress) {
                    onProgress(progress, currentFrame, totalFrames);
                }

                if (currentExportTime <= this.totalDuration) {
                    setTimeout(processFrame, (1000 / fps));
                } else {
                    setTimeout(() => {
                        if (this.audioMixer) this.audioMixer.stopAll();
                        recorder.stop();
                    }, 300);
                }
            };

            recorder.onstop = () => {
                this.isExporting = false;
                const blob = new Blob(this.recordedChunks, { type: mimeType });
                const videoUrl = URL.createObjectURL(blob);
                resolve({
                    blob: blob,
                    url: videoUrl,
                    format: mimeType.includes('mp4') ? 'mp4' : 'webm',
                    sizeMB: (blob.size / (1024 * 1024)).toFixed(2)
                });
            };

            processFrame();
        });
    }

    cancelExport() {
        this.isExporting = false;
        if (this.audioMixer) this.audioMixer.stopAll();
    }
}

window.VideoRenderer = VideoRenderer;
