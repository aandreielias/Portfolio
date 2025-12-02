<script>
    import { fade } from "svelte/transition";
    import Modal from "../common/Modal.svelte";
    import TechCompiler from "./TechCompiler.svelte";
    import TechRun from "./TechRun.svelte";
    import TechCode from "./TechCode.svelte";
    import TechDescription from "./TechDescription.svelte";

    export let techItem;
    export let close;

    let activeTab = "description";
    let compiledData = null;
    let error = null;

    function handleCompiled(event) {
        compiledData = event.detail;
        error = null;
    }

    function handleError(event) {
        error = event.detail;
        compiledData = null;
    }
</script>

<Modal
    title={techItem.title}
    on:close={close}
    width="66vw"
    maxWidth="66vw"
    maxHeight="95vh"
    scrollableBody={false}
>
    <div class="tabs">
        <button
            class:active={activeTab === "description"}
            on:click={() => (activeTab = "description")}
        >
            Description
        </button>
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
        <TechCompiler
            files={techItem.files}
            language={techItem.language}
            on:compiled={handleCompiled}
            on:error={handleError}
        />

        {#if activeTab === "run"}
            <div class="tab-pane" in:fade={{ duration: 200 }}>
                {#if error}
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
        {:else if activeTab === "code"}
            <div class="tab-pane" in:fade={{ duration: 200 }}>
                <TechCode files={techItem.files} />
            </div>
        {:else if activeTab === "description"}
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
</Modal>

<style>
    .tabs {
        display: flex;
        gap: 2rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid var(--glass-border);
        padding-bottom: 0.5rem;
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
        min-height: 50vh;
    }
    .tab-pane {
        width: 100%;
        flex: 1;
        display: flex;
        flex-direction: column;
        overflow: hidden; /* Ensure content doesn't spill */
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
