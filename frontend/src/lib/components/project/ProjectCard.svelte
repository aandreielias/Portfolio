<script>
  export let project;
  export let onClick;

  const BASE_URL = import.meta.env.BASE_URL;

  // Helper to construct full URL
  function getFullUrl(path) {
    if (!path) return null;
    if (path.startsWith("http")) return path;

    // Remove leading slash from path if it exists to avoid double slash with BASE_URL
    const cleanPath = path.startsWith("/") ? path.slice(1) : path;
    return `${BASE_URL}${cleanPath}`;
  }
  // Helper to strip HTML tags
  function stripHtml(html) {
    if (!html) return "";
    return html.replace(/<[^>]*>?/gm, "");
  }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="card glass-panel" on:click={onClick}>
  <div class="card-content">
    <div class="card-header">
      <h3>{project.title}</h3>
      {#if project.logo}
        <img
          src={getFullUrl(project.logo)}
          alt="{project.title} logo"
          class="logo"
        />
      {/if}
    </div>
    <p class="summary">
      {stripHtml(project.description).substring(0, 100)}...
    </p>
    <div class="footer">
      <span class="status">{project.status || "Completed"}</span>
      <span class="arrow">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="currentColor"
          style="image-rendering: pixelated;"
        >
          <path
            d="M11 4H13V14H15V12H17V14H15V16H13V18H11V16H9V14H7V12H9V14H11V4Z"
            transform="rotate(-90 12 12)"
          />
        </svg>
      </span>
    </div>
  </div>
</div>

<style>
  .card {
    border-radius: var(--radius);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.8s cubic-bezier(0.25, 0.8, 0.25, 1);
    display: flex;
    flex-direction: column;
    height: 100%;
    border: 1px solid var(--glass-border);
  }

  .card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-glow);
    border-color: var(--color-primary);
  }

  .card-content {
    padding: 1.5rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    text-align: left;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
  }

  .logo {
    width: 32px;
    height: 32px;
    object-fit: cover;
    border-radius: var(--radius);
  }

  h3 {
    margin: 0;
    font-size: 1.25rem;
    color: var(--color-text);
  }

  .summary {
    font-size: 0.95rem;
    color: var(--color-text-muted);
    margin-bottom: 1.5rem;
    flex: 1;
    line-height: 1.6;
  }

  .footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
  }

  .status {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--color-primary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .arrow {
    color: var(--color-text-muted);
    transition:
      transform 0.2s,
      color 0.2s;
    display: inline-flex;
    align-items: center;
  }

  .card:hover .arrow {
    transform: translateX(5px);
    color: var(--color-primary);
  }
</style>
