document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.cta-button');

    button.addEventListener('click', (e) => {
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = '';
        }, 100);
    });

    document.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;

        const container = document.querySelector('.hero');
        const moveX = (mouseX - 0.5) * 20;
        const moveY = (mouseY - 0.5) * 20;

        container.style.backgroundPosition = `${50 + moveX}% ${50 + moveY}%`;
    });
});



