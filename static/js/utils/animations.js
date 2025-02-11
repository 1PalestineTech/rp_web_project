// utils/animations.js
const animate = {
    fadeIn: (element, duration = 300) => {
        element.style.opacity = 0;
        element.style.display = 'block';
        
        let start = null;
        const animate = (timestamp) => {
            if (!start) start = timestamp;
            const progress = timestamp - start;
            
            element.style.opacity = Math.min(progress / duration, 1);
            
            if (progress < duration) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    },

    fadeOut: (element, callback, duration = 300) => {
        let start = null;
        
        const animate = (timestamp) => {
            if (!start) start = timestamp;
            const progress = timestamp - start;
            
            element.style.opacity = Math.max(1 - (progress / duration), 0);
            
            if (progress < duration) {
                requestAnimationFrame(animate);
            } else {
                element.style.display = 'none';
                if (callback) callback();
            }
        };
        
        requestAnimationFrame(animate);
    },

    slideIn: (element, direction = 'left', duration = 500) => {
        element.style.display = 'block';
        element.style.opacity = '0';
        element.style.transform = direction === 'left' 
            ? 'translateX(-50px)' 
            : 'translateX(50px)';
        element.style.transition = `all ${duration}ms ease-out`;
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateX(0)';
        }, 10);
    },

    zoomIn: (element, duration = 300) => {
        element.style.display = 'block';
        element.style.opacity = '0';
        element.style.transform = 'scale(0.95)';
        element.style.transition = `all ${duration}ms ease-out`;
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'scale(1)';
        }, 10);
    }
};