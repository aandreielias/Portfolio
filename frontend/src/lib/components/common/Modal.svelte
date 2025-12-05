<script>
    import { createEventDispatcher, onMount, onDestroy } from "svelte";
    import { fade, scale, slide } from "svelte/transition";
    import { quintOut, cubicOut } from "svelte/easing";

    export let title = "";
    export let maxWidth = "800px";
    export let width = "90%";
    export let height = "auto";
    export let maxHeight = "90vh";
    export let scrollableBody = true;
    export let visibleColumns = 1;
    export let maxColumns = 1;
    export let minPanelWidth = 0;

    const dispatch = createEventDispatcher();

    let modalContent;
    let isDragging = false;
    let isCollapsed = false;
    let isMaximized = false;
    let startX;
    let startY;
    let translateX = 0;
    let translateY = 0;
    let initialTranslateX = 0;
    let initialTranslateY = 0;

    // Resize state
    let resizableWidth = null;
    let resizableHeight = null;
    let isResizing = false;
    let resizeDirection = "";
    let startResizeX, startResizeY;
    let startResizeWidth, startResizeHeight;
    let startResizeTX, startResizeTY;
    let activeResizeHandle = null;

    function close() {
        dispatch("close");
    }

    function toggleCollapse() {
        isCollapsed = !isCollapsed;
    }

    function toggleMaximize() {
        if (!isMaximized) {
            // About to maximize
            const windowWidth = window.innerWidth;
            let potentialColumns = 1;

            if (minPanelWidth > 0) {
                // Calculate based on strict panel width requirements
                potentialColumns = Math.floor(windowWidth / minPanelWidth);
            } else if (modalContent) {
                const rect = modalContent.getBoundingClientRect();
                const currentWidth = rect.width;
                // Calculate how many columns fit based on ratio
                const ratio = windowWidth / currentWidth;
                potentialColumns = Math.floor(ratio);
            }

            // Clamp between 1 and maxColumns
            visibleColumns = Math.max(
                1,
                Math.min(potentialColumns, maxColumns),
            );
        } else {
            // Restoring
            visibleColumns = 1;
        }

        isMaximized = !isMaximized;
        // Reset collapse state when expanding
        if (isMaximized) {
            isCollapsed = false;
        }
    }

    function handleKeydown(event) {
        if (event.key === "Escape") {
            close();
        }
    }

    function handlePointerDown(event) {
        if (event.target.closest("button") || event.target.closest("a")) return;
        // Disable drag if maximized
        if (isMaximized) return;

        isDragging = true;
        startX = event.clientX;
        startY = event.clientY;
        initialTranslateX = translateX;
        initialTranslateY = translateY;

        event.currentTarget.setPointerCapture(event.pointerId);
    }

    function handlePointerMove(event) {
        if (!isDragging) return;

        const dx = event.clientX - startX;
        const dy = event.clientY - startY;

        let newX = initialTranslateX + dx;
        let newY = initialTranslateY + dy;

        if (modalContent) {
            const rect = modalContent.getBoundingClientRect();
            const xLimit = (window.innerWidth - rect.width) / 2;
            const yLimit = (window.innerHeight - rect.height) / 2;

            const minX = Math.min(-xLimit, xLimit);
            const maxX = Math.max(-xLimit, xLimit);
            const minY = Math.min(-yLimit, yLimit);
            const maxY = Math.max(-yLimit, yLimit);

            newX = Math.max(minX, Math.min(maxX, newX));
            newY = Math.max(minY, Math.min(maxY, newY));
        }

        translateX = newX;
        translateY = newY;
    }

    function handlePointerUp(event) {
        isDragging = false;
        event.currentTarget.releasePointerCapture(event.pointerId);
    }

    // Resize Handlers
    function handleResizeStart(event, direction) {
        event.preventDefault();
        event.stopPropagation();

        // Disable resize if maximized
        if (isMaximized) return;

        activeResizeHandle = event.currentTarget;
        activeResizeHandle.setPointerCapture(event.pointerId);

        isResizing = true;
        resizeDirection = direction;
        startResizeX = event.clientX;
        startResizeY = event.clientY;

        const rect = modalContent.getBoundingClientRect();
        startResizeWidth = rect.width;
        startResizeHeight = rect.height;
        startResizeTX = translateX;
        startResizeTY = translateY;

        // Initialize resizable values if they are null
        if (!resizableWidth) resizableWidth = `${rect.width}px`;
        if (!resizableHeight) resizableHeight = `${rect.height}px`;

        window.addEventListener("pointermove", handleResizeMove);
        window.addEventListener("pointerup", handleResizeEnd);
    }

    function handleResizeMove(event) {
        if (!isResizing) return;

        const dx = event.clientX - startResizeX;
        const dy = event.clientY - startResizeY;

        let newW = startResizeWidth;
        let newH = startResizeHeight;
        let newTX = startResizeTX;
        let newTY = startResizeTY;

        // Calculate raw new dimensions
        if (resizeDirection.includes("e")) {
            newW = startResizeWidth + dx;
        } else if (resizeDirection.includes("w")) {
            newW = startResizeWidth - dx;
        }

        if (resizeDirection.includes("s")) {
            newH = startResizeHeight + dy;
        } else if (resizeDirection.includes("n")) {
            newH = startResizeHeight - dy;
        }

        // Constraints
        if (newW < 300) newW = 300;
        if (newH < 200) newH = 200;

        // Calculate position shifts based on ACTUAL dimension changes
        const deltaW = newW - startResizeWidth;
        const deltaH = newH - startResizeHeight;

        if (resizeDirection.includes("e")) {
            newTX = startResizeTX + deltaW / 2;
        } else if (resizeDirection.includes("w")) {
            newTX = startResizeTX - deltaW / 2;
        }

        if (resizeDirection.includes("s")) {
            newTY = startResizeTY + deltaH / 2;
        } else if (resizeDirection.includes("n")) {
            newTY = startResizeTY - deltaH / 2;
        }

        resizableWidth = `${newW}px`;
        resizableHeight = `${newH}px`;
        translateX = newTX;
        translateY = newTY;
    }

    function handleResizeEnd(event) {
        isResizing = false;

        if (activeResizeHandle) {
            activeResizeHandle.releasePointerCapture(event.pointerId);
            activeResizeHandle = null;
        }

        window.removeEventListener("pointermove", handleResizeMove);
        window.removeEventListener("pointerup", handleResizeEnd);
    }

    onMount(() => {
        window.addEventListener("keydown", handleKeydown);
        document.body.style.overflow = "hidden";
    });

    onDestroy(() => {
        window.removeEventListener("keydown", handleKeydown);
        document.body.style.overflow = "";
        if (typeof window !== "undefined") {
            window.removeEventListener("pointermove", handleResizeMove);
            window.removeEventListener("pointerup", handleResizeEnd);
        }
    });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
    class="modal-backdrop"
    on:click={close}
    transition:fade={{ duration: 200 }}
>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div
        class="modal-content glass-panel"
        class:maximized={isMaximized}
        bind:this={modalContent}
        on:click|stopPropagation
        style="
            --max-width: {isMaximized
            ? '100vw'
            : resizableWidth
              ? '100vw'
              : maxWidth}; 
            --width: {isMaximized ? '100vw' : resizableWidth || width}; 
            --height: {isMaximized
            ? '100vh'
            : isCollapsed
              ? 'auto'
              : resizableHeight || height}; 
            --max-height: {isMaximized ? '100vh' : maxHeight}; 
            transform: {isMaximized
            ? 'translate(0px, 0px)'
            : `translate(${translateX}px, ${translateY}px)`};
        "
        transition:scale={{
            duration: 300,
            start: 0.95,
            opacity: 0,
            easing: quintOut,
        }}
    >
        <!-- Resize Handles -->
        {#if !isMaximized}
            <div
                class="resize-handle n"
                on:pointerdown={(e) => handleResizeStart(e, "n")}
            ></div>
            <div
                class="resize-handle s"
                on:pointerdown={(e) => handleResizeStart(e, "s")}
            ></div>
            <div
                class="resize-handle e"
                on:pointerdown={(e) => handleResizeStart(e, "e")}
            ></div>
            <div
                class="resize-handle w"
                on:pointerdown={(e) => handleResizeStart(e, "w")}
            ></div>
            <div
                class="resize-handle ne"
                on:pointerdown={(e) => handleResizeStart(e, "ne")}
            ></div>
            <div
                class="resize-handle nw"
                on:pointerdown={(e) => handleResizeStart(e, "nw")}
            ></div>
            <div
                class="resize-handle se"
                on:pointerdown={(e) => handleResizeStart(e, "se")}
            ></div>
            <div
                class="resize-handle sw"
                on:pointerdown={(e) => handleResizeStart(e, "sw")}
            ></div>
        {/if}

        <div class="window-controls">
            <button
                class="maximize-btn"
                on:click={toggleMaximize}
                aria-label="Maximize"
            ></button>
            <button class="close-btn" on:click={close} aria-label="Close"
            ></button>
        </div>

        {#if title || $$slots.header}
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div
                class="modal-header"
                on:pointerdown={handlePointerDown}
                on:pointermove={handlePointerMove}
                on:pointerup={handlePointerUp}
                on:pointercancel={handlePointerUp}
                style="cursor: {isMaximized ? 'default' : 'grab'};"
            >
                {#if title}
                    <h1>{title}</h1>
                {/if}
                <slot name="header" />
            </div>
        {/if}

        <div class="body-wrapper" class:collapsed={isCollapsed}>
            <div
                class="modal-body"
                class:scrollable={scrollableBody}
                class:no-scroll={!scrollableBody}
            >
                <slot />
            </div>
        </div>
    </div>
</div>

<style>
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        backdrop-filter: blur(8px);
    }

    .modal-content {
        background-color: var(--color-bg);
        width: var(--width);
        max-width: var(--max-width);
        height: var(--height);
        max-height: var(--max-height);
        border-radius: var(--radius);
        padding: 0; /* Remove padding to allow full-width header */
        position: relative;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        border: 1px solid var(--glass-border);
        display: flex;
        flex-direction: column;
        /* Important for transform to work as expected without layout shifts */
        will-change: transform;
        /* overflow: hidden; Removed to allow resize handles to be grabbed easily if needed, but keeping handles inside for now */
        overflow: hidden;
        transition:
            width 0.3s ease,
            height 0.3s ease,
            max-width 0.3s ease,
            max-height 0.3s ease,
            transform 0.3s ease,
            border-radius 0.3s ease;
    }

    .modal-content.maximized {
        border-radius: 0;
        border: none;
    }

    .modal-content.collapsed {
        height: auto !important;
    }

    /* Resize Handles */
    .resize-handle {
        position: absolute;
        z-index: 100;
        touch-action: none;
    }

    .n {
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        cursor: ns-resize;
    }
    .s {
        bottom: 0;
        left: 0;
        right: 0;
        height: 6px;
        cursor: ns-resize;
    }
    .e {
        right: 0;
        top: 0;
        bottom: 0;
        width: 6px;
        cursor: ew-resize;
    }
    .w {
        left: 0;
        top: 0;
        bottom: 0;
        width: 6px;
        cursor: ew-resize;
    }

    .ne {
        top: 0;
        right: 0;
        width: 12px;
        height: 12px;
        cursor: ne-resize;
        z-index: 101;
    }
    .nw {
        top: 0;
        left: 0;
        width: 12px;
        height: 12px;
        cursor: nw-resize;
        z-index: 101;
    }
    .se {
        bottom: 0;
        right: 0;
        width: 12px;
        height: 12px;
        cursor: se-resize;
        z-index: 101;
    }
    .sw {
        bottom: 0;
        left: 0;
        width: 12px;
        height: 12px;
        cursor: sw-resize;
        z-index: 101;
    }

    .window-controls {
        position: absolute;
        top: 1.5rem;
        right: 1.5rem;
        display: flex;
        gap: 0.75rem;
        z-index: 10;
    }

    .close-btn,
    .maximize-btn {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        border: none;
        cursor: pointer;
        padding: 0;
        transition:
            transform 0.2s,
            background-color 0.2s;
    }

    .close-btn {
        background-color: #ef4444;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }

    .close-btn:hover {
        transform: scale(1.2);
        background-color: #d64a4a;
    }

    .maximize-btn {
        background-color: #1fa34f;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
    }

    .maximize-btn:hover {
        transform: scale(1.2);
        background-color: #155f30;
    }

    .modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        /* Move padding here to make the drag area larger */
        padding: 3rem 3rem 1.5rem 3rem;
        border-bottom: 1px solid var(--glass-border);
        flex-shrink: 0;
        user-select: none; /* Prevent text selection while dragging */
        background: var(--glass-panel-bg); /* Ensure header has background */
        transition: padding 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Center text when collapsed */
    .modal-content.collapsed .modal-header {
        padding-top: 1rem;
        padding-bottom: 1rem;
        border-bottom: none; /* Optional: remove border when collapsed for cleaner look */
    }

    .modal-header:active {
        cursor: grabbing !important;
    }

    h1 {
        margin: 0;
        font-size: 2rem;
        line-height: 1;
        background: var(--gradient-heading);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Smooth collapse animation wrapper */
    .body-wrapper {
        display: grid;
        grid-template-rows: 1fr;
        transition: grid-template-rows 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        flex: 1; /* Take remaining vertical space */
        min-height: 0; /* Allow shrinking below content size */
    }

    .body-wrapper.collapsed {
        grid-template-rows: 0fr;
    }

    .modal-body {
        flex: 1;
        display: flex;
        flex-direction: column;
        /* Ensure content doesn't get cut off if it's scrollable */
        min-height: 0;
        padding: 2rem 3rem 3rem 3rem; /* Add padding to body */
        overflow: hidden; /* Required for grid transition to hide content */
        transition:
            padding 0.4s cubic-bezier(0.16, 1, 0.3, 1),
            opacity 0.3s ease;
        opacity: 1;
    }

    .body-wrapper.collapsed .modal-body {
        padding-top: 0;
        padding-bottom: 0;
        opacity: 0;
    }

    .modal-body.scrollable {
        overflow-y: auto;
    }

    /* Custom Scrollbar */
    .modal-body.scrollable::-webkit-scrollbar {
        width: 8px;
    }

    .modal-body.scrollable::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }

    .modal-body.scrollable::-webkit-scrollbar-thumb {
        background: var(--glass-border);
        border-radius: 4px;
    }

    .modal-body.scrollable::-webkit-scrollbar-thumb:hover {
        background: var(--color-text-muted);
    }

    .modal-body.no-scroll {
        overflow-y: hidden;
    }
</style>
