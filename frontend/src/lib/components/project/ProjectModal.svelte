<script>
    import { createEventDispatcher } from "svelte";
    import Modal from "../common/Modal.svelte";
    import ERootsDescription from "./descriptions/ERootsDescription.svelte";
    import PortfolioDescription from "./descriptions/PortfolioDescription.svelte";
    import { API_BASE } from "../../services/api";

    export let project;

    const dispatch = createEventDispatcher();

    function close() {
        dispatch("close");
    }

    // Helper to construct full URL
    function getFullUrl(path) {
        if (!path) return null;
        if (path.startsWith("http")) return path;
        return `${API_BASE}${path.startsWith("/") ? "" : "/"}${path}`;
    }

    function getPdfUrl(url, title) {
        let fullUrl = getFullUrl(url);
        if (title && title.toLowerCase().includes("eroots")) {
            return `${fullUrl}#page=129`;
        }
        return fullUrl;
    }
</script>

<Modal title={project.title} on:close={close}>
    <div slot="header" class="header-actions">
        {#if project.pdf}
            <a
                href={getPdfUrl(project.pdf, project.title)}
                target="_blank"
                class="primary-btn small-btn"
            >
                View PDF
            </a>
        {/if}
        {#if project.logo}
            <img
                src={getFullUrl(project.logo)}
                alt="{project.title} logo"
                class="project-logo"
            />
        {/if}
    </div>

    {#if project.id === "ERoots"}
        <ERootsDescription />
    {:else if project.id === "Portfolio"}
        <PortfolioDescription />
    {:else}
        <p class="description">{project.description}</p>
    {/if}

    {#if project.pdf && project.title !== "ERoots"}
        <div class="actions">
            <a href={getFullUrl(project.pdf)} download class="secondary-btn">
                Download PDF
            </a>
        </div>
    {/if}
</Modal>

<style>
    .header-actions {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .project-logo {
        width: 38px;
        height: 38px;
        object-fit: cover;
        border-radius: var(--radius);
        background: rgba(255, 255, 255, 0.05);
        padding: 0;
    }

    .description {
        margin-bottom: 2rem;
        text-align: left;
        font-size: 1.1rem;
        line-height: 1.6;
        color: var(--color-text-muted);
    }

    .actions {
        display: flex;
        gap: 1rem;
    }

    .primary-btn {
        background-color: var(--color-primary);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: var(--radius);
        font-weight: bold;
        text-decoration: none;
        transition: all 0.2s;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
    }

    .primary-btn.small-btn {
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }

    .primary-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
    }

    .secondary-btn {
        background-color: var(--btn-secondary-bg);
        color: var(--color-text);
        padding: 0.8rem 1.5rem;
        border-radius: var(--radius);
        font-weight: bold;
        text-decoration: none;
        transition: all 0.2s;
        border: 1px solid var(--btn-secondary-border);
    }

    .secondary-btn:hover {
        background-color: var(--btn-secondary-hover-bg);
    }
</style>
