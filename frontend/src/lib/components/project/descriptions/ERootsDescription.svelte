<script>
    import { openImage } from "../../../stores/imageViewerStore.js";
    // Images
    const image1 = "/api/project/ERoots/file/eroots-client-ui.png";
    const image2 = "/api/project/ERoots/file/eroots_architecture.png";
</script>

<div class="project-details">
    <div class="meta-header">
        <div class="badge">School Diploma Thesis • 2023/24</div>
        <div class="stack">
            Stack: Next.js • Tailwind CSS • MongoDB, Mongoose • AWS S3 • Google
            OAuth • Cypress • GitLab CI/CD
        </div>
    </div>

    <div class="intro">
        <p>
            In Kiambu, Kenya, a dedicated women's self-help group actively
            promotes local producesales in their community. They are on a
            mission. They want to expand their market reachand tackle the
            chronic problem of food waste caused by the spoilage of unsold
            produce. Recognising the transformative potential of technology,
            they're keen to build a robustweb-based platform to do this. This
            digital marketplace will serve as a centralised tool, streamlining
            operations and increasing accessibility for both those producing and
            those consuming.
        </p>
        <p>
            Showcasing the vibrant diversity of their agricultural offering, the
            proposed platform will offer a comprehensive range of locally
            sourced products. Customers will enjoy the convenience of browsing
            this virtual marketplace. They will be able to place orders with
            ease and choose to pay for products when they are collected. The
            women's self-helpgroup aims not only to modernise their business but
            also to promote economic empowerment within their community by
            integrating modern technology into their sales strategy. They aim to
            create a sustainable solution that benefits both their business and
            the local agricultural ecosystem through this innovative approach.
        </p>
    </div>

    <div class="section">
        <h3>The Solution</h3>
        <p>
            We designed and built a user-friendly web application that serves as
            both a product catalogue and a reservation system. The platform
            enables customers to browse unique items, manage their shopping
            cart, and place orders seamlessly.
        </p>

        <figure class="figure">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <img
                src={image1}
                alt="ERoots client UI showing the product catalogue"
                on:click={() => openImage(image1, "ERoots client UI")}
                class="clickable-image"
            />
            <figcaption class="figcap">
                The client-facing web application featuring the product
                catalogue and shopping interface.
            </figcaption>
        </figure>

        <p>
            Beyond the storefront, we implemented a comprehensive <strong
                >Admin Dashboard</strong
            >. This tool empowers the self-help group to manage their inventory,
            track reservations, and update product categories without needing
            technical expertise. We integrated <strong>Google OAuth</strong> for
            secure and easy authentication.
        </p>
    </div>

    <div class="section">
        <h3>Technical Architecture</h3>
        <p>
            We chose a modern, scalable tech stack to ensure the platform's
            longevity and performance. The frontend is built with <strong
                >Next.js</strong
            >, providing a fast and responsive user experience.
        </p>
        <p>
            For data persistence, we utilized <strong>MongoDB</strong>, which
            offers the flexibility needed for a diverse product catalog. Product
            images are securely stored and served using <strong>AWS S3</strong>,
            ensuring fast load times and reliability.
        </p>

        <figure class="figure">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <img
                src={image2}
                alt="ERoots system architecture diagram"
                on:click={() => openImage(image2, "ERoots system architecture")}
                class="clickable-image"
            />
            <figcaption class="figcap">
                System architecture illustrating the interaction between
                Next.js, MongoDB, and AWS S3.
            </figcaption>
        </figure>
    </div>

    <div class="section">
        <h3>Quality Assurance & Deployment</h3>
        <p>
            Reliability was a key priority. I led the deployment and QA
            strategy, implementing a robust
            <strong>CI/CD pipeline</strong> using GitLab CI to automate testing and
            deployment.
        </p>
        <p>
            I used <strong>Cypress</strong> for end-to-end (E2E) testing, covering
            critical user flows such as search, product selection, and the order
            process. This automated testing approach ensures that new features can
            be deployed with confidence, minimizing the risk of regressions.
        </p>
    </div>

    <div class="footer-meta">Client: Mutundu Women Self Help Group</div>
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

    .clickable-image {
        cursor: pointer;
        transition: transform 0.2s;
    }

    .clickable-image:hover {
        transform: scale(1.02);
    }
</style>
