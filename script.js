/**
 * 3D Software ocean effect with Canvas2D
 * Modified version to fix display issues
 */

document.addEventListener('DOMContentLoaded', () => {
    // Create main canvas
    const container = document.body;
    container.style.margin = '0';
    container.style.overflow = 'hidden';
    container.style.backgroundColor = 'black';
    
    const canvas = document.createElement('canvas');
    const postCanvas = document.createElement('canvas');
    container.appendChild(canvas);
    container.appendChild(postCanvas);
    
    const c = canvas.getContext('2d');
    const postctx = postCanvas.getContext('2d');
    
    let vertices = [];

    // Effect Properties - You can adjust these
    const vertexCount = 7000;
    const vertexSize = 3;
    const oceanWidth = 204;
    const oceanHeight = -80;
    const gridSize = 32;
    const waveSize = 16;
    const perspective = 100;

    // Common variables
    const depth = (vertexCount / oceanWidth * gridSize);
    let frame = 0;
    const { sin, cos, PI } = Math;

    // Set canvas sizes
    function resizeCanvases() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        canvas.width = width;
        canvas.height = height;
        postCanvas.width = width;
        postCanvas.height = height;
        
        canvas.style.position = 'absolute';
        canvas.style.top = '0';
        canvas.style.left = '0';
        
        postCanvas.style.position = 'absolute';
        postCanvas.style.top = '0';
        postCanvas.style.left = '0';
    }

    // Generate initial vertices
    function generateVertices() {
        for (let i = 0; i < vertexCount; i++) {
            let x = i % oceanWidth;
            let z = Math.floor(i / oceanWidth);
            let offset = oceanWidth / 2;
            vertices.push([(-offset + x) * gridSize, 0, z * gridSize]);
        }
    }

    // Main render loop
    function loop(timeStamp) {
        const rad = sin(frame / 100) * PI / 20;
        const rad2 = sin(frame / 50) * PI / 10;
        
        // Clear canvases
        c.fillStyle = 'hsl(200, 100%, 2%)';
        c.fillRect(0, 0, canvas.width, canvas.height);
        
        c.save();
        c.translate(canvas.width / 2, canvas.height / 2);
        
        // Draw waves
        vertices.forEach((vertex, i) => {
            let x = vertex[0] - frame % (gridSize * 2);
            let z = vertex[2] - frame * 2 % gridSize + (i % 2 === 0 ? gridSize / 2 : 0);
            let wave = (cos(frame / 45 + x / 50) - sin(frame / 20 + z / 50) + sin(frame / 30 + z * x / 10000));
            let y = vertex[1] + wave * waveSize;
            let a = Math.max(0, 1 - (Math.sqrt(x ** 2 + z ** 2) / depth));
            
            if (a < 0.01 || z < 0) return;
            
            y -= oceanHeight;
            
            // Apply 3D transformations
            let tx = x * cos(rad) + z * sin(rad);
            let tz = -x * sin(rad) + z * cos(rad);
            let ty = y;
            
            // Apply perspective
            tx /= tz / perspective;
            ty /= tz / perspective;
            
            c.globalAlpha = a;
            c.fillStyle = `hsl(${180 + wave * 20}, 100%, 50%)`;
            c.fillRect(tx - a * vertexSize / 2, ty - a * vertexSize / 2, a * vertexSize, a * vertexSize);
        });
        
        c.restore();
        
        // Post-processing effects
        postctx.drawImage(canvas, 0, 0);
        postctx.globalCompositeOperation = "screen";
        postctx.filter = 'blur(16px)';
        postctx.drawImage(canvas, 0, 0);
        postctx.filter = 'blur(0)';
        postctx.globalCompositeOperation = "source-over";
        
        frame += 0.5;
        requestAnimationFrame(loop);
    }

    // Initialize everything
    resizeCanvases();
    generateVertices();
    window.addEventListener('resize', resizeCanvases);
    loop(0);
});