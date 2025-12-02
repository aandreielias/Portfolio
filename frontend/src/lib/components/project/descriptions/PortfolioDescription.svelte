<script>
    import { openImage } from "../../../stores/imageViewerStore.js";
    // Images
    const image1 = "/api/project/Portfolio/file/landing.png"; // Placeholder
    const image2 = "/api/project/Portfolio/file/SystemArchitecture.png";
</script>

<div class="project-details">
    <div class="meta-header">
        <div class="badge">Personal Project • 2025</div>
        <div class="stack">
            Stack: Svelte • Spring Boot • Java 25 • Vite • CSS Variables •
            Glassmorphism
        </div>
    </div>

    <div class="intro">
        <p>
            This portfolio website itself is a testament to my full-stack
            development capabilities. Designed with a "Glassmorphism" aesthetic,
            it combines a highly responsive <strong>Svelte</strong> frontend
            with a robust <strong>Spring Boot</strong> backend, serving as a dynamic
            showcase of my work.
        </p>
    </div>

    <div class="section">
        <h3>Design</h3>
        <p>
            I wanted a design that feels modern, premium, and alive. Using <strong
                >CSS Variables</strong
            > and custom glassmorphism effects, I created a dark-themed UI that highlights
            content while maintaining visual depth. The interface features smooth
            transitions, a responsive grid layout, and interactive elements that
            engage the visitor.
        </p>

        <figure class="figure">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <img
                src={image1}
                alt="Portfolio Landing Page"
                on:click={() => openImage(image1, "Portfolio Landing Page")}
                class="clickable-image"
            />
            <figcaption class="figcap">
                The landing page featuring a dynamic project grid and
                glassmorphism header.
            </figcaption>
        </figure>

        <p>
            The "Contact Me" modal and project detail views are designed to be
            unobtrusive yet informative, using overlays and blur effects to keep
            the user's context while presenting new information.
        </p>
    </div>

    <div class="section">
        <h3>Key Components</h3>

        <h4>Header & Theme Toggle</h4>
        <p>
            The header features a sticky glassmorphism effect and a custom-built
            theme toggle. I implemented a unique transition using the <strong
                >View Transitions API</strong
            > combined with a mathematically generated SVG wave animation. This creates
            a fluid, organic "blob" effect when switching between light and dark
            modes.
        </p>

        <h4>Project System</h4>
        <p>
            The project showcase is built on a flexible architecture. The <code
                >ProjectCard</code
            >
            component handles the preview state, while the
            <code>ProjectModal</code>
            dynamically loads detailed content. For special projects like this portfolio
            or ERoots, it renders custom Svelte components (<code
                >PortfolioDescription</code
            >, <code>ERootsDescription</code>) for a tailored presentation,
            while standard projects use a generic template.
        </p>

        <h4>Tech Showcase</h4>
        <p>
            To highlight smaller experiments, I created a separate <strong
                >Tech Showcase</strong
            > section. These components are lighter weight but share the same design
            DNA, allowing me to display code snippets and mini-projects without cluttering
            the main project grid.
        </p>

        <h4>Backend Integration</h4>
        <p>
            Data isn't hardcoded. A dedicated <code>InputHandler</code> service on
            the frontend communicates with the Spring Boot backend. It fetches project
            metadata, handles asset URLs for images and PDFs, and ensures that the
            frontend state stays synchronized with the server's file system.
        </p>
    </div>

    <div class="section">
        <h3>Technical Architecture</h3>
        <p>
            The application is built as a decoupled monolith. The frontend is a
            Single Page Application (SPA) powered by <strong>Svelte 5</strong>
            and <strong>Vite</strong>, ensuring lightning-fast load times and a
            reactive user experience.
        </p>

        <figure class="figure">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <img
                src={image2}
                alt="System Architecture Diagram"
                on:click={() =>
                    openImage(image2, "System Architecture Diagram")}
                class="clickable-image"
            />
            <figcaption class="figcap">
                High-level overview of the frontend-backend communication and
                component structure.
            </figcaption>
        </figure>

        <p>
            The backend is powered by <strong>Spring Boot 3</strong> running on
            <strong>Java 25</strong>. It serves as a REST API for project data
            and handles static asset delivery for project images and resources.
            The architecture is designed to be easily extensible, allowing for
            future additions like a blog or admin panel.
        </p>
    </div>

    <div class="footer-meta">Source: This Website!</div>
</div>

<style>
    .project-details {
        color: var(--color-text);
        font-size: 1.05rem;
        line-height: 1.7;
    }

    .meta-header {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid var(--glass-border);
    }

    .badge {
        font-size: 0.8rem;
        color: #fff;
        background: var(--color-primary);
        padding: 0.25rem 0.8rem;
        border-radius: 999px;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    .stack {
        font-size: 0.9rem;
        color: var(--color-text-muted);
        font-family: monospace;
    }

    .intro p {
        font-size: 1.15rem;
        color: var(--color-text);
        margin-bottom: 2rem;
    }

    .section {
        margin-bottom: 3rem;
    }

    h3 {
        font-size: 1.4rem;
        margin-bottom: 1rem;
        color: var(--color-text);
        font-weight: 700;
    }

    p {
        color: var(--color-text-muted);
        margin-bottom: 1.5rem;
    }

    strong {
        color: var(--color-text);
        font-weight: 600;
    }

    .figure {
        margin: 2rem 0;
        border-radius: var(--radius);
        overflow: hidden;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--glass-border);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }

    .figure img {
        width: 100%;
        height: auto;
        display: block;
    }

    .figcap {
        padding: 1rem;
        font-size: 0.9rem;
        color: var(--color-text-muted);
        background: rgba(0, 0, 0, 0.2);
        border-top: 1px solid var(--glass-border);
        text-align: center;
        font-style: italic;
    }

    .footer-meta {
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--glass-border);
        color: var(--color-text-muted);
        font-size: 0.95rem;
        font-weight: 500;
    }

    h4 {
        font-size: 1.15rem;
        margin-bottom: 0.5rem;
        color: var(--color-text);
        font-weight: 600;
        margin-top: 1.5rem;
    }

    code {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9em;
        color: var(--color-primary);
    }

    .clickable-image {
        cursor: pointer;
        transition: transform 0.2s;
    }

    .clickable-image:hover {
        transform: scale(1.02);
    }
</style>
