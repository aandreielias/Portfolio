<script>
  import hljs from "highlight.js";
  import "highlight.js/styles/atom-one-dark.css";

  export let code = "";
  export let language = "text";
  export let showHeader = true;
  export let embedded = false;

  let highlightedCode = "";

  $: {
    if (code) {
      try {
        // Check if language is supported, otherwise fallback to plaintext
        const validLanguage = hljs.getLanguage(language)
          ? language
          : "plaintext";
        highlightedCode = hljs.highlight(code, {
          language: validLanguage,
        }).value;
      } catch (e) {
        console.error("Highlighting error:", e);
        // Fallback to auto-detection or plain text
        highlightedCode = hljs.highlightAuto(code).value;
      }
    } else {
      highlightedCode = "";
    }
  }
</script>

<div class="code-block-container" class:embedded>
  {#if showHeader}
    <div class="header">
      <div class="dots">
        <span class="dot red"></span>
        <span class="dot yellow"></span>
        <span class="dot green"></span>
      </div>
      <span class="lang">{language}</span>
    </div>
  {/if}
  <div class="code-content">
    <pre><code class="hljs language-{language}"
        >{@html highlightedCode || "Work in Progress"}</code
      ></pre>
  </div>
</div>

<style>
  .code-block-container {
    background-color: #282c34; /* Atom One Dark background */
    border-radius: 8px;
    overflow: hidden;
    text-align: left;
    margin-top: 1rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    font-family: "Fira Code", "Consolas", "Monaco", "Courier New", monospace;
    border: 1px solid #181a1f;
    display: flex;
    flex-direction: column;
    height: 100%; /* Fill parent if possible */
    flex: 1;
  }

  .code-block-container.embedded {
    margin-top: 0;
    box-shadow: none;
    border: none;
    border-radius: 0;
  }

  .header {
    background-color: #21252b;
    padding: 0.75rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #181a1f;
  }

  .dots {
    display: flex;
    gap: 6px;
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

  .lang {
    color: #abb2bf;
    font-size: 0.75rem;
    text-transform: uppercase;
    font-weight: bold;
    letter-spacing: 0.05em;
  }

  .code-content {
    overflow: auto;
    flex: 1; /* Take remaining height */
    height: 100%;
  }

  pre {
    margin: 0;
    padding: 1.5rem;
    background: transparent;
    width: fit-content; /* Allow horizontal scroll */
    min-width: 100%;
  }

  code {
    font-family: inherit;
    font-size: 0.9rem;
    line-height: 1.6;
    background: transparent !important; /* Override hljs background */
    padding: 0 !important; /* Override hljs padding */
  }

  /* Scrollbar styling for the code block */
  .code-content::-webkit-scrollbar {
    width: 10px;
    height: 10px;
  }

  .code-content::-webkit-scrollbar-track {
    background: #21252b;
  }

  .code-content::-webkit-scrollbar-thumb {
    background: #4b5363;
    border-radius: 5px;
    border: 2px solid #21252b;
  }

  .code-content::-webkit-scrollbar-thumb:hover {
    background: #5c6579;
  }
</style>
