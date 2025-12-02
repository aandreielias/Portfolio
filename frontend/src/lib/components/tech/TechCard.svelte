<script>
    export let techItem;
    export let onClick;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="card glass-panel" on:click={onClick}>
    <div class="card-content">
        <div class="header">
            <h3>{techItem.title}</h3>
            <span class="language-badge">{techItem.language}</span>
        </div>
        <p class="description">
            {techItem.description || "No description available."}
        </p>
        <div class="footer">
            <span class="cta">View Demo &rarr;</span>
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
        min-height: 180px;
        border: 1px solid var(--glass-border);
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-glow);
        border-color: var(--color-primary);
    }

    .card-content {
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
        gap: 1rem;
    }

    h3 {
        margin: 0;
        font-size: 1.25rem;
        text-align: left;
        color: var(--color-text);
        line-height: 1.3;
    }

    .language-badge {
        background: rgba(99, 102, 241, 0.1);
        color: var(--color-primary);
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        white-space: nowrap;
        letter-spacing: 0.05em;
    }

    .description {
        font-size: 0.95rem;
        text-align: left;
        color: var(--color-text-muted);
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        flex: 1;
    }

    .footer {
        margin-top: auto;
        text-align: right;
    }

    .cta {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--color-primary);
        opacity: 0;
        transform: translateX(-10px);
        transition: all 0.3s ease;
        display: inline-block;
    }

    .card:hover .cta {
        opacity: 1;
        transform: translateX(0);
    }
</style>
