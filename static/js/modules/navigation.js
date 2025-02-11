// modules/navigation.js
import { animate } from '../utils/animations.js';

export class NavigationManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupEventListeners();
        this.setupScrollSpy();
    }

    setupNavigation() {
        this.nav = document.querySelector('.main-nav');
        this.mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        this.navigationItems = document.querySelectorAll('.nav-item');
    }

    setupEventListeners() {
        if (this.mobileMenuBtn) {
            this.mobileMenuBtn.addEventListener('click', () => this.toggleMobileMenu());
        }

        this.navigationItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = e.currentTarget.getAttribute('href');
                this.scrollToSection(targetId);
            });
        });

        // Close mobile menu on click outside
        document.addEventListener('click', (e) => {
            if (this.nav?.classList.contains('active') && 
                !e.target.closest('.main-nav') && 
                !e.target.closest('.mobile-menu-btn')) {
                this.toggleMobileMenu();
            }
        });
    }

    toggleMobileMenu() {
        if (!this.nav) return;
        
        const isOpen = this.nav.classList.contains('active');
        
        if (isOpen) {
            animate.fadeOut(this.nav, () => {
                this.nav.classList.remove('active');
            });
        } else {
            this.nav.classList.add('active');
            animate.fadeIn(this.nav);
        }
    }

    scrollToSection(targetId) {
        const targetSection = document.querySelector(targetId);
        if (!targetSection) return;

        const headerOffset = 80;
        const elementPosition = targetSection.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });

        // Close mobile menu after navigation
        if (this.nav?.classList.contains('active')) {
            this.toggleMobileMenu();
        }
    }

    setupScrollSpy() {
        const sections = document.querySelectorAll('section[id]');
        
        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (window.pageYOffset >= sectionTop - 200) {
                    current = section.getAttribute('id');
                }
            });

            this.navigationItems.forEach(item => {
                item.classList.remove('active');
                if (item.getAttribute('href').substring(1) === current) {
                    item.classList.add('active');
                }
            });
        });
    }
}