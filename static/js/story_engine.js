/**
 * Story Engine JS for Black Bulls Cutscene Renderer & Investigation Panel.
 */
class GrimoireStoryEngine {
    constructor() {
        this.currentSceneIdx = 0;
        this.scenes = [];
        this.typewriterTimer = null;
    }

    initCutscene(scenesData) {
        this.scenes = scenesData || [];
        this.currentSceneIdx = 0;
        this.renderCurrentScene();
    }

    renderCurrentScene() {
        if (!this.scenes || this.scenes.length === 0) return;
        
        const scene = this.scenes[this.currentSceneIdx];
        const speakerElem = document.getElementById('speaker-name');
        const textElem = document.getElementById('dialogue-text-body');
        const btnNext = document.getElementById('btn-next-scene');
        const btnPrev = document.getElementById('btn-prev-scene');
        
        if (speakerElem) speakerElem.innerText = scene.speaker || 'Narrator';
        if (textElem) {
            this.typewriterText(textElem, scene.text || '');
        }

        if (btnPrev) {
            btnPrev.style.display = this.currentSceneIdx > 0 ? 'inline-flex' : 'none';
        }
        
        if (btnNext) {
            const isLast = this.currentSceneIdx === this.scenes.length - 1;
            btnNext.innerText = isLast ? 'PROCEED TO CHALLENGE ⚔️' : 'CONTINUE ▶';
        }
    }

    nextScene() {
        if (window.soundEngine) window.soundEngine.playPageFlip();
        if (this.currentSceneIdx < this.scenes.length - 1) {
            this.currentSceneIdx++;
            this.renderCurrentScene();
        } else {
            // Redirect or unveil challenge
            const chapterId = document.getElementById('chapter-story-container')?.dataset?.chapterId;
            if (chapterId) {
                window.location.href = `/challenge/${chapterId}`;
            }
        }
    }

    prevScene() {
        if (window.soundEngine) window.soundEngine.playPageFlip();
        if (this.currentSceneIdx > 0) {
            this.currentSceneIdx--;
            this.renderCurrentScene();
        }
    }

    typewriterText(container, text, speed = 25) {
        if (this.typewriterTimer) clearInterval(this.typewriterTimer);
        container.innerHTML = '';
        let i = 0;
        this.typewriterTimer = setInterval(() => {
            if (i < text.length) {
                container.innerHTML += text.charAt(i);
                i++;
            } else {
                clearInterval(this.typewriterTimer);
            }
        }, speed);
    }
}

window.storyEngine = new GrimoireStoryEngine();
