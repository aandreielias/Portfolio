<script>
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";

    export let name;

    function scrollTo(id) {
        const element = document.getElementById(id);
        if (element) {
            element.scrollIntoView({ behavior: "smooth" });
        }
    }

    let isDark = false;

    function toggleTheme(event) {
        const x = event.clientX;
        const y = event.clientY;

        const endRadius = Math.hypot(
            Math.max(x, innerWidth - x),
            Math.max(y, innerHeight - y),
        );

        // @ts-ignore
        if (!document.startViewTransition) {
            isDark = !isDark;
            updateTheme();
            return;
        }

        // @ts-ignore
        const transition = document.startViewTransition(async () => {
            isDark = !isDark;
            updateTheme();
        });

        transition.ready.then(() => {
            // Generate a random number between 0 and 1 to drive the unique animation
            const randomFactor = Math.random();

            const points = 60;
            const angleStep = (Math.PI * 2) / points;

            // Use the random number to determine wave frequencies (must be integers to close the loop)
            const freq1 = 2 + Math.floor(randomFactor * 3); // Range: 2, 3, 4
            const freq2 = 4 + Math.floor(randomFactor * 3); // Range: 4, 5, 6

            // Use the random number for phase offset
            const phase = randomFactor * Math.PI * 2;

            const endPolygonPoints = [];
            const startPolygonPoints = [];

            for (let i = 0; i < points; i++) {
                const angle = i * angleStep;

                // Start points are all at the click center
                startPolygonPoints.push(`${x}px ${y}px`);

                // Calculate uneven radius using the random-derived function
                // This creates a different "blob" shape every time
                const wave =
                    0.13 * Math.sin(freq1 * angle + phase) +
                    0.08 * Math.sin(freq2 * angle - phase);

                // Ensure the radius covers the screen (base multiplier + wave)
                const r = endRadius * (1.5 + wave);

                const px = x + r * Math.cos(angle);
                const py = y + r * Math.sin(angle);
                endPolygonPoints.push(`${px}px ${py}px`);
            }

            const clipPath = [
                `polygon(${startPolygonPoints.join(", ")})`,
                `polygon(${endPolygonPoints.join(", ")})`,
            ];

            document.documentElement.animate(
                {
                    clipPath: clipPath,
                },
                {
                    duration: 700,
                    easing: "ease-in",
                    pseudoElement: "::view-transition-new(root)",
                },
            );
        });
    }

    function updateTheme() {
        if (isDark) {
            document.documentElement.setAttribute("data-theme", "dark");
        } else {
            document.documentElement.removeAttribute("data-theme");
        }
    }
</script>

<header in:fly={{ y: -50, duration: 800, delay: 200 }} class="glass">
    <div class="container">
        <div class="logo">
            <span class="name">Andrei Elias</span>
        </div>
        <nav>
            <button class="nav-link" on:click={() => scrollTo("projects")}
                >Projects</button
            >
            <button class="nav-link" on:click={() => scrollTo("tech-showcase")}
                >Tech Showcase</button
            >
            <button
                class="theme-toggle"
                on:click={toggleTheme}
                aria-label="Toggle Dark Mode"
            >
                {#if isDark}
                    <!-- Sun Icon -->
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        ><circle cx="12" cy="12" r="5"></circle><line
                            x1="12"
                            y1="1"
                            x2="12"
                            y2="3"
                        ></line><line x1="12" y1="21" x2="12" y2="23"
                        ></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"
                        ></line><line
                            x1="18.36"
                            y1="18.36"
                            x2="19.78"
                            y2="19.78"
                        ></line><line x1="1" y1="12" x2="3" y2="12"></line><line
                            x1="21"
                            y1="12"
                            x2="23"
                            y2="12"
                        ></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"
                        ></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"
                        ></line></svg
                    >
                {:else}
                    <!-- Moon Icon -->
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        ><path
                            d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"
                        ></path></svg
                    >
                {/if}
            </button>
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
        text-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
    }

    .theme-toggle {
        background: none;
        border: none;
        color: var(--color-text);
        cursor: pointer;
        padding: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: color 0.2s;
    }

    .theme-toggle:hover {
        color: var(--color-primary);
    }
</style>
