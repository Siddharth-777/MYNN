import * as THREE from 'three';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import './style.css';
import { createSpaceship } from './spaceships.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { ScrollToPlugin } from 'gsap/ScrollToPlugin';
import { toggleBB8 } from './bb8Easteregg.js';
import { initBabyYoda } from './babyYoda.js';


gsap.registerPlugin(ScrollTrigger);
gsap.registerPlugin(ScrollToPlugin);

let stars; // ⭐ global star meshx`
let mouseX = 0, mouseY = 0; // 🖱️ for mouse movement rotation

// 🌌 Star generator
function createStars(scene, count = 1500) {
    const geometry = new THREE.BufferGeometry();
    const positions = [];

    for (let i = 0; i < count; i++) {
        positions.push(
            (Math.random() - 0.5) * 200,
            (Math.random() - 0.5) * 200,
            (Math.random() - 0.5) * 200
        );
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
        color: 0xff6b35,
        size: 0.7,
        transparent: true,
        opacity: 0.7,
        depthWrite: false
    });

    stars = new THREE.Points(geometry, material);
    scene.add(stars);
}

// 🚀 App
class StarWarsApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupHeroScene();
        this.setupFleetShips();
        this.setupScrollAnimations();
        this.setupNavigation();
        this.setupFileUpload();
        this.setupModuleAnimations();
    }

setupHeroScene() {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas) return;

    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
        75,
        canvas.clientWidth / canvas.clientHeight,
        0.1,
        1000
    );
    camera.position.set(.2, 2, 45); // 🚀 Start very far
    camera.lookAt(-22, -5, 0);

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    renderer.setClearColor(0x000000, 0);
    renderer.shadowMap.enabled = true;

    // LIGHTS
    scene.add(new THREE.AmbientLight(0xffffff, 0.4));
    const directionalLight = new THREE.DirectionalLight(0xff6b35, 1);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);

    // STARS
    createStars(scene);

    // SPACESHIP
    const loader = new GLTFLoader();
    let spaceship;
    loader.load(
        '/models/spaceship.glb',
        (gltf) => {
            spaceship = gltf.scene;
            spaceship.scale.set(0.5, 0.5, 0.5);
            spaceship.position.set(0, 0, 0);
             spaceship.traverse((child) => {
            if (child.isMesh && child.material) {
                child.material.emissive?.set('#4a2519');
                child.material.emissiveIntensity = 0.3;
                child.material.metalness = 0.6;
                child.material.roughness = 0.4;
            }
        });
            scene.add(spaceship);
        },
        undefined,
        (error) => console.error('Failed to load GLB:', error)
    );

    // CURSOR ROTATION
    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
    });

    // === ZOOM TARGET CONTROL ===
    let zoomTargetZ = 15; // 👈 Start far out
    const zoomRange = { min: 5, max: 12 };

    // ✅ PAGE LOAD ZOOM ANIMATION
    gsap.to({ z: zoomTargetZ }, {
        z: 5,
        duration: 2.5,
        ease: 'power3.out',
        onUpdate: function () {
            zoomTargetZ = this.targets()[0].z;
        },
        onComplete: () => {
            // ✅ ENABLE SCROLL ZOOM AFTER INITIAL ZOOM
            ScrollTrigger.create({
                trigger: '#home',
                start: 'top top',
                end: 'bottom center',
                scrub: true,
                onUpdate: (self) => {
                    zoomTargetZ = THREE.MathUtils.lerp(zoomRange.max, zoomRange.min, self.progress);
                }
            });
        }
    });

    // ANIMATION LOOP
    let time = 0;
    function animate() {
        requestAnimationFrame(animate);
        time += 0.01;

        if (spaceship) {
            spaceship.rotation.y = mouseX * 0.5;
            spaceship.rotation.x = mouseY * 0.3;
            spaceship.position.y = Math.sin(time * 0.8) * 0.2;
        }

        if (stars) {
            stars.rotation.y += 0.0007;
            stars.rotation.x += 0.0003;
        }

        // Smooth camera zoom
        camera.position.z += (zoomTargetZ - camera.position.z) * 0.05;

        renderer.render(scene, camera);
    }

    animate();

    // RESPONSIVE
    window.addEventListener('resize', () => {
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });
}


    setupFleetShips() {
        const shipCanvases = document.querySelectorAll('.ship-canvas');
        shipCanvases.forEach(canvas => {
            const shipType = canvas.getAttribute('data-ship-type');
            createSpaceship(canvas, shipType);
        });
    }

    setupScrollAnimations() {
        gsap.fromTo('.hero-title', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 1.5, ease: 'power3.out' });
        gsap.fromTo('.hero-tagline', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1.2, delay: 0.3, ease: 'power3.out' });
        gsap.fromTo('.hero-description', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1.2, delay: 0.6, ease: 'power3.out' });
        gsap.fromTo('.hero-buttons', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1.2, delay: 0.9, ease: 'power3.out' });
        gsap.fromTo('.hero-stats', { opacity: 0, x: 50 }, { opacity: 1, x: 0, duration: 1.2, delay: 1.2, ease: 'power3.out' });

        gsap.utils.toArray('.section-title').forEach(title => {
            gsap.fromTo(title,
                { opacity: 0, y: 50 },
                {
                    opacity: 1,
                    y: 0,
                    duration: 1,
                    scrollTrigger: {
                        trigger: title,
                        start: 'top 80%',
                        end: 'bottom 20%',
                        toggleActions: 'play none none reverse'
                    }
                }
            );
        });

        gsap.utils.toArray('.ship-card').forEach((card, index) => {
            gsap.fromTo(card,
                { opacity: 0, y: 50, scale: 0.9 },
                {
                    opacity: 1,
                    y: 0,
                    scale: 1,
                    duration: 0.8,
                    delay: index * 0.2,
                    scrollTrigger: {
                        trigger: card,
                        start: 'top 85%',
                        end: 'bottom 15%',
                        toggleActions: 'play none none reverse'
                    }
                }
            );
        });

        gsap.utils.toArray('.module-card').forEach((card, index) => {
            gsap.fromTo(card,
                { opacity: 0, y: 50, scale: 0.9 },
                {
                    opacity: 1,
                    y: 0,
                    scale: 1,
                    duration: 0.8,
                    delay: index * 0.1,
                    scrollTrigger: {
                        trigger: card,
                        start: 'top 85%',
                        end: 'bottom 15%',
                        toggleActions: 'play none none reverse'
                    }
                }
            );
        });

        gsap.utils.toArray('.feature').forEach((feature, index) => {
            gsap.fromTo(feature,
                { opacity: 0, x: -50 },
                {
                    opacity: 1,
                    x: 0,
                    duration: 0.8,
                    delay: index * 0.2,
                    scrollTrigger: {
                        trigger: feature,
                        start: 'top 85%',
                        end: 'bottom 15%',
                        toggleActions: 'play none none reverse'
                    }
                }
            );
        });

        // Force bar fill
        gsap.utils.toArray('.force-fill').forEach(bar => {
            const targetWidth = bar.style.width;
            bar.style.width = '0%';

            gsap.to(bar, {
                width: targetWidth,
                duration: 1.5,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: bar.closest('.module-card'),
                    start: 'top 80%',
                    end: 'bottom 20%',
                    toggleActions: 'play none none reverse'
                }
            });
        });
    }

    setupNavigation() {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    gsap.to(window, {
                        duration: 1.5,
                        scrollTo: targetElement,
                        ease: 'power3.inOut'
                    });
                }
            });
        });

        ScrollTrigger.create({
            start: 'top -80',
            end: 99999,
            toggleClass: { className: 'nav-scrolled', targets: '.nav' }
        });

        document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();

    // Remove active from all
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            // Add active to current
            link.classList.add('active');

            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
            gsap.to(window, {
                duration: 0.6,
                scrollTo: { y: targetElement, offsetY: 90 },
                ease: 'power2.out'
            });
            }
        });
        });     
    }

    setupFileUpload() {
        const uploadZone = document.querySelector('.upload-zone');
        const fileInput = document.getElementById('file-upload');
        const uploadBtn = document.querySelector('.upload-btn');

        uploadBtn.addEventListener('click', () => fileInput.click());
        uploadZone.addEventListener('click', () => fileInput.click());

        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('drag-over');
        });

        uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('drag-over');
            this.handleFiles(e.dataTransfer.files);
        });

        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });
    }

    setupModuleAnimations() {
        const moduleCards = document.querySelectorAll('.module-card');

        moduleCards.forEach((card, index) => {
            card.addEventListener('mouseenter', () => {
                gsap.to(card, { scale: 1.05, duration: 0.3, ease: 'power2.out' });
                const icon = card.querySelector('.module-icon');
                gsap.to(icon, { scale: 1.2, rotation: 10, duration: 0.3, ease: 'back.out(1.7)' });
            });

            card.addEventListener('mouseleave', () => {
                gsap.to(card, { scale: 1, duration: 0.3, ease: 'power2.out' });
                const icon = card.querySelector('.module-icon');
                gsap.to(icon, { scale: 1, rotation: 0, duration: 0.3, ease: 'back.out(1.7)' });
            });

            card.addEventListener('click', () => {
                gsap.to(card, {
                    scale: 0.95,
                    duration: 0.1,
                    yoyo: true,
                    repeat: 1,
                    ease: 'power2.inOut'
                });
            });

            gsap.to(card, {
                y: -5,
                duration: 2 + index * 0.2,
                ease: 'power2.inOut',
                yoyo: true,
                repeat: -1,
                delay: index * 0.1
            });
        });
    }

    handleFiles(files) {
        console.log('Files uploaded:', files);

        const uploadIcon = document.querySelector('.upload-icon');
        const uploadText = document.querySelector('.upload-text');
        const originalIcon = uploadIcon.textContent;
        const originalText = uploadText.textContent;

        uploadIcon.textContent = '✅';
        uploadText.textContent = 'Files uploaded successfully!';

        gsap.to('.upload-zone', {
            scale: 1.05,
            duration: 0.2,
            yoyo: true,
            repeat: 1,
            ease: 'power2.inOut'
        });

        setTimeout(() => {
            uploadIcon.textContent = originalIcon;
            uploadText.textContent = originalText;
        }, 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new StarWarsApp();
});

window.addEventListener('load', () => {
  const loader = document.getElementById('preloader');
  if (loader) {
    loader.classList.add('hidden');
    setTimeout(() => loader.remove(), 500);
  }
});

document.addEventListener('DOMContentLoaded', () => {
  document.body.style.visibility = 'visible';
});


const yodaCanvas = document.getElementById('babyYodaCanvas');
initBabyYoda(yodaCanvas);

document.addEventListener('DOMContentLoaded', () => {
  const toggleButton = document.querySelector('.btn-primary');
  const bb8Canvas = document.getElementById('bb8-easteregg');

  if (toggleButton && bb8Canvas) {
    toggleButton.addEventListener('click', () => {
      toggleBB8(bb8Canvas);
    });
  }
});