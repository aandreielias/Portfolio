<script>
    import { onDestroy, onMount } from "svelte";
    import { fade, scale } from "svelte/transition";
    import {
        imageViewerStore,
        closeImage,
    } from "../../stores/imageViewerStore.js";

    let isOpen = false;
    let src = "";
    let alt = "";
    let zoomLevel = 1;
    let isDragging = false;
    let startX, startY;
    let translateX = 0;
    let translateY = 0;

    const unsubscribe = imageViewerStore.subscribe((state) => {
        isOpen = state.isOpen;
        src = state.src;
        alt = state.alt;
        if (!state.isOpen) {
            resetZoom();
        }
    });

    function resetZoom() {
        zoomLevel = 1;
        translateX = 0;
        translateY = 0;
    }

    function handleWheel(event) {
        event.preventDefault();
        const delta = event.deltaY * -0.001;
        const newZoom = Math.min(Math.max(1, zoomLevel + delta), 5);
        zoomLevel = newZoom;
    }

    function handleKeydown(event) {
        if (event.key === "Escape") {
            closeImage();
        }
    }

    function handleMouseDown(event) {
        if (zoomLevel > 1) {
            isDragging = true;
            startX = event.clientX - translateX;
            startY = event.clientY - translateY;
            event.preventDefault(); // Prevent default drag behavior
        }
    }

    function handleMouseMove(event) {
        if (isDragging && zoomLevel > 1) {
            translateX = event.clientX - startX;
            translateY = event.clientY - startY;
        }
    }

    function handleMouseUp() {
        isDragging = false;
    }

    onMount(() => {
        window.addEventListener("keydown", handleKeydown);
    });

    onDestroy(() => {
        unsubscribe();
        window.removeEventListener("keydown", handleKeydown);
    });
</script>

{#if isOpen}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div
        class="viewer-backdrop"
        transition:fade={{ duration: 200 }}
        on:click|self={closeImage}
    >
        <div
            class="viewer-content"
            transition:scale={{ duration: 300, start: 0.9 }}
            on:wheel={handleWheel}
            on:mousedown={handleMouseDown}
            on:mousemove={handleMouseMove}
            on:mouseup={handleMouseUp}
            on:mouseleave={handleMouseUp}
        >
            <button class="close-btn" on:click={closeImage} aria-label="Close"
            ></button>
            <img
                {src}
                {alt}
                style="transform: scale({zoomLevel}) translate({translateX /
                    zoomLevel}px, {translateY / zoomLevel}px);"
                draggable="false"
            />
        </div>
    </div>
{/if}

<style>
    .viewer-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 2000;
        backdrop-filter: blur(5px);
    }

    .viewer-content {
        position: relative;
        max-width: 90vw;
        max-height: 90vh;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 12px; /* Rounded edges as requested */
        overflow: hidden; /* Clip image to rounded edges */
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        background: #000;
    }

    img {
        max-width: 100%;
        max-height: 90vh;
        object-fit: contain;
        transition: transform 0.1s ease-out;
        cursor: grab;
        display: block;
    }

    img:active {
        cursor: grabbing;
    }

    .close-btn {
        position: absolute;
        top: 20px;
        right: 20px; /* Positioned "above" (inside top right) */
        width: 16px;
        height: 16px;
        background-color: #ff5f56; /* Red dot */
        border-radius: 50%;
        border: none;
        cursor: pointer;
        z-index: 10;
        transition: transform 0.2s;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    .close-btn:hover {
        transform: scale(1.2);
        background-color: #ff3b30;
    }
</style>
