// modules/gallery.js
// modules/gallery.js
import { animate } from '../utils/animations.js';
import { helpers } from '../utils/helpers.js';

export class GalleryManager {
    constructor() {
        this.currentCategory = 'all';
        this.currentIndex = 0;
        this.images = {
            architecture: [
                {
                    id: 'arch-001',
                    src: 'images/gallery/architecture/old-jerusalem.jpg',
                    title: 'Old City of Jerusalem',
                    description: 'Historic view of Jerusalem\'s ancient architecture',
                    category: 'architecture'
                },
                // Add more architecture images
            ],
            culture: [
                {
                    id: 'traditional-embroidery',
                    title: 'Palestinian Embroidery',
                    description: 'Traditional Palestinian tatreez (embroidery) showcasing intricate patterns and cultural symbolism',
                    year: '1930',
                    location: 'Bethlehem',
                    source: 'Cultural Heritage Collection',
                    image: '/images/gallery/traditions/embroidery-detail.jpg',
                    thumbnail: '/images/articles/thumbnails/article-thumb1.jpg',
                    category: 'culture'
                },
                // Add more cultural images
            ]
            // Add more categories
        };

        this.currentCategory = 'all';
        this.currentIndex = 0;
        this.isLoading = false;
    }

    async init() {
        try {
            this.container = document.querySelector('.gallery-grid');
            if (!this.container) {
                console.warn('Gallery container not found');
                return;
            }

            await this.loadInitialImages();
            this.setupEventListeners();
        } catch (error) {
            console.error('Gallery initialization error:', error);
        }
    }

    createLoadingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'gallery-loading';
        indicator.innerHTML = `
            <div class="loading-spinner"></div>
            <p>Loading historical images...</p>
        `;
        return indicator;
    }

    async setupGallery() {
        // Create gallery structure
        this.grid.innerHTML = '';
        this.container.classList.add('gallery-loading');

        // Create filter buttons
        const filterContainer = document.createElement('div');
        filterContainer.className = 'gallery-filters';
        filterContainer.innerHTML = `
            <button class="filter-btn active" data-category="all">
                All Images
            </button>
            <button class="filter-btn" data-category="architecture">
                Architecture
            </button>
            <button class="filter-btn" data-category="culture">
                Cultural Heritage
            </button>
            <button class="filter-btn" data-category="daily-life">
                Daily Life
            </button>
        `;

        this.container.insertBefore(filterContainer, this.grid);
    }

    setupEventListeners() {
        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleFilter(e));
        });
    

        // Modal controls
        if (this.modal) {
            this.modal.querySelector('.modal-close')?.addEventListener('click', () => this.closeModal());
            this.modal.querySelector('.modal-prev')?.addEventListener('click', () => this.navigateImage(-1));
            this.modal.querySelector('.modal-next')?.addEventListener('click', () => this.navigateImage(1));
            
            // Keyboard navigation
            document.addEventListener('keydown', (e) => this.handleKeyPress(e));
        }

        // Lazy loading on scroll
        window.addEventListener('scroll', helpers.debounce(() => {
            this.handleScroll();
        }, 150));
    }

    async loadInitialImages() {
        if (!this.container) return;
        
        const allImages = this.getAllImages();
        await this.renderImages(allImages);
    }

    getAllImages() {
        return Object.values(this.images)
            .flat()
            .filter(img => img && img.src);
    }

    async renderImages(images) {
        if (!this.container) return;

        this.container.innerHTML = '';
        const fragment = document.createDocumentFragment();

        images.forEach(image => {
            const item = this.createGalleryItem(image);
            fragment.appendChild(item);
        });

        this.container.appendChild(fragment);
    }

    createGalleryItem(image) {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        
        item.innerHTML = `
            <img src="${image.src}" 
                 alt="${image.title}"
                 loading="lazy">
            <div class="gallery-caption">
                <h3>${image.title}</h3>
                <p>${image.description}</p>
            </div>
        `;

        item.addEventListener('click', () => this.openModal(image));
        return item;
    }

    // Continue with modal and navigation methods...


    openModal(imageData) {
        if (!this.modal) return;

        const modalContent = this.modal.querySelector('.modal-content');
        const modalCaption = this.modal.querySelector('.modal-caption');

        // Set up modal content
        modalContent.innerHTML = `
            <img src="${imageData.image}" alt="${imageData.title}" class="modal-image">
            <div class="modal-details">
                <h3>${imageData.title}</h3>
                <p class="modal-description">${imageData.description}</p>
                <div class="modal-metadata">
                    <span class="modal-year">${imageData.year}</span>
                    <span class="modal-location">${imageData.location}</span>
                    <span class="modal-source">Source: ${imageData.source}</span>
                </div>
            </div>
        `;

        // Show modal with animation
        this.modal.classList.add('modal-loading');
        this.modal.style.display = 'flex';

        // Load high-resolution image
        const modalImage = modalContent.querySelector('.modal-image');
        modalImage.onload = () => {
            this.modal.classList.remove('modal-loading');
            animate.fadeIn(this.modal);
        };

        // Enable zoom functionality
        this.setupImageZoom(modalImage);

        // Update navigation state
        this.currentIndex = this.getAllImages().findIndex(img => img.id === imageData.id);
        this.updateNavigationButtons();
    }

    setupImageZoom(image) {
        let scale = 1;
        let panning = false;
        let pointX = 0;
        let pointY = 0;
        let start = { x: 0, y: 0 };

        const resetZoom = () => {
            scale = 1;
            pointX = 0;
            pointY = 0;
            image.style.transform = 'translate(0,0) scale(1)';
        };

        image.addEventListener('mousedown', (e) => {
            e.preventDefault();
            start = { x: e.clientX - pointX, y: e.clientY - pointY };
            panning = true;
        });

        image.addEventListener('mousemove', (e) => {
            if (!panning) return;
            pointX = (e.clientX - start.x);
            pointY = (e.clientY - start.y);
            image.style.transform = `translate(${pointX}px, ${pointY}px) scale(${scale})`;
        });

        image.addEventListener('mouseup', () => panning = false);
        image.addEventListener('mouseleave', () => panning = false);

        image.addEventListener('wheel', (e) => {
            e.preventDefault();
            const xs = (e.clientX - pointX) / scale;
            const ys = (e.clientY - pointY) / scale;
            
            const delta = -Math.sign(e.deltaY) * 0.1;
            scale = Math.min(Math.max(1, scale + delta), 3);
            
            pointX = e.clientX - xs * scale;
            pointY = e.clientY - ys * scale;
            
            image.style.transform = `translate(${pointX}px, ${pointY}px) scale(${scale})`;
        });

        // Double click to reset zoom
        image.addEventListener('dblclick', resetZoom);
    }

    updateNavigationButtons() {
        const allImages = this.getAllImages();
        const prevBtn = this.modal.querySelector('.modal-prev');
        const nextBtn = this.modal.querySelector('.modal-next');

        if (prevBtn) {
            prevBtn.disabled = this.currentIndex === 0;
            prevBtn.classList.toggle('disabled', this.currentIndex === 0);
        }

        if (nextBtn) {
            nextBtn.disabled = this.currentIndex === allImages.length - 1;
            nextBtn.classList.toggle('disabled', this.currentIndex === allImages.length - 1);
        }
    }

    navigateImage(direction) {
        const allImages = this.getAllImages();
        const newIndex = this.currentIndex + direction;

        if (newIndex >= 0 && newIndex < allImages.length) {
            this.currentIndex = newIndex;
            const newImage = allImages[newIndex];
            
            // Preload next image
            if (direction > 0 && newIndex + 1 < allImages.length) {
                this.preloadImage(allImages[newIndex + 1].image);
            }
            
            // Update modal content with animation
            animate.fadeOut(this.modal.querySelector('.modal-content'), () => {
                this.openModal(newImage);
            });
        }
    }

    preloadImage(src) {
        const img = new Image();
        img.src = src;
    }

    handleKeyPress(event) {
        if (!this.modal || this.modal.style.display === 'none') return;

        switch(event.key) {
            case 'Escape':
                this.closeModal();
                break;
            case 'ArrowLeft':
                this.navigateImage(-1);
                break;
            case 'ArrowRight':
                this.navigateImage(1);
                break;
        }
    }

    closeModal() {
        if (!this.modal) return;
        
        animate.fadeOut(this.modal, () => {
            this.modal.style.display = 'none';
            // Reset zoom and position
            const modalImage = this.modal.querySelector('.modal-image');
            if (modalImage) {
                modalImage.style.transform = 'translate(0,0) scale(1)';
            }
        });
    }

    handleFilter(event) {
        const category = event.target.dataset.category;
        
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.category === category);
        });

        const filteredImages = category === 'all' 
            ? this.getAllImages()
            : this.getAllImages().filter(img => img.category === category);

        this.renderImages(filteredImages);
    }
    

    async loadFilteredImages(category) {
        try {
            this.showLoading();
            const filteredImages = category === 'all' 
                ? this.getAllImages() 
                : this.galleryData[category] || [];

            await this.renderImages(filteredImages);
            this.hideLoading();
        } catch (error) {
            console.error('Error loading filtered images:', error);
            this.handleError(error);
        }
    }

    showLoading() {
        this.isLoading = true;
        this.container.appendChild(this.loadingIndicator);
    }

    hideLoading() {
        this.isLoading = false;
        this.loadingIndicator.remove();
    }

    handleError(error) {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'gallery-error';
        errorMessage.innerHTML = `
            <p>We apologize, but there was an error loading the gallery content.</p>
            <button onclick="location.reload()">Try Again</button>
        `;
        this.container.appendChild(errorMessage);
    }

    destroy() {
        // Cleanup event listeners and resources
        document.removeEventListener('keydown', this.handleKeyPress);
        window.removeEventListener('scroll', this.handleScroll);
    }
}