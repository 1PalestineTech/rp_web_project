// modules/stories.js
import { animate } from '../utils/animations.js';
import { helpers } from '../utils/helpers.js';

export class StoriesManager {
    constructor() {
        this.stories = [
            {
                id: 'palestinian-culture',
                title: 'Palestinian Cultural Heritage',
                content: 'The rich cultural heritage of Palestine spans thousands of years...',
                images: [/* Array of image objects */],
                category: 'culture'
            },
            // Add more stories
        ];

        this.init();
    }

    init() {
        this.container = document.querySelector('.stories-container');
        if (!this.container) return;

        this.setupStories();
        this.setupEventListeners();
        this.renderStories();
    }

    setupStories() {
        this.storiesGrid = document.createElement('div');
        this.storiesGrid.className = 'stories-grid';
        this.container.appendChild(this.storiesGrid);
    }

    setupEventListeners() {
        // Story navigation
        document.querySelectorAll('.story-nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const direction = e.target.dataset.direction;
                this.navigateStories(direction);
            });
        });
    }

    renderStories() {
        if (!this.storiesGrid) return;

        this.storiesGrid.innerHTML = '';
        const fragment = document.createDocumentFragment();

        this.stories.forEach(story => {
            const storyElement = this.createStoryElement(story);
            fragment.appendChild(storyElement);
        });

        this.storiesGrid.appendChild(fragment);
        animate.fadeIn(this.storiesGrid);
    }

    createStoryElement(story) {
        const element = document.createElement('div');
        element.className = 'story-card';
        element.innerHTML = `
            <div class="story-header">
                <h3>${story.title}</h3>
            </div>
            <div class="story-content">
                <p>${helpers.truncateText(story.content, 200)}</p>
            </div>
            <div class="story-footer">
                <button class="read-story-btn" data-story-id="${story.id}">
                    Read Full Story
                </button>
            </div>
        `;

        element.querySelector('.read-story-btn').addEventListener('click', () => {
            this.openStory(story.id);
        });

        return element;
    }

    openStory(storyId) {
        const story = this.stories.find(s => s.id === storyId);
        if (!story) return;

        const modal = document.createElement('div');
        modal.className = 'story-modal';
        modal.innerHTML = `
            <div class="story-modal-content">
                <button class="modal-close">&times;</button>
                <h2>${story.title}</h2>
                <div class="story-full-content">${story.content}</div>
                <div class="story-gallery"></div>
            </div>
        `;

        document.body.appendChild(modal);
        animate.zoomIn(modal.querySelector('.story-modal-content'));

        modal.querySelector('.modal-close').addEventListener('click', () => {
            animate.fadeOut(modal, () => modal.remove());
        });
    }

    navigateStories(direction) {
        // Implement story navigation logic
    }
}