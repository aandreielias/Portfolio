<script>
  import { slide } from "svelte/transition";
  import { createEventDispatcher } from "svelte";
  import Timeline from "./Timeline.svelte";

  const dispatch = createEventDispatcher();

  // Environment variables for personalization
  const name = import.meta.env.VITE_NAME;
  const email = import.meta.env.VITE_EMAIL;
  const phone = import.meta.env.VITE_PHONE;

  export let activeTab = "about";

  const timelineItems = [
    {
      start: 2025.0,
      end: 2026.0,
      title: "FH Wiener Neustadt",
      description: "Software Engineering and System Design",
      type: "education",
      displayDate: "2025 - Present",
      skills: ["Java", "Pascal", "R"],
    },
    {
      start: 2024.6, // Aug
      end: 2025.1, // Feb
      title: "Österreichisches Bundesheer",
      description: "Basic Military Service",
      type: "work",
      displayDate: "Aug 2024 - Feb 2025",
    },
    {
      start: 2019.7, // Sept
      end: 2024.5, // June
      title: "HTL Spengergasse",
      description: "Biomedicine and Health Informatics",
      type: "education",
      displayDate: "2019 - 2024",
      skills: [
        "Java",
        "JavaScript",
        "SQL",
        "Python",
        "Springboot",
        "Git",
        "Docker",
      ],
      action: {
        label: "View Thesis",
        projectId: "ERoots",
      },
    },
    {
      start: 2022.6, // Aug
      end: 2022.7, // Aug
      title: "Rehab Zentrum Stadlau",
      description: "Research Internship",
      type: "work",
      displayDate: "Aug 2022",
    },
    {
      start: 2021.6, // Aug
      end: 2021.7, // Aug
      title: "Rehab Zentrum Stadlau",
      description: "Research Internship",
      type: "work",
      displayDate: "Aug 2021",
    },
  ];

  const skills = {
    Languages: [
      "Java",
      "JavaScript",
      "TypeScript",
      "Python",
      "HTML",
      "CSS",
      "SQL",
    ],
    Frameworks: ["Svelte", "Spring Boot", "Three.js", "Tkinter"],
    "Tools & DevOps": ["Git", "Docker", "GitLab CI", "Cypress", "Vite"],
    Concepts: ["System Design", "REST APIs", "UI/UX Design"],
  };

  const certifications = [
    {
      title: "Project Management Basics (pm basic)",
      issuer: "pma (Projekt Management Austria)",
      date: "2023",
    },
  ];
</script>

<div class="contact-sheet">
  <div class="sheet-header">
    <h1>{activeTab === "about" ? "About Me" : "Contact Me"}</h1>
  </div>

  <div class="content-grid">
    <div class="main-column">
      <div class="tabs">
        <button
          class="tab-btn"
          class:active={activeTab === "about"}
          on:click={() => (activeTab = "about")}
        >
          About Me
        </button>
        <button
          class="tab-btn"
          class:active={activeTab === "contact"}
          on:click={() => (activeTab = "contact")}
        >
          Contact Me
        </button>
        <a
          href="{import.meta.env.BASE_URL}uploads/Lebenslauf.pdf"
          target="_blank"
          class="tab-btn view-cv-btn"
        >
          View CV
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            ><line x1="7" y1="17" x2="17" y2="7"></line><polyline
              points="7 7 17 7 17 17"
            ></polyline></svg
          >
        </a>
      </div>

      <div class="content-area">
        <div class="about-container">
          <div class="toggle-wrapper">
            {#if activeTab === "about"}
              <div
                class="about-text"
                transition:slide|local={{ duration: 300 }}
              >
                <p>
                  I'm {name}, a student of System Engineering and System Design
                  and a passion for programming.
                </p>
                <p>
                  I have a strong foundation in software development and a keen
                  interest in creating innovative solutions.
                </p>
              </div>
            {:else}
              <div
                class="contact-info"
                transition:slide|local={{ duration: 300 }}
              >
                <div class="contact-item">
                  <span class="label">Name</span>
                  <span class="value">{name}</span>
                </div>
                <div class="contact-item">
                  <span class="label">Email</span>
                  <a href="mailto:{email}" class="value link">{email}</a>
                </div>
                <div class="contact-item">
                  <span class="label">Phone</span>
                  <a href="tel:{phone}" class="value link">{phone}</a>
                </div>
              </div>
            {/if}
          </div>

          <div class="section-spacer"></div>

          <Timeline items={timelineItems} mode="combined" on:viewProject />

          <div class="section-spacer"></div>

          <h3 class="section-title">Skills</h3>
          <div class="skills-grid">
            {#each Object.entries(skills) as [category, items]}
              <div class="skill-category">
                <h4>{category}</h4>
                <div class="skill-tags">
                  {#each items as skill}
                    <span class="skill-tag">{skill}</span>
                  {/each}
                </div>
              </div>
            {/each}
          </div>

          <div class="section-spacer"></div>

          <h3 class="section-title">Certifications</h3>
          <div class="certifications-list">
            {#each certifications as cert}
              <div class="cert-card">
                <div class="cert-icon">
                  <!-- Simple Award Icon -->
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    ><circle cx="12" cy="8" r="7"></circle><polyline
                      points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"
                    ></polyline></svg
                  >
                </div>
                <div class="cert-content">
                  <div class="cert-title">
                    {cert.title}
                  </div>
                  <div class="cert-issuer">
                    {cert.issuer}
                  </div>
                  {#if cert.date}
                    <div class="cert-date">
                      {cert.date}
                    </div>
                  {/if}
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </div>

    <div class="side-column">
      <div class="profile-placeholder">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="64"
          height="64"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1"
          stroke-linecap="round"
          stroke-linejoin="round"
          ><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle
            cx="12"
            cy="7"
            r="4"
          ></circle></svg
        >
      </div>
      <div class="interests-section">
        <h3>Personal Interests</h3>
        <p>
          I have studied classical harp for 11 years and bassoon for 7 years and
          participated in various concerts over the years.
        </p>
      </div>
    </div>
  </div>
</div>

<style>
  .contact-sheet {
    background-color: var(--color-bg);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); /* Shadow downwards */
    width: 66.67%;
    height: 100%; /* Takes height of parent wrapper */
    margin: 0 auto;
    border-radius: 0 0 var(--radius) var(--radius);
    display: flex;
    flex-direction: column;
    padding: 3rem;
    pointer-events: auto;
  }

  .sheet-header {
    margin-bottom: 2rem;
    flex-shrink: 0;
  }

  .sheet-header h1 {
    margin: 0;
    font-size: 2rem;
    line-height: 1;
    background: var(--gradient-heading);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .content-grid {
    display: flex;
    gap: 2rem;
    flex: 1;
    overflow: hidden; /* Internal scrolling within columns if needed */
  }

  .main-column {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    height: 100%;
    overflow-y: auto; /* Internal scroll for main content */
    padding-right: 1rem;
  }

  /* Custom Scrollbar for columns */
  .main-column::-webkit-scrollbar,
  .side-column::-webkit-scrollbar {
    width: 6px;
  }

  .main-column::-webkit-scrollbar-track,
  .side-column::-webkit-scrollbar-track {
    background: transparent;
  }

  .main-column::-webkit-scrollbar-thumb,
  .side-column::-webkit-scrollbar-thumb {
    background: var(--glass-border);
    border-radius: 3px;
  }

  .side-column {
    flex-shrink: 0;
    width: 250px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    overflow-y: auto;
    height: 100%;
    padding-right: 0.5rem;
  }

  .interests-section {
    background: var(--glass-panel-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 1rem;
    font-size: 0.9rem;
    color: var(--color-text-muted);
    line-height: 1.5;
  }

  .interests-section h3 {
    font-size: 1rem;
    color: var(--color-text);
    margin-bottom: 0.5rem;
    font-weight: 600;
  }

  .tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--color-border);
    padding-bottom: 0.5rem;
    flex-shrink: 0;
  }

  .tab-btn {
    background: none;
    border: none;
    color: var(--color-text-muted);
    font-size: 1.1rem;
    cursor: pointer;
    padding: 0.5rem 1rem;
    border-radius: var(--radius);
    transition: all 0.2s;
  }

  .tab-btn:hover {
    color: var(--color-text);
    background: var(--color-bg-secondary);
  }

  .tab-btn.active {
    color: var(--color-primary);
    font-weight: 600;
    background: rgba(99, 102, 241, 0.1);
  }

  .about-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .label {
    font-size: 0.9rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
  }

  .value {
    font-size: 1.2rem;
    color: var(--color-text);
  }

  .link {
    color: var(--color-primary);
    text-decoration: none;
    transition: color 0.2s;
  }

  .link:hover {
    color: #818cf8;
    text-decoration: underline;
  }

  .profile-placeholder {
    width: 100%;
    aspect-ratio: 3/4;
    background: var(--glass-panel-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-muted);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  }

  .view-cv-btn {
    margin-left: auto;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  @media (max-width: 768px) {
    .contact-sheet {
      width: 95%;
      padding: 1.5rem;
    }

    .content-grid {
      flex-direction: column;
      overflow-y: auto;
      overscroll-behavior: contain;
    }

    .side-column {
      width: 100%;
      height: auto;
      overflow-y: visible;
      order: -1;
    }

    .main-column {
      overflow-y: visible;
      height: auto;
    }

    /* On mobile, parent should handle scrolling, but for consistent behavior we might need adjustments */
  }

  /* Skills Grid, Certs, etc. reused from previous */
  .skills-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }

  .skill-category h4 {
    font-size: 0.95rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.75rem;
    font-weight: 600;
  }

  .skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .skill-tag {
    background: rgba(var(--color-primary-rgb), 0.1);
    color: var(--color-primary);
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 500;
    border: 1px solid rgba(var(--color-primary-rgb), 0.2);
    cursor: default;
  }

  .certifications-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .cert-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: var(--glass-panel-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 1rem;
  }

  .cert-icon {
    color: var(--color-primary);
    background: rgba(var(--color-primary-rgb), 0.1);
    padding: 0.75rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .cert-content {
    flex: 1;
  }

  .cert-title {
    font-weight: 600;
    color: var(--color-text);
    font-size: 1rem;
    margin-bottom: 0.2rem;
  }

  .cert-issuer {
    color: var(--color-text-muted);
    font-size: 0.9rem;
  }

  .cert-date {
    color: var(--color-text-muted);
    font-size: 0.8rem;
    margin-top: 0.25rem;
    opacity: 0.8;
  }

  .section-spacer {
    height: 2rem;
    margin: 1.5rem 0;
    border-bottom: 1px solid var(--glass-border);
  }

  .section-title {
    font-size: 1.25rem;
    color: var(--color-primary);
    font-weight: 700;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  @media (max-width: 600px) {
    .skills-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
