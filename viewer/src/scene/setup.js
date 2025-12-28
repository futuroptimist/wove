import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/controls/OrbitControls.js';

export function createViewerScene(options = {}) {
  const {
    container = document.body,
    backgroundColor = 0x0b0c13,
    cameraFov = 45,
    cameraNear = 0.1,
    cameraFar = 500,
  } = options;

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(backgroundColor);

  const camera = new THREE.PerspectiveCamera(
    cameraFov,
    window.innerWidth / window.innerHeight,
    cameraNear,
    cameraFar,
  );
  camera.position.set(12, 8, 18);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.minDistance = 4;
  controls.maxDistance = 60;
  controls.maxPolarAngle = Math.PI * 0.49;

  return {
    renderer,
    scene,
    camera,
    controls,
  };
}

export { THREE };
