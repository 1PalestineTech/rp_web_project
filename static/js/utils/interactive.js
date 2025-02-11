// utils/interactive.js
export const interactive = {
    enableZoom: (element) => {
        let scale = 1;
        let panning = false;
        let pointX = 0;
        let pointY = 0;
        let start = { x: 0, y: 0 };

        element.addEventListener('mousedown', (e) => {
            e.preventDefault();
            start = { x: e.clientX - pointX, y: e.clientY - pointY };
            panning = true;
        });

        element.addEventListener('mousemove', (e) => {
            e.preventDefault();
            if (!panning) return;
            
            pointX = (e.clientX - start.x);
            pointY = (e.clientY - start.y);
            
            element.style.transform = `translate(${pointX}px, ${pointY}px) scale(${scale})`;
        });

        element.addEventListener('mouseup', () => panning = false);
        element.addEventListener('wheel', (e) => {
            e.preventDefault();
            const xs = (e.clientX - pointX) / scale;
            const ys = (e.clientY - pointY) / scale;
            
            scale += e.deltaY * -0.01;
            scale = Math.min(Math.max(1, scale), 4);
            
            pointX = e.clientX - xs * scale;
            pointY = e.clientY - ys * scale;
            
            element.style.transform = `translate(${pointX}px, ${pointY}px) scale(${scale})`;
        });
    },

    createTooltip: (element, content) => {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        tooltip.textContent = content;
        
        element.addEventListener('mouseenter', () => {
            document.body.appendChild(tooltip);
            const rect = element.getBoundingClientRect();
            tooltip.style.top = `${rect.bottom + 10}px`;
            tooltip.style.left = `${rect.left}px`;
        });

        element.addEventListener('mouseleave', () => {
            tooltip.remove();
        });
    }
};