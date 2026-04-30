// Animated particle network background
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let particles = [], W, H;

function resize() {
  W = canvas.width = window.innerWidth;
  H = canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

class Particle {
  constructor() {
    this.x = Math.random() * W;
    this.y = Math.random() * H;
    this.vx = (Math.random() - 0.5) * 0.4;
    this.vy = (Math.random() - 0.5) * 0.4;
    this.r = Math.random() * 2 + 1;
    this.color = ['#7c3aed','#ec4899','#06b6d4'][Math.floor(Math.random()*3)];
  }
  update() {
    this.x += this.vx; this.y += this.vy;
    if (this.x < 0 || this.x > W) this.vx *= -1;
    if (this.y < 0 || this.y > H) this.vy *= -1;
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.globalAlpha = 0.6;
    ctx.fill();
  }
}

for (let i = 0; i < 70; i++) particles.push(new Particle());

function connect() {
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < 130) {
        ctx.beginPath();
        ctx.strokeStyle = '#7c3aed';
        ctx.globalAlpha = (1 - dist/130) * 0.25;
        ctx.lineWidth = 1;
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.stroke();
      }
    }
  }
}

function animate() {
  ctx.clearRect(0, 0, W, H);
  particles.forEach(p => { p.update(); p.draw(); });
  connect();
  requestAnimationFrame(animate);
}
animate();

// GSAP entrance animations
window.addEventListener('DOMContentLoaded', () => {
  gsap.from('.auth-card', { opacity:0, y:40, duration:0.8, ease:'power3.out' });
  gsap.from('.stat-card', { opacity:0, y:30, duration:0.6, stagger:0.1, ease:'power2.out' });
  gsap.from('.project-card', { opacity:0, scale:0.9, duration:0.5, stagger:0.08 });
  gsap.from('.task-card', { opacity:0, x:-20, duration:0.4, stagger:0.05 });
  gsap.from('.sidebar', { x:-260, duration:0.6, ease:'power3.out' });
  gsap.from('.topbar', { opacity:0, y:-20, duration:0.6, delay:0.2 });
});