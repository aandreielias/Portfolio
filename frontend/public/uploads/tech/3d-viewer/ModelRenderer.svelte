<script>
    import { onMount, onDestroy } from "svelte";
    import * as THREE from "three";
    import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader.js";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

    let container;
    let scene, camera, renderer, controls;
    let directionalLight, ambientLight;
    let isLoading = true;
    let loadingProgress = 0;
    let resizeObserver;
    let animationId;

    export let lightIntensity = 1.2;

    const BASE_URL = import.meta.env.BASE_URL;
    const MODEL_PATH = `${BASE_URL}uploads/tech/3d-viewer/model.obj`;
    const TEXTURE_PATH = `${BASE_URL}uploads/tech/3d-viewer/texture.jpg`;

    onMount(() => {
        init();
        loadModel();
        animate();

        // Handle window resizing
        resizeObserver = new ResizeObserver(() => {
            if (container) {
                const width = container.clientWidth;
                const height = container.clientHeight;
                camera.aspect = width / height;
                camera.updateProjectionMatrix();
                renderer.setSize(width, height);
            }
        });
        resizeObserver.observe(container);
    });

    onDestroy(() => {
        if (resizeObserver) resizeObserver.disconnect();
        cancelAnimationFrame(animationId);
        if (renderer) renderer.dispose();
        if (controls) controls.dispose();
    });

    function init() {
        const width = container.clientWidth;
        const height = container.clientHeight;

        // Initialize Scene
        scene = new THREE.Scene();
        scene.background = null;

        // Initialize Camera
        camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
        camera.position.set(0, 0, 80);

        // Initialize Renderer
        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(width, height);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.outputColorSpace = THREE.SRGBColorSpace;
        container.appendChild(renderer.domElement);

        // Initialize Controls
        controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 20;
        controls.maxDistance = 200;

        // Restrict rotation to horizontal axis only
        controls.minPolarAngle = Math.PI / 2;
        controls.maxPolarAngle = Math.PI / 2;

        // Initialize Lights
        ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
        scene.add(ambientLight);

        directionalLight = new THREE.DirectionalLight(0xffffff, lightIntensity);
        directionalLight.position.set(5, 10, 7.5);
        scene.add(directionalLight);
    }

    function loadModel() {
        const textureLoader = new THREE.TextureLoader();
        const objLoader = new OBJLoader();

        // Load Texture
        const texture = textureLoader.load(
            TEXTURE_PATH,
            (tex) => {
                tex.colorSpace = THREE.SRGBColorSpace;
            },
            undefined,
            (err) => console.error("Error loading texture:", err),
        );

        // Load OBJ Model
        objLoader.load(
            MODEL_PATH,
            (object) => {
                object.traverse((child) => {
                    if (child.isMesh) {
                        child.material.map = texture;
                        child.material.roughness = 0.6;
                        child.material.metalness = 0.0;
                        child.material.needsUpdate = true;
                    }
                });

                // Center and Scale the model
                const box = new THREE.Box3().setFromObject(object);
                const size = box.getSize(new THREE.Vector3());

                const maxDim = Math.max(size.x, size.y, size.z);
                const scale = 50 / maxDim;

                object.scale.set(scale, scale, scale);
                // Correct orientation
                object.rotation.x = -Math.PI / 2;

                // Adjust position
                object.position.x = 0;
                object.position.y = -28;
                object.position.z = 0;

                scene.add(object);
                isLoading = false;
            },
            (xhr) => {
                if (xhr.lengthComputable) {
                    loadingProgress = (xhr.loaded / xhr.total) * 100;
                }
            },
            (error) => {
                console.error("Error loading model:", error);
                isLoading = false;
            },
        );
    }

    function animate() {
        animationId = requestAnimationFrame(animate);
        if (controls) controls.update();
        if (directionalLight) directionalLight.intensity = lightIntensity;
        if (renderer && scene && camera) renderer.render(scene, camera);
    }
</script>

<div class="viz-container">
    <div class="canvas-wrapper" bind:this={container}></div>

    {#if isLoading}
        <div class="loading-overlay">
            <div class="spinner"></div>
            <div class="loading-text">
                Loading Model... {Math.round(loadingProgress)}%
            </div>
        </div>
    {/if}

    <div class="controls-overlay">
        <div class="control-group">
            <label for="light">Lighting</label>
            <input
                id="light"
                type="range"
                min="0"
                max="3"
                step="0.1"
                bind:value={lightIntensity}
            />
        </div>
    </div>
</div>

<style>
    .viz-container {
        width: 100%;
        height: 100%;
        position: relative;
        overflow: hidden;
        background: #f0f0f0;
        border-radius: var(--radius);
    }

    .loading-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(240, 240, 240, 0.8);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 20;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #ddd;
        border-top: 4px solid var(--color-primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }

    .loading-text {
        font-family: var(--font-sans);
        color: var(--color-text);
        font-weight: 500;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    .canvas-wrapper {
        width: 100%;
        height: 100%;
    }

    .controls-overlay {
        position: absolute;
        bottom: 1.5rem;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        padding: 0.8rem 1.5rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        z-index: 10;
        display: flex;
        gap: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    .control-group {
        display: flex;
        align-items: center;
        gap: 1rem;
        font-family: var(--font-sans);
        font-size: 0.9rem;
        font-weight: 500;
    }

    input[type="range"] {
        -webkit-appearance: none;
        appearance: none;
        width: 150px;
        height: 6px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        outline: none;
        cursor: pointer;
    }

    input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: white;
        cursor: pointer;
        transition: transform 0.1s;
    }

    input[type="range"]::-webkit-slider-thumb:hover {
        transform: scale(1.2);
    }
</style>
