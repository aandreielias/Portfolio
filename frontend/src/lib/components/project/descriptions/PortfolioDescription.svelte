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
            Stack: Svelte 5 • Vite • Static JSON API • GitHub Pages • CSS
            Variables
        </div>
    </div>

    <div class="intro">
        <p>
            An evolved portfolio platform that proves you don't need a complex
            backend to build a dynamic, high-performance application. This
            project uses a <strong>serverless, static-first architecture</strong
            >
            where a reactive <strong>Svelte 5</strong> frontend consumes structured
            metadata from static JSON endpoints. The result is an ultra-fast, "Retro
            Future" experience that can be hosted anywhere.
        </p>
    </div>

    <div class="section">
        <h3>Core Architecture</h3>
        <p>
            The system is built as a pure Single Page Application (SPA). By
            leveraging <strong>Vite</strong> for building and
            <strong>GitHub Pages</strong> for hosting, it eliminates server-side
            latency. Data is decoupled from the UI, stored in structured JSON files
            that serve as a lightweight, read-only database.
        </p>

        <div class="table-container">
            <table class="tech-table">
                <thead>
                    <tr>
                        <th>Layer</th>
                        <th>Technology</th>
                        <th>Role</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="primary-col">Frontend</td>
                        <td>Svelte 5 + Vite</td>
                        <td>Reactive UI, Router, State Stores</td>
                    </tr>
                    <tr>
                        <td class="primary-col">Data</td>
                        <td>Static JSON</td>
                        <td>"Serverless" Database for projects & tech</td>
                    </tr>
                    <tr>
                        <td class="primary-col">Hosting</td>
                        <td>GitHub Pages</td>
                        <td>Global CDN Distribution</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="section">
        <h3>Visual Identity: Retro Future</h3>
        <p>
            The design merges high-fidelity glassmorphism with retro-digital
            elements, creating a unique contrast between the smooth and the
            pixelated.
        </p>
        <div class="features-grid">
            <div class="feature-card">
                <h4>Pixel Art Iconography</h4>
                <p>
                    Custom 24px pixel-art SVGs (rectilinear paths) rendered with <code
                        >image-rendering: pixelated</code
                    >
                    provide a sharp, 8-bit aesthetic that pops against the blurred
                    backgrounds.
                </p>
            </div>
            <div class="feature-card">
                <h4>Mathematical Animations</h4>
                <p>
                    The theme switch uses a custom wave-propagation algorithm.
                    It grows a mask organically from the cursor position using
                    the <strong>View Transitions API</strong>.
                </p>
            </div>
            <div class="feature-card">
                <h4>Glassmorphism</h4>
                <p>
                    Deep CSS layers using <code>backdrop-filter: blur()</code> and
                    semi-transparent borders create a sense of physical depth and
                    hierarchy.
                </p>
            </div>
        </div>

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
                The landing page showcasing the synthesis of pixel-art icons and
                modern glassmorphism.
            </figcaption>
        </figure>
    </div>

    <div class="section">
        <h3>Data Integration</h3>
        <p>
            Despite lacking a dynamic server, the application maintains a
            "dynamic" architecture through smart data handling. The <code
                >ApiService</code
            > module abstracts the `fetch` calls, treating static JSON files as REST
            endpoints.
        </p>

        <ul class="data-points">
            <li>
                <strong>Structured Metadata:</strong> <code>project.json</code>
                and <code>tech.json</code> act as the source of truth, allowing content
                updates without changing code.
            </li>
            <li>
                <strong>Asset Resolution:</strong> A central
                <code>ApiService</code> handles URL normalization, ensuring assets
                load correctly whether on localhost or a subpath-distributed CDN.
            </li>
            <li>
                <strong>Live Code Loading:</strong> The Tech Showcase fetches
                raw text files from the <code>/public</code> directory, enabling
                real-time code display.
            </li>
        </ul>

        <div class="code-preview">
            <code>
                // Example: Fetching static data as an API<br />
                const projects = await fetch(`${"{"}BASE_URL{"}"}data/project.json`);
            </code>
        </div>
    </div>

    <div class="footer-meta">
        <span class="source-tag"
            >Source: This Website (v2.2 - Static Edition)</span
        >
    </div>
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
        border-radius: var(--radius) var(--radius) 0 0;
    }

    .clickable-image:hover {
        transform: scale(1.02);
    }

    /* New Styles */
    .table-container {
        overflow-x: auto;
        margin-bottom: 2rem;
        border-radius: var(--radius);
        border: 1px solid var(--glass-border);
    }

    .tech-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
        background: rgba(255, 255, 255, 0.02);
    }

    .tech-table th,
    .tech-table td {
        padding: 0.8rem 1rem;
        text-align: left;
        border-bottom: 1px solid var(--glass-border);
    }

    .tech-table th {
        background: rgba(var(--color-primary-rgb), 0.1);
        color: var(--color-primary);
        font-weight: 600;
    }

    .tech-table tr:last-child td {
        border-bottom: none;
    }

    .primary-col {
        font-weight: 600;
        color: var(--color-text);
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 1.5rem;
        border-radius: var(--radius);
        border: 1px solid var(--glass-border);
    }

    .feature-card h4 {
        margin-top: 0;
        color: var(--color-primary);
        font-size: 1.1rem;
    }

    .feature-card p {
        margin-bottom: 0;
        font-size: 0.9rem;
    }

    .data-points {
        list-style-type: disc;
        padding-left: 1.5rem;
        margin-bottom: 2rem;
        color: var(--color-text-muted);
    }

    .data-points li {
        margin-bottom: 0.5rem;
    }

    .code-preview {
        background: #1e1e1e;
        padding: 1rem;
        border-radius: var(--radius);
        border: 1px solid var(--glass-border);
        margin-bottom: 2rem;
        overflow-x: auto;
    }

    .code-preview code {
        background: transparent;
        color: #d4d4d4;
        padding: 0;
    }

    .source-tag {
        font-family: monospace;
        background: rgba(var(--color-primary-rgb), 0.1);
        color: var(--color-primary);
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
    }
</style>
