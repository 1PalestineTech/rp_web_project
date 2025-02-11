// utils/image-processor.js
export class ImageProcessor {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.maxWidth = 1200;
        this.quality = 0.85;
    }

    async processImage(imageElement) {
        try {
            const optimizedImage = await this.optimize(imageElement);
            return optimizedImage;
        } catch (error) {
            console.error('Image processing error:', error);
            return imageElement;
        }
    }

    async optimize(img) {
        return new Promise((resolve) => {
            const optimizedImage = new Image();
            
            if (img.naturalWidth > this.maxWidth) {
                const aspectRatio = img.naturalHeight / img.naturalWidth;
                this.canvas.width = this.maxWidth;
                this.canvas.height = this.maxWidth * aspectRatio;
                
                this.ctx.drawImage(img, 0, 0, this.canvas.width, this.canvas.height);
                optimizedImage.src = this.canvas.toDataURL('image/jpeg', this.quality);
            } else {
                optimizedImage.src = img.src;
            }
            
            optimizedImage.onload = () => resolve(optimizedImage);
        });
    }

    createThumbnail(img, maxWidth = 300) {
        const aspectRatio = img.naturalHeight / img.naturalWidth;
        this.canvas.width = maxWidth;
        this.canvas.height = maxWidth * aspectRatio;
        
        this.ctx.drawImage(img, 0, 0, this.canvas.width, this.canvas.height);
        return this.canvas.toDataURL('image/jpeg', 0.7);
    }
}

export const imageProcessor = new ImageProcessor();