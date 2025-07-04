import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

let bb8, scene, camera, renderer, animationId;
let isVisible = false;

export function toggleBB8(canvas) {
  if (isVisible) {
    cancelAnimationFrame(animationId);
    if (bb8 && scene) scene.remove(bb8);
    if (renderer) renderer.dispose();
    canvas.style.display = 'none';
    isVisible = false;
    return;
  }

  isVisible = true;
  canvas.style.display = 'block';

  // 🔧 Fullscreen canvas
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  canvas.style.position = 'fixed';
  canvas.style.top = '0';
  canvas.style.left = '0';
  canvas.style.width = '100vw';
  canvas.style.height = '100vh';
  canvas.style.zIndex = '999';
  canvas.style.pointerEvents = 'none';

  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 5;

  renderer = new THREE.WebGLRenderer({ canvas, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);

  const light = new THREE.AmbientLight(0xffffff, 1.2);
  scene.add(light);

  const loader = new GLTFLoader();
  loader.load('/models/bb8.glb', (gltf) => {
    bb8 = gltf.scene;
    bb8.scale.set(0.7, 0.7, 0.7);
    bb8.position.set(0, 0, 0);
    scene.add(bb8);
  });

  function animate() {
    animationId = requestAnimationFrame(animate);
    if (bb8) bb8.rotation.y += 0.01;
    renderer.render(scene, camera);
  }

  animate();

  // ✅ Mouse moves BB8 across full screen width/height
  window.addEventListener('mousemove', (event) => {
    if (bb8) {
      const x = (event.clientX / window.innerWidth) * 2 - 1;
      const y = -(event.clientY / window.innerHeight) * 2 + 1;

      // 🔧 Multiply for more visible movement
      const maxX = 3; // left-right limit
      const maxY = 2; // up-down limit
      bb8.position.x = x * maxX;
      bb8.position.y = y * maxY;
    }
  });

  // 📱 Resize support
  window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
}
