/**
 * Main Application Logic - UI & State Coordinator
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Core Engines
    const canvas = document.getElementById('video-canvas');
    const audioMixer = new AudioMixer();
    const ttsEngine = new TTSEngine();
    const videoRenderer = new VideoRenderer(canvas, audioMixer);

    // Initialize Web Audio Context on first user click (for background music only).
    const initAudioOnInteraction = async () => {
        await audioMixer.init();
        document.removeEventListener('click', initAudioOnInteraction);
    };
    document.addEventListener('click', initAudioOnInteraction);

    // 2. Application State
    const state = {
        slides: [], // Array of { id, imageSrc, imageElement, duration, text, motion, transition, overlay }
        defaultDuration: 3.5,
        defaultTransition: 'auto',
        voiceId: '',
        ttsRate: 1.0,
        isMuted: false
    };

    // Helper: Create default text box configuration
    function createDefaultTextBox(text = '', x = 50, y = 85, overrides = {}) {
        return {
            id: 'tb_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
            enabled: true,
            text: text || '',
            x: x,
            y: y,
            customX: x,
            customY: y,
            textAlign: 'center',
            fontFamily: 'Be Vietnam Pro',
            fontSize: 46,
            color: '#ffffff',
            bgStyle: 'pill',
            bgColor: '#000000',
            animation: 'fade',
            ...overrides
        };
    }

    // Helper: Ensure slide has proper textBoxes array
    function ensureSlideTextBoxes(slide) {
        if (!slide) return [];
        if (!Array.isArray(slide.textBoxes)) {
            slide.textBoxes = [];
            if (slide.overlay && (slide.overlay.text || slide.overlay.enabled !== false)) {
                slide.textBoxes.push(createDefaultTextBox(
                    slide.overlay.text || '',
                    slide.overlay.customX ?? slide.overlay.x ?? 50,
                    slide.overlay.customY ?? slide.overlay.y ?? 85,
                    slide.overlay
                ));
            } else if (slide.text && slide.text.trim()) {
                slide.textBoxes.push(createDefaultTextBox(slide.text, 50, 85));
            } else {
                slide.textBoxes.push(createDefaultTextBox('', 50, 85));
            }
        }
        return slide.textBoxes;
    }

    // Helper: Create default overlay configuration for backward compatibility
    function createDefaultOverlay(text = '', motion = 'kenburns', transition = 'crossfade') {
        return createDefaultTextBox(text, 50, 85, { motion: motion || 'kenburns', transition: transition || 'crossfade' });
    }

    // Quick Style Presets definition
    const OVERLAY_PRESETS = {
        cinema: {
            position: 'bottom-center',
            customX: 50,
            customY: 86,
            textAlign: 'center',
            fontFamily: 'Be Vietnam Pro',
            fontSize: 44,
            color: '#ffffff',
            bgStyle: 'pill',
            bgColor: '#000000',
            animation: 'slide-up'
        },
        hero: {
            position: 'center',
            customX: 50,
            customY: 50,
            textAlign: 'center',
            fontFamily: 'Oswald',
            fontSize: 64,
            color: '#fde047',
            bgStyle: 'shadow',
            bgColor: '#000000',
            animation: 'pop'
        },
        neon: {
            position: 'center',
            customX: 50,
            customY: 50,
            textAlign: 'center',
            fontFamily: 'Montserrat',
            fontSize: 52,
            color: '#ffffff',
            bgStyle: 'neon',
            bgColor: '#38bdf8',
            animation: 'glow'
        },
        highlight: {
            position: 'top-left',
            customX: 8,
            customY: 14,
            textAlign: 'left',
            fontFamily: 'Nunito',
            fontSize: 48,
            color: '#0f172a',
            bgStyle: 'highlight',
            bgColor: '#fde047',
            animation: 'bounce'
        },
        banner: {
            position: 'bottom-center',
            customX: 50,
            customY: 84,
            textAlign: 'center',
            fontFamily: 'Playfair Display',
            fontSize: 46,
            color: '#ffffff',
            bgStyle: 'gradient-banner',
            bgColor: '#0f172a',
            animation: 'slide-up'
        },
        karaoke: {
            position: 'bottom-center',
            customX: 50,
            customY: 85,
            textAlign: 'center',
            fontFamily: 'Be Vietnam Pro',
            fontSize: 48,
            color: '#ffffff',
            bgStyle: 'shadow',
            bgColor: '#000000',
            animation: 'karaoke'
        },
        lecture: {
            position: 'center',
            customX: 50,
            customY: 50,
            textAlign: 'center',
            fontFamily: 'Be Vietnam Pro',
            fontSize: 46,
            color: '#38bdf8',
            bgStyle: 'boxed-border',
            bgColor: '#0f172a',
            animation: 'bounce'
        },
        handwritten: {
            position: 'top-right',
            customX: 88,
            customY: 14,
            textAlign: 'right',
            fontFamily: 'Caveat',
            fontSize: 58,
            color: '#fef08a',
            bgStyle: 'shadow',
            bgColor: '#000000',
            animation: 'typewriter'
        }
    };

    // Motion presets (Intra-slide motion)
    const EFFECTS = [
        ['kenburns', 'Zoom điện ảnh (Ken Burns)'],
        ['zoom-in', 'Phóng to dần'], ['zoom-out', 'Thu nhỏ dần'],
        ['push-in', 'Đẩy vào mạnh'], ['pull-back', 'Kéo lùi'],
        ['pulse', 'Nhịp phóng nhẹ'], ['breathe', 'Hơi thở điện ảnh'],
        ['pan-left', 'Pan sang trái'], ['pan-right', 'Pan sang phải'],
        ['pan-up', 'Pan lên'], ['pan-down', 'Pan xuống'],
        ['diagonal-tl', 'Chéo lên trái'], ['diagonal-tr', 'Chéo lên phải'],
        ['diagonal-bl', 'Chéo xuống trái'], ['diagonal-br', 'Chéo xuống phải'],
        ['drift-left', 'Lướt trái'], ['drift-right', 'Lướt phải'],
        ['drift-up', 'Lướt lên'], ['drift-down', 'Lướt xuống'],
        ['zoom-pan-left', 'Zoom + trái'], ['zoom-pan-right', 'Zoom + phải'],
        ['zoom-pan-up', 'Zoom + lên'], ['zoom-pan-down', 'Zoom + xuống'],
        ['rotate-left', 'Xoay nhẹ trái'], ['rotate-right', 'Xoay nhẹ phải'],
        ['tilt-left', 'Nghiêng trái'], ['tilt-right', 'Nghiêng phải'],
        ['orbit-left', 'Vòng cung trái'], ['orbit-right', 'Vòng cung phải'],
        ['cinematic-left', 'Cinematic trái'], ['cinematic-right', 'Cinematic phải'],
        ['sweep-top', 'Quét từ trên'], ['sweep-bottom', 'Quét từ dưới'],
        ['none', 'Không hiệu ứng']
    ];

    const effectOptions = (selected) => EFFECTS.map(([id, label]) =>
        `<option value="${id}"${id === selected ? ' selected' : ''}>${label}</option>`
    ).join('');

    const autoEffectFor = (index, previous) => {
        let effect = EFFECTS[(index * 7 + state.slides.length * 3) % (EFFECTS.length - 1)][0];
        if (effect === previous) effect = EFFECTS[(index * 7 + state.slides.length * 3 + 1) % (EFFECTS.length - 1)][0];
        return effect;
    };

    const applyAutoEffects = () => {
        let previous = null;
        state.slides.forEach((slide, index) => {
            slide.motion = autoEffectFor(index, previous);
            slide.transition = 'crossfade';
            if (slide.overlay) {
                slide.overlay.motion = slide.motion;
                slide.overlay.transition = slide.transition;
            }
            previous = slide.motion;
        });
    };

    // 3. Lucide Icons re-render helper
    const refreshIcons = () => {
        if (window.lucide) {
            window.lucide.createIcons();
        }
    };
    refreshIcons();

    // 4. V-TTS local voice catalog. It is fixed by the local V-TTS model.
    const voiceSelect = document.getElementById('voice-select');
    const voiceCapabilityNote = document.getElementById('voice-capability-note');
    const selectedVoice = () => ttsEngine.getPresetVoices().find(v => v.id === state.voiceId);
    const updateVoiceCapabilities = () => {
        const voice = selectedVoice();
        if (!voice) return;
        if (voiceCapabilityNote) voiceCapabilityNote.textContent = `V-TTS cục bộ · ${voice.region} · ${voice.gender} · Không sao chép giọng`;
    };
    const populateVoiceList = () => {
        voiceSelect.innerHTML = '';
        const presetVoices = ttsEngine.getPresetVoices();
        if (!presetVoices.length) {
            const opt = document.createElement('option');
            opt.textContent = 'Chưa có giọng tiếng Việt trong trình duyệt';
            opt.disabled = true;
            opt.selected = true;
            voiceSelect.appendChild(opt);
            return;
        }
        presetVoices.forEach(v => {
            const opt = document.createElement('option');
            opt.value = v.id;
            opt.textContent = `${v.name} — ${v.region}, ${v.gender}`;
            if (v.id === state.voiceId) opt.selected = true;
            voiceSelect.appendChild(opt);
        });
        if (!presetVoices.some(v => v.id === state.voiceId)) state.voiceId = presetVoices[0].id;
        voiceSelect.value = state.voiceId;
        updateVoiceCapabilities();
    };

    populateVoiceList();
    ttsEngine.onStatus = ({ message, progress, error, ready }) => {
        const badge = document.getElementById('server-status-badge');
        if (badge) badge.innerHTML = `<span class="w-2 h-2 rounded-full ${error ? 'bg-rose-400' : ready ? 'bg-emerald-400' : 'bg-amber-400'} inline-block"></span><span class="text-slate-300">${message}${progress !== null ? ` (${progress}%)` : ''}</span>`;
    };

    voiceSelect.addEventListener('change', (e) => {
        state.voiceId = e.target.value;
        state.slides.forEach(slide => { slide.ttsAudioBuffer = null; slide.ttsMetadata = null; });
        updateVoiceCapabilities();
    });

    // 5. Initialize SortableJS on Slides Container
    const slidesContainer = document.getElementById('slides-container');
    new Sortable(slidesContainer, {
        animation: 150,
        ghostClass: 'sortable-ghost',
        dragClass: 'sortable-drag',
        onEnd: () => {
            // Re-order state.slides based on DOM order
            const domSlideIds = Array.from(slidesContainer.children).map(el => el.dataset.id);
            const newSlides = [];
            domSlideIds.forEach(id => {
                const found = state.slides.find(s => s.id === id);
                if (found) newSlides.push(found);
            });
            state.slides = newSlides;
            updateSlidesUI();
            videoRenderer.setSlides(state.slides);
        }
    });

    // 6. UI Elements
    const emptyState = document.getElementById('canvas-empty-state');
    const previewSlideBadge = document.getElementById('preview-slide-badge');
    const currentSlideIdxEl = document.getElementById('current-slide-idx');
    const totalSlidesCountEl = document.getElementById('total-slides-count');
    const timelineStatsEl = document.getElementById('timeline-stats');

    const btnPlayPause = document.getElementById('btn-play-pause');
    const playPauseIcon = document.getElementById('play-pause-icon');
    const btnRestart = document.getElementById('btn-restart');
    const playerScrubber = document.getElementById('player-scrubber');
    const playerCurrentTimeEl = document.getElementById('player-current-time');
    const playerTotalTimeEl = document.getElementById('player-total-time');
    const btnToggleMute = document.getElementById('btn-toggle-mute');
    const muteIcon = document.getElementById('mute-icon');

    // Sidebar Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => {
                b.classList.remove('text-brand-400', 'bg-brand-500/10', 'border', 'border-brand-500/30');
                b.classList.add('text-slate-400');
            });
            tabContents.forEach(c => c.classList.add('hidden'));

            btn.classList.remove('text-slate-400');
            btn.classList.add('text-brand-400', 'bg-brand-500/10', 'border', 'border-brand-500/30');
            const tabId = btn.dataset.tab;
            document.getElementById(tabId)?.classList.remove('hidden');
            refreshIcons();
        });
    });

    // Aspect Ratio Selection
    const ratioCards = document.querySelectorAll('.ratio-card');
    ratioCards.forEach(card => {
        card.addEventListener('click', () => {
            ratioCards.forEach(c => c.classList.remove('active-ratio'));
            card.classList.add('active-ratio');
            const ratio = card.dataset.ratio;
            videoRenderer.setAspectRatio(ratio);
        });
    });

    // Resolution & Default Settings
    const resolutionSelect = document.getElementById('video-resolution');
    resolutionSelect.addEventListener('change', (e) => {
        videoRenderer.setResolution(e.target.value);
    });

    const defaultTransitionSelect = document.getElementById('default-transition');
    defaultTransitionSelect.addEventListener('change', (e) => {
        state.defaultTransition = e.target.value;
        videoRenderer.defaultTransition = e.target.value === 'auto' ? 'kenburns' : e.target.value;
        if (e.target.value === 'auto') applyAutoEffects();
        else state.slides.forEach(s => s.transition = e.target.value);
        updateSlidesUI();
        videoRenderer.renderFrame(videoRenderer.currentTime);
    });

    const defaultDurationInput = document.getElementById('default-duration');
    const defaultDurationVal = document.getElementById('default-duration-val');
    defaultDurationInput.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        defaultDurationVal.textContent = val.toFixed(1) + 's';
        state.defaultDuration = val;
    });

    // Subtitles Settings
    const enableSubtitlesCheck = document.getElementById('enable-subtitles');
    const subtitlesOptionsBox = document.getElementById('subtitles-options');
    const subPositionSelect = document.getElementById('sub-position');
    const subFontSizeSelect = document.getElementById('sub-font-size');
    const subStyleSelect = document.getElementById('sub-style');

    enableSubtitlesCheck.addEventListener('change', (e) => {
        videoRenderer.enableSubtitles = e.target.checked;
        subtitlesOptionsBox.style.display = e.target.checked ? 'block' : 'none';
        videoRenderer.renderFrame(videoRenderer.currentTime);
    });

    const updateSubtitleConfig = () => {
        videoRenderer.subtitleOptions = {
            position: subPositionSelect.value,
            size: subFontSizeSelect.value,
            style: subStyleSelect.value
        };
        videoRenderer.renderFrame(videoRenderer.currentTime);
    };
    subPositionSelect.addEventListener('change', updateSubtitleConfig);
    subFontSizeSelect.addEventListener('change', updateSubtitleConfig);
    subStyleSelect.addEventListener('change', updateSubtitleConfig);

    // AI Voice Tab Handlers
    const voiceRateInput = document.getElementById('voice-rate');
    const voiceRateVal = document.getElementById('voice-rate-val');
    const btnTestVoice = document.getElementById('btn-test-voice');
    const testTtsText = document.getElementById('test-tts-text');

    voiceRateInput.addEventListener('input', (e) => {
        state.ttsRate = parseFloat(e.target.value);
        state.slides.forEach(slide => { slide.ttsAudioBuffer = null; slide.ttsMetadata = null; });
        voiceRateVal.textContent = state.ttsRate.toFixed(2) + 'x';
    });

    document.getElementById('btn-generate-all-tts')?.addEventListener('click', async () => {
        const targets = state.slides.filter(slide => slide.text?.trim());
        if (!targets.length) return alert('Chưa có lời thoại để tạo giọng.');
        for (const slide of targets) {
            const result = await ttsEngine.synthesize(slide.text, state.voiceId, state.ttsRate);
            slide.ttsAudioBuffer = result.buffer;
            slide.ttsMetadata = { text: slide.text, voiceId: state.voiceId, rate: state.ttsRate, wav: result.wav };
            if (slide.duration < result.duration) slide.duration = Math.ceil(result.duration * 10) / 10;
        }
        videoRenderer.setSlides(state.slides); updateSlidesUI();
    });

    // Quick previews produce the same audio buffer used in the exported video.
    const quickVoiceContainer = document.getElementById('quick-voice-buttons');
    const renderQuickVoiceButtons = () => {
        quickVoiceContainer.innerHTML = '';
        ttsEngine.getPresetVoices().forEach(voice => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn-quick-voice px-2.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-left text-xs transition flex items-center justify-between group';
            btn.dataset.voice = voice.id;
            btn.innerHTML = `<span class="font-bold text-slate-200 truncate">${voice.name}</span><i data-lucide="play-circle" class="w-4 h-4 text-brand-400 group-hover:scale-110 transition"></i>`;
            quickVoiceContainer.appendChild(btn);
        });
        refreshIcons();
    };
    renderQuickVoiceButtons();
    quickVoiceContainer.addEventListener('click', async (event) => {
        const btn = event.target.closest('.btn-quick-voice');
        if (!btn) return;
        try {
            const vId = btn.dataset.voice;
            state.voiceId = vId;
            voiceSelect.value = vId;
            updateVoiceCapabilities();
            const textToSpeak = testTtsText.value || 'Chào bạn, đây là câu đọc thử bằng giọng AI đang chọn.';
            testTtsText.value = textToSpeak;
            const result = await ttsEngine.synthesize(textToSpeak, vId, state.ttsRate);
            await audioMixer.init();
            const source = audioMixer.ctx.createBufferSource(); source.buffer = result.buffer; source.connect(audioMixer.voiceGainNode); source.start();
        } catch (error) {
            alert(error.message);
        }
    });

    // Nút nghe thử câu tùy chỉnh
    btnTestVoice.addEventListener('click', async () => {
        const text = testTtsText.value || 'Chào bạn, đây là câu đọc thử bằng giọng AI tự nhiên.';
        try {
            const result = await ttsEngine.synthesize(text, state.voiceId, state.ttsRate);
            await audioMixer.init();
            const source = audioMixer.ctx.createBufferSource(); source.buffer = result.buffer; source.connect(audioMixer.voiceGainNode); source.start();
        } catch (error) {
            alert(error.message);
        }
    });

    // Background Music Tab Handlers
    const musicDropzone = document.getElementById('music-dropzone');
    const musicFileInput = document.getElementById('music-file-input');
    const loadedMusicCard = document.getElementById('loaded-music-card');
    const musicFilenameEl = document.getElementById('music-filename');
    const musicDurationBadge = document.getElementById('music-duration-badge');
    const btnRemoveMusic = document.getElementById('btn-remove-music');
    const btnPlayMusicPreview = document.getElementById('btn-play-music-preview');
    const musicVolumeInput = document.getElementById('music-volume');
    const musicVolumeVal = document.getElementById('music-volume-val');
    const enableAudioDucking = document.getElementById('enable-audio-ducking');
    const enableMusicLoop = document.getElementById('enable-music-loop');
    const sampleTuneBtns = document.querySelectorAll('.sample-tune-btn');

    musicDropzone.addEventListener('click', () => musicFileInput.click());
    musicFileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (file) {
            try {
                const info = await audioMixer.loadBgmFromFile(file);
                showMusicLoaded(info.name, info.duration);
            } catch (err) {
                alert('Không thể đọc file nhạc: ' + err.message);
            }
        }
    });

    sampleTuneBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const tune = btn.dataset.tune;
            try {
                const info = await audioMixer.generatePresetTune(tune, 30);
                showMusicLoaded(info.name, info.duration);
            } catch (err) {
                alert('Lỗi tạo nhạc mẫu: ' + err.message);
            }
        });
    });

    function showMusicLoaded(name, duration) {
        musicFilenameEl.textContent = name;
        musicDurationBadge.textContent = Utils.formatTime(duration);
        loadedMusicCard.classList.remove('hidden');
        musicDropzone.classList.add('hidden');
    }

    btnRemoveMusic.addEventListener('click', () => {
        audioMixer.bgmBuffer = null;
        audioMixer.stopAll();
        loadedMusicCard.classList.add('hidden');
        musicDropzone.classList.remove('hidden');
        musicFileInput.value = '';
    });

    let isMusicPreviewPlaying = false;
    let musicPreviewSource = null;
    btnPlayMusicPreview.addEventListener('click', async () => {
        if (!audioMixer.bgmBuffer) return;
        await audioMixer.init();

        if (isMusicPreviewPlaying) {
            if (musicPreviewSource) {
                try { musicPreviewSource.stop(); } catch(e){}
            }
            isMusicPreviewPlaying = false;
            document.getElementById('music-preview-text').textContent = 'Nghe';
            refreshIcons();
        } else {
            musicPreviewSource = audioMixer.ctx.createBufferSource();
            musicPreviewSource.buffer = audioMixer.bgmBuffer;
            musicPreviewSource.connect(audioMixer.bgmGainNode);
            musicPreviewSource.start(0);
            isMusicPreviewPlaying = true;
            document.getElementById('music-preview-text').textContent = 'Dừng';
            musicPreviewSource.onended = () => {
                isMusicPreviewPlaying = false;
                document.getElementById('music-preview-text').textContent = 'Nghe';
                refreshIcons();
            };
            refreshIcons();
        }
    });

    musicVolumeInput.addEventListener('input', (e) => {
        const val = parseInt(e.target.value, 10);
        musicVolumeVal.textContent = val + '%';
        audioMixer.setBgmVolume(val / 100);
    });

    enableAudioDucking.addEventListener('change', (e) => {
        audioMixer.isDuckingEnabled = e.target.checked;
    });

    enableMusicLoop.addEventListener('change', (e) => {
        audioMixer.isLoopEnabled = e.target.checked;
    });

    // 7. Image Uploading & Slide Management
    const imageFileInput = document.getElementById('image-file-input');
    const btnAddImages = document.getElementById('btn-add-images');
    const btnQuickUpload = document.getElementById('btn-quick-upload');
    const addSlideDropzone = document.getElementById('add-slide-dropzone');

    const triggerImageUpload = () => imageFileInput.click();
    btnAddImages.addEventListener('click', triggerImageUpload);
    btnQuickUpload.addEventListener('click', triggerImageUpload);
    addSlideDropzone.addEventListener('click', triggerImageUpload);

    imageFileInput.addEventListener('change', async (e) => {
        const files = Array.from(e.target.files);
        if (files.length > 0) {
            await handleImageFiles(files);
            imageFileInput.value = '';
        }
    });

    // Drag and Drop files to workspace
    window.addEventListener('dragover', (e) => e.preventDefault());
    window.addEventListener('drop', async (e) => {
        e.preventDefault();
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            const files = Array.from(e.dataTransfer.files);
            const imageFiles = files.filter(f => f.type.startsWith('image/'));
            const audioFiles = files.filter(f => f.type.startsWith('audio/'));

            if (imageFiles.length > 0) {
                await handleImageFiles(imageFiles);
            }
            if (audioFiles.length > 0) {
                const info = await audioMixer.loadBgmFromFile(audioFiles[0]);
                showMusicLoaded(info.name, info.duration);
            }
        }
    });

    async function handleImageFiles(files) {
        for (const file of files) {
            const dataUrl = await Utils.fileToDataURL(file);
            const imgEl = await Utils.loadImage(dataUrl);

            const initialMotion = state.defaultTransition === 'auto'
                ? autoEffectFor(state.slides.length, state.slides[state.slides.length - 1]?.motion)
                : state.defaultTransition;

            const newSlide = {
                id: 'slide_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5),
                imageSrc: dataUrl,
                imageElement: imgEl,
                duration: state.defaultDuration,
                text: '',
                motion: initialMotion,
                transition: 'crossfade',
                textBoxes: [
                    createDefaultTextBox('Tiêu đề ảnh', 50, 85, { motion: initialMotion, transition: 'crossfade' })
                ]
            };

            state.slides.push(newSlide);
        }

        updateSlidesUI();
        videoRenderer.setSlides(state.slides);
    }

    // =========================================================================
    // 8. Canvas Drag & Drop and Quick Floating Toolbar Controller
    // =========================================================================
    const canvasQuickToolbar = document.getElementById('canvas-quick-toolbar');
    const quickTbText = document.getElementById('quick-tb-text');
    const quickTbFont = document.getElementById('quick-tb-font');
    const quickTbSizeDec = document.getElementById('quick-tb-size-dec');
    const quickTbSizeInc = document.getElementById('quick-tb-size-inc');
    const quickTbSizeVal = document.getElementById('quick-tb-size-val');
    const quickTbColor = document.getElementById('quick-tb-color');
    const quickTbBgStyle = document.getElementById('quick-tb-bg-style');
    const quickTbAnim = document.getElementById('quick-tb-anim');
    const quickTbDuplicate = document.getElementById('quick-tb-duplicate');
    const quickTbDelete = document.getElementById('quick-tb-delete');
    const quickTbModalOpen = document.getElementById('quick-tb-modal-open');
    const quickTbClose = document.getElementById('quick-tb-close');
    const canvasAddTextBtn = document.getElementById('canvas-add-text-btn');

    let isDragging = false;
    let draggedTextBox = null;
    let dragStartPointer = { x: 0, y: 0 };
    let dragStartBox = { x: 50, y: 85 };

    function getCanvasPointerCoords(e) {
        const rect = canvas.getBoundingClientRect();
        const clientX = e.clientX ?? (e.touches && e.touches[0]?.clientX) ?? 0;
        const clientY = e.clientY ?? (e.touches && e.touches[0]?.clientY) ?? 0;
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return {
            x: (clientX - rect.left) * scaleX,
            y: (clientY - rect.top) * scaleY
        };
    }

    function getCurrentActiveSlide() {
        const current = videoRenderer.getSlideAtTime(videoRenderer.currentTime);
        if (!current || !current.slide) return null;
        ensureSlideTextBoxes(current.slide);
        return current.slide;
    }

    function updateQuickColorChips(color) {
        if (!color) return;
        const norm = color.toLowerCase();
        document.querySelectorAll('.quick-color-chip').forEach(chip => {
            if (chip.dataset.color && chip.dataset.color.toLowerCase() === norm) {
                chip.classList.add('active-chip');
            } else {
                chip.classList.remove('active-chip');
            }
        });
    }

    function updateModalColorChips(color) {
        if (!color) return;
        const norm = color.toLowerCase();
        document.querySelectorAll('.color-chip').forEach(chip => {
            if (chip.dataset.color && chip.dataset.color.toLowerCase() === norm) {
                chip.classList.add('active-chip');
            } else {
                chip.classList.remove('active-chip');
            }
        });
    }

    function updateQuickToolbar() {
        const currentSlide = getCurrentActiveSlide();
        if (!currentSlide || state.slides.length === 0) {
            canvasQuickToolbar?.classList.add('hidden');
            canvasAddTextBtn?.classList.add('hidden');
            return;
        }

        canvasAddTextBtn?.classList.remove('hidden');

        if (!videoRenderer.selectedTextBoxId) {
            canvasQuickToolbar?.classList.add('hidden');
            return;
        }

        const selBox = currentSlide.textBoxes?.find(tb => tb.id === videoRenderer.selectedTextBoxId);
        if (!selBox) {
            canvasQuickToolbar?.classList.add('hidden');
            return;
        }

        if (quickTbText) quickTbText.value = selBox.text || '';
        if (quickTbFont) quickTbFont.value = selBox.fontFamily || 'Be Vietnam Pro';
        if (quickTbSizeVal) quickTbSizeVal.textContent = selBox.fontSize || 46;
        if (quickTbColor) quickTbColor.value = selBox.color || '#ffffff';
        updateQuickColorChips(selBox.color || '#ffffff');
        if (quickTbBgStyle) quickTbBgStyle.value = selBox.bgStyle || 'pill';
        if (quickTbAnim) quickTbAnim.value = selBox.animation || 'fade';

        canvasQuickToolbar?.classList.remove('hidden');
        refreshIcons();
    }

    // Canvas Pointer Event Listeners
    canvas.addEventListener('pointerdown', (e) => {
        if (videoRenderer.isPlaying) {
            videoRenderer.pause();
            playPauseIcon.setAttribute('data-lucide', 'play');
            refreshIcons();
        }

        const currentSlide = getCurrentActiveSlide();
        if (!currentSlide) return;

        const coords = getCanvasPointerCoords(e);
        const hit = videoRenderer.getTextBoxAtCoords(coords.x, coords.y, currentSlide);

        if (hit) {
            if (hit.hitButton === 'delete') {
                currentSlide.textBoxes = currentSlide.textBoxes.filter(tb => tb.id !== hit.textBox.id);
                if (videoRenderer.selectedTextBoxId === hit.textBox.id) {
                    videoRenderer.selectedTextBoxId = null;
                }
                updateQuickToolbar();
                updateSlidesUI();
                videoRenderer.renderFrame(videoRenderer.currentTime);
                return;
            }

            if (hit.hitButton === 'edit') {
                videoRenderer.selectedTextBoxId = hit.textBox.id;
                updateQuickToolbar();
                quickTbText?.focus();
                quickTbText?.select();
                videoRenderer.renderFrame(videoRenderer.currentTime);
                return;
            }

            // Hit body: select & start drag
            videoRenderer.selectedTextBoxId = hit.textBox.id;
            isDragging = true;
            draggedTextBox = hit.textBox;
            dragStartPointer = { x: coords.x, y: coords.y };
            dragStartBox = { x: hit.textBox.x ?? hit.textBox.customX ?? 50, y: hit.textBox.y ?? hit.textBox.customY ?? 85 };
            canvas.classList.add('cursor-grabbing');
            updateQuickToolbar();
            videoRenderer.renderFrame(videoRenderer.currentTime);
            canvas.setPointerCapture(e.pointerId);
        } else {
            // Clicked outside any text box
            videoRenderer.selectedTextBoxId = null;
            updateQuickToolbar();
            videoRenderer.renderFrame(videoRenderer.currentTime);
        }
    });

    canvas.addEventListener('pointermove', (e) => {
        const currentSlide = getCurrentActiveSlide();
        if (!currentSlide) return;
        const coords = getCanvasPointerCoords(e);

        if (isDragging && draggedTextBox) {
            const dx = coords.x - dragStartPointer.x;
            const dy = coords.y - dragStartPointer.y;
            const deltaXPercent = (dx / canvas.width) * 100;
            const deltaYPercent = (dy / canvas.height) * 100;

            draggedTextBox.x = Math.max(5, Math.min(95, Math.round(dragStartBox.x + deltaXPercent)));
            draggedTextBox.y = Math.max(5, Math.min(95, Math.round(dragStartBox.y + deltaYPercent)));
            draggedTextBox.customX = draggedTextBox.x;
            draggedTextBox.customY = draggedTextBox.y;

            videoRenderer.renderFrame(videoRenderer.currentTime);
        } else if (!videoRenderer.isPlaying) {
            const hit = videoRenderer.getTextBoxAtCoords(coords.x, coords.y, currentSlide);
            if (hit) {
                videoRenderer.hoveredTextBoxId = hit.textBox.id;
                canvas.style.cursor = hit.hitButton === 'body' ? 'grab' : 'pointer';
            } else {
                videoRenderer.hoveredTextBoxId = null;
                canvas.style.cursor = 'default';
            }
            videoRenderer.renderFrame(videoRenderer.currentTime);
        }
    });

    const endDrag = (e) => {
        if (isDragging) {
            isDragging = false;
            draggedTextBox = null;
            canvas.classList.remove('cursor-grabbing');
            try { canvas.releasePointerCapture(e.pointerId); } catch(err){}
            videoRenderer.renderFrame(videoRenderer.currentTime);
        }
    };

    canvas.addEventListener('pointerup', endDrag);
    canvas.addEventListener('pointercancel', endDrag);

    canvas.addEventListener('dblclick', (e) => {
        const currentSlide = getCurrentActiveSlide();
        if (!currentSlide) return;
        const coords = getCanvasPointerCoords(e);
        const hit = videoRenderer.getTextBoxAtCoords(coords.x, coords.y, currentSlide);
        if (hit) {
            videoRenderer.selectedTextBoxId = hit.textBox.id;
            updateQuickToolbar();
            quickTbText?.focus();
            quickTbText?.select();
            videoRenderer.renderFrame(videoRenderer.currentTime);
        }
    });

    // Quick Toolbar Input Bindings
    quickTbText?.addEventListener('input', (e) => {
        const currentSlide = getCurrentActiveSlide();
        const selBox = currentSlide?.textBoxes?.find(tb => tb.id === videoRenderer.selectedTextBoxId);
        if (selBox) {
            selBox.text = e.target.value;
            videoRenderer.renderFrame(videoRenderer.currentTime);
            updateSlidesUI();
        }
    });

    quickTbFont?.addEventListener('change', (e) => {
        const currentSlide = getCurrentActiveSlide();
        const selBox = currentSlide?.textBoxes?.find(tb => tb.id === videoRenderer.selectedTextBoxId);
        if (selBox) {
            selBox.fontFamily = e.target.value;
            videoRenderer.renderFrame(videoRenderer.currentTime);
        }
    });

    quickTbSizeDec?.addEventListener('click', () => {
        const currentSlide = getCurrentActiveSlide();
        const selBox = currentSlide?.textBoxes?.find(tb => tb.id === videoRenderer.selectedTextBoxId);
        if (selBox) {
            selBox.fontSize = Math.max(16, (selBox.fontSize || 46) - 4);
            if (quickTbSizeVal) quickTbSizeVal.textContent = selBox.fontSize;
            videoRenderer.renderFrame(videoRenderer.currentTime);
        }
    });

    quickTbSizeInc?.addEventListener('click', () => {
        const currentSlide = getCurrentActiveSlide();
        const selBox = currentSlide?.textBoxes?.find(tb => tb.id === videoRenderer.selectedTextBoxId);
        if (selBox) {
            selBox.fontSize = Math.min(120, (selBox.fontSize || 46) + 4);
            if (quickTbSizeVal) quickTbSizeVal.textContent = selBox.fontSize;
            videoRenderer.renderFrame(videoRenderer.currentTime);
        }
    });

    const handleQuickColorChange = (newColor) => {
        if (!newColor) return;
        const currentSlide = getCurrentActiveSlide();
        const selBox = currentSlide?.textBoxes?.find(tb => tb.id === videoRenderer.selectedTextBoxId);
        if (selBox) {
            selBox.color = newColor;
            if (quickTbColor) quickTbColor.value = newColor;
            if (modalTextColor) modalTextColor.value = newColor;
            updateQuickColorChips(newColor);
            updateModalColorChips(newColor);
            videoRenderer.renderFrame(videoRenderer.currentTime);
        }
    };

    quickTbColor?.addEventListener('input', (e) => handleQuickColorChange(e.target.value));
    quickTbColor?.addEventListener('change', (e) => handleQuickColorChange(e.target.value));

    document.querySelectorAll('.quick-color-chip').forEach(chip => {
        chip.addEventListener('click', (e) => {
            e.stopPropagation();
            const color = chip.dataset.color;
            if (color) handleQuickColorChange(color);
        });
    });

    quickTbBgStyle?.addEventListener('change', (e) => {
        const currentSlide = getCurrentActiveSlide();
        const selBox = currentSlide?.textBoxes?.find(tb => tb.id === videoRenderer.selectedTextBoxId);
        if (selBox) {
            selBox.bgStyle = e.target.value;
            videoRenderer.renderFrame(videoRenderer.currentTime);
            updateSlidesUI();
        }
    });

    quickTbAnim?.addEventListener('change', (e) => {
        const currentSlide = getCurrentActiveSlide();
        const selBox = currentSlide?.textBoxes?.find(tb => tb.id === videoRenderer.selectedTextBoxId);
        if (selBox) {
            selBox.animation = e.target.value;
            videoRenderer.renderFrame(videoRenderer.currentTime);
            updateSlidesUI();
        }
    });

    quickTbDuplicate?.addEventListener('click', () => {
        const currentSlide = getCurrentActiveSlide();
        const selBox = currentSlide?.textBoxes?.find(tb => tb.id === videoRenderer.selectedTextBoxId);
        if (selBox) {
            const newBox = createDefaultTextBox(selBox.text, Math.min(90, (selBox.x || 50) + 4), Math.min(90, (selBox.y || 85) + 4), {
                textAlign: selBox.textAlign,
                fontFamily: selBox.fontFamily,
                fontSize: selBox.fontSize,
                color: selBox.color,
                bgStyle: selBox.bgStyle,
                bgColor: selBox.bgColor,
                animation: selBox.animation
            });
            currentSlide.textBoxes.push(newBox);
            videoRenderer.selectedTextBoxId = newBox.id;
            updateQuickToolbar();
            updateSlidesUI();
            videoRenderer.renderFrame(videoRenderer.currentTime);
        }
    });

    quickTbDelete?.addEventListener('click', () => {
        const currentSlide = getCurrentActiveSlide();
        if (currentSlide && videoRenderer.selectedTextBoxId) {
            currentSlide.textBoxes = currentSlide.textBoxes.filter(tb => tb.id !== videoRenderer.selectedTextBoxId);
            videoRenderer.selectedTextBoxId = null;
            updateQuickToolbar();
            updateSlidesUI();
            videoRenderer.renderFrame(videoRenderer.currentTime);
        }
    });

    quickTbModalOpen?.addEventListener('click', () => {
        const currentSlide = getCurrentActiveSlide();
        if (currentSlide) {
            openOverlayModal(currentSlide, videoRenderer.selectedTextBoxId);
        }
    });

    quickTbClose?.addEventListener('click', () => {
        videoRenderer.selectedTextBoxId = null;
        updateQuickToolbar();
        videoRenderer.renderFrame(videoRenderer.currentTime);
    });

    canvasAddTextBtn?.addEventListener('click', () => {
        const currentSlide = getCurrentActiveSlide();
        if (!currentSlide) return;
        const newBox = createDefaultTextBox('Nhập nội dung chữ...', 50, 50);
        currentSlide.textBoxes = currentSlide.textBoxes || [];
        currentSlide.textBoxes.push(newBox);
        videoRenderer.selectedTextBoxId = newBox.id;
        updateQuickToolbar();
        updateSlidesUI();
        videoRenderer.renderFrame(videoRenderer.currentTime);
        setTimeout(() => {
            quickTbText?.focus();
            quickTbText?.select();
        }, 50);
    });

    // =========================================================================
    // 9. Text Overlay & Slide Effects Modal Editor
    // =========================================================================
    const overlayModal = document.getElementById('slide-overlay-modal');
    const modalSlideBadge = document.getElementById('modal-slide-badge');
    const btnCloseOverlayModal = document.getElementById('btn-close-overlay-modal');
    const btnSaveOverlay = document.getElementById('btn-save-overlay');
    const btnApplyAllOverlay = document.getElementById('btn-apply-all-overlay');

    const modalTextboxTabs = document.getElementById('modal-textbox-tabs');
    const modalBtnAddTextbox = document.getElementById('modal-btn-add-textbox');
    const modalBtnDeleteTextbox = document.getElementById('modal-btn-delete-textbox');

    const modalOverlayEnabled = document.getElementById('modal-overlay-enabled');
    const modalOverlayText = document.getElementById('modal-overlay-text');
    const modalFontFamily = document.getElementById('modal-font-family');
    const modalFontSize = document.getElementById('modal-font-size');
    const modalFontSizeVal = document.getElementById('modal-font-size-val');
    const modalTextColor = document.getElementById('modal-text-color');
    const modalBgColor = document.getElementById('modal-bg-color');
    const modalBgColorLabel = document.getElementById('modal-bg-color-label');
    const modalTextAnimation = document.getElementById('modal-text-animation');
    const modalPosX = document.getElementById('modal-pos-x');
    const modalPosY = document.getElementById('modal-pos-y');
    const customCoordsVal = document.getElementById('custom-coords-val');
    const posLabelBadge = document.getElementById('pos-label-badge');
    const modalSlideMotion = document.getElementById('modal-slide-motion');
    const modalSlideTransition = document.getElementById('modal-slide-transition');

    let activeEditingSlide = null;
    let activeEditingTextBoxId = null;

    function renderModalTextBoxTabs() {
        if (!activeEditingSlide || !modalTextboxTabs) return;
        ensureSlideTextBoxes(activeEditingSlide);
        modalTextboxTabs.innerHTML = '';

        activeEditingSlide.textBoxes.forEach((tb, idx) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `modal-tb-tab px-3 py-1.5 rounded-lg border text-xs flex items-center gap-1.5 transition ${
                tb.id === activeEditingTextBoxId
                    ? 'active-tb-tab bg-brand-500/20 border-brand-500 text-brand-300 font-bold'
                    : 'bg-slate-900 border-slate-700 text-slate-400 hover:text-white'
            }`;
            btn.dataset.id = tb.id;
            const snippet = tb.text ? (tb.text.length > 12 ? tb.text.slice(0, 12) + '…' : tb.text) : `Khung #${idx + 1}`;
            btn.innerHTML = `<i data-lucide="type" class="w-3 h-3"></i><span>Khung #${idx + 1}: ${snippet}</span>`;
            
            btn.addEventListener('click', () => {
                activeEditingTextBoxId = tb.id;
                videoRenderer.selectedTextBoxId = tb.id;
                populateModalFields();
                renderModalTextBoxTabs();
                videoRenderer.renderFrame(videoRenderer.currentTime);
            });
            modalTextboxTabs.appendChild(btn);
        });

        refreshIcons();
    }

    function populateModalFields() {
        if (!activeEditingSlide) return;
        ensureSlideTextBoxes(activeEditingSlide);

        let tb = activeEditingSlide.textBoxes.find(t => t.id === activeEditingTextBoxId);
        if (!tb && activeEditingSlide.textBoxes.length > 0) {
            tb = activeEditingSlide.textBoxes[0];
            activeEditingTextBoxId = tb.id;
        }
        if (!tb) return;

        videoRenderer.selectedTextBoxId = tb.id;

        if (modalOverlayEnabled) modalOverlayEnabled.checked = tb.enabled !== false;
        if (modalOverlayText) modalOverlayText.value = tb.text || '';

        const curX = tb.x ?? tb.customX ?? 50;
        const curY = tb.y ?? tb.customY ?? 85;

        if (modalPosX) modalPosX.value = curX;
        if (modalPosY) modalPosY.value = curY;
        if (customCoordsVal) customCoordsVal.textContent = `${curX}%, ${curY}%`;

        updatePosGridUI(tb.position || 'custom');
        updateTextAlignUI(tb.textAlign || 'center');

        if (modalFontFamily) modalFontFamily.value = tb.fontFamily || 'Be Vietnam Pro';
        if (modalFontSize) modalFontSize.value = tb.fontSize || 46;
        if (modalFontSizeVal) modalFontSizeVal.textContent = (tb.fontSize || 46) + 'px';
        if (modalTextColor) modalTextColor.value = tb.color || '#ffffff';
        updateModalColorChips(tb.color || '#ffffff');

        // Select Bg Style radio
        const bgRadios = document.querySelectorAll('input[name="modal-bg-style"]');
        bgRadios.forEach(r => {
            r.checked = (r.value === (tb.bgStyle || 'pill'));
        });

        if (modalBgColor) modalBgColor.value = tb.bgColor || '#000000';
        if (modalBgColorLabel) modalBgColorLabel.textContent = tb.bgColor || '#000000';

        if (modalTextAnimation) modalTextAnimation.value = tb.animation || 'fade';
        if (modalSlideMotion) modalSlideMotion.value = activeEditingSlide.motion || activeEditingSlide.transition || 'kenburns';
        if (modalSlideTransition) modalSlideTransition.value = activeEditingSlide.transition || 'crossfade';
    }

    function openOverlayModal(slide, targetTextBoxId = null) {
        if (!slide) return;
        activeEditingSlide = slide;
        ensureSlideTextBoxes(slide);

        activeEditingTextBoxId = targetTextBoxId || (slide.textBoxes[0]?.id) || null;
        const idx = state.slides.indexOf(slide);

        if (modalSlideBadge) modalSlideBadge.textContent = `Slide #${idx + 1}`;

        renderModalTextBoxTabs();
        populateModalFields();

        // Seek player to this slide so user can see WYSIWYG preview immediately
        let startSec = 0;
        for (let i = 0; i < idx; i++) {
            startSec += (state.slides[i].duration || 3.5);
        }
        videoRenderer.seek(startSec);

        if (overlayModal) {
            overlayModal.classList.remove('hidden');
            refreshIcons();
        }
    }

    function closeOverlayModal() {
        if (overlayModal) overlayModal.classList.add('hidden');
        updateQuickToolbar();
        updateSlidesUI();
        videoRenderer.renderFrame(videoRenderer.currentTime);
    }

    function syncModalToSlide() {
        if (!activeEditingSlide) return;
        ensureSlideTextBoxes(activeEditingSlide);

        const tb = activeEditingSlide.textBoxes.find(t => t.id === activeEditingTextBoxId);
        if (!tb) return;

        if (modalOverlayEnabled) tb.enabled = modalOverlayEnabled.checked;
        if (modalOverlayText) {
            tb.text = modalOverlayText.value;
        }

        if (modalFontFamily) tb.fontFamily = modalFontFamily.value;
        if (modalFontSize) {
            tb.fontSize = parseInt(modalFontSize.value, 10) || 46;
            if (modalFontSizeVal) modalFontSizeVal.textContent = tb.fontSize + 'px';
        }
        if (modalTextColor) {
            tb.color = modalTextColor.value;
            updateModalColorChips(tb.color);
            if (quickTbColor) quickTbColor.value = tb.color;
            updateQuickColorChips(tb.color);
        }

        const checkedBg = document.querySelector('input[name="modal-bg-style"]:checked');
        if (checkedBg) tb.bgStyle = checkedBg.value;

        if (modalBgColor) {
            tb.bgColor = modalBgColor.value;
            if (modalBgColorLabel) modalBgColorLabel.textContent = modalBgColor.value;
        }

        if (modalTextAnimation) tb.animation = modalTextAnimation.value;

        if (modalPosX && modalPosY) {
            tb.x = parseInt(modalPosX.value, 10);
            tb.y = parseInt(modalPosY.value, 10);
            tb.customX = tb.x;
            tb.customY = tb.y;
            if (customCoordsVal) customCoordsVal.textContent = `${tb.x}%, ${tb.y}%`;
        }

        if (modalSlideMotion) {
            activeEditingSlide.motion = modalSlideMotion.value;
        }

        if (modalSlideTransition) {
            activeEditingSlide.transition = modalSlideTransition.value;
        }

        renderModalTextBoxTabs();
        updateQuickToolbar();
        videoRenderer.renderFrame(videoRenderer.currentTime);
    }

    function updatePosGridUI(pos) {
        const gridBtns = document.querySelectorAll('.btn-pos-grid');
        gridBtns.forEach(btn => {
            if (btn.dataset.pos === pos) {
                btn.classList.add('active-pos');
            } else {
                btn.classList.remove('active-pos');
            }
        });

        const labels = {
            'top-left': 'Trên trái', 'top-center': 'Trên giữa', 'top-right': 'Trên phải',
            'mid-left': 'Giữa trái', 'center': 'Chính giữa', 'mid-right': 'Giữa phải',
            'bottom-left': 'Dưới trái', 'bottom-center': 'Dưới giữa', 'bottom-right': 'Dưới phải',
            'custom': 'Tùy chỉnh'
        };
        if (posLabelBadge) posLabelBadge.textContent = labels[pos] || pos;
    }

    function updateTextAlignUI(align) {
        if (!activeEditingSlide) return;
        const tb = activeEditingSlide.textBoxes?.find(t => t.id === activeEditingTextBoxId);
        if (tb) tb.textAlign = align;

        const alignBtns = document.querySelectorAll('.btn-text-align');
        alignBtns.forEach(btn => {
            if (btn.dataset.align === align) {
                btn.classList.add('active-align', 'text-brand-400', 'bg-brand-500/20', 'font-bold');
                btn.classList.remove('text-slate-300');
            } else {
                btn.classList.remove('active-align', 'text-brand-400', 'bg-brand-500/20', 'font-bold');
                btn.classList.add('text-slate-300');
            }
        });
    }

    function applyPreset(presetKey) {
        if (!activeEditingSlide || !OVERLAY_PRESETS[presetKey]) return;
        const p = OVERLAY_PRESETS[presetKey];
        const tb = activeEditingSlide.textBoxes?.find(t => t.id === activeEditingTextBoxId);
        if (!tb) return;

        tb.position = p.position;
        tb.x = p.customX;
        tb.y = p.customY;
        tb.customX = p.customX;
        tb.customY = p.customY;
        tb.textAlign = p.textAlign;
        tb.fontFamily = p.fontFamily;
        tb.fontSize = p.fontSize;
        tb.color = p.color;
        tb.bgStyle = p.bgStyle;
        tb.bgColor = p.bgColor;
        tb.animation = p.animation;

        updatePosGridUI(tb.position);
        updateTextAlignUI(tb.textAlign);

        if (modalPosX) modalPosX.value = tb.x;
        if (modalPosY) modalPosY.value = tb.y;
        if (customCoordsVal) customCoordsVal.textContent = `${tb.x}%, ${tb.y}%`;

        if (modalFontFamily) modalFontFamily.value = tb.fontFamily;
        if (modalFontSize) modalFontSize.value = tb.fontSize;
        if (modalFontSizeVal) modalFontSizeVal.textContent = tb.fontSize + 'px';
        if (modalTextColor) modalTextColor.value = tb.color;
        updateModalColorChips(tb.color);

        const bgRadios = document.querySelectorAll('input[name="modal-bg-style"]');
        bgRadios.forEach(r => { r.checked = (r.value === tb.bgStyle); });

        if (modalBgColor) modalBgColor.value = tb.bgColor;
        if (modalBgColorLabel) modalBgColorLabel.textContent = tb.bgColor;

        if (modalTextAnimation) modalTextAnimation.value = tb.animation;

        syncModalToSlide();
    }

    // Modal Events Binding
    btnCloseOverlayModal?.addEventListener('click', closeOverlayModal);
    btnSaveOverlay?.addEventListener('click', closeOverlayModal);

    modalBtnAddTextbox?.addEventListener('click', () => {
        if (!activeEditingSlide) return;
        const newBox = createDefaultTextBox('Khung chữ mới', 50, 50);
        activeEditingSlide.textBoxes.push(newBox);
        activeEditingTextBoxId = newBox.id;
        renderModalTextBoxTabs();
        populateModalFields();
        videoRenderer.renderFrame(videoRenderer.currentTime);
    });

    modalBtnDeleteTextbox?.addEventListener('click', () => {
        if (!activeEditingSlide || !activeEditingSlide.textBoxes) return;
        if (activeEditingSlide.textBoxes.length <= 1) {
            alert('Mỗi slide cần giữ ít nhất 1 khung chữ.');
            return;
        }
        activeEditingSlide.textBoxes = activeEditingSlide.textBoxes.filter(t => t.id !== activeEditingTextBoxId);
        activeEditingTextBoxId = activeEditingSlide.textBoxes[0].id;
        renderModalTextBoxTabs();
        populateModalFields();
        videoRenderer.renderFrame(videoRenderer.currentTime);
    });

    modalOverlayEnabled?.addEventListener('change', syncModalToSlide);
    modalOverlayText?.addEventListener('input', syncModalToSlide);
    modalFontFamily?.addEventListener('change', syncModalToSlide);
    modalFontSize?.addEventListener('input', syncModalToSlide);
    modalTextColor?.addEventListener('input', syncModalToSlide);
    modalTextColor?.addEventListener('change', syncModalToSlide);
    modalBgColor?.addEventListener('input', syncModalToSlide);
    modalTextAnimation?.addEventListener('change', syncModalToSlide);
    modalSlideMotion?.addEventListener('change', syncModalToSlide);
    modalSlideTransition?.addEventListener('change', syncModalToSlide);

    modalPosX?.addEventListener('input', () => {
        updatePosGridUI('custom');
        syncModalToSlide();
    });
    modalPosY?.addEventListener('input', () => {
        updatePosGridUI('custom');
        syncModalToSlide();
    });

    document.querySelectorAll('.btn-pos-grid').forEach(btn => {
        btn.addEventListener('click', () => {
            const pos = btn.dataset.pos;
            updatePosGridUI(pos);
            if (pos === 'top-left') { if (modalPosX) modalPosX.value = 8; if (modalPosY) modalPosY.value = 12; }
            else if (pos === 'top-center') { if (modalPosX) modalPosX.value = 50; if (modalPosY) modalPosY.value = 12; }
            else if (pos === 'top-right') { if (modalPosX) modalPosX.value = 92; if (modalPosY) modalPosY.value = 12; }
            else if (pos === 'mid-left') { if (modalPosX) modalPosX.value = 8; if (modalPosY) modalPosY.value = 50; }
            else if (pos === 'center') { if (modalPosX) modalPosX.value = 50; if (modalPosY) modalPosY.value = 50; }
            else if (pos === 'mid-right') { if (modalPosX) modalPosX.value = 92; if (modalPosY) modalPosY.value = 50; }
            else if (pos === 'bottom-left') { if (modalPosX) modalPosX.value = 8; if (modalPosY) modalPosY.value = 85; }
            else if (pos === 'bottom-center') { if (modalPosX) modalPosX.value = 50; if (modalPosY) modalPosY.value = 85; }
            else if (pos === 'bottom-right') { if (modalPosX) modalPosX.value = 92; if (modalPosY) modalPosY.value = 85; }
            syncModalToSlide();
        });
    });

    document.querySelectorAll('.btn-text-align').forEach(btn => {
        btn.addEventListener('click', () => {
            updateTextAlignUI(btn.dataset.align);
            syncModalToSlide();
        });
    });

    document.querySelectorAll('input[name="modal-bg-style"]').forEach(r => {
        r.addEventListener('change', syncModalToSlide);
    });

    document.querySelectorAll('.color-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const color = chip.dataset.color;
            if (modalTextColor && color) {
                modalTextColor.value = color;
                updateModalColorChips(color);
                syncModalToSlide();
            }
        });
    });

    document.querySelectorAll('.btn-quick-preset').forEach(btn => {
        btn.addEventListener('click', () => {
            const preset = btn.dataset.preset;
            applyPreset(preset);
        });
    });

    btnApplyAllOverlay?.addEventListener('click', () => {
        if (!activeEditingSlide) return;
        const curTb = activeEditingSlide.textBoxes?.find(t => t.id === activeEditingTextBoxId);
        if (!curTb) return;

        state.slides.forEach(slide => {
            ensureSlideTextBoxes(slide);
            const targetTb = slide.textBoxes[0] || createDefaultTextBox();
            targetTb.enabled = curTb.enabled;
            targetTb.x = curTb.x;
            targetTb.y = curTb.y;
            targetTb.customX = curTb.customX;
            targetTb.customY = curTb.customY;
            targetTb.textAlign = curTb.textAlign;
            targetTb.fontFamily = curTb.fontFamily;
            targetTb.fontSize = curTb.fontSize;
            targetTb.color = curTb.color;
            targetTb.bgStyle = curTb.bgStyle;
            targetTb.bgColor = curTb.bgColor;
            targetTb.animation = curTb.animation;

            slide.motion = activeEditingSlide.motion;
            slide.transition = activeEditingSlide.transition;
        });

        updateSlidesUI();
        videoRenderer.renderFrame(videoRenderer.currentTime);
        alert(`Đã áp dụng mẫu chữ & hiệu ứng cho toàn bộ ${state.slides.length} slide!`);
    });

    // =========================================================================
    // 10. Render Slide Cards in Timeline
    // =========================================================================
    function updateSlidesUI() {
        slidesContainer.innerHTML = '';
        const totalSlides = state.slides.length;
        const totalDur = state.slides.reduce((acc, s) => acc + (s.duration || 3.5), 0);

        timelineStatsEl.textContent = `${totalSlides} ảnh • ${totalDur.toFixed(1)} giây`;
        totalSlidesCountEl.textContent = totalSlides;

        if (totalSlides === 0) {
            emptyState.classList.remove('hidden');
            previewSlideBadge.classList.add('hidden');
            canvasAddTextBtn?.classList.add('hidden');
            canvasQuickToolbar?.classList.add('hidden');
        } else {
            emptyState.classList.add('hidden');
            previewSlideBadge.classList.remove('hidden');
            canvasAddTextBtn?.classList.remove('hidden');
        }

        state.slides.forEach((slide, idx) => {
            ensureSlideTextBoxes(slide);

            const card = document.createElement('div');
            card.className = 'slide-card group flex flex-col justify-between p-2.5';
            card.dataset.id = slide.id;

            // Generate tags for all text boxes on this slide
            const textBoxTagsHTML = slide.textBoxes.map((tb, tbIdx) => {
                const previewText = tb.text ? (tb.text.length > 10 ? tb.text.slice(0, 10) + '…' : tb.text) : `Chữ #${tbIdx + 1}`;
                return `
                    <button type="button" class="tb-tag-chip px-1.5 py-0.5 rounded bg-slate-900/90 border border-slate-700/80 hover:border-brand-500 text-[10px] text-slate-200 flex items-center gap-1 transition" data-tb-id="${tb.id}" title="Nhấp để chọn & kéo thả khung chữ này trên Canvas">
                        <i data-lucide="type" class="w-2.5 h-2.5 text-brand-400"></i>
                        <span class="truncate max-w-[80px]">${previewText}</span>
                    </button>
                `;
            }).join('');

            card.innerHTML = `
                <!-- Top thumbnail preview & badge -->
                <div class="relative w-full h-20 rounded-lg overflow-hidden bg-slate-900 mb-1.5 border border-slate-700/60 shrink-0">
                    <img src="${slide.imageSrc}" class="w-full h-full object-cover pointer-events-none">
                    <span class="absolute top-1 left-1 px-1.5 py-0.5 rounded bg-black/70 text-[10px] font-bold text-white">#${idx + 1}</span>
                    <button class="btn-delete-slide absolute top-1 right-1 w-6 h-6 rounded bg-black/70 hover:bg-rose-600 text-slate-300 hover:text-white flex items-center justify-center transition">
                        <i data-lucide="trash" class="w-3.5 h-3.5"></i>
                    </button>
                    ${slide.ttsAudioBuffer ? '<span class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-emerald-500/90 text-[9px] font-bold text-white flex items-center gap-0.5"><i data-lucide="volume-2" class="w-2.5 h-2.5"></i> Audio WAV</span>' : ''}
                </div>

                <!-- Canvas Text Boxes Section -->
                <div class="space-y-1 mb-1.5">
                    <div class="flex items-center justify-between">
                        <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                            <i data-lucide="layers" class="w-3 h-3 text-brand-400"></i> Khung Chữ (${slide.textBoxes.length})
                        </span>
                        <button type="button" class="btn-card-add-tb px-1.5 py-0.5 bg-brand-600/20 hover:bg-brand-600/40 border border-brand-500/30 text-brand-300 rounded text-[9px] font-semibold flex items-center gap-0.5 transition" title="Thêm khung chữ mới">
                            <i data-lucide="plus" class="w-2.5 h-2.5"></i> Chữ
                        </button>
                    </div>

                    <!-- Tags list -->
                    <div class="flex flex-wrap gap-1 items-center max-h-12 overflow-y-auto">
                        ${textBoxTagsHTML}
                    </div>

                    <button type="button" class="btn-edit-slide-overlay w-full py-1 px-2 bg-gradient-to-r from-brand-600/20 to-indigo-600/20 hover:from-brand-600/40 hover:to-indigo-600/40 border border-brand-500/30 text-brand-200 hover:text-white rounded-lg text-[10px] font-semibold flex items-center justify-between transition mt-1" title="Chỉnh sửa chi tiết chữ & hiệu ứng">
                        <span class="flex items-center gap-1"><i data-lucide="sparkles" class="w-3 h-3 text-amber-400"></i> Sửa & Hiệu ứng</span>
                        <i data-lucide="sliders" class="w-3 h-3 text-slate-400"></i>
                    </button>
                </div>

                <!-- Slide Voice Narration Prompt (Separate for V-TTS) -->
                <div class="space-y-1.5 flex-1 flex flex-col justify-between pt-1 border-t border-slate-700/50">
                    <div>
                        <label class="text-[9px] font-bold text-slate-400 uppercase tracking-wider block mb-0.5 flex items-center gap-1">
                            <i data-lucide="mic" class="w-2.5 h-2.5 text-emerald-400"></i> Lời thoại đọc AI (TTS)
                        </label>
                        <textarea class="slide-text-input w-full bg-slate-900/90 border border-slate-700/80 rounded-lg p-1.5 text-[11px] text-white placeholder-slate-500 resize-none focus:ring-1 focus:ring-brand-500 outline-none h-11" placeholder="Nhập lời đọc cho giọng AI...">${slide.text || ''}</textarea>
                    </div>

                    <!-- Per-slide motion effect -->
                    <select class="slide-effect-select w-full bg-slate-900 border border-slate-700 rounded px-1.5 py-0.5 text-[10px] text-indigo-200 focus:ring-1 focus:ring-brand-500 outline-none" title="Chuyển động trong ảnh">
                        ${effectOptions(slide.motion || slide.transition || 'kenburns')}
                    </select>

                    <!-- Slide Controls: Duration & Voice Button -->
                    <div class="flex items-center justify-between gap-1 pt-1 border-t border-slate-700/50">
                        <div class="flex items-center gap-1">
                            <i data-lucide="clock" class="w-3 h-3 text-slate-400"></i>
                            <input type="number" step="0.5" min="1" max="60" value="${slide.duration || 3.5}" class="slide-duration-input w-12 bg-slate-900 border border-slate-700 rounded px-1 py-0.5 text-[10px] text-brand-300 font-bold text-center">
                            <span class="text-[10px] text-slate-400">s</span>
                        </div>
                        <button class="btn-generate-slide-tts px-2 py-0.5 bg-brand-600/30 hover:bg-brand-600 border border-brand-500/40 text-brand-200 hover:text-white rounded text-[10px] font-medium flex items-center gap-1 transition" title="Tạo WAV V-TTS và nhúng vào video">
                            <i data-lucide="volume-2" class="w-3 h-3"></i> Tạo giọng
                        </button>
                    </div>
                </div>
            `;

            // Card Event Listeners
            const btnEditOverlay = card.querySelector('.btn-edit-slide-overlay');
            btnEditOverlay.addEventListener('click', (e) => {
                e.stopPropagation();
                openOverlayModal(slide);
            });

            const btnCardAddTb = card.querySelector('.btn-card-add-tb');
            btnCardAddTb.addEventListener('click', (e) => {
                e.stopPropagation();
                let startSec = 0;
                for (let i = 0; i < idx; i++) {
                    startSec += (state.slides[i].duration || 3.5);
                }
                videoRenderer.seek(startSec);
                const newBox = createDefaultTextBox('Nhập nội dung...', 50, 50);
                slide.textBoxes.push(newBox);
                videoRenderer.selectedTextBoxId = newBox.id;
                updateSlidesUI();
                updateQuickToolbar();
                videoRenderer.renderFrame(videoRenderer.currentTime);
            });

            // Click tag chips to select & highlight text box on Canvas
            card.querySelectorAll('.tb-tag-chip').forEach(chip => {
                chip.addEventListener('click', (e) => {
                    e.stopPropagation();
                    let startSec = 0;
                    for (let i = 0; i < idx; i++) {
                        startSec += (state.slides[i].duration || 3.5);
                    }
                    videoRenderer.seek(startSec);
                    const tbId = chip.dataset.tbId;
                    videoRenderer.selectedTextBoxId = tbId;
                    updateQuickToolbar();
                    videoRenderer.renderFrame(videoRenderer.currentTime);
                });
            });

            const textInput = card.querySelector('.slide-text-input');
            textInput.addEventListener('input', (e) => {
                slide.text = e.target.value;
                slide.ttsAudioBuffer = null;
                slide.ttsMetadata = null;
                videoRenderer.renderFrame(videoRenderer.currentTime);
            });

            const durInput = card.querySelector('.slide-duration-input');
            durInput.addEventListener('change', (e) => {
                const val = Math.max(0.5, parseFloat(e.target.value) || 3.5);
                slide.duration = val;
                timelineStatsEl.textContent = `${state.slides.length} ảnh • ${videoRenderer.calculateTotalDuration().toFixed(1)} giây`;
                videoRenderer.setSlides(state.slides);
            });

            const effectSelect = card.querySelector('.slide-effect-select');
            effectSelect.addEventListener('change', (e) => {
                slide.motion = e.target.value;
                videoRenderer.renderFrame(videoRenderer.currentTime);
            });

            const btnDelete = card.querySelector('.btn-delete-slide');
            btnDelete.addEventListener('click', (e) => {
                e.stopPropagation();
                state.slides = state.slides.filter(s => s.id !== slide.id);
                videoRenderer.selectedTextBoxId = null;
                updateSlidesUI();
                updateQuickToolbar();
                videoRenderer.setSlides(state.slides);
            });

            const btnSlideTts = card.querySelector('.btn-generate-slide-tts');
            btnSlideTts.addEventListener('click', async (e) => {
                e.stopPropagation();
                if (!slide.text || !slide.text.trim()) {
                    alert('Vui lòng nhập lời thoại cho ảnh trước!');
                    return;
                }
                try {
                    btnSlideTts.disabled = true;
                    btnSlideTts.textContent = 'Đang tạo…';
                    const result = await ttsEngine.synthesize(slide.text, state.voiceId, state.ttsRate);
                    slide.ttsAudioBuffer = result.buffer;
                    slide.ttsMetadata = { text: slide.text, voiceId: state.voiceId, rate: state.ttsRate, wav: result.wav };
                    if (slide.duration < result.duration) slide.duration = Math.ceil(result.duration * 10) / 10;
                    videoRenderer.setSlides(state.slides);
                    updateSlidesUI();
                } catch (error) {
                    alert(error.message);
                } finally {
                    btnSlideTts.disabled = false;
                }
            });

            // Click slide card to seek preview to that slide
            card.addEventListener('click', () => {
                let startSec = 0;
                for (let i = 0; i < idx; i++) {
                    startSec += (state.slides[i].duration || 3.5);
                }
                videoRenderer.seek(startSec);
                updateQuickToolbar();
            });

            slidesContainer.appendChild(card);
        });

        refreshIcons();
    }

    // =========================================================================
    // 11. Video Renderer Event Listeners & Player Controls
    // =========================================================================
    videoRenderer.onTimeUpdate = (current, total) => {
        playerCurrentTimeEl.textContent = Utils.formatTime(current);
        playerTotalTimeEl.textContent = Utils.formatTime(total);
        if (total > 0) {
            playerScrubber.value = (current / total) * 100;
        } else {
            playerScrubber.value = 0;
        }
    };

    videoRenderer.onSlideChange = (currentIdx, totalCount) => {
        currentSlideIdxEl.textContent = currentIdx;
        totalSlidesCountEl.textContent = totalCount;

        const cards = slidesContainer.querySelectorAll('.slide-card');
        cards.forEach((c, idx) => {
            if (idx === currentIdx - 1) c.classList.add('active-playing');
            else c.classList.remove('active-playing');
        });
    };

    videoRenderer.onPlaybackPaused = () => {
        updateQuickToolbar();
    };

    videoRenderer.onPlaybackEnded = () => {
        playPauseIcon.setAttribute('data-lucide', 'play');
        updateQuickToolbar();
        refreshIcons();
    };

    btnPlayPause.addEventListener('click', async () => {
        await audioMixer.init();
        if (videoRenderer.isPlaying) {
            videoRenderer.pause();
            playPauseIcon.setAttribute('data-lucide', 'play');
            updateQuickToolbar();
        } else {
            canvasQuickToolbar?.classList.add('hidden');
            videoRenderer.play();
            playPauseIcon.setAttribute('data-lucide', 'pause');
        }
        refreshIcons();
    });

    btnRestart.addEventListener('click', () => {
        videoRenderer.seek(0);
        updateQuickToolbar();
    });

    playerScrubber.addEventListener('input', (e) => {
        const percent = parseFloat(e.target.value);
        const targetTime = (percent / 100) * videoRenderer.totalDuration;
        videoRenderer.seek(targetTime);
        updateQuickToolbar();
    });

    btnToggleMute.addEventListener('click', () => {
        state.isMuted = !state.isMuted;
        audioMixer.setMute(state.isMuted);
        muteIcon.setAttribute('data-lucide', state.isMuted ? 'volume-x' : 'volume-2');
        refreshIcons();
    });

    // =========================================================================
    // 12. Sample Demo Project Loader with Multi-Text Box Canvas Drag & Drop
    // =========================================================================
    const btnLoadSample = document.getElementById('btn-load-sample');
    btnLoadSample.addEventListener('click', async () => {
        btnLoadSample.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Đang nạp...';
        refreshIcons();

        try {
            await audioMixer.init();

            // Generate sample procedural images
            const img1 = Utils.generateSampleImage('Chào Mừng Bạn Đến Với', 'Studio Làm Video AI Bài Giảng', '#4f46e5', '#9333ea');
            const img2 = Utils.generateSampleImage('Tạo Video Từ Ảnh', 'Chuyển cảnh & Chuyển động Ken Burns', '#0ea5e9', '#3b82f6');
            const img3 = Utils.generateSampleImage('Lồng Tiếng AI Chuẩn', 'Tự động đồng bộ giọng nói và chữ nghệ thuật', '#059669', '#10b981');
            const img4 = Utils.generateSampleImage('Xuất Video Full HD', 'Tải về MP4 chất lượng cao ngay trên web!', '#d97706', '#ea580c');

            const loadedImg1 = await Utils.loadImage(img1);
            const loadedImg2 = await Utils.loadImage(img2);
            const loadedImg3 = await Utils.loadImage(img3);
            const loadedImg4 = await Utils.loadImage(img4);

            state.slides = [
                {
                    id: 'sample_1',
                    imageSrc: img1,
                    imageElement: loadedImg1,
                    duration: 4.5,
                    text: 'Chào mừng bạn đến với Studio làm Video AI bài giảng trực quan.',
                    motion: 'kenburns',
                    transition: 'crossfade',
                    textBoxes: [
                        createDefaultTextBox('CHÀO MỪNG BẠN ĐẾN VỚI\nAI VIDEO STUDIO', 50, 40, {
                            fontFamily: 'Oswald',
                            fontSize: 60,
                            color: '#fde047',
                            bgStyle: 'shadow',
                            animation: 'pop'
                        }),
                        createDefaultTextBox('✨ Kéo thả trực tiếp khung chữ trên Canvas', 50, 75, {
                            fontFamily: 'Be Vietnam Pro',
                            fontSize: 38,
                            color: '#38bdf8',
                            bgStyle: 'pill',
                            animation: 'glow'
                        })
                    ]
                },
                {
                    id: 'sample_2',
                    imageSrc: img2,
                    imageElement: loadedImg2,
                    duration: 4.5,
                    text: 'Tùy biến hiệu ứng chuyển động Ken Burns và đa khung chữ nghệ thuật.',
                    motion: 'pan-left',
                    transition: 'slide-left',
                    textBoxes: [
                        createDefaultTextBox('ĐA KHUNG CHỮ NGHỆ THUẬT', 50, 22, {
                            fontFamily: 'Montserrat',
                            fontSize: 50,
                            color: '#ffffff',
                            bgStyle: 'gradient-banner',
                            animation: 'slide-down'
                        }),
                        createDefaultTextBox('🖍️ Dạ quang nổi bật', 30, 58, {
                            fontFamily: 'Nunito',
                            fontSize: 42,
                            color: '#0f172a',
                            bgStyle: 'highlight',
                            bgColor: '#fde047',
                            animation: 'bounce'
                        }),
                        createDefaultTextBox('⚡ Neon phát sáng', 70, 58, {
                            fontFamily: 'Montserrat',
                            fontSize: 42,
                            color: '#ffffff',
                            bgStyle: 'neon',
                            bgColor: '#38bdf8',
                            animation: 'glow'
                        })
                    ]
                },
                {
                    id: 'sample_3',
                    imageSrc: img3,
                    imageElement: loadedImg3,
                    duration: 4.8,
                    text: 'Lồng tiếng AI chuẩn xác, đồng bộ âm thanh và hình ảnh sống động.',
                    motion: 'orbit-left',
                    transition: 'circle-reveal',
                    textBoxes: [
                        createDefaultTextBox('🎓 KHUNG BÀI GIẢNG HIỆN ĐẠI', 50, 45, {
                            fontFamily: 'Be Vietnam Pro',
                            fontSize: 48,
                            color: '#38bdf8',
                            bgStyle: 'boxed-border',
                            bgColor: '#0f172a',
                            animation: 'bounce'
                        }),
                        createDefaultTextBox('🎤 Hỗ trợ Karaoke lướt màu chữ theo câu đọc', 50, 84, {
                            fontFamily: 'Be Vietnam Pro',
                            fontSize: 40,
                            color: '#ffffff',
                            bgStyle: 'pill',
                            animation: 'karaoke'
                        })
                    ]
                },
                {
                    id: 'sample_4',
                    imageSrc: img4,
                    imageElement: loadedImg4,
                    duration: 4.5,
                    text: 'Xuất video Full HD MP4 và WebM siêu nét, sẵn sàng chia sẻ ngay!',
                    motion: 'zoom-in',
                    transition: 'crossfade',
                    textBoxes: [
                        createDefaultTextBox('XUẤT VIDEO FULL HD 1080P', 50, 50, {
                            fontFamily: 'Playfair Display',
                            fontSize: 54,
                            color: '#ffffff',
                            bgStyle: 'gradient-banner',
                            bgColor: '#0f172a',
                            animation: 'slide-up'
                        })
                    ]
                }
            ];

            // Load preset ambient music
            const tuneInfo = await audioMixer.generatePresetTune('ambient', 30);
            showMusicLoaded(tuneInfo.name, tuneInfo.duration);

            updateSlidesUI();
            videoRenderer.setSlides(state.slides);
            videoRenderer.seek(0);
            updateQuickToolbar();

        } catch (err) {
            alert('Không thể tải dự án mẫu: ' + err.message);
        } finally {
            btnLoadSample.innerHTML = '<i data-lucide="sparkles" class="w-4 h-4 text-amber-400"></i> Nạp Dự Án Mẫu';
            refreshIcons();
        }
    });

    // Clear All button
    const btnClearAll = document.getElementById('btn-clear-all');
    btnClearAll.addEventListener('click', () => {
        if (confirm('Bạn có chắc chắn muốn làm mới và xóa tất cả hình ảnh hiện tại?')) {
            videoRenderer.pause();
            state.slides = [];
            updateSlidesUI();
            videoRenderer.setSlides([]);
            videoRenderer.seek(0);
        }
    });

    // 11. Export Video Modal Handlers
    const exportModal = document.getElementById('export-modal');
    const btnOpenExportModal = document.getElementById('btn-open-export-modal');
    const btnCloseExportModal = document.getElementById('btn-close-export-modal');
    const exportInitialState = document.getElementById('export-initial-state');
    const exportProgressState = document.getElementById('export-progress-state');
    const exportSuccessState = document.getElementById('export-success-state');
    const btnStartExport = document.getElementById('btn-start-export');
    const exportProgressBar = document.getElementById('export-progress-bar');
    const exportPercentText = document.getElementById('export-percent-text');
    const exportFrameText = document.getElementById('export-frame-text');
    const btnDownloadVideo = document.getElementById('btn-download-video');
    const exportVideoInfo = document.getElementById('export-video-info');

    btnOpenExportModal.addEventListener('click', () => {
        if (state.slides.length === 0) {
            alert('Vui lòng thêm ít nhất 1 ảnh trước khi xuất video!');
            return;
        }

        document.getElementById('modal-summary-ratio').textContent = videoRenderer.aspectRatio;
        document.getElementById('modal-summary-slides').textContent = `${state.slides.length} ảnh`;
        document.getElementById('modal-summary-duration').textContent = `${videoRenderer.totalDuration.toFixed(1)}s`;
        
        let audioDesc = 'Không có âm thanh';
        const hasBgm = !!audioMixer.bgmBuffer;
        const narrationCount = state.slides.filter(slide => slide.ttsAudioBuffer).length;
        if (hasBgm && narrationCount) audioDesc = `Nhạc nền + giọng V-TTS (${narrationCount} ảnh)`;
        else if (narrationCount) audioDesc = `Giọng V-TTS (${narrationCount} ảnh)`;
        else if (hasBgm) audioDesc = 'Nhạc nền hoặc tệp âm thanh đã tải lên';
        document.getElementById('modal-summary-audio').textContent = audioDesc;

        exportInitialState.classList.remove('hidden');
        exportProgressState.classList.add('hidden');
        exportSuccessState.classList.add('hidden');
        exportModal.classList.remove('hidden');
        refreshIcons();
    });

    btnCloseExportModal.addEventListener('click', () => {
        if (videoRenderer.isExporting) {
            if (confirm('Đang xuất video, bạn có chắc muốn hủy bỏ?')) {
                videoRenderer.cancelExport();
                exportModal.classList.add('hidden');
            }
        } else {
            exportModal.classList.add('hidden');
        }
    });

    btnStartExport.addEventListener('click', async () => {
        const formatInput = document.querySelector('input[name="export-format"]:checked');
        const format = formatInput ? formatInput.value : 'mp4';

        exportInitialState.classList.add('hidden');
        exportProgressState.classList.remove('hidden');
        exportSuccessState.classList.add('hidden');
        refreshIcons();

        try {
            await audioMixer.init();
            const result = await videoRenderer.exportVideo({ format }, (progress, currentFrame, totalFrames) => {
                const percent = Math.round(progress * 100);
                exportProgressBar.style.width = `${percent}%`;
                exportPercentText.textContent = `${percent}%`;
                exportFrameText.textContent = `Khung hình ${currentFrame}/${totalFrames}`;
            });

            exportProgressState.classList.add('hidden');
            exportSuccessState.classList.remove('hidden');
            btnDownloadVideo.href = result.url;
            btnDownloadVideo.download = `ai-video-${Date.now()}.${result.format}`;
            exportVideoInfo.textContent = `Định dạng: ${result.format.toUpperCase()} • Kích thước: ${result.sizeMB} MB • Thời lượng: ${videoRenderer.totalDuration.toFixed(1)}s`;
            refreshIcons();
        } catch (err) {
            alert('Lỗi xuất video: ' + err.message);
            exportInitialState.classList.remove('hidden');
            exportProgressState.classList.add('hidden');
        }
    });

    // Spacebar to Play/Pause shortcut
    window.addEventListener('keydown', (e) => {
        if (e.code === 'Space' && e.target.tagName !== 'TEXTAREA' && e.target.tagName !== 'INPUT') {
            e.preventDefault();
            btnPlayPause.click();
        }
    });
});
