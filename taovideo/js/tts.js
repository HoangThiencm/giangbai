/* Browser-only V-TTS ONNX pipeline (V-TTS upstream, CC BY-NC 4.0). */
class TTSEngine {
    constructor() {
        this.sessions = {}; this.config = null; this.ready = false; this.loading = null; this.onStatus = null;
        this.voices = [
            { id: 'NF', name: 'NF', region: 'Miền Bắc', gender: 'Nữ', speakerId: 0 },
            { id: 'SF', name: 'SF', region: 'Miền Nam', gender: 'Nữ', speakerId: 1 },
            { id: 'NM1', name: 'NM1', region: 'Miền Bắc', gender: 'Nam', speakerId: 2 },
            { id: 'SM', name: 'SM', region: 'Miền Nam', gender: 'Nam', speakerId: 3 },
            { id: 'NM2', name: 'NM2', region: 'Miền Bắc', gender: 'Nam', speakerId: 4 }
        ];
    }
    getPresetVoices() { return this.voices; }
    emit(message, progress = null, error = false) { this.onStatus?.({ message, progress, error, ready: this.ready }); }
    async load() {
        if (this.ready) return;
        if (!this.loading) this.loading = this.loadInternal().finally(() => { this.loading = null; });
        return this.loading;
    }
    async loadInternal() {
        if (location.protocol === 'file:') throw new Error('V-TTS cần mở qua website GiangBai bằng HTTP(S), không mở trực tiếp file HTML.');
        if (!window.ort || !window.VietnameseG2P) throw new Error('Thiếu ONNX Runtime Web hoặc V-TTS G2P.');
        ort.env.wasm.wasmPaths = 'assets/vtts/ort/';
        const models = ['text_encoder', 'duration_predictor', 'flow', 'decoder'];
        for (let i = 0; i < models.length; i++) {
            this.emit(`Đang tải ${models[i]}.onnx…`, i * 22);
            this.sessions[models[i]] = await ort.InferenceSession.create(`assets/vtts/models/${models[i]}.onnx`, { executionProviders: ['wasm'] });
        }
        this.emit('Đang tải cấu hình V-TTS…', 92);
        const response = await fetch('assets/vtts/tts_config.json');
        if (!response.ok) throw new Error('Thiếu tts_config.json hoặc bộ model V-TTS.');
        this.config = await response.json(); this.ready = true; this.emit('V-TTS sẵn sàng trên thiết bị này.', 100);
    }
    async synthesize(text, voiceId, rate = 1) {
        const clean = (text || '').trim().replace(/[\r\n]+/g, ' ');
        if (!clean) throw new Error('Hãy nhập lời thoại trước.');
        await this.load();
        const voice = this.voices.find(v => v.id === voiceId) || this.voices[0];
        const raw = VietnameseG2P.textToPhonemes(clean, this.config.symbol_to_id, this.config.language_id_map.VI);
        const seq = VietnameseG2P.addBlanks(raw, this.config.language_id_map.VI), n = seq.phonemes.length;
        if (!n) throw new Error('Không thể chuyển lời thoại sang âm vị tiếng Việt.');
        const tensor = (type, data, dims) => new ort.Tensor(type, data, dims);
        const i64 = values => new BigInt64Array(values.map(value => BigInt(value)));
        this.emit('Bước 1/4: chuẩn bị âm vị…');
        const input = {
            phone_ids: tensor('int64', i64(seq.phonemes), [1, n]), phone_lengths: tensor('int64', i64([n]), [1]),
            tone_ids: tensor('int64', i64(seq.tones), [1, n]), language_ids: tensor('int64', i64(seq.languages), [1, n]),
            bert: tensor('float32', new Float32Array(1024 * n), [1, 1024, n]), ja_bert: tensor('float32', new Float32Array(768 * n), [1, 768, n]),
            speaker_id: tensor('int64', i64([voice.speakerId]), [1])
        };
        this.emit('Bước 2/4: mã hóa văn bản…');
        const enc = await this.sessions.text_encoder.run(input);
        this.emit('Bước 3/4: dự đoán thời lượng…');
        const dp = await this.sessions.duration_predictor.run({ x: enc.x_encoded, x_mask: enc.x_mask, g: enc.g });
        const speed = Math.max(.5, Math.min(2, Number(rate) || 1));
        const duration = Array.from(dp.logw.data, (v, i) => Math.max(1, Math.ceil(Math.exp(v) * enc.x_mask.data[i] / speed)));
        const frames = duration.reduce((a, b) => a + b, 0), channels = enc.m_p.dims[1];
        const mp = new Float32Array(channels * frames), logs = new Float32Array(channels * frames); let frame = 0;
        for (let t = 0; t < n; t++) for (let d = 0; d < duration[t]; d++, frame++) for (let c = 0; c < channels; c++) {
            mp[c * frames + frame] = enc.m_p.data[c * n + t]; logs[c * frames + frame] = enc.logs_p.data[c * n + t];
        }
        const zp = new Float32Array(channels * frames);
        for (let i = 0; i < zp.length; i++) zp[i] = mp[i] + Math.exp(logs[i]) * ((Math.random() * 2 - 1) * .667);
        this.emit('Bước 4/4: sinh âm thanh…');
        const yMask = tensor('float32', new Float32Array(frames).fill(1), [1, 1, frames]);
        const flow = await this.sessions.flow.run({ z_p: tensor('float32', zp, [1, channels, frames]), y_mask: yMask, g: enc.g });
        const decoded = await this.sessions.decoder.run({ z: flow.z, g: enc.g });
        const samples = new Float32Array(decoded.audio.data), sampleRate = this.config.sample_rate;
        const context = new (window.AudioContext || window.webkitAudioContext)({ sampleRate });
        const buffer = context.createBuffer(1, samples.length, sampleRate); buffer.copyToChannel(samples, 0); await context.close();
        this.emit(`Đã tạo WAV ${buffer.duration.toFixed(1)} giây.`);
        return { buffer, wav: this.toWav(samples, sampleRate), duration: buffer.duration, voice };
    }
    toWav(samples, sampleRate) {
        const bytes = new ArrayBuffer(44 + samples.length * 2), view = new DataView(bytes);
        const write = (at, text) => [...text].forEach((ch, i) => view.setUint8(at + i, ch.charCodeAt(0)));
        write(0, 'RIFF'); view.setUint32(4, 36 + samples.length * 2, true); write(8, 'WAVE'); write(12, 'fmt ');
        view.setUint32(16, 16, true); view.setUint16(20, 1, true); view.setUint16(22, 1, true); view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true); view.setUint16(32, 2, true); view.setUint16(34, 16, true); write(36, 'data'); view.setUint32(40, samples.length * 2, true);
        samples.forEach((sample, i) => view.setInt16(44 + i * 2, Math.max(-1, Math.min(1, sample)) * (sample < 0 ? 0x8000 : 0x7fff), true));
        return new Blob([bytes], { type: 'audio/wav' });
    }
}
window.TTSEngine = TTSEngine;
