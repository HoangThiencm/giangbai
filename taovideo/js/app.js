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
        slides: [], // Array of { id, imageSrc, imageElement, duration, text, transition }
        defaultDuration: 3.5,
        defaultTransition: 'kenburns',
        voiceId: '',
        ttsRate: 1.0,
        isMuted: false
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
        videoRenderer.defaultTransition = e.target.value;
        state.slides.forEach(s => s.transition = e.target.value);
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

            const newSlide = {
                id: 'slide_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5),
                imageSrc: dataUrl,
                imageElement: imgEl,
                duration: state.defaultDuration,
                text: '',
                transition: state.defaultTransition
            };

            state.slides.push(newSlide);
        }

        updateSlidesUI();
        videoRenderer.setSlides(state.slides);
    }

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
            const card = document.createElement('div');
            card.className = 'slide-card group flex flex-col justify-between p-2.5';
            card.dataset.id = slide.id;

            card.innerHTML = `
                <!-- Top thumbnail preview & badge -->
                <div class="relative w-full h-24 rounded-lg overflow-hidden bg-slate-900 mb-2 border border-slate-700/60 shrink-0">
                    <img src="${slide.imageSrc}" class="w-full h-full object-cover pointer-events-none">
                    <span class="absolute top-1 left-1 px-1.5 py-0.5 rounded bg-black/70 text-[10px] font-bold text-white">#${idx + 1}</span>
                    <button class="btn-delete-slide absolute top-1 right-1 w-6 h-6 rounded bg-black/70 hover:bg-rose-600 text-slate-300 hover:text-white flex items-center justify-center transition">
                        <i data-lucide="trash" class="w-3.5 h-3.5"></i>
                    </button>
                    ${slide.text ? '<span class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-emerald-500/90 text-[9px] font-bold text-white flex items-center gap-0.5"><i data-lucide="mic" class="w-2.5 h-2.5"></i> Lời thoại</span>' : ''}
                </div>

                <!-- Slide Text Prompt / Captions -->
                <div class="space-y-1.5 flex-1 flex flex-col justify-between">
                    <div class="relative">
                        <textarea class="slide-text-input w-full bg-slate-900/90 border border-slate-700/80 rounded-lg p-1.5 text-[11px] text-white placeholder-slate-500 resize-none focus:ring-1 focus:ring-brand-500 outline-none h-14" placeholder="Nhập lời thoại / phụ đề...">${slide.text || ''}</textarea>
                    </div>

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

    // 8. Playback/export use the V-TTS AudioBuffer tracks in AudioMixer.

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

        // Highlight active slide card
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

    // Play/Pause button
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

    // 9. Sample Demo Project Loader
    const btnLoadSample = document.getElementById('btn-load-sample');
    btnLoadSample.addEventListener('click', async () => {
        btnLoadSample.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Đang nạp...';
        refreshIcons();

        try {
            await audioMixer.init();

            // Generate sample procedural images
            const img1 = Utils.generateSampleImage('Chào Mừng Bạn Đến Với', 'Studio Làm Video AI Tự Động', '#4f46e5', '#9333ea');
            const img2 = Utils.generateSampleImage('Tạo Video Từ Ảnh', 'Hiệu ứng Ken Burns & Chuyển cảnh mượt mà', '#0ea5e9', '#3b82f6');
            const img3 = Utils.generateSampleImage('Lồng Tiếng AI Chuẩn', 'Tự động tính thời lượng khớp từng câu đọc', '#059669', '#10b981');
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
                    duration: 4.2,
                    text: 'Chào mừng bạn đến với Studio tạo video từ hình ảnh và giọng đọc AI ngọt ngào!',
                    transition: 'kenburns'
                },
                {
                    id: 'sample_2',
                    imageSrc: img2,
                    imageElement: loadedImg2,
                    duration: 4.2,
                    text: 'Bạn có thể tải lên ảnh của riêng mình và sắp xếp thứ tự phân cảnh thật dễ dàng.',
                    transition: 'slide'
                },
                {
                    id: 'sample_3',
                    imageSrc: img3,
                    imageElement: loadedImg3,
                    duration: 4.5,
                    text: 'Hệ thống tự động lồng tiếng thuyết minh và đồng bộ chính xác với nhạc nền MP3.',
                    transition: 'kenburns'
                },
                {
                    id: 'sample_4',
                    imageSrc: img4,
                    imageElement: loadedImg4,
                    duration: 4.2,
                    text: 'Nhấn nút Xuất Video để tải về file MP4 chất lượng cao ngay hôm nay!',
                    transition: 'crossfade'
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

    // 10. Export Video Modal Handlers
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

        // Populate summary
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

            // Show success
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
