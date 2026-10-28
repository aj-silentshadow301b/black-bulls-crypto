/**
 * Main JS Bootstrap for Black Bulls Crypto Grimoire.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Sound Toggle Button
    const soundBtn = document.getElementById('sound-toggle-btn');
    if (soundBtn) {
        soundBtn.addEventListener('click', () => {
            if (window.soundEngine) {
                const isMuted = window.soundEngine.toggleMute();
                soundBtn.innerHTML = isMuted ? '🔇 SOUND OFF' : '🔊 SOUND ON';
            }
        });
    }

    // Reset Progress Button
    const resetBtn = document.getElementById('btn-reset-journey');
    if (resetBtn) {
        resetBtn.addEventListener('click', async () => {
            if (confirm('Are you sure you want to reset your Grimoire progress back to Chapter 1?')) {
                try {
                    const resp = await fetch('/api/reset', { method: 'POST' });
                    const res = await resp.json();
                    if (res.status === 'success') {
                        window.location.href = '/grimoire';
                    }
                } catch (e) {
                    console.error('Reset error:', e);
                }
            }
        });
    }

    // Reduced Motion Support
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.body.classList.add('reduced-motion');
        console.log('Reduced motion mode active.');
    }
});
