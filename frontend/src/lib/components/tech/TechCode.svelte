<script>
    import { fly } from "svelte/transition";
    import CodeBlock from "../common/CodeBlock.svelte";

    export let files = {};

    let fileKeys = [];
    let currentIndex = 0;
    let direction = 1; // 1 for next, -1 for prev
    let displayedCode = "";

    $: fileKeys = Object.keys(files);
    $: currentFile = fileKeys[currentIndex] || "";
    $: rawContent = files[currentFile] || "";

    // Effect to handle content loading (string vs URL)
    $: {
        if (
            rawContent &&
            (rawContent.startsWith("/") || rawContent.startsWith("http"))
        ) {
            // It's likely a file path, valid for fetching
            displayedCode = "Loading...";
            fetch(rawContent)
                .then((res) => {
                    if (!res.ok) throw new Error("Failed to load code");
                    return res.text();
                })
                .then((text) => {
                    displayedCode = text;
                })
                .catch((err) => {
                    console.error("Code loading error:", err);
                    displayedCode = `Error loading code from ${rawContent}`;
                });
        } else {
            // It's raw code string
            displayedCode = rawContent;
        }
    }

    function nextFile() {
        direction = 1;
        currentIndex = (currentIndex + 1) % fileKeys.length;
    }

    function prevFile() {
        direction = -1;
        currentIndex = (currentIndex - 1 + fileKeys.length) % fileKeys.length;
    }

    function getLanguage(filename) {
        if (!filename) return "text";
        if (filename.endsWith(".py")) return "python";
        if (filename.endsWith(".js")) return "javascript";
        if (filename.endsWith(".java")) return "java";
        if (filename.endsWith(".svelte")) return "svelte";
        if (filename.endsWith(".html")) return "html";
        if (filename.endsWith(".css")) return "css";
        return "text";
    }
</script>

<div class="tech-code">
    <div class="header">
        <div class="dots">
            <span class="dot red"></span>
            <span class="dot yellow"></span>
            <span class="dot green"></span>
        </div>
        <span class="filename">{currentFile}</span>
        <div class="spacer"></div>
    </div>

    <div class="content-area">
        <button
            class="nav-btn prev"
            on:click={prevFile}
            aria-label="Previous file"
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
            >
                <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
        </button>

        <div class="code-wrapper">
            {#key currentFile}
                <div
                    class="code-slide"
                    in:fly={{ x: 50 * direction, duration: 300 }}
                    out:fly={{ x: -50 * direction, duration: 300 }}
                >
                    <CodeBlock
                        code={displayedCode}
                        language={getLanguage(currentFile)}
                        showHeader={false}
                        embedded={true}
                    />
                </div>
            {/key}
        </div>

        <button class="nav-btn next" on:click={nextFile} aria-label="Next file">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
            >
                <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
        </button>
    </div>
</div>

<style>
    .tech-code {
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 100%;
        flex: 1;
        border-radius: 8px;
        overflow: hidden;
        background: var(--code-bg); /* Match CodeBlock background */
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 1px solid var(--glass-border);
    }

    .header {
        background-color: var(--sidebar-bg);
        padding: 0.75rem 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--glass-border);
        z-index: 10;
        flex-shrink: 0;
    }

    .dots {
        display: flex;
        gap: 6px;
        width: 60px; /* Fixed width for centering */
    }

    .dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }

    .red {
        background-color: #ff5f56;
    }
    .yellow {
        background-color: #ffbd2e;
    }
    .green {
        background-color: #27c93f;
    }

    .spacer {
        width: 60px; /* Balance the dots */
    }

    .filename {
        font-family: "Fira Code", monospace;
        font-size: 0.9rem;
        color: var(--color-text-muted);
        font-weight: 600;
    }

    .content-area {
        flex: 1;
        position: relative;
        display: flex;
        overflow: hidden;
        background: var(--code-bg);
    }

    .code-wrapper {
        flex: 1;
        position: relative;
        overflow: hidden;
    }

    .code-slide {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden; /* Let CodeBlock handle scrolling */
    }

    .nav-btn {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background: rgba(0, 0, 0, 0.3);
        border: none;
        color: white;
        width: 40px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        opacity: 0; /* Hidden by default */
        transition: all 0.2s ease;
        z-index: 20;
    }

    .content-area:hover .nav-btn {
        opacity: 0.5; /* Visible on hover */
    }

    .nav-btn:hover {
        opacity: 1 !important;
        background: rgba(0, 0, 0, 0.6);
    }

    .nav-btn.prev {
        left: 0;
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
    }

    .nav-btn.next {
        right: 0;
        border-top-left-radius: 8px;
        border-bottom-left-radius: 8px;
    }

    svg {
        width: 24px;
        height: 24px;
    }
</style>
