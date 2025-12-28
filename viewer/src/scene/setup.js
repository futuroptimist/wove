import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/controls/OrbitControls.js';

const DEFAULT_CAMERA_POSITION = new THREE.Vector3(12, 8, 18);
const DEFAULT_CONTROLS_CONFIG = {
  enableDamping: true,
  dampingFactor: 0.05,
  minDistance: 4,
  maxDistance: 60,
  maxPolarAngle: Math.PI * 0.49,
};

function resolveVector3(value, fallback) {
  if (value instanceof THREE.Vector3) {
    return value.clone();
  }

  if (
    value &&
    typeof value === 'object' &&
    Number.isFinite(value.x) &&
    Number.isFinite(value.y) &&
    Number.isFinite(value.z)
  ) {
    return new THREE.Vector3(value.x, value.y, value.z);
  }

  return fallback.clone();
}

export function createViewerScene(options = {}) {
  const {
    container = document.body,
    backgroundColor = 0x0b0c13,
    cameraFov = 45,
    cameraNear = 0.1,
    cameraFar = 500,
    cameraPosition = DEFAULT_CAMERA_POSITION,
    controlsConfig = {},
    controlsTarget = null,
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
  camera.position.copy(resolveVector3(cameraPosition, DEFAULT_CAMERA_POSITION));

  const {
    enableDamping = DEFAULT_CONTROLS_CONFIG.enableDamping,
    dampingFactor = DEFAULT_CONTROLS_CONFIG.dampingFactor,
    minDistance = DEFAULT_CONTROLS_CONFIG.minDistance,
    maxDistance = DEFAULT_CONTROLS_CONFIG.maxDistance,
    maxPolarAngle = DEFAULT_CONTROLS_CONFIG.maxPolarAngle,
  } = controlsConfig;

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = enableDamping;
  controls.dampingFactor = dampingFactor;
  controls.minDistance = minDistance;
  controls.maxDistance = maxDistance;
  controls.maxPolarAngle = maxPolarAngle;

  if (controlsTarget) {
    controls.target.copy(resolveVector3(controlsTarget, controls.target));
  }

  return {
    renderer,
    scene,
    camera,
    controls,
  };
}

export { THREE };
