<script>
  import { onMount, onDestroy } from "svelte";
  import { ApiService } from "./lib/services/api.js";

  import { projectRegistry } from "./lib/stores/projectStore.js";
  import ProjectCard from "./lib/components/project/ProjectCard.svelte";

  import ProjectModal from "./lib/components/project/ProjectModal.svelte";

  import ContactModal from "./lib/components/common/ContactModal.svelte";
  import ImageViewer from "./lib/components/common/ImageViewer.svelte";
  import Header from "./lib/components/layout/Header.svelte";
  import Footer from "./lib/components/layout/Footer.svelte";

  import Dither from "./lib/components/visualizations/Dither.svelte";
  import KineticTypography from "./lib/components/visualizations/KineticTypography.svelte";
  import { glitchChars } from "./lib/utils/glitchCharacters.js";

  // Environment variables
  const name = import.meta.env.VITE_NAME || "Portfolio";
  const email = import.meta.env.VITE_EMAIL || "email@example.com";

  // State
  let selectedProject = null;

  let showContactModal = false;
  let scrollY = 0;

  // Initialize data on mount
  onMount(async () => {
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

  function openContact() {
    showContactModal = true;
  }

  function closeContact() {
    showContactModal = false;
  }

  function scrollTo(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
  }

  // Glitch effect for AsciiText (now used for Main Name)
  // Glitch effect manager
  import { GlitchString } from "./lib/components/visualizations/GlitchText.svelte";

  // Initialize managers
  const nameGlitcher = new GlitchString(name);
  const helloGlitcher = new GlitchString("HELLO");
  const introGlitcher = new GlitchString("MY NAME IS");

  let glitchedName = name;
  let glitchedHello = "HELLO";
  let glitchedIntro = "MY NAME IS";
  let frameId;

  function updateGlitches() {
    glitchedName = nameGlitcher.update();
    glitchedHello = helloGlitcher.update();
    glitchedIntro = introGlitcher.update();

    frameId = requestAnimationFrame(updateGlitches);
  }

  onMount(() => {
    updateGlitches();
  });

  onDestroy(() => {
    if (frameId) cancelAnimationFrame(frameId);
  });
</script>

<svelte:window bind:scrollY />

<div class="hero-bg-container">
  <Dither
    waveSpeed={0.01}
    waveFrequency={2.7}
    waveAmplitude={0.43}
    waveColor={[0.1, 0.1, 0.1]}
    backgroundColor={[1.0, 1.0, 1.0]}
    colorIntensity={10.5}
    pixelSize={2}
    disableAnimation={false}
    enableMouseInteraction={true}
    mouseRadius={0.1}
  />
</div>

<Header />

<section class="hero">
  <div class="hero-content">
    <div class="kinetic-wrapper">
      <KineticTypography
        name={glitchedName || name}
        helloText={glitchedHello}
        introText={glitchedIntro}
      />
    </div>

    <div class="hero-footer">
      <p class="subtitle">Student of Systems Engineering and Systems Design</p>
      <div class="actions">
        <button class="primary-btn" on:click={() => scrollTo("projects")}
          >View Work</button
        >
        <button class="secondary-btn" on:click={openContact}>About Me</button>
      </div>
    </div>
  </div>
</section>

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

  {#if showContactModal}
    <ContactModal on:close={closeContact} />
  {/if}

  <ImageViewer />
</main>

<Footer />

<style>
  .hero {
    min-height: 80vh;
    display: flex;
    justify-content: flex-start; /* Align to top */
    align-items: center;
    position: relative;
    padding-top: 15vh; /* Distance from top of site (under header) */
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
    /* 
       Distance grid -> box should equal top -> grid.
       Top -> Grid is roughly Header(~60px) + HeroPadding(15vh).
       So Gap should be ~ 15vh + 60px. 
       Let's approximate gap as 20vh to be safe and visually distinct.
    */
    gap: 5vh;
    padding-top: 0;
  }

  .kinetic-wrapper {
    /* Square container as requested */
    aspect-ratio: 1 / 1;
    width: auto;
    height: 55vh;
    max-width: 100%;
    /* Ensure it doesn't overflow width on mobile */
    max-height: 90vw;
    /* Center it if flex doesn't */
    margin: 0 auto;
  }

  /* Legacy styles removed */
  /* --------------------------- */

  .hero-footer {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    width: 100%;
    z-index: 10;
  }

  .subtitle {
    font-size: 1.5rem;
    /* Make it bold or darker if needed without the box, strictly following user requesting 'Student of...' text */
    color: var(
      --color-text
    ); /* Changed from muted to text for better contrast without box */
    font-weight: 500;
    margin: 0;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.05em;
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
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
  }

  .section {
    margin-bottom: 8rem;
    scroll-margin-top: 120px;
    margin-top: 10vh; /* Push projects down slightly so they aren't seen on load but close */
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
  }
</style>
