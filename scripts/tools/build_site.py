import re

with open("original_stitch.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update logo to zevaro.png
html = html.replace("https://lh3.googleusercontent.com/aida-public/AB6AXuAV2cjjdDqLMACc0scqOGivnJXqqJKPn0Sys-rjuu4yDt_uHYyWUdLBOOxpKp-PM6qwRjBhnU88s9oIcLB9HW4ZiMJEbLSM5UtIoire-EBOLA6V6LOTUzG41hsYoXRu8dRYwfkFiqbACntkgTOVBDeTQ7AiqdCILYoJyxfB5fi2L1EBnyAKx1OdSmTULB7-j9viabZ9AhqI4bvfNQ7ujjH1HvAn78jb2c9WD3Fr4a4CPIoBf2kUeICaB9pnTD_lYgK3qy4", "zevaro.png")
html = html.replace("https://lh3.googleusercontent.com/aida-public/AB6AXuBnvRudYfUACJZcVpHt0pYYvV0CDedBRZr_rmaVohH-lu3C3deFjA1XPXz3BbTocdLrrpw3Ig369T4ncMXrOi8IAbJYleLECEn1jv5pvGDUZBzWet5WDnlY5zxlXdqauQZkaDXUkCj22IQ5FUIxlbwWp4OsOVaXKRJL_s7u4q86XLFc2tcA26VbMtScHq_aVCjQDEzQ9IAohjWsx4Tek9IWuMtvd7Yljl-jROjJVIm51b_WWe6rGuV5fSZEMyievCVE7QM", "zevaro.png")

# 2. Add Three.js & GSAP in the head
libs = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>
.perspective-1200 { perspective: 1200px; }
.preserve-3d { transform-style: preserve-3d; }
.card-3d-tilt { transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1); }
</style>
"""
html = html.replace("</head>", libs + "</head>")

# 3. Strip all blue / purple / cyan colors from Tailwind palette and replace with Obsidian / Slate / Charcoal Luxury Palette
tailwind_replacements = {
    '"primary": "#4648d4"': '"primary": "#0f172a"',
    '"primary-fixed-dim": "#c0c1ff"': '"primary-fixed-dim": "#cbd5e1"',
    '"primary-fixed": "#e1e0ff"': '"primary-fixed": "#f1f5f9"',
    '"primary-container": "#6063ee"': '"primary-container": "#1e293b"',
    '"on-primary-fixed-variant": "#2f2ebe"': '"on-primary-fixed-variant": "#0f172a"',
    '"on-primary-fixed": "#07006c"': '"on-primary-fixed": "#0f172a"',
    '"tertiary": "#712ae2"': '"tertiary": "#0f172a"',
    '"tertiary-fixed-dim": "#d2bbff"': '"tertiary-fixed-dim": "#cbd5e1"',
    '"tertiary-fixed": "#eaddff"': '"tertiary-fixed": "#f1f5f9"',
    '"tertiary-container": "#8a4cfc"': '"tertiary-container": "#1e293b"',
    '"secondary": "#006398"': '"secondary": "#0f172a"',
    '"secondary-fixed-dim": "#93ccff"': '"secondary-fixed-dim": "#cbd5e1"',
    '"secondary-fixed": "#cce5ff"': '"secondary-fixed": "#f1f5f9"',
    '"secondary-container": "#5bb8fe"': '"secondary-container": "#334155"',
    '"on-secondary-fixed-variant": "#004b73"': '"on-secondary-fixed-variant": "#0f172a"',
    '"on-secondary-container": "#00476e"': '"on-secondary-container": "#0f172a"',
    '"surface": "#faf9ff"': '"surface": "#FAFAFC"',
    '"surface-bright": "#faf9ff"': '"surface-bright": "#FAFAFC"',
    '"background": "#faf9ff"': '"background": "#FAFAFC"',
    '"surface-container-high": "#e5e8f5"': '"surface-container-high": "#e2e8f0"',
    '"surface-container": "#ebedfb"': '"surface-container": "#f1f5f9"',
    '"surface-container-low": "#f1f3ff"': '"surface-container-low": "#f8fafc"',
    '"surface-container-highest": "#dfe2ef"': '"surface-container-highest": "#e2e8f0"',
    '"surface-variant": "#dfe2ef"': '"surface-variant": "#e2e8f0"',
}

for old, new in tailwind_replacements.items():
    html = html.replace(old, new)

# 4. Replace the old oily WebGL shader with the luxury Monochromatic 3D kinetic particle lattice (NO BLUE)
old_shader_pattern = re.compile(r'<!-- STITCH_SHADER_START:ANIMATION_5.*?<!-- STITCH_SHADER_END:ANIMATION_5 -->', re.DOTALL)

luxury_3d_bg = """<!-- LUXURY MONOCHROME 3D KINETIC FIELD (THREE.JS + GSAP) -->
<div id="threejs-hero-bg" class="fixed inset-0 w-full h-full pointer-events-none -z-10"></div>
<div class="fixed top-0 left-1/2 -translate-x-1/2 w-[1100px] h-[450px] bg-gradient-to-b from-slate-200/30 via-slate-100/10 to-transparent blur-3xl pointer-events-none -z-10"></div>
<script>
(function() {
  const container = document.getElementById("threejs-hero-bg");
  if (!container || typeof THREE === "undefined") return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 50;

  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // Smooth monochrome slate/platinum circular glow texture (NO BLUE)
  const canvas = document.createElement("canvas");
  canvas.width = 64;
  canvas.height = 64;
  const ctx = canvas.getContext("2d");
  const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
  gradient.addColorStop(0, "rgba(15, 23, 42, 0.9)");
  gradient.addColorStop(0.3, "rgba(71, 85, 105, 0.5)");
  gradient.addColorStop(0.7, "rgba(148, 163, 184, 0.15)");
  gradient.addColorStop(1, "rgba(255, 255, 255, 0)");
  ctx.fillStyle = gradient;
  ctx.beginPath();
  ctx.arc(32, 32, 32, 0, Math.PI * 2);
  ctx.fill();
  const particleTexture = new THREE.CanvasTexture(canvas);

  const particleCount = 180;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(particleCount * 3);

  for (let i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 110;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 80;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 50;
  }

  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

  const material = new THREE.PointsMaterial({
    map: particleTexture,
    size: 4.5,
    transparent: true,
    opacity: 0.55,
    depthWrite: false,
    blending: THREE.NormalBlending
  });

  const particles = new THREE.Points(geometry, material);
  scene.add(particles);

  let mouseX = 0, mouseY = 0, targetX = 0, targetY = 0;
  window.addEventListener("mousemove", (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  const clock = new THREE.Clock();
  function animate() {
    requestAnimationFrame(animate);
    const time = clock.getElapsedTime();
    targetX += (mouseX - targetX) * 0.04;
    targetY += (mouseY - targetY) * 0.04;

    const pos = geometry.attributes.position.array;
    for (let i = 0; i < particleCount; i++) {
      pos[i * 3 + 1] += Math.sin(time * 0.8 + i) * 0.02;
    }
    geometry.attributes.position.needsUpdate = true;

    particles.rotation.y = time * 0.02 + targetX * 0.1;
    particles.rotation.x = Math.sin(time * 0.02) * 0.05 + targetY * 0.1;

    renderer.render(scene, camera);
  }
  animate();
})();
</script>
<!-- LUXURY MONOCHROME 3D BG END -->"""

html = old_shader_pattern.sub(luxury_3d_bg, html)

# 5. Add 3D Framer tilt script to the Hero Terminal card
hero_tilt_script = """
<script>
document.addEventListener('DOMContentLoaded', () => {
  const stage = document.querySelector('.lg\\\\:col-span-6.relative');
  const card = stage ? stage.querySelector('.w-full.rounded-2xl') : null;
  if (stage && card) {
    stage.classList.add('perspective-1200');
    card.classList.add('preserve-3d', 'card-3d-tilt');
    
    stage.addEventListener('mousemove', (e) => {
      const rect = stage.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      const rotX = -y * 10;
      const rotY = x * 10;
      if (typeof gsap !== 'undefined') {
        gsap.to(card, { rotateX: rotX, rotateY: rotY, duration: 0.35, ease: 'power2.out' });
      } else {
        card.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;
      }
    });

    stage.addEventListener('mouseleave', () => {
      if (typeof gsap !== 'undefined') {
        gsap.to(card, { rotateX: 0, rotateY: 0, duration: 0.8, ease: 'elastic.out(1, 0.5)' });
      } else {
        card.style.transform = 'rotateX(0deg) rotateY(0deg)';
      }
    });
  }
});
</script>
"""
html = html.replace("</body>", hero_tilt_script + "</body>")

# 6. Shorten long button text
html = html.replace("Get Started Now — Free Assessment", "Get Started")

# 7. Button styling: Deep Obsidian Black with white text and delicate top specular highlight (NO BLUE / PURPLE)
button_old_classes = "bg-gradient-to-r from-tertiary via-primary to-secondary text-on-primary font-label-lg text-label-lg shadow-[inset_0_1px_0_rgba(255,255,255,0.25)] hover:brightness-105 hover:-translate-y-0.5 shadow-md shadow-primary/20"
button_new_classes = "bg-slate-950 text-white font-label-lg text-label-lg shadow-[inset_0_1px_0_rgba(255,255,255,0.2),0_4px_16px_rgba(15,23,42,0.18)] hover:bg-slate-900 hover:-translate-y-0.5"
html = html.replace(button_old_classes, button_new_classes)

button_hero_old = "bg-gradient-to-r from-tertiary via-primary to-secondary text-on-primary font-label-lg text-label-lg shadow-lg shadow-primary/20 hover:shadow-xl hover:shadow-primary/30 hover:-translate-y-0.5"
button_hero_new = "bg-slate-950 text-white font-label-lg text-label-lg shadow-[inset_0_1px_0_rgba(255,255,255,0.2),0_4px_20px_rgba(15,23,42,0.22)] hover:bg-slate-900 hover:-translate-y-0.5"
html = html.replace(button_hero_old, button_hero_new)

button_cta_old = "bg-gradient-to-r from-tertiary via-primary to-secondary text-on-primary font-label-lg text-label-lg shadow-xl shadow-primary/25 hover:shadow-2xl hover:shadow-primary/35 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
button_cta_new = "bg-slate-950 text-white font-label-lg text-label-lg shadow-[inset_0_1px_0_rgba(255,255,255,0.2),0_4px_20px_rgba(15,23,42,0.22)] hover:bg-slate-900 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
html = html.replace(button_cta_old, button_cta_new)

# 8. Clean text gradient on "interview" (Obsidian to Charcoal)
html = html.replace('bg-gradient-to-r from-tertiary via-primary to-secondary bg-clip-text text-transparent', 'text-slate-950 underline decoration-slate-300 decoration-2 underline-offset-4')
html = html.replace('from-slate-950 via-blue-700 to-indigo-800', 'text-slate-950')
html = html.replace('from-slate-900 via-blue-700 to-indigo-800', 'text-slate-950')

# 9. Clean up all remaining blue classes across the file
html = re.sub(r'\btext-secondary\b', 'text-slate-800', html)
html = re.sub(r'\btext-primary\b', 'text-slate-900', html)
html = re.sub(r'\btext-tertiary\b', 'text-slate-800', html)
html = re.sub(r'\bbg-primary\b', 'bg-slate-950', html)
html = re.sub(r'\bbg-secondary\b', 'bg-slate-900', html)
html = re.sub(r'\bbg-tertiary\b', 'bg-slate-800', html)
html = re.sub(r'\bborder-primary\b', 'border-slate-900', html)
html = re.sub(r'\bborder-secondary\b', 'border-slate-800', html)
html = re.sub(r'\bborder-tertiary\b', 'border-slate-700', html)

# SVG trajectory line gradient
html = html.replace('#4648d4', '#0f172a')
html = html.replace('#712ae2', '#1e293b')
html = html.replace('#006398', '#334155')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully replaced all blue colors with luxury Obsidian/Slate aesthetic and updated button to 'Get Started'!")
