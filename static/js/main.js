// main.js
class PalestineHistoryApp {
    constructor() {
        this.config = {
            scrollOffset: 100,
            animationDuration: 800,
            breakpoints: {
                mobile: 768,
                tablet: 1024
            }
        };
        this.init();
    }

    async init() {
        try {
            this.showLoader();
            await this.initializeComponents();
            this.setupEventListeners();
            this.initializeAnimations();
            this.hideLoader();
            this.initializeTimeline();
        } catch (error) {
            console.error('Initialization error:', error);
            this.handleError(error);
        }
    }

    async initializeComponents() {
        try {
            await Promise.all([
                this.setupGallery(),
                this.setupTimeline(),
                this.setupNavigation()
            ]);
        } catch (error) {
            throw new Error(`Component initialization failed: ${error.message}`);
        }
    }

    setupGallery() {
        const gallery = document.querySelector('.gallery-section');
        if (gallery) {
            // Gallery initialization code will go here
        }
    }

    setupTimeline() {
        const timeline = document.querySelector('.timeline-section');
        if (timeline) {
            // Timeline initialization code will go here
        }
    }

    setupNavigation() {
        const nav = document.querySelector('.main-navigation');
        if (nav) {
            // Navigation initialization code will go here
        }
    }

    setupEventListeners() {
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });

        // Scroll and resize handlers
        window.addEventListener('scroll', () => this.handleScroll());
        window.addEventListener('resize', () => this.handleResize());

        // Theme toggle
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }

    initializeAnimations() {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            },
            { threshold: 0.2 }
        );

        document.querySelectorAll('[data-animate]').forEach(element => {
            observer.observe(element);
        });
    }

    handleScroll() {
        const scrollPosition = window.scrollY;
        
        // Update active navigation state
        document.querySelectorAll('section[id]').forEach(section => {
            const sectionTop = section.offsetTop - this.config.scrollOffset;
            const sectionBottom = sectionTop + section.offsetHeight;

            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                this.updateNavigation(section.id);
            }
        });
    }

    initializeTimeline() {
        const observerOptions = {
            root: null,
            threshold: 0.2,
            rootMargin: "0px"
        };
    
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);
    
        // Observe timeline entries
        document.querySelectorAll('.timeline-entry').forEach(entry => {
            observer.observe(entry);
        });
    }

    handleResize() {
        const width = window.innerWidth;
        document.body.classList.toggle('is-mobile', width < this.config.breakpoints.mobile);
        document.body.classList.toggle('is-tablet', width < this.config.breakpoints.tablet);
    }

    updateNavigation(currentSection) {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', 
                link.getAttribute('href') === `#${currentSection}`);
        });
    }

    toggleTheme() {
        document.body.classList.toggle('dark-theme');
        localStorage.setItem('theme', 
            document.body.classList.contains('dark-theme') ? 'dark' : 'light');
    }

    showLoader() {
        const loader = document.createElement('div');
        loader.className = 'site-loader';
        loader.innerHTML = '<div class="loader-spinner"></div>';
        document.body.appendChild(loader);
    }

    hideLoader() {
        const loader = document.querySelector('.site-loader');
        if (loader) {
            loader.classList.add('fade-out');
            setTimeout(() => loader.remove(), 500);
        }
    }

    handleError(error) {
        console.error('Application error:', error);
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.innerHTML = `
            <div class="error-content">
                <h2>We apologize for the inconvenience</h2>
                <p>Please try refreshing the page.</p>
                <button onclick="window.location.reload()">Refresh</button>
            </div>
        `;
        document.body.appendChild(errorMessage);
    }
}



// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new PalestineHistoryApp();
});

