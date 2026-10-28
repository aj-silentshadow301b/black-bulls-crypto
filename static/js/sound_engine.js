/**
 * Web Audio API Sound Synthesizer for Black Bulls Crypto Grimoire.
 * Generates custom dark-fantasy anime audio cues natively without copyrighted audio assets.
 */
class GrimoireSoundEngine {
    constructor() {
        this.ctx = null;
        this.isMuted = false;
        this.volume = 0.3;
        this.ambientGain = null;
        this.isInitialized = false;
    }

    init() {
        if (this.isInitialized) return;
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
            this.isInitialized = true;
        } catch (e) {
            console.warn("Web Audio API not supported:", e);
        }
    }

    playPageFlip() {
        if (this.isMuted || !this.ctx) return;
        this.init();
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(150, now + 0.08);
        
        gain.gain.setValueAtTime(this.volume * 0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.08);
        
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        osc.start(now);
        osc.stop(now + 0.08);
    }

    playSpellCast() {
        if (this.isMuted || !this.ctx) return;
        this.init();
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(200, now);
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.3);

        gain.gain.setValueAtTime(0.01, now);
        gain.gain.linearRampToValueAtTime(this.volume * 0.5, now + 0.15);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.3);
    }

    playSuccessChime() {
        if (this.isMuted || !this.ctx) return;
        this.init();
        const now = this.ctx.currentTime;
        
        // Triumphant chord (D4, F#4, A4, D5)
        const freqs = [293.66, 369.99, 440.00, 587.33];
        freqs.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, now + idx * 0.06);
            
            gain.gain.setValueAtTime(0.01, now + idx * 0.06);
            gain.gain.linearRampToValueAtTime(this.volume * 0.4, now + idx * 0.06 + 0.05);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
            
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            
            osc.start(now + idx * 0.06);
            osc.stop(now + 1.2);
        });
    }

    playFailureSound() {
        if (this.isMuted || !this.ctx) return;
        this.init();
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.linearRampToValueAtTime(50, now + 0.4);

        gain.gain.setValueAtTime(this.volume * 0.6, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.4);
    }

    toggleMute() {
        this.isMuted = !this.isMuted;
        return this.isMuted;
    }
}

window.soundEngine = new GrimoireSoundEngine();
