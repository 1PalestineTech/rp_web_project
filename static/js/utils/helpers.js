// utils/helpers.js
const helpers = {
    formatDate: (date) => {
        if (!date) return '';
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(date).toLocaleDateString('en-US', options);
    },

    truncateText: (text, length = 100) => {
        if (!text || text.length <= length) return text;
        return text.substring(0, length).trim() + '...';
    },

    slugify: (text) => {
        return text
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/(^-|-$)+/g, '');
    },

    debounce: (func, wait = 300) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    generateImageAlt: (title, category) => {
        return `Historical image of ${title} showing ${category} in Palestinian history`;
    },

    validateImageUrl: (url) => {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(true);
            img.onerror = () => reject(false);
            img.src = url;
        });
    }
};