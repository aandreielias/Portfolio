<script>
  import { onMount } from "svelte";
  import { fade, fly } from "svelte/transition";

  // Smooth scroll to the specified element ID
  function scrollTo(id) {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  }
</script>

<header in:fly={{ y: -50, duration: 800, delay: 200 }} class="glass">
  <div class="container">
    <div class="logo">
      <span class="name gradient-text">Andrei Elias</span>
    </div>
    <nav>
      <button class="nav-link" on:click={() => scrollTo("projects")}
        >Projects</button
      >
    </nav>
  </div>
</header>

<style>
  header {
    position: sticky;
    top: 0;
    z-index: 100;
    padding: 1rem 0;
    border-bottom: 1px solid var(--glass-border);
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  nav {
    display: flex;
    gap: 2rem;
  }

  .nav-link {
    background: none;
    border: none;
    color: var(--color-text-muted);
    font-size: 0.95rem;
    font-weight: 500;
    padding: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
  }

  .nav-link:hover {
    color: var(--color-primary);
    text-shadow: 0 0 10px rgba(var(--color-primary-rgb), 0.3);
  }
</style>
