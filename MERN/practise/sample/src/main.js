import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 1, 3);

const renderer = new THREE.WebGLRenderer({ antialias: true });
const duckDiv = document.getElementById('duck');
renderer.setSize(window.innerWidth, window.innerHeight);
duckDiv.appendChild(renderer.domElement);

// Lighting
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(2, 2, 2);
scene.add(light);

const ambient = new THREE.AmbientLight(0x404040, 1);
scene.add(ambient);

// Load the 3D model
const loader = new GLTFLoader();

let duckModel = null;

loader.load(
  '/blind_man.glb',
  function (gltf) {
    duckModel = gltf.scene;
    duckModel.position.set(0, 0, 0);
    duckModel.scale.set(1, 1, 1);
    scene.add(duckModel);
  },
  undefined,
  function (error) {
    console.error('Error loading model:', error);
  }
);

// Helper function to interpolate between two values
function lerp(start, end, t) {
  return start + (end - start) * t;
}

// Helper function to interpolate between two THREE.Vector3
function lerpVector3(start, end, t) {
  return new THREE.Vector3(
    lerp(start.x, end.x, t),
    lerp(start.y, end.y, t),
    lerp(start.z, end.z, t)
  );
}

// Keyframes for scrollPercent and corresponding properties
const keyframes = [
  {
    scroll: 0,
    position: new THREE.Vector3(0, 0, 0),
    scale: new THREE.Vector3(1, 1, 1),
    rotation: new THREE.Euler(0, 0, 0),
  },
  {
    scroll: 0.5,
    position: new THREE.Vector3(0, -1, 0),
    scale: new THREE.Vector3(2, 2, 2),
    rotation: new THREE.Euler(0, Math.PI, 0),
  },
  {
    scroll: 1,
    position: new THREE.Vector3(0, -2, 0),
    scale: new THREE.Vector3(3, 3, 3),
    rotation: new THREE.Euler(0, 2 * Math.PI, 0),
  },
];

// Scroll event to map scroll position to model properties with custom keyframes
window.addEventListener('scroll', () => {
  if (duckModel) {
    const scrollTop = window.scrollY || window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = Math.min(Math.max(scrollTop / docHeight, 0), 1);

    // Update 3D model properties
    let startKeyframe = keyframes[0];
    let endKeyframe = keyframes[keyframes.length - 1];

    for (let i = 0; i < keyframes.length - 1; i++) {
      if (scrollPercent >= keyframes[i].scroll && scrollPercent <= keyframes[i + 1].scroll) {
        startKeyframe = keyframes[i];
        endKeyframe = keyframes[i + 1];
        break;
      }
    }

    const localT = (scrollPercent - startKeyframe.scroll) / (endKeyframe.scroll - startKeyframe.scroll);

    const position = lerpVector3(startKeyframe.position, endKeyframe.position, localT);
    const scale = lerpVector3(startKeyframe.scale, endKeyframe.scale, localT);

    const rotation = new THREE.Euler(
      lerp(startKeyframe.rotation.x, endKeyframe.rotation.x, localT),
      lerp(startKeyframe.rotation.y, endKeyframe.rotation.y, localT),
      lerp(startKeyframe.rotation.z, endKeyframe.rotation.z, localT)
    );

    duckModel.position.copy(position);
    duckModel.scale.copy(scale);
    duckModel.rotation.copy(rotation);
  }
});

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Animate
function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();
