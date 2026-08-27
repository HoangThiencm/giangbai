/**
 * Audio Mixer - Web Audio API management for BGM & Voiceover mixing
 */

class AudioMixer {
    constructor() {
        this.ctx = null;
        this.bgmBuffer = null;
        this.bgmSourceNode = null;
        this.bgmGainNode = null;
        this.voiceGainNode = null;
        this.masterGainNode = null;
        this.destNode = null; // MediaStreamDestination for video recording

        this.bgmVolume = 0.4; // 0.0 to 1.0
        this.isDuckingEnabled = true;
        this.isLoopEnabled = true;
        this.isMuted = false;

        this.activeVoiceSources = [];
        this.isPlaying = false;
        this.startTime = 0;
        this.pauseOffset = 0;
    }

    /**
     * Ensure AudioContext is created and running
     */
    async init() {
        if (!this.ctx) {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContextClass();

            // Gain nodes
            this.masterGainNode = this.ctx.createGain();
            this.bgmGainNode = this.ctx.createGain();
            this.voiceGainNode = this.ctx.createGain();

            // Output destination node for MediaRecorder
            this.destNode = this.ctx.createMediaStreamDestination();

            // Connect graph
            this.bgmGainNode.connect(this.masterGainNode);
            this.voiceGainNode.connect(this.masterGainNode);

            // Connect to speakers and recording stream
            this.masterGainNode.connect(this.ctx.destination);
            this.masterGainNode.connect(this.destNode);

            this.setBgmVolume(this.bgmVolume);
        }

        if (this.ctx.state === 'suspended') {
            await this.ctx.resume();
        }

        return this.ctx;
    }

    getStream() {
        return this.destNode ? this.destNode.stream : null;
    }

    /**
     * Load an audio file (MP3/WAV) from File or Blob
     */
    async loadBgmFromFile(file) {
        await this.init();
        const arrayBuffer = await Utils.fileToArrayBuffer(file);
        this.bgmBuffer = await this.ctx.decodeAudioData(arrayBuffer);
        return {
            name: file.name,
            duration: this.bgmBuffer.duration
        };
    }

    /**
     * Generate synthetic background music presets (Ambient chill or Upbeat)
     */
    async generatePresetTune(type = 'ambient', duration = 30) {
        await this.init();
        const sampleRate = this.ctx.sampleRate;
        const length = sampleRate * duration;
        const buffer = this.ctx.createBuffer(2, length, sampleRate);
        const left = buffer.getChannelData(0);
        const right = buffer.getChannelData(1);

        if (type === 'ambient') {
            // Calming chord progression: Cmaj7 - Am7 - Fmaj7 - G
            const baseFreqs = [261.63, 220.0, 174.61, 196.0];
            for (let i = 0; i < length; i++) {
                const t = i / sampleRate;
                const chordIdx = Math.floor((t % 16) / 4);
                const baseF = baseFreqs[chordIdx];
                
                // Multi-harmonic soft chime
                const note1 = Math.sin(2 * Math.PI * baseF * t) * 0.15;
                const note2 = Math.sin(2 * Math.PI * (baseF * 1.25) * t) * 0.1;
                const note3 = Math.sin(2 * Math.PI * (baseF * 1.5) * t) * 0.08;
                const note4 = Math.sin(2 * Math.PI * (baseF * 1.875) * t) * 0.05;
                
                // Slow envelope & pan
                const env = (Math.sin(t * Math.PI * 0.5) + 1) * 0.5;
                const wave = (note1 + note2 + note3 + note4) * (0.6 + 0.4 * env);
                
                left[i] = wave * (0.8 + 0.2 * Math.sin(t * 0.5));
                right[i] = wave * (0.8 + 0.2 * Math.cos(t * 0.5));
            }
        } else {
            // Upbeat acoustic beat / rhythm
            for (let i = 0; i < length; i++) {
                const t = i / sampleRate;
                const beat = (t * 2) % 1; // 120 BPM
                const bassF = 110 + (Math.floor(t * 2) % 4) * 20;
                
                const bass = Math.sin(2 * Math.PI * bassF * t) * Math.exp(-beat * 4) * 0.25;
                const melody = Math.sin(2 * Math.PI * (bassF * 2) * t) * 0.1;
                const noise = (Math.random() * 2 - 1) * Math.exp(-((beat + 0.5) % 1) * 20) * 0.08; // hi-hat
                
                const wave = bass + melody + noise;
                left[i] = wave;
                right[i] = wave;
            }
        }

        this.bgmBuffer = buffer;
        return {
            name: type === 'ambient' ? 'Ambient Chill Synth' : 'Upbeat Vlog Beat',
            duration: duration
        };
    }

    setBgmVolume(val) {
        this.bgmVolume = Math.max(0, Math.min(1, val));
        if (this.bgmGainNode && !this.isMuted) {
            this.bgmGainNode.gain.setValueAtTime(this.bgmVolume, this.ctx ? this.ctx.currentTime : 0);
        }
    }

    setMute(isMuted) {
        this.isMuted = isMuted;
        if (this.masterGainNode && this.ctx) {
            this.masterGainNode.gain.setValueAtTime(isMuted ? 0 : 1, this.ctx.currentTime);
        }
    }

    /**
     * Start playing BGM and timeline voice tracks at a given timeline offset
     */
    playTimeline(slides, startTimelineSec = 0) {
        this.stopAll();
        if (!this.ctx) return;

        this.isPlaying = true;
        this.pauseOffset = startTimelineSec;
        this.startTime = this.ctx.currentTime - startTimelineSec;

        // 1. Play BGM if available
        if (this.bgmBuffer) {
            this.bgmSourceNode = this.ctx.createBufferSource();
            this.bgmSourceNode.buffer = this.bgmBuffer;
            this.bgmSourceNode.loop = this.isLoopEnabled;
            this.bgmSourceNode.connect(this.bgmGainNode);

            const bgmOffset = this.isLoopEnabled ? (startTimelineSec % this.bgmBuffer.duration) : startTimelineSec;
            if (bgmOffset < this.bgmBuffer.duration) {
                this.bgmSourceNode.start(0, bgmOffset);
            }
        }

        // 2. Schedule Voiceovers for each slide
        let currentSlideStart = 0;
        slides.forEach((slide) => {
            const slideDur = slide.duration || 3.5;
            const slideEnd = currentSlideStart + slideDur;

            if (slide.ttsAudioBuffer && slideEnd > startTimelineSec) {
                const voiceSource = this.ctx.createBufferSource();
                voiceSource.buffer = slide.ttsAudioBuffer;
                voiceSource.connect(this.voiceGainNode);

                let whenToStart = 0;
                let bufferOffset = 0;

                if (currentSlideStart >= startTimelineSec) {
                    whenToStart = this.ctx.currentTime + (currentSlideStart - startTimelineSec);
                    bufferOffset = 0;
                } else {
                    whenToStart = this.ctx.currentTime;
                    bufferOffset = startTimelineSec - currentSlideStart;
                }

                if (bufferOffset < slide.ttsAudioBuffer.duration) {
                    voiceSource.start(whenToStart, bufferOffset);
                    this.activeVoiceSources.push(voiceSource);

                    // Apply ducking automation to BGM
                    if (this.isDuckingEnabled && this.bgmGainNode) {
                        const duckTime = whenToStart;
                        const restoreTime = duckTime + (slide.ttsAudioBuffer.duration - bufferOffset);
                        const duckedVol = this.bgmVolume * 0.25;

                        this.bgmGainNode.gain.setValueAtTime(this.bgmVolume, duckTime);
                        this.bgmGainNode.gain.linearRampToValueAtTime(duckedVol, duckTime + 0.15);
                        this.bgmGainNode.gain.setValueAtTime(duckedVol, restoreTime);
                        this.bgmGainNode.gain.linearRampToValueAtTime(this.bgmVolume, restoreTime + 0.3);
                    }
                }
            }

            currentSlideStart = slideEnd;
        });
    }

    /**
     * Stop all audio sources
     */
    stopAll() {
        this.isPlaying = false;
        if (this.bgmSourceNode) {
            try {
                this.bgmSourceNode.stop();
                this.bgmSourceNode.disconnect();
            } catch (e) {}
            this.bgmSourceNode = null;
        }

        this.activeVoiceSources.forEach(src => {
            try {
                src.stop();
                src.disconnect();
            } catch (e) {}
        });
        this.activeVoiceSources = [];

        if (this.bgmGainNode && this.ctx) {
            this.bgmGainNode.gain.cancelScheduledValues(this.ctx.currentTime);
            this.bgmGainNode.gain.setValueAtTime(this.bgmVolume, this.ctx.currentTime);
        }
    }
}

window.AudioMixer = AudioMixer;
