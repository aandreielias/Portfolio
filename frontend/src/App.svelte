<script>
  import { onMount, onDestroy } from "svelte";
  import { ApiService } from "./lib/services/api.js";

  import { projectRegistry } from "./lib/stores/projectStore.js";
  import ProjectCard from "./lib/components/project/ProjectCard.svelte";

  import ProjectModal from "./lib/components/project/ProjectModal.svelte";

  import ContactSheet from "./lib/components/common/ContactSheet.svelte";
  import ImageViewer from "./lib/components/common/ImageViewer.svelte";
  import Header from "./lib/components/layout/Header.svelte";
  import Footer from "./lib/components/layout/Footer.svelte";

  import Dither from "./lib/components/visualizations/Dither.svelte";
  import KineticTypography from "./lib/components/visualizations/KineticTypography.svelte";
  import InversionMask from "./lib/components/visualizations/InversionMask.svelte";

  // Environment variables
  const name = import.meta.env.VITE_NAME || "Portfolio";
  const email = import.meta.env.VITE_EMAIL || "email@example.com";

  // State
  let selectedProject = null;

  let contactActiveTab = "about";
  let scrollY = 0;

  // Calculated positions
  // Contact Sheet: ends at 85vh
  // Spacer: 150vh long. Starts at 85vh. Ends at 235vh.
  // Projects: Starts at 235vh.

  // Hero View Target: Midpoint of spacer.
  // Spacer Start (85) + Spacer Height/2 (75) - Viewport/2 (50) = 110vh

  // Initialize data on mount
  onMount(async () => {
    if ("scrollRestoration" in history) history.scrollRestoration = "manual";

    // Start at the Hero position (Middle)
    window.scrollTo(0, window.innerHeight * 1.1);

    const projects = await ApiService.fetchAllProjects();
    projectRegistry.set(projects);
  });

  // Modal controls
  function openProject(project) {
    selectedProject = project;
  }
  function closeProject() {
    selectedProject = null;
  }

  function openContact(tab = "about") {
    contactActiveTab = tab;
    scrollTo("contact");
  }

  function scrollTo(id) {
    let targetPosition = null;
    const vh = window.innerHeight;

    if (id === "contact") {
      targetPosition = 0; // Top of page (Contact Sheet)
    } else if (id === "hero" || id === "top") {
      // "top" now refers to the main view (Hero)
      targetPosition = vh * 1.1;
    } else if (id === "projects") {
      // Target projects start (235vh) minus offset (Sticky 15vh) = 220vh
      targetPosition = vh * 2.2;
    }

    if (targetPosition !== null) {
      const startPosition = window.scrollY;
      const distance = targetPosition - startPosition;
      const duration = 1200;
      let startTime = null;

      function animation(currentTime) {
        if (!startTime) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);

        // Ease In Out Quad
        const ease =
          progress < 0.5
            ? 2 * progress * progress
            : 1 - Math.pow(-2 * progress + 2, 2) / 2;

        window.scrollTo(0, startPosition + distance * ease);

        if (timeElapsed < duration) {
          requestAnimationFrame(animation);
        }
      }

      requestAnimationFrame(animation);
    } else {
      document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
    }
  }

  function handleOutsideClick(event) {
    // Determine where we are
    const vh = window.innerHeight;
    const scrollY = window.scrollY;

    // Contact Sheet is 85vh.
    const isAtContact = scrollY < vh * 0.5;

    // Projects starts at 235vh.
    // Sticky offset is 15vh. So effective top of projects view is 220vh.
    const isAtProjects = scrollY > vh * 1.8;

    // Ignore clicks on interactive elements
    if (event.target.closest("button") || event.target.closest("a")) return;

    // If not at Hero, scroll to Hero (Middle)
    // "top" here refers to the landing state
    if (isAtContact || isAtProjects) {
      scrollTo("hero");
    }
  }
</script>

<svelte:window bind:scrollY />

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="landing-fixed" on:click={handleOutsideClick}>
  <div class="hero-bg-container">
    <Dither
      waveSpeed={0.02}
      waveFrequency={4}
      waveAmplitude={0.3}
      waveColor={[0.5, 0.5, 0.5]}
      colorIntensity={7}
      pixelSize={2}
      disableAnimation={false}
      enableMouseInteraction={true}
      mouseRadius={0.2}
    />
  </div>

  <Header on:openContact={() => openContact("contact")} />

  <section class="hero">
    <div class="hero-content">
      <div class="kinetic-wrapper">
        <KineticTypography {name} helloText="HELLO" introText="MY NAME IS" />
        <InversionMask />
        <p class="subtitle">
          Student of Systems Engineering<br />and Systems Design
        </p>
      </div>

      <div class="hero-footer">
        <div class="actions">
          <button class="primary-btn" on:click={() => scrollTo("projects")}
            >View Work</button
          >
          <button class="secondary-btn" on:click={() => openContact("about")}
            >About Me</button
          >
        </div>
      </div>
    </div>
  </section>
</div>

<div class="content-scroll">
  <!-- Top Sheet (Contact) -->
  <!-- "slides down from the top when scrolling up" -->
  <div class="top-sheet-wrapper">
    <ContactSheet
      bind:activeTab={contactActiveTab}
      on:viewProject={(e) => {
        const projectId = e.detail;
        projectRegistry.subscribe((projects) => {
          const project = projects.find((p) => p.id === projectId);
          if (project) {
            openProject(project);
            scrollTo("projects"); // Optional: scroll to show context
          }
        })();
      }}
    />
  </div>

  <!-- Hero Spacer -->
  <!-- This is the gap that allows the fixed background to be seen -->
  <div class="hero-spacer"></div>

  <!-- Bottom Sheet (Projects) -->
  <div class="sheet">
    <main>
      <section id="projects" class="section">
        <div class="section-header">
          <h2>Selected Projects</h2>
          <p>A collection of my recent work.</p>
        </div>
        <div class="grid">
          {#each $projectRegistry as project (project.id)}
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div class="grid-item">
              <ProjectCard {project} onClick={() => openProject(project)} />
            </div>
          {/each}
        </div>
      </section>

      {#if selectedProject}
        <ProjectModal project={selectedProject} on:close={closeProject} />
      {/if}

      <ImageViewer />
    </main>

    <Footer />
  </div>
</div>

<style>
  /* Fixed Landing Page Layer */
  .landing-fixed {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    z-index: 1;
    pointer-events: auto;
  }

  /* Scrollable Content Layer */
  .content-scroll {
    position: relative;
    z-index: 2;
    /* Reset margins as we control flow */
    margin: 0;
    pointer-events: none; /* Let clicks pass through empty areas */
  }

  /* Top Sheet (Contact) */
  .top-sheet-wrapper {
    height: 85vh; /* Stops at 15vh from bottom (when viewed from top) */
    pointer-events: none; /* Let clicks pass through to landing-fixed */
    position: relative;
    /* Ensures it is above the spacer in the document flow */
    /* Note: Normal flow places this at 0-85vh */
  }

  /* Hero Spacer */
  .hero-spacer {
    height: 150vh;
    width: 100%;
    pointer-events: none; /* See-through to fixed landing */
  }

  /* The actual rising sheet (Projects) */
  .sheet {
    pointer-events: auto;
    background-color: var(--color-bg);
    box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.1);

    /* Sticky behavior */
    position: sticky;
    top: 15vh; /* Max rising point: 1/4 from top */

    /* Flex column for sticky footer */
    display: flex;
    flex-direction: column;

    /* Layout */
    height: 85vh; /* Occupy remaining space (100vh - 15vh) */
    overflow-y: auto; /* Internal scroll */
    width: 66.67%; /* 2/3 of the width */
    margin: 0 auto; /* Center the sheet */

    /* Padding above Selected Projects */
    padding-top: 4rem;

    /* Smoothness */
    border-radius: var(--radius);
  }

  .hero {
    min-height: 80vh;
    display: flex;
    justify-content: flex-start; /* Align to top */
    align-items: center;
    position: relative;
    padding-top: 5vh; /* Distance from top of site (under header) */
    /* Ensure it takes full height in the fixed container */
    height: 100%;
  }

  .hero-bg-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1;
    pointer-events: auto;
    opacity: 0.8;
    mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
  }

  .hero-content {
    text-align: center;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5vh;
    padding-top: 0;
  }

  .kinetic-wrapper {
    position: relative;
    aspect-ratio: 1 / 1;
    width: auto;
    height: 55vh;
    max-width: 100%;
    max-height: 90vw;
    margin: 0 auto;
    transform: translateY(-10%); /* Move up to clear buttons */
  }

  .hero-footer {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    width: 100%;
    z-index: 10;
  }

  .subtitle {
    position: absolute;
    bottom: -15%; /* Position inside the lower part of the circle (which extends 25% down) */
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    font-size: 1.1rem; /* Slightly smaller to fit nicely */
    color: white;
    font-weight: 600;
    margin: 0;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    max-width: 60%; /* Tighter width to clear the curve */
    z-index: 2;
    pointer-events: none;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5); /* Improve readability vs dither if exposed */
  }

  .actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }

  .primary-btn {
    background: rgba(var(--color-primary-rgb), 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: white;
    padding: 0.8rem 2rem;
    border-radius: var(--radius);
    font-size: 1.1rem;
    box-shadow: 0 4px 15px rgba(var(--color-primary-rgb), 0.4);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .primary-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(var(--color-primary-rgb), 0.6);
    background: rgba(var(--color-primary-rgb), 0.9);
  }

  .secondary-btn {
    background: var(--glass-panel-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: var(--color-text);
    padding: 0.8rem 2rem;
    border-radius: var(--radius);
    font-size: 1.1rem;
    border: 1px solid var(--glass-border);
    transition: all 0.3s ease;
  }

  .secondary-btn:hover {
    background: var(--btn-secondary-hover-bg);
    border-color: var(--color-primary);
    transform: translateY(-2px);
  }

  main {
    width: 100%;
    flex-grow: 1;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
  }

  .section {
    margin-bottom: 8rem;
    scroll-margin-top: 120px;
    margin-top: 0;
  }

  .section-header {
    margin-bottom: 3rem;
  }

  h2 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }

  .section-header p {
    color: var(--color-text-muted);
    font-size: 1.1rem;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .grid-item {
    grid-column: span 1;
    grid-row: span 1;
    height: 100%;
  }

  @media (max-width: 768px) {
    .grid {
      grid-template-columns: 1fr;
    }

    .sheet,
    .top-sheet-wrapper {
      width: 100%;
    }
  }
</style>
