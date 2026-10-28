/**
 * Challenge Engine JS for Flag Submission, Ciphertext Clipboard,
 * Progressive 3-Tier Hints, and Success Spell Animations.
 */
class GrimoireChallengeEngine {
    constructor() {
        this.chapterId = null;
    }

    init(chapterId) {
        this.chapterId = chapterId;
        this.bindEvents();
    }

    bindEvents() {
        const submitForm = document.getElementById('flag-submit-form');
        if (submitForm) {
            submitForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitFlag();
            });
        }

        const copyBtn = document.getElementById('btn-copy-ciphertext');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => this.copyCiphertext());
        }
    }

    copyCiphertext() {
        const ctText = document.getElementById('ciphertext-raw')?.innerText;
        if (ctText) {
            navigator.clipboard.writeText(ctText.trim()).then(() => {
                const btn = document.getElementById('btn-copy-ciphertext');
                if (btn) {
                    const orig = btn.innerText;
                    btn.innerText = 'COPIED! ✓';
                    setTimeout(() => btn.innerText = orig, 2000);
                }
            });
        }
    }

    async submitFlag() {
        const flagInput = document.getElementById('flag-input-field');
        const statusMsg = document.getElementById('submission-status-msg');
        if (!flagInput) return;

        const submittedFlag = flagInput.value.strip ? flagInput.value.strip() : flagInput.value.trim();
        if (!submittedFlag) {
            if (statusMsg) {
                statusMsg.innerText = '⚠️ Please enter a flag solution.';
                statusMsg.className = 'status-alert warning';
            }
            return;
        }

        if (window.soundEngine) window.soundEngine.playSpellCast();

        try {
            const resp = await fetch('/api/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chapter_id: this.chapterId,
                    flag: submittedFlag
                })
            });

            const data = await resp.json();

            if (data.is_correct) {
                if (window.soundEngine) window.soundEngine.playSuccessChime();
                this.triggerSuccessAnimation(data);
            } else {
                if (window.soundEngine) window.soundEngine.playFailureSound();
                this.triggerFailureAnimation(data.message);
            }
        } catch (err) {
            console.error('Submission error:', err);
            if (statusMsg) {
                statusMsg.innerText = 'Server error during spell verification.';
            }
        }
    }

    triggerSuccessAnimation(data) {
        const modal = document.getElementById('spell-unlock-modal');
        const spellTitle = document.getElementById('unlocked-spell-title');
        const spellDesc = document.getElementById('unlocked-spell-desc');
        const nextBtn = document.getElementById('btn-proceed-next-ch');

        if (spellTitle) spellTitle.innerText = data.spell_unlocked.name;
        if (spellDesc) spellDesc.innerText = data.spell_unlocked.description;

        if (nextBtn) {
            nextBtn.onclick = () => {
                if (data.is_final_victory) {
                    window.location.href = '/archive';
                } else {
                    window.location.href = `/chapter/${data.next_chapter}`;
                }
            };
        }

        if (modal) {
            modal.style.display = 'flex';
        }
    }

    triggerFailureAnimation(msg) {
        const statusMsg = document.getElementById('submission-status-msg');
        const container = document.querySelector('.grimoire-artifact-box');

        if (container) {
            container.classList.add('shake-recoil');
            setTimeout(() => container.classList.remove('shake-recoil'), 600);
        }

        if (statusMsg) {
            statusMsg.innerText = `❌ ${msg}`;
            statusMsg.className = 'status-alert failure';
        }
    }

    async requestHint(hintIndex) {
        try {
            const resp = await fetch('/api/hint', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chapter_id: this.chapterId,
                    hint_index: hintIndex
                })
            });

            const data = await resp.json();
            if (data.status === 'success') {
                const hintContainer = document.getElementById(`hint-content-${hintIndex}`);
                const hintBtn = document.getElementById(`btn-hint-${hintIndex}`);
                if (hintContainer) {
                    hintContainer.innerText = data.hint.text;
                    hintContainer.style.display = 'block';
                }
                if (hintBtn) {
                    hintBtn.disabled = true;
                    hintBtn.innerText = `HINT ${hintIndex} UNLOCKED ✓`;
                }
            }
        } catch (e) {
            console.error('Hint error:', e);
        }
    }
}

window.challengeEngine = new GrimoireChallengeEngine();
