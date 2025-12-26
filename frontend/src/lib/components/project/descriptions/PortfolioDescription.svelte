<script>
  import { openImage } from "../../../stores/imageViewerStore.js";
  // Images
  const image1 = "/api/project/Portfolio/file/landing.png";
  const image2 = "/api/project/Portfolio/file/SystemArchitecture.png";
</script>

<div class="project-details">
  <div class="meta-header">
    <div class="badge">Personal Project • 2025</div>
    <div class="stack">
      Stack: Svelte 5 • Vite • Static JSON • CSS Variables
    </div>
  </div>

  <div class="intro">
    <p>
      This portfolio is designed to showcase my work. Built as a static Single
      Page Application (SPA), it focuses on user experience and unique visual
      interactions without the need for a complex backend infrastructure.
    </p>
  </div>

  <div class="section">
    <h3>System Architecture</h3>
    <p>
      The project follows a "static-first" approach. Data is decoupled from the
      interface, allowing for easy updates and fast content delivery.
    </p>

    <div class="table-container">
      <table class="tech-table">
        <thead>
          <tr>
            <th>Component</th>
            <th>Technology</th>
            <th>Purpose</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="primary-col">Frontend</td>
            <td>Svelte 5 + Vite</td>
            <td>Application logic and reactive UI state</td>
          </tr>
          <tr>
            <td class="primary-col">Data Layer</td>
            <td>Static JSON</td>
            <td>Lightweight content management</td>
          </tr>
          <tr>
            <td class="primary-col">Styling</td>
            <td>Custom CSS</td>
            <td>Glassmorphism and responsive layout</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <h3>Key Visual Features</h3>
    <p>
      The aesthetic combines modern minimalism with retro-digital inspirations,
      featuring custom animations and interactive elements.
    </p>
    <div class="features-grid">
      <div class="feature-card">
        <h4>Dynamic Typography</h4>
        <p>
          Headlines and key text elements feature kinetic motion and glitch
          effects, bringing static content to life.
        </p>
      </div>
      <div class="feature-card">
        <h4>Atmospheric Effects</h4>
        <p>
          A custom dithered background shader provides texture and depth,
          reacting dynamically to user interaction.
        </p>
      </div>
      <div class="feature-card">
        <h4>Glassmorphism</h4>
        <p>
          Translucent layers and blurred backdrops create a sense of hierarchy
          and physical depth within the interface.
        </p>
      </div>
    </div>
  </div>

  <div class="section">
    <h3>Development Philosophy</h3>
    <p>
      The codebase emphasizes clarity and maintainability. By using modern
      browser standards and a clear component structure, the project remains
      easy to extend and refine. New features, such as the tech simulator or
      additional project types, can be integrated seamlessly into the existing
      architecture.
    </p>

    <ul class="data-points">
      <li>
        <strong>Efficient Rendering:</strong> The Svelte compiler ensures that only
        necessary DOM updates occur.
      </li>
      <li>
        <strong>Scalable Data:</strong> Projects and skills are defined in external
        files, making content updates trivial.
      </li>
      <li>
        <strong>Modern Tooling:</strong> Vite provides an optimized development experience
        and production builds.
      </li>
    </ul>
  </div>

  <div class="footer-meta">
    <span class="source-tag">Source: This Website (Static Edition)</span>
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
    margin-top: 0; /* Updated from 1.5rem to 0 for card alignment */
  }

  /* Table Styles */
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

  /* Grid Styles */
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

  .feature-card p {
    margin-bottom: 0;
    font-size: 0.9rem;
  }

  /* List Styles */
  .data-points {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-bottom: 2rem;
    color: var(--color-text-muted);
  }

  .data-points li {
    margin-bottom: 0.5rem;
  }

  .source-tag {
    font-family: monospace;
    background: rgba(var(--color-primary-rgb), 0.1);
    color: var(--color-primary);
    padding: 0.3rem 0.8rem;
    border-radius: 4px;
  }
</style>
