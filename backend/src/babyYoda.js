import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

let renderer, scene, camera, yodaModel, animationId;

export function initBabyYoda(canvas) {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(50, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
  camera.position.set(0, 1.5, 3);

  renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  renderer.setClearColor(0x000000, 0);
  renderer.shadowMap.enabled = true;

  const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
  scene.add(light);

  const loader = new GLTFLoader();
  loader.load('/models/baby_yoda.glb', (gltf) => {
    yodaModel = gltf.scene;
    yodaModel.scale.set(0.6, 0.6, 0.6);
    yodaModel.position.set(0, -0.7, 0);
    scene.add(yodaModel);
  });

  // Animate
  animate();

  // Resize handling
  window.addEventListener('resize', () => {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  });
}

function animate() {
  animationId = requestAnimationFrame(animate);
  if (yodaModel) yodaModel.rotation.y += 0.01;
  renderer.render(scene, camera);
}
