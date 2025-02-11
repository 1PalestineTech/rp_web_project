// modules/articles.js
import { animate } from '../utils/animations.js';
import { helpers } from '../utils/helpers.js';

export class ArticlesManager {
    constructor() {
        this.articles = [
            {
                id: 'nakba-1948',
                title: 'The Nakba of 1948',
                summary: 'Understanding the historical events of 1948 and their impact on Palestinian society',
                content: `<p>The Nakba ("catastrophe" in Arabic) marks a pivotal moment in Palestinian history...</p>`,
                date: '1948',
                category: 'historical-events',
                images: [
                    {
                        src: '/images/timeline/1948/nakba-exodus.jpg',
                        caption: 'Palestinian refugees leaving their homes',
                        alt: 'Palestinian families walking with their belongings during the Nakba'
                    }
                ]
            },
            // Add more articles
        ];

        this.init();
    }

    async init() {
        try {
            this.container = document.querySelector('.articles-container');
            if (!this.container) return;

            await this.setupArticles();
            this.setupEventListeners();
            this.renderArticles();
        } catch (error) {
            console.error('Articles initialization error:', error);
        }
    }

    async setupArticles() {
        // Initialize article components
        this.articlesList = document.createElement('div');
        this.articlesList.className = 'articles-list';
        this.container.appendChild(this.articlesList);
    }

    setupEventListeners() {
        // Article filtering and sorting
        document.querySelectorAll('.article-filter').forEach(btn => {
            btn.addEventListener('click', (e) => this.filterArticles(e.target.dataset.category));
        });

        // Article search
        const searchInput = document.querySelector('.article-search');
        if (searchInput) {
            searchInput.addEventListener('input', helpers.debounce((e) => {
                this.searchArticles(e.target.value);
            }, 300));
        }
    }

    renderArticles(articles = this.articles) {
        if (!this.articlesList) return;

        this.articlesList.innerHTML = '';
        const fragment = document.createDocumentFragment();

        articles.forEach(article => {
            const articleElement = this.createArticleElement(article);
            fragment.appendChild(articleElement);
        });

        this.articlesList.appendChild(fragment);
        animate.fadeIn(this.articlesList);
    }

    createArticleElement(article) {
        const element = document.createElement('article');
        element.className = 'article-card';
        element.innerHTML = `
            <div class="article-image">
                <img src="${article.images[0]?.src}" alt="${article.images[0]?.alt}" loading="lazy">
            </div>
            <div class="article-content">
                <h3>${article.title}</h3>
                <p>${helpers.truncateText(article.summary, 150)}</p>
                <span class="article-date">${article.date}</span>
                <button class="read-more" data-article-id="${article.id}">Read More</button>
            </div>
        `;

        element.querySelector('.read-more').addEventListener('click', () => {
            this.openArticle(article.id);
        });

        return element;
    }

    openArticle(articleId) {
        const article = this.articles.find(a => a.id === articleId);
        if (!article) return;

        const modal = document.createElement('div');
        modal.className = 'article-modal';
        modal.innerHTML = `
            <div class="article-modal-content">
                <button class="modal-close">&times;</button>
                <h2>${article.title}</h2>
                <div class="article-full-content">${article.content}</div>
                <div class="article-gallery"></div>
            </div>
        `;

        document.body.appendChild(modal);
        animate.zoomIn(modal.querySelector('.article-modal-content'));

        modal.querySelector('.modal-close').addEventListener('click', () => {
            animate.fadeOut(modal, () => modal.remove());
        });
    }

    filterArticles(category) {
        const filtered = category === 'all' 
            ? this.articles 
            : this.articles.filter(article => article.category === category);
        
        this.renderArticles(filtered);
    }

    searchArticles(query) {
        if (!query) {
            this.renderArticles();
            return;
        }

        const searchResults = this.articles.filter(article => {
            const searchText = `${article.title} ${article.summary}`.toLowerCase();
            return searchText.includes(query.toLowerCase());
        });

        this.renderArticles(searchResults);
    }
}