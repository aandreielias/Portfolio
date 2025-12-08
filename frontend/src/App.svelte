<script>
  import { onMount } from "svelte";
  import { ApiService } from "./lib/services/api.js";
  import { techRegistry } from "./lib/stores/techStore.js";
  import { projectRegistry } from "./lib/stores/projectStore.js";
  import ProjectCard from "./lib/components/project/ProjectCard.svelte";
  import TechCard from "./lib/components/tech/TechCard.svelte";
  import ProjectModal from "./lib/components/project/ProjectModal.svelte";
  import TechShowcase from "./lib/components/tech/TechShowcase.svelte";
  import ContactModal from "./lib/components/common/ContactModal.svelte";
  import ImageViewer from "./lib/components/common/ImageViewer.svelte";
  import Header from "./lib/components/layout/Header.svelte";
  import Footer from "./lib/components/layout/Footer.svelte";

  // Environment variables
  const name = import.meta.env.VITE_NAME || "Portfolio";
  const email = import.meta.env.VITE_EMAIL || "email@example.com";

  // State
  let selectedProject = null;
  let selectedTechItem = null;
  let showContactModal = false;
  let scrollY = 0;

  // Initialize data on mount
  onMount(async () => {
    const techs = await ApiService.fetchAllTechs();
    techRegistry.set(techs);
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

  function openTech(item) {
    selectedTechItem = item;
  }

  function closeTech() {
    selectedTechItem = null;
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
</script>

<svelte:window bind:scrollY />

<div class="hero-bg"></div>

<Header {name} />

<section class="hero">
  <div class="hero-content">
    <h1 class="gradient-text">Hello, I'm {name}.</h1>
    <p class="subtitle">Student of System Engineering and System Design</p>
    <div class="actions">
      <button class="primary-btn" on:click={() => scrollTo("projects")}
        >View Work</button
      >
      <button class="secondary-btn" on:click={openContact}>About Me</button>
    </div>
  </div>
  <div
    class="scroll-indicator"
    style="opacity: {Math.max(0, 1 - scrollY / 200)}"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="currentColor"
      style="image-rendering: pixelated;"
    >
      <path
        d="M11 4H13V14H15V12H17V14H15V16H13V18H11V16H9V14H7V12H9V14H11V4Z"
      />
    </svg>
  </div>
</section>

<main>
  <section id="projects" class="section">
    <div class="section-header">
      <h2>Selected Projects</h2>
      <p>A collection of my recent work.</p>
    </div>
    <div class="grid">
      {#each $projectRegistry as project}
        <ProjectCard {project} onClick={() => openProject(project)} />
      {/each}
    </div>
  </section>

  <section id="tech-showcase" class="section">
    <div class="section-header">
      <h2>Tech Showcase</h2>
      <p>Small passion projects I created in my free time.</p>
    </div>
    <div class="grid">
      {#each $techRegistry as snippet}
        <TechCard techItem={snippet} onClick={() => openTech(snippet)} />
      {/each}
    </div>
  </section>

  {#if selectedProject}
    <ProjectModal project={selectedProject} on:close={closeProject} />
  {/if}

  {#if selectedTechItem}
    <TechShowcase techItem={selectedTechItem} close={closeTech} />
  {/if}

  {#if showContactModal}
    <ContactModal on:close={closeContact} />
  {/if}

  <ImageViewer />
</main>

<Footer />

<style>
  .hero {
    height: 80vh;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
  }

  .hero-bg {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80vw;
    height: 80vw;
    background: radial-gradient(
      circle,
      rgba(var(--color-primary-rgb), 0.15) 0%,
      rgba(0, 0, 0, 0) 70%
    );
    filter: blur(80px);
    z-index: -1;
    animation: pulse 8s ease-in-out infinite;
    pointer-events: none;
  }

  .hero-content {
    text-align: center;
    z-index: 1;
  }

  h1 {
    font-size: 5rem;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
  }

  .subtitle {
    font-size: 1.5rem;
    color: var(--color-text-muted);
    margin-bottom: 2.5rem;
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
    color: white; /* Keep white for contrast on primary */
    padding: 0.8rem 2rem;
    border-radius: 50px;
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
    border-radius: 50px;
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
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 2rem;
  }

  @keyframes pulse {
    0%,
    100% {
      opacity: 0.5;
      transform: translate(-50%, -50%) scale(1);
    }
    50% {
      opacity: 0.8;
      transform: translate(-50%, -50%) scale(1.1);
    }
  }

  .scroll-indicator {
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    animation: bounce 2s infinite;
    color: var(--color-text-muted);
    transition: opacity 0.3s ease;
  }

  @keyframes bounce {
    0%,
    20%,
    50%,
    80%,
    100% {
      transform: translateX(-50%) translateY(0);
    }
    40% {
      transform: translateX(-50%) translateY(-10px);
    }
    60% {
      transform: translateX(-50%) translateY(-5px);
    }
  }
</style>
