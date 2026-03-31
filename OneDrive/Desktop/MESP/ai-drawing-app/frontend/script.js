document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    const clearBtn = document.getElementById('clearBtn');
    const predictBtn = document.getElementById('predictBtn');
    const resultText = document.getElementById('resultText');
    const loadingIndicator = document.getElementById('loadingIndicator');

    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    // Set canvas defaults
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.lineWidth = 14; 
    ctx.strokeStyle = '#000000';

    // Clear canvas to white background
    function initCanvas() {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    initCanvas();

    // Event Listeners for Drawing (Mouse)
    canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    });

    canvas.addEventListener('mousemove', (e) => {
        if (!isDrawing) return;
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        [lastX, lastY] = [e.offsetX, e.offsetY];
    });

    canvas.addEventListener('mouseup', () => isDrawing = false);
    canvas.addEventListener('mouseout', () => isDrawing = false);

    // Event Listeners for Drawing (Touch)
    canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
        isDrawing = true;
        const touch = e.touches[0];
        const rect = canvas.getBoundingClientRect();
        [lastX, lastY] = [touch.clientX - rect.left, touch.clientY - rect.top];
    }, { passive: false });

    canvas.addEventListener('touchmove', (e) => {
        e.preventDefault();
        if (!isDrawing) return;
        const touch = e.touches[0];
        const rect = canvas.getBoundingClientRect();
        
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(touch.clientX - rect.left, touch.clientY - rect.top);
        ctx.stroke();
        
        [lastX, lastY] = [touch.clientX - rect.left, touch.clientY - rect.top];
    }, { passive: false });

    canvas.addEventListener('touchend', (e) => {
        e.preventDefault();
        isDrawing = false;
    });

    // Button Actions
    clearBtn.addEventListener('click', () => {
        initCanvas();
        resultText.innerHTML = "I'm waiting for your drawing...";
        
        // Add a cute little clear animation to canvas
        canvas.style.transform = 'scale(0.95) rotate(-2deg)';
        setTimeout(() => {
            canvas.style.transform = 'scale(1) rotate(0deg)';
        }, 200);
    });

    predictBtn.addEventListener('click', async () => {
        // Show loading state
        resultText.classList.add('hidden');
        loadingIndicator.classList.remove('hidden');
        
        // Button animation
        predictBtn.style.transform = 'scale(0.9) translateY(2px)';
        setTimeout(() => predictBtn.style.transform = '', 150);

        try {
            // Get base64 image from canvas
            const imageData = canvas.toDataURL('image/png');

            // Call Backend
            // Using absolute URL or relative if hosted together
            // Fallback to localhost:5000 for local dev
            const apiEndpoint = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
                ? 'http://127.0.0.1:5000/predict' 
                : '/predict'; // for deployment

            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageData })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Hide loading
            loadingIndicator.classList.add('hidden');
            resultText.classList.remove('hidden');

            if (data.prediction) {
                const confidence = Math.round(data.confidence * 100);
                resultText.innerHTML = `It's a <strong style='font-size: 1.5em; text-transform: uppercase;'>${data.prediction}</strong>! (${confidence}% sure)`;
                
                // Trigger confetti if high confidence
                if (confidence > 60) {
                    createConfetti();
                }
                
                // Add bounce animation to robot
                const robot = document.querySelector('.robot-character');
                robot.style.animation = 'none';
                void robot.offsetWidth; // trigger reflow
                robot.style.animation = 'bounce 0.5s ease 2';
                setTimeout(() => {
                    robot.style.animation = 'float 3s ease-in-out infinite';
                }, 1000);
            } else {
                resultText.innerHTML = "Hm, I'm not sure what this is! Try drawing one of the target words.";
            }

        } catch (error) {
            console.error('Prediction Error:', error);
            loadingIndicator.classList.add('hidden');
            resultText.classList.remove('hidden');
            resultText.innerHTML = "Oops! Connection to my brain (backend) failed! Make sure the server is running.";
        }
    });

    // Fun confetti effect
    function createConfetti() {
        const colors = ['#ff6b6b', '#4ecdc4', '#ffe66d', '#23a6d5', '#e73c7e'];
        for (let i = 0; i < 30; i++) {
            const confetti = document.createElement('div');
            confetti.classList.add('confetti');
            
            // Random properties
            const color = colors[Math.floor(Math.random() * colors.length)];
            const left = Math.random() * 100;
            const size = Math.random() * 8 + 4;
            const delay = Math.random() * 0.5;
            
            confetti.style.backgroundColor = color;
            confetti.style.left = `${left}%`;
            confetti.style.top = '-10px';
            confetti.style.width = `${size}px`;
            confetti.style.height = `${size}px`;
            confetti.style.animationDelay = `${delay}s`;
            
            document.body.appendChild(confetti);
            
            // Remove after animation
            setTimeout(() => {
                confetti.remove();
            }, 3000 + delay * 1000);
        }
    }
});
