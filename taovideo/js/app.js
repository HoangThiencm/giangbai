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

    // Helper: Create default overlay configuration for a slide
    function createDefaultOverlay(text = '', motion = 'kenburns', transition = 'crossfade') {
        return {
            enabled: true,
            text: text || '',
            position: 'bottom-center',
            customX: 50,
            customY: 85,
            textAlign: 'center',
            fontFamily: 'Be Vietnam Pro',
            fontSize: 46,
            color: '#ffffff',
            bgStyle: 'pill',
            bgColor: '#000000',
            animation: 'fade',
            motion: motion || 'kenburns',
            transition: transition || 'crossfade'
        };
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
                overlay: createDefaultOverlay('', initialMotion, 'crossfade')
            };

            state.slides.push(newSlide);
        }

        updateSlidesUI();
        videoRenderer.setSlides(state.slides);
    }

    // =========================================================================
    // 8. Text Overlay & Slide Effects Modal Editor
    // =========================================================================
    const overlayModal = document.getElementById('slide-overlay-modal');
    const modalSlideBadge = document.getElementById('modal-slide-badge');
    const btnCloseOverlayModal = document.getElementById('btn-close-overlay-modal');
    const btnSaveOverlay = document.getElementById('btn-save-overlay');
    const btnApplyAllOverlay = document.getElementById('btn-apply-all-overlay');

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

    function openOverlayModal(slide) {
        if (!slide) return;
        activeEditingSlide = slide;

        if (!slide.overlay) {
            slide.overlay = createDefaultOverlay(slide.text, slide.motion, slide.transition);
        }
        // Ensure text is synced
        slide.overlay.text = slide.text !== undefined ? slide.text : (slide.overlay.text || '');

        const o = slide.overlay;
        const idx = state.slides.indexOf(slide);

        if (modalSlideBadge) modalSlideBadge.textContent = `Slide #${idx + 1}`;
        if (modalOverlayEnabled) modalOverlayEnabled.checked = o.enabled !== false;
        if (modalOverlayText) modalOverlayText.value = o.text || '';

        updatePosGridUI(o.position || 'bottom-center');

        if (modalPosX) modalPosX.value = o.customX ?? 50;
        if (modalPosY) modalPosY.value = o.customY ?? 85;
        if (customCoordsVal) customCoordsVal.textContent = `${o.customX ?? 50}%, ${o.customY ?? 85}%`;

        updateTextAlignUI(o.textAlign || 'center');

        if (modalFontFamily) modalFontFamily.value = o.fontFamily || 'Be Vietnam Pro';
        if (modalFontSize) modalFontSize.value = o.fontSize || 46;
        if (modalFontSizeVal) modalFontSizeVal.textContent = (o.fontSize || 46) + 'px';
        if (modalTextColor) modalTextColor.value = o.color || '#ffffff';

        // Select Bg Style radio
        const bgRadios = document.querySelectorAll('input[name="modal-bg-style"]');
        bgRadios.forEach(r => {
            r.checked = (r.value === (o.bgStyle || 'pill'));
        });

        if (modalBgColor) modalBgColor.value = o.bgColor || '#000000';
        if (modalBgColorLabel) modalBgColorLabel.textContent = o.bgColor || '#000000';

        if (modalTextAnimation) modalTextAnimation.value = o.animation || 'fade';
        if (modalSlideMotion) modalSlideMotion.value = slide.motion || slide.transition || 'kenburns';
        if (modalSlideTransition) modalSlideTransition.value = slide.transition || 'crossfade';

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
        updateSlidesUI();
    }

    function syncModalToSlide() {
        if (!activeEditingSlide || !activeEditingSlide.overlay) return;
        const o = activeEditingSlide.overlay;

        if (modalOverlayEnabled) o.enabled = modalOverlayEnabled.checked;
        if (modalOverlayText) {
            o.text = modalOverlayText.value;
            activeEditingSlide.text = modalOverlayText.value;
            activeEditingSlide.ttsAudioBuffer = null;
            activeEditingSlide.ttsMetadata = null;
        }

        if (modalFontFamily) o.fontFamily = modalFontFamily.value;
        if (modalFontSize) {
            o.fontSize = parseInt(modalFontSize.value, 10) || 46;
            if (modalFontSizeVal) modalFontSizeVal.textContent = o.fontSize + 'px';
        }
        if (modalTextColor) o.color = modalTextColor.value;

        const checkedBg = document.querySelector('input[name="modal-bg-style"]:checked');
        if (checkedBg) o.bgStyle = checkedBg.value;

        if (modalBgColor) {
            o.bgColor = modalBgColor.value;
            if (modalBgColorLabel) modalBgColorLabel.textContent = modalBgColor.value;
        }

        if (modalTextAnimation) o.animation = modalTextAnimation.value;

        if (modalPosX && modalPosY) {
            o.customX = parseInt(modalPosX.value, 10);
            o.customY = parseInt(modalPosY.value, 10);
            if (customCoordsVal) customCoordsVal.textContent = `${o.customX}%, ${o.customY}%`;
        }

        if (modalSlideMotion) {
            activeEditingSlide.motion = modalSlideMotion.value;
            o.motion = modalSlideMotion.value;
        }

        if (modalSlideTransition) {
            activeEditingSlide.transition = modalSlideTransition.value;
            o.transition = modalSlideTransition.value;
        }

        // Live preview redraw
        videoRenderer.renderFrame(videoRenderer.currentTime);
    }

    function updatePosGridUI(pos) {
        if (!activeEditingSlide || !activeEditingSlide.overlay) return;
        activeEditingSlide.overlay.position = pos;

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
        if (!activeEditingSlide || !activeEditingSlide.overlay) return;
        activeEditingSlide.overlay.textAlign = align;

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
        const o = activeEditingSlide.overlay;

        o.position = p.position;
        o.customX = p.customX;
        o.customY = p.customY;
        o.textAlign = p.textAlign;
        o.fontFamily = p.fontFamily;
        o.fontSize = p.fontSize;
        o.color = p.color;
        o.bgStyle = p.bgStyle;
        o.bgColor = p.bgColor;
        o.animation = p.animation;

        updatePosGridUI(o.position);
        updateTextAlignUI(o.textAlign);

        if (modalPosX) modalPosX.value = o.customX;
        if (modalPosY) modalPosY.value = o.customY;
        if (customCoordsVal) customCoordsVal.textContent = `${o.customX}%, ${o.customY}%`;

        if (modalFontFamily) modalFontFamily.value = o.fontFamily;
        if (modalFontSize) modalFontSize.value = o.fontSize;
        if (modalFontSizeVal) modalFontSizeVal.textContent = o.fontSize + 'px';
        if (modalTextColor) modalTextColor.value = o.color;

        const bgRadios = document.querySelectorAll('input[name="modal-bg-style"]');
        bgRadios.forEach(r => { r.checked = (r.value === o.bgStyle); });

        if (modalBgColor) modalBgColor.value = o.bgColor;
        if (modalBgColorLabel) modalBgColorLabel.textContent = o.bgColor;

        if (modalTextAnimation) modalTextAnimation.value = o.animation;

        syncModalToSlide();
    }

    // Modal Events Binding
    btnCloseOverlayModal?.addEventListener('click', closeOverlayModal);
    btnSaveOverlay?.addEventListener('click', closeOverlayModal);

    modalOverlayEnabled?.addEventListener('change', syncModalToSlide);
    modalOverlayText?.addEventListener('input', syncModalToSlide);
    modalFontFamily?.addEventListener('change', syncModalToSlide);
    modalFontSize?.addEventListener('input', syncModalToSlide);
    modalTextColor?.addEventListener('input', syncModalToSlide);
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
            if (modalTextColor) {
                modalTextColor.value = color;
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
        if (!activeEditingSlide || !activeEditingSlide.overlay) return;
        const src = activeEditingSlide.overlay;

        state.slides.forEach(slide => {
            if (!slide.overlay) {
                slide.overlay = createDefaultOverlay(slide.text);
            }
            slide.overlay.enabled = src.enabled;
            slide.overlay.position = src.position;
            slide.overlay.customX = src.customX;
            slide.overlay.customY = src.customY;
            slide.overlay.textAlign = src.textAlign;
            slide.overlay.fontFamily = src.fontFamily;
            slide.overlay.fontSize = src.fontSize;
            slide.overlay.color = src.color;
            slide.overlay.bgStyle = src.bgStyle;
            slide.overlay.bgColor = src.bgColor;
            slide.overlay.animation = src.animation;

            slide.motion = activeEditingSlide.motion;
            slide.transition = activeEditingSlide.transition;
            slide.overlay.motion = slide.motion;
            slide.overlay.transition = slide.transition;
        });

        updateSlidesUI();
        videoRenderer.renderFrame(videoRenderer.currentTime);
        alert(`Đã áp dụng mẫu chữ & hiệu ứng cho toàn bộ ${state.slides.length} slide!`);
    });

    // Render Slide Cards in Timeline
    function updateSlidesUI() {
        slidesContainer.innerHTML = '';
        const totalSlides = state.slides.length;
        const totalDur = state.slides.reduce((acc, s) => acc + (s.duration || 3.5), 0);

        timelineStatsEl.textContent = `${totalSlides} ảnh • ${totalDur.toFixed(1)} giây`;
        totalSlidesCountEl.textContent = totalSlides;

        if (totalSlides === 0) {
            emptyState.classList.remove('hidden');
            previewSlideBadge.classList.add('hidden');
        } else {
            emptyState.classList.add('hidden');
            previewSlideBadge.classList.remove('hidden');
        }

        state.slides.forEach((slide, idx) => {
            // Ensure overlay exists
            if (!slide.overlay) {
                slide.overlay = createDefaultOverlay(slide.text, slide.motion, slide.transition);
            }

            const card = document.createElement('div');
            card.className = 'slide-card group flex flex-col justify-between p-2.5';
            card.dataset.id = slide.id;

            const bgStyleName = slide.overlay.bgStyle || 'pill';
            const animName = slide.overlay.animation || 'fade';

            card.innerHTML = `
                <!-- Top thumbnail preview & badge -->
                <div class="relative w-full h-20 rounded-lg overflow-hidden bg-slate-900 mb-1.5 border border-slate-700/60 shrink-0">
                    <img src="${slide.imageSrc}" class="w-full h-full object-cover pointer-events-none">
                    <span class="absolute top-1 left-1 px-1.5 py-0.5 rounded bg-black/70 text-[10px] font-bold text-white">#${idx + 1}</span>
                    <button class="btn-delete-slide absolute top-1 right-1 w-6 h-6 rounded bg-black/70 hover:bg-rose-600 text-slate-300 hover:text-white flex items-center justify-center transition">
                        <i data-lucide="trash" class="w-3.5 h-3.5"></i>
                    </button>
                    ${slide.text ? '<span class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-emerald-500/90 text-[9px] font-bold text-white flex items-center gap-0.5"><i data-lucide="mic" class="w-2.5 h-2.5"></i> Giọng đọc</span>' : ''}
                </div>

                <!-- Action Button: Open Text Overlay & Effects Editor -->
                <button type="button" class="btn-edit-slide-overlay w-full py-1.5 px-2 bg-gradient-to-r from-brand-600/30 to-indigo-600/30 hover:from-brand-600 hover:to-indigo-600 border border-brand-500/40 text-brand-200 hover:text-white rounded-lg text-[10px] font-semibold flex items-center justify-between transition shadow-sm mb-1.5" title="Chỉnh sửa chữ, kiểu dáng & hiệu ứng">
                    <span class="flex items-center gap-1"><i data-lucide="sparkles" class="w-3 h-3 text-amber-400"></i> Sửa Chữ & Hiệu ứng</span>
                    <span class="text-[9px] font-mono text-indigo-300 opacity-90">${bgStyleName} · ${animName}</span>
                </button>

                <!-- Slide Text Prompt / Captions -->
                <div class="space-y-1.5 flex-1 flex flex-col justify-between">
                    <div class="relative">
                        <textarea class="slide-text-input w-full bg-slate-900/90 border border-slate-700/80 rounded-lg p-1.5 text-[11px] text-white placeholder-slate-500 resize-none focus:ring-1 focus:ring-brand-500 outline-none h-12" placeholder="Nhập lời thoại / chữ hiển thị...">${slide.text || ''}</textarea>
                    </div>

                    <!-- Per-slide motion effect -->
                    <select class="slide-effect-select w-full bg-slate-900 border border-slate-700 rounded px-1.5 py-1 text-[10px] text-indigo-200 focus:ring-1 focus:ring-brand-500 outline-none" title="Chuyển động trong ảnh">
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

            const textInput = card.querySelector('.slide-text-input');
            textInput.addEventListener('input', (e) => {
                slide.text = e.target.value;
                if (slide.overlay) slide.overlay.text = e.target.value;
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
                if (slide.overlay) slide.overlay.motion = e.target.value;
                videoRenderer.renderFrame(videoRenderer.currentTime);
            });

            const btnDelete = card.querySelector('.btn-delete-slide');
            btnDelete.addEventListener('click', (e) => {
                e.stopPropagation();
                state.slides = state.slides.filter(s => s.id !== slide.id);
                updateSlidesUI();
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
            });

            slidesContainer.appendChild(card);
        });

        refreshIcons();
    }

    // 9. Video Renderer Event Listeners & Player Controls
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

    videoRenderer.onPlaybackEnded = () => {
        playPauseIcon.setAttribute('data-lucide', 'play');
        refreshIcons();
    };

    btnPlayPause.addEventListener('click', async () => {
        await audioMixer.init();
        if (videoRenderer.isPlaying) {
            videoRenderer.pause();
            playPauseIcon.setAttribute('data-lucide', 'play');
        } else {
            videoRenderer.play();
            playPauseIcon.setAttribute('data-lucide', 'pause');
        }
        refreshIcons();
    });

    btnRestart.addEventListener('click', () => {
        videoRenderer.seek(0);
    });

    playerScrubber.addEventListener('input', (e) => {
        const percent = parseFloat(e.target.value);
        const targetTime = (percent / 100) * videoRenderer.totalDuration;
        videoRenderer.seek(targetTime);
    });

    btnToggleMute.addEventListener('click', () => {
        state.isMuted = !state.isMuted;
        audioMixer.setMute(state.isMuted);
        muteIcon.setAttribute('data-lucide', state.isMuted ? 'volume-x' : 'volume-2');
        refreshIcons();
    });

    // 10. Sample Demo Project Loader
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
                    text: 'CHÀO MỪNG BẠN ĐẾN VỚI\nSTUDIO LÀM VIDEO AI BÀI GIẢNG',
                    motion: 'kenburns',
                    transition: 'crossfade',
                    overlay: {
                        enabled: true,
                        text: 'CHÀO MỪNG BẠN ĐẾN VỚI\nSTUDIO LÀM VIDEO AI BÀI GIẢNG',
                        position: 'center',
                        customX: 50,
                        customY: 50,
                        textAlign: 'center',
                        fontFamily: 'Oswald',
                        fontSize: 58,
                        color: '#fde047',
                        bgStyle: 'shadow',
                        bgColor: '#000000',
                        animation: 'pop',
                        motion: 'kenburns',
                        transition: 'crossfade'
                    }
                },
                {
                    id: 'sample_2',
                    imageSrc: img2,
                    imageElement: loadedImg2,
                    duration: 4.5,
                    text: 'Tùy biến hiệu ứng chuyển động Ken Burns và chuyển cảnh nối tiếp đa dạng cho từng phân cảnh.',
                    motion: 'pan-left',
                    transition: 'slide-left',
                    overlay: {
                        enabled: true,
                        text: 'Tùy biến hiệu ứng chuyển động Ken Burns và chuyển cảnh nối tiếp đa dạng cho từng phân cảnh.',
                        position: 'bottom-center',
                        customX: 50,
                        customY: 85,
                        textAlign: 'center',
                        fontFamily: 'Be Vietnam Pro',
                        fontSize: 44,
                        color: '#ffffff',
                        bgStyle: 'pill',
                        bgColor: '#000000',
                        animation: 'slide-up',
                        motion: 'pan-left',
                        transition: 'slide-left'
                    }
                },
                {
                    id: 'sample_3',
                    imageSrc: img3,
                    imageElement: loadedImg3,
                    duration: 4.8,
                    text: 'LỒNG TIẾNG AI CHUẨN XÁC\nĐồng bộ âm thanh và chữ nghệ thuật rực rỡ.',
                    motion: 'orbit-left',
                    transition: 'circle-reveal',
                    overlay: {
                        enabled: true,
                        text: 'LỒNG TIẾNG AI CHUẨN XÁC\nĐồng bộ âm thanh và chữ nghệ thuật rực rỡ.',
                        position: 'center',
                        customX: 50,
                        customY: 50,
                        textAlign: 'center',
                        fontFamily: 'Montserrat',
                        fontSize: 50,
                        color: '#ffffff',
                        bgStyle: 'neon',
                        bgColor: '#38bdf8',
                        animation: 'glow',
                        motion: 'orbit-left',
                        transition: 'circle-reveal'
                    }
                },
                {
                    id: 'sample_4',
                    imageSrc: img4,
                    imageElement: loadedImg4,
                    duration: 4.5,
                    text: 'Xuất video Full HD MP4 / WebM siêu nét, sẵn sàng chia sẻ ngay hôm nay!',
                    motion: 'zoom-in',
                    transition: 'crossfade',
                    overlay: {
                        enabled: true,
                        text: 'Xuất video Full HD MP4 / WebM siêu nét, sẵn sàng chia sẻ ngay hôm nay!',
                        position: 'bottom-center',
                        customX: 50,
                        customY: 84,
                        textAlign: 'center',
                        fontFamily: 'Playfair Display',
                        fontSize: 46,
                        color: '#ffffff',
                        bgStyle: 'gradient-banner',
                        bgColor: '#0f172a',
                        animation: 'slide-up',
                        motion: 'zoom-in',
                        transition: 'crossfade'
                    }
                }
            ];

            // Load preset ambient music
            const tuneInfo = await audioMixer.generatePresetTune('ambient', 30);
            showMusicLoaded(tuneInfo.name, tuneInfo.duration);

            updateSlidesUI();
            videoRenderer.setSlides(state.slides);
            videoRenderer.seek(0);

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
