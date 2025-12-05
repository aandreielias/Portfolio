<script>
    import { fade } from "svelte/transition";
    import Modal from "../common/Modal.svelte";
    import TechCompiler from "./TechCompiler.svelte";
    import TechRun from "./TechRun.svelte";
    import TechCode from "./TechCode.svelte";
    import TechDescription from "./TechDescription.svelte";
    import ModelRenderer from "./visualizations/ModelRenderer.svelte";

    export let techItem;
    export let close;

    let activeTab = "description";
    let compiledData = null;
    let error = null;
    let visibleColumns = 1;

    // Resizing State
    let panelSizes = [];
    let isResizing = false;
    let activeResizerIndex = -1;
    let startX = 0;
    let startSizes = [];
    let layoutContainer;

    function handleCompiled(event) {
        compiledData = event.detail;
        error = null;
    }

    function handleError(event) {
        error = event.detail;
        compiledData = null;
    }

    // Switch away from description tab if entering split mode (2 or more columns)
    $: if (visibleColumns >= 2 && activeTab === "description") {
        activeTab = "run";
    }

    // Initialize or Reset panel sizes when column count changes
    $: if (visibleColumns) {
        // Only reset if the count changes, to preserve sizes during other updates if needed
        if (panelSizes.length !== visibleColumns) {
            panelSizes = new Array(visibleColumns).fill(100 / visibleColumns);
        }
    }

    const MIN_PANEL_WIDTH_PX = 375;

    function startResize(index, event) {
        isResizing = true;
        activeResizerIndex = index;
        startX = event.clientX;
        startSizes = [...panelSizes];

        // Prevent text selection during drag
        document.body.style.userSelect = "none";
        document.body.style.cursor = "col-resize";

        window.addEventListener("pointermove", onResize);
        window.addEventListener("pointerup", stopResize);
    }

    function onResize(event) {
        if (!isResizing || !layoutContainer) return;

        const containerWidth = layoutContainer.getBoundingClientRect().width;
        const dx = event.clientX - startX;
        const dxPercent = (dx / containerWidth) * 100;

        const leftIndex = activeResizerIndex;
        const rightIndex = activeResizerIndex + 1;

        const newLeft = startSizes[leftIndex] + dxPercent;
        const newRight = startSizes[rightIndex] - dxPercent;

        // Calculate min percent dynamically based on 340px
        const minPercent = (MIN_PANEL_WIDTH_PX / containerWidth) * 100;

        if (newLeft > minPercent && newRight > minPercent) {
            panelSizes[leftIndex] = newLeft;
            panelSizes[rightIndex] = newRight;
        }
    }

    function stopResize() {
        isResizing = false;
        document.body.style.userSelect = "";
        document.body.style.cursor = "";
        window.removeEventListener("pointermove", onResize);
        window.removeEventListener("pointerup", stopResize);
    }
</script>

<Modal
    title={techItem.title}
    on:close={close}
    width="800px"
    maxWidth="95vw"
    maxHeight="95vh"
    scrollableBody={false}
    bind:visibleColumns
    maxColumns={3}
    minPanelWidth={375}
>
    <!-- Layout Wrapper -->
    <div class="layout-container" bind:this={layoutContainer} style="gap: 0;">
        <!-- Left Panel: Description (Index 0 in 2+ cols) -->
        {#if visibleColumns >= 2}
            <div
                class="panel description-panel"
                style="width: {panelSizes[0]}%; flex: none;"
                in:fade={{ duration: 200 }}
            >
                <TechDescription
                    id={techItem.id}
                    description={techItem.description}
                    files={techItem.files}
                    title={techItem.title}
                />
            </div>

            <!-- Resizer 0 -->
            <div class="resizer" on:pointerdown={(e) => startResize(0, e)}>
                <div class="resizer-line"></div>
            </div>
        {/if}

        {#if visibleColumns === 3}
            <!-- Middle Panel: Run (Index 1) -->
            <div
                class="panel run-panel"
                style="width: {panelSizes[1]}%; flex: none;"
                in:fade={{ duration: 200 }}
            >
                <div class="panel-header">Run</div>
                <div class="panel-content">
                    {#if techItem.id === "3d-viewer"}
                        <div
                            class="viewer-container"
                            style="width: 100%; height: 100%; display: flex; flex-direction: column; background: var(--code-view-bg);"
                        >
                            <ModelRenderer />
                        </div>
                    {:else if error}
                        <div class="error">
                            <span class="error-icon">⚠️</span>
                            {error.message}
                        </div>
                    {:else if compiledData}
                        <TechRun techId={techItem.id} data={compiledData} />
                    {:else}
                        <div class="loading-container">
                            <div class="loading-bar">
                                <div class="loading-progress"></div>
                            </div>
                            <p>Initializing Environment...</p>
                        </div>
                    {/if}
                </div>
            </div>

            <!-- Resizer 1 -->
            <div class="resizer" on:pointerdown={(e) => startResize(1, e)}>
                <div class="resizer-line"></div>
            </div>

            <!-- Right Panel: Code (Index 2) -->
            <div
                class="panel code-panel"
                style="width: {panelSizes[2]}%; flex: none;"
                in:fade={{ duration: 200 }}
            >
                <div class="panel-header">Code</div>
                <div class="panel-content">
                    <TechCode files={techItem.files} />
                </div>
            </div>
        {:else}
            <!-- Columns is 1 or 2. -->
            <!-- If 2 cols, this is Panel Index 1. If 1 col, standard flex. -->
            <div
                class="main-panel"
                style={visibleColumns === 2
                    ? `width: ${panelSizes[1]}%; flex: none;`
                    : "flex: 1;"}
            >
                <div class="tabs">
                    {#if visibleColumns === 1}
                        <button
                            class:active={activeTab === "description"}
                            on:click={() => (activeTab = "description")}
                        >
                            Description
                        </button>
                    {/if}
                    <button
                        class:active={activeTab === "run"}
                        on:click={() => (activeTab = "run")}
                    >
                        Run
                    </button>
                    <button
                        class:active={activeTab === "code"}
                        on:click={() => (activeTab = "code")}
                    >
                        Code
                    </button>
                </div>

                <div class="tab-content">
                    {#if activeTab === "run"}
                        <div class="tab-pane" in:fade={{ duration: 200 }}>
                            {#if techItem.id === "3d-viewer"}
                                <div
                                    class="viewer-container"
                                    style="width: 100%; height: 100%; min-height: 500px; display: flex; flex-direction: column; background: var(--code-view-bg);"
                                >
                                    <ModelRenderer />
                                </div>
                            {:else if error}
                                <div class="error">
                                    <span class="error-icon">⚠️</span>
                                    {error.message}
                                </div>
                            {:else if compiledData}
                                <!-- DEBUG: Remove in production -->
                                <!-- <pre style="color:white; font-size: 10px;">{JSON.stringify(compiledData)}</pre> -->
                                <TechRun
                                    techId={techItem.id}
                                    data={compiledData}
                                />
                            {:else}
                                <div class="loading-container">
                                    <div class="loading-bar">
                                        <div class="loading-progress"></div>
                                    </div>
                                    <p>Initializing Environment...</p>
                                </div>
                            {/if}
                        </div>
                    {:else if activeTab === "code"}
                        <div
                            class="tab-pane"
                            in:fade={{ duration: 200 }}
                            style="min-height: 500px;"
                        >
                            <TechCode files={techItem.files} />
                        </div>
                    {:else if activeTab === "description" && visibleColumns === 1}
                        <div class="tab-pane" in:fade={{ duration: 200 }}>
                            <TechDescription
                                id={techItem.id}
                                description={techItem.description}
                                files={techItem.files}
                                title={techItem.title}
                            />
                        </div>
                    {/if}
                </div>
            </div>
        {/if}
    </div>

    <!-- Hidden Compiler (always runs) -->
    <div style="display: none;">
        <TechCompiler
            files={techItem.files}
            language={techItem.language}
            on:compiled={handleCompiled}
            on:error={handleError}
        />
    </div>
</Modal>

<style>
    .layout-container {
        display: flex;
        flex-direction: row;
        height: 100%;
        width: 100%;
        overflow: hidden;
    }

    .panel {
        display: flex;
        flex-direction: column;
        overflow: hidden;
        min-width: 0;
        /* Border handled by resizer aesthetics or individual styling */
    }

    .resizer {
        width: 24px;
        cursor: col-resize;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-shrink: 0;
        z-index: 10;
        user-select: none;
        touch-action: none;
        background: transparent;
    }

    .resizer-line {
        width: 3px;
        height: 90%;
        background: var(--color-text);
        opacity: 0.3;
        border-radius: 10px;
        transition: all 0.2s;
    }

    .resizer:hover .resizer-line,
    .resizer:active .resizer-line {
        width: 5px;
        opacity: 0.8;
        background: var(--color-primary);
        box-shadow: 0 0 10px var(--color-primary);
    }

    .description-panel {
        overflow-y: auto;
    }
    .description-panel::-webkit-scrollbar {
        width: 4px;
    }
    .description-panel::-webkit-scrollbar-track {
        background: transparent;
    }
    .description-panel::-webkit-scrollbar-thumb {
        background: var(--glass-border);
        border-radius: 2px;
    }

    .panel-header {
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--glass-border);
        font-size: 1.1rem;
        color: var(--color-primary);
        font-weight: 600;
        flex-shrink: 0;
    }

    .panel-content {
        flex: 1;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }

    .main-panel {
        display: flex;
        flex-direction: column;
        overflow: hidden;
        min-width: 0;
    }

    .tabs {
        display: flex;
        gap: 2rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid var(--glass-border);
        padding-bottom: 0.5rem;
        flex-shrink: 0;
    }
    .tabs button {
        padding: 0.5rem 0;
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1.1rem;
        color: var(--color-text-muted);
        border-bottom: 2px solid transparent;
        transition: all 0.2s;
    }
    .tabs button:hover {
        color: var(--color-text);
    }
    .tabs button.active {
        color: var(--color-primary);
        border-bottom-color: var(--color-primary);
        text-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
    }
    .tab-content {
        flex: 1;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        position: relative;
    }
    .tab-pane {
        width: 100%;
        flex: 1;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    .error {
        color: #f87171;
        padding: 2rem;
        background: rgba(239, 68, 68, 0.1);
        border-radius: var(--radius);
        border: 1px solid rgba(239, 68, 68, 0.2);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: var(--color-text-muted);
    }
    .loading-bar {
        width: 200px;
        height: 4px;
        background: var(--loading-bar-bg);
        border-radius: 2px;
        overflow: hidden;
        margin-bottom: 1rem;
        position: relative;
    }
    .loading-progress {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 50%;
        background: var(--color-primary);
        border-radius: 2px;
        animation: loading 1.5s infinite ease-in-out;
        box-shadow: 0 0 10px var(--color-primary);
    }
    @keyframes loading {
        0% {
            left: -50%;
            width: 50%;
        }
        50% {
            left: 25%;
            width: 75%;
        }
        100% {
            left: 100%;
            width: 50%;
        }
    }
</style>
