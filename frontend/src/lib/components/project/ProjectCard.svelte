<script>
    export let project;
    export let onClick;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="card glass-panel" on:click={onClick}>
    <div class="card-content">
        <div class="card-header">
            <h3>{project.title}</h3>
            {#if project.logo}
                <img
                    src={project.logo}
                    alt="{project.title} logo"
                    class="logo"
                />
            {/if}
        </div>
        <p class="summary">{project.description.substring(0, 100)}...</p>
        <div class="footer">
            <span class="status">{project.status || "Completed"}</span>
            <span class="arrow">→</span>
        </div>
    </div>
</div>

<style>
    .card {
        border-radius: var(--radius);
        overflow: hidden;
        cursor: pointer;
        transition: all 0.3s ease;
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
        transition: transform 0.2s;
    }

    .card:hover .arrow {
        transform: translateX(5px);
        color: var(--color-primary);
    }
</style>
