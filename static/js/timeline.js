/* Palestinian History Interactive Timeline */
(() => {
    class TimelineExperience {
        constructor() {
            if (window.timelineInstance) {
                return window.timelineInstance;
            }

            console.log('Timeline initializing...');
            
            // Core elements
            this.timeline = document.querySelector('.timeline-wrapper');
            this.events = document.querySelectorAll('.timeline-event');
            this.eraButtons = document.querySelectorAll('.era-bubble');
            this.centralLine = document.querySelector('.timeline-central-line');
            this.modal = document.querySelector('.feature-modal');
            this.progressLine = document.querySelector('.progress-line');
            this.prevBtn = document.querySelector('.nav-btn.prev');
            this.nextBtn = document.querySelector('.nav-btn.next');

            // State management
            this.isAnimating = false;
            this.touchStartX = 0;
            this.touchEndX = 0;
            this.isNavigating = false;
            this.navigationCooldown = 800;

            // Set initial era
            const firstEraSection = document.querySelector('.timeline-era');
            if (firstEraSection) {
                this.currentEra = firstEraSection.getAttribute('data-era');
                this.updateNavigationState();
            }

            window.timelineInstance = this;
            this.init();
            return this;
        }

        init() {
            if (typeof gsap !== 'undefined') {
                gsap.registerPlugin(ScrollTrigger);
                this.setupGSAP();
            }
            this.setupEventListeners();
            this.initializeMediaHandling();
            this.setupInteractiveFeatures();
            this.initializeTimelineProgress();
            this.setupMobileInteractions();
            this.initializeScrollEffects();
        }

        setupGSAP() {
            gsap.to('.intro-parallax', {
                y: -100,
                opacity: 0,
                ease: "none",
                scrollTrigger: {
                    trigger: '.intro-experience',
                    start: "top top",
                    end: "bottom top",
                    scrub: true
                }
            });

            this.events.forEach(event => {
                gsap.fromTo(event,
                    { opacity: 0, y: 50, scale: 0.95 },
                    {
                        opacity: 1,
                        y: 0,
                        scale: 1,
                        duration: 1,
                        scrollTrigger: {
                            trigger: event,
                            start: "top 80%",
                            end: "top 20%",
                            toggleActions: "play none none reverse"
                        }
                    }
                );
            });
        }

        initializeScrollEffects() {
            if (!this.timeline) return;

            const updateProgress = (progress) => {
                if (this.progressLine) {
                    gsap.to(this.progressLine, {
                        width: `${progress * 100}%`,
                        duration: 0.1
                    });
                }
            };

            ScrollTrigger.create({
                trigger: this.timeline,
                start: 'top top',
                end: 'bottom bottom',
                onUpdate: (self) => {
                    updateProgress(self.progress);
                }
            });

            this.events.forEach(event => {
                if (!event.dataset.era) return;
                
                ScrollTrigger.create({
                    trigger: event,
                    start: "top center",
                    end: "bottom center",
                    onEnter: () => {
                        if (event.dataset.era) {
                            this.currentEra = event.dataset.era;
                            this.updateNavigationState();
                        }
                    },
                    onEnterBack: () => {
                        if (event.dataset.era) {
                            this.currentEra = event.dataset.era;
                            this.updateNavigationState();
                        }
                    }
                });
            });
        }

        setupEventListeners() {
            if (this.prevBtn) {
                this.prevBtn.addEventListener('click', () => {
                    if (!this.isNavigating && !this.prevBtn.disabled) {
                        this.navigateToPreviousEra();
                    }
                });
            }

            if (this.nextBtn) {
                this.nextBtn.addEventListener('click', () => {
                    if (!this.isNavigating && !this.nextBtn.disabled) {
                        this.navigateToNextEra();
                    }
                });
            }

            this.eraButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    if (!this.isNavigating) {
                        const targetEra = e.target.closest('.era-bubble').dataset.era;
                        this.smoothScrollToEra(targetEra);
                    }
                });
            });

            document.querySelectorAll('.explore-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const event = e.target.closest('.timeline-event');
                    this.openEventDetail(event);
                });
            });

            document.querySelector('.modal-close')?.addEventListener('click', () => {
                this.closeModal();
            });

            document.addEventListener('keydown', (e) => {
                if (this.isNavigating) return;
                
                if (e.key === 'Escape') this.closeModal();
                if (e.key === 'ArrowRight' && !this.nextBtn.disabled) {
                    this.navigateToNextEra();
                }
                if (e.key === 'ArrowLeft' && !this.prevBtn.disabled) {
                    this.navigateToPreviousEra();
                }
            });
        }

        navigateToNextEra() {
            if (this.isNavigating) return;
            
            const currentSection = document.querySelector(`.timeline-era[data-era="${this.currentEra}"]`);
            if (!currentSection) return;

            const nextSection = currentSection.nextElementSibling;
            if (nextSection && nextSection.classList.contains('timeline-era')) {
                this.isNavigating = true;
                this.nextBtn.classList.add('navigating');
                
                const nextEra = nextSection.getAttribute('data-era');
                this.smoothScrollToEra(nextEra);
            }
        }

        navigateToPreviousEra() {
            if (this.isNavigating) return;
            
            const currentSection = document.querySelector(`.timeline-era[data-era="${this.currentEra}"]`);
            if (!currentSection) return;

            const prevSection = currentSection.previousElementSibling;
            if (prevSection && prevSection.classList.contains('timeline-era')) {
                this.isNavigating = true;
                this.prevBtn.classList.add('navigating');
                
                const prevEra = prevSection.getAttribute('data-era');
                this.smoothScrollToEra(prevEra);
            }
        }

        smoothScrollToEra(era) {
            const targetSection = document.querySelector(`.timeline-era[data-era="${era}"]`);
            
            if (targetSection) {
                const offset = window.innerHeight * 0.2;
                const targetPosition = targetSection.offsetTop - offset;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                this.currentEra = era;
                this.updateNavigationState();

                setTimeout(() => {
                    this.isNavigating = false;
                    this.nextBtn.classList.remove('navigating');
                    this.prevBtn.classList.remove('navigating');
                }, this.navigationCooldown);
            }
        }

        updateNavigationState() {
            if (!this.prevBtn || !this.nextBtn) return;

            const currentSection = document.querySelector(`.timeline-era[data-era="${this.currentEra}"]`);
            if (!currentSection) return;

            const hasPrev = !!currentSection.previousElementSibling?.classList.contains('timeline-era');
            const hasNext = !!currentSection.nextElementSibling?.classList.contains('timeline-era');

            this.prevBtn.disabled = !hasPrev;
            this.nextBtn.disabled = !hasNext;
            
            this.prevBtn.style.opacity = hasPrev ? '1' : '0.5';
            this.nextBtn.style.opacity = hasNext ? '1' : '0.5';

            this.eraButtons.forEach(btn => {
                btn.classList.toggle('active', btn.dataset.era === this.currentEra);
            });
        }

        initializeTimelineProgress() {
            if (this.progressLine) {
                const updateProgressBar = () => {
                    const scrollPercentage = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
                    this.progressLine.style.width = `${scrollPercentage}%`;
                };

                window.addEventListener('scroll', updateProgressBar);
                updateProgressBar();
            }
        }

        initializeMediaHandling() {
            const images = document.querySelectorAll('.primary-media img');
            
            images.forEach(img => {
                if ('loading' in HTMLImageElement.prototype) {
                    img.loading = 'lazy';
                }

                img.addEventListener('load', () => {
                    img.closest('.primary-media')?.classList.add('loaded');
                });

                img.addEventListener('error', () => {
                    this.handleImageError(img);
                });
            });
        }

        setupInteractiveFeatures() {
            document.querySelectorAll('.interactive-map').forEach(map => {
                this.initializeMap(map);
            });
        }

        setupMobileInteractions() {
            if (this.timeline) {
                this.timeline.addEventListener('touchstart', (e) => {
                    this.touchStartX = e.touches[0].clientX;
                }, { passive: true });

                this.timeline.addEventListener('touchend', (e) => {
                    this.touchEndX = e.changedTouches[0].clientX;
                    this.handleSwipe();
                }, { passive: true });
            }
        }

        handleSwipe() {
            const swipeDistance = this.touchEndX - this.touchStartX;
            const threshold = 50;

            if (Math.abs(swipeDistance) > threshold) {
                if (swipeDistance > 0 && !this.prevBtn.disabled) {
                    this.navigateToPreviousEra();
                } else if (swipeDistance < 0 && !this.nextBtn.disabled) {
                    this.navigateToNextEra();
                }
            }
        }

        openEventDetail(event) {
            if (!this.modal) return;
            
            const content = event.querySelector('.event-content')?.cloneNode(true);
            if (!content) return;

            const modalBody = this.modal.querySelector('.modal-body');
            if (!modalBody) return;
            
            modalBody.innerHTML = '';
            modalBody.appendChild(content);

            gsap.to(this.modal, {
                opacity: 1,
                visibility: 'visible',
                duration: 0.3
            });
        }

        closeModal() {
            if (!this.modal) return;

            gsap.to(this.modal, {
                opacity: 0,
                duration: 0.3,
                onComplete: () => {
                    this.modal.style.visibility = 'hidden';
                }
            });
        }

        handleImageError(img) {
            img.src = 'images/placeholder.jpg';
            img.alt = 'Image temporarily unavailable';
            const mediaContainer = img.closest('.primary-media');
            if (mediaContainer) {
                mediaContainer.classList.add('error');
            }
        }

        initializeMap(mapElement) {
            const mapControls = mapElement.querySelector('.map-controls');
            if (mapControls) {
                mapControls.querySelectorAll('button').forEach(btn => {
                    btn.addEventListener('click', () => {
                        if (btn.dataset.layer) {
                            this.toggleMapLayer(mapElement, btn.dataset.layer);
                        }
                    });
                });
            }
        }

        toggleMapLayer(mapElement, layer) {
            console.log(`Toggling map layer: ${layer}`);
        }
    }

    // Assign the class to window object
    window.PalestineTimelineExperience = TimelineExperience;

    // Initialize when DOM is ready
    const initTimeline = () => {
        if (!window.timelineInstance) {
            new TimelineExperience();
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTimeline);
    } else {
        initTimeline();
    }
})();