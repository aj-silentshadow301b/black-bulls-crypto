/**
 * Dynamic HTML5 Canvas Mana Particle Engine.
 * Renders floating mana particles, magical runes, glowing embers, and spell aura effects.
 */
class ManaParticleEngine {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.runes = ['✦', '✧', '★', '⚙', '⚖', '☯', '✵', '🔮', '⚡', '🌀'];
        this.numParticles = 50;
        this.animFrameId = null;

        this.init();
    }

    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());

        for (let i = 0; i < this.numParticles; i++) {
            this.particles.push(this.createParticle());
        }

        this.animate();
    }

    resize() {
        if (!this.canvas) return;
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticle() {
        const isRune = Math.random() < 0.2;
        return {
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            size: isRune ? Math.random() * 12 + 10 : Math.random() * 3 + 1,
            speedY: (Math.random() * 0.8 + 0.2) * -1,
            speedX: (Math.random() - 0.5) * 0.4,
            opacity: Math.random() * 0.7 + 0.2,
            maxOpacity: Math.random() * 0.8 + 0.3,
            fadeSpeed: Math.random() * 0.01 + 0.005,
            color: Math.random() < 0.6 ? 'rgba(255, 215, 0, ' : (Math.random() < 0.5 ? 'rgba(138, 43, 226, ' : 'rgba(77, 238, 234, '),
            isRune: isRune,
            runeChar: this.runes[Math.floor(Math.random() * this.runes.length)]
        };
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        for (let i = 0; i < this.particles.length; i++) {
            let p = this.particles[i];
            p.y += p.speedY;
            p.x += p.speedX;

            if (p.y < -20 || p.x < -20 || p.x > this.canvas.width + 20) {
                this.particles[i] = this.createParticle();
                this.particles[i].y = this.canvas.height + 20;
            }

            this.ctx.fillStyle = p.color + p.opacity + ')';
            
            if (p.isRune) {
                this.ctx.font = `${p.size}px 'Cinzel', serif`;
                this.ctx.fillText(p.runeChar, p.x, p.y);
            } else {
                this.ctx.beginPath();
                this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                this.ctx.fill();
            }
        }

        this.animFrameId = requestAnimationFrame(() => this.animate());
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.manaParticles = new ManaParticleEngine('particle-canvas');
});
