<script>
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";

    export let name;

    // Smooth scroll to the specified element ID
    function scrollTo(id) {
        const element = document.getElementById(id);
        if (element) {
            element.scrollIntoView({ behavior: "smooth" });
        }
    }

    let isDark = false;

    // Toggle theme with a circular revealing animation
    function toggleTheme(event) {
        const x = event.clientX;
        const y = event.clientY;

        const endRadius = Math.hypot(
            Math.max(x, innerWidth - x),
            Math.max(y, innerHeight - y),
        );

        // Fallback for browsers without View Transition API
        // @ts-ignore
        if (!document.startViewTransition) {
            isDark = !isDark;
            updateTheme();
            return;
        }

        // Use View Transition API for smooth theme switch
        // @ts-ignore
        const transition = document.startViewTransition(async () => {
            isDark = !isDark;
            updateTheme();
        });

        // Custom animation logic
        transition.ready.then(() => {
            const gridSize = 32;
            const stepsPerFrame = 400; // Polygon resolution
            const angleStep = (Math.PI * 2) / stepsPerFrame;
            const duration = 750;
            const fps = 60;
            const totalFrames = Math.ceil((duration / 1000) * fps);
            const keyframes = [];

            // Track max radius to ensure the circle only grows
            const maxRadii = new Array(stepsPerFrame).fill(0);

            for (let f = 0; f <= totalFrames; f++) {
                const linearProgress = f / totalFrames;
                const progress = Math.pow(linearProgress, 3); // Cubic easing

                // Randomize wave parameters for each frame
                const randomFactor = Math.random();
                const freq1 = 2 + Math.floor(randomFactor * 3);
                const freq2 = 4 + Math.floor(randomFactor * 3);
                const phase = randomFactor * Math.PI * 2;
                const rBase = endRadius * 1.5 * progress;

                const framePoints = [];
                const frameCoords = [];

                for (let i = 0; i < stepsPerFrame; i++) {
                    const angle = i * angleStep;
                    let r = rBase;

                    if (rBase > 0) {
                        const wave =
                            0.15 * Math.sin(freq1 * angle + phase) +
                            0.1 * Math.sin(freq2 * angle - phase);
                        r = rBase * (1 + wave);
                    }

                    // Enforce monotonic growth
                    if (r < maxRadii[i]) {
                        r = maxRadii[i];
                    } else {
                        maxRadii[i] = r;
                    }

                    const rawX = x + r * Math.cos(angle);
                    const rawY = y + r * Math.sin(angle);

                    // Snap to grid for pixelated effect
                    const dx = rawX - x;
                    const dy = rawY - y;
                    const snappedDx = Math.round(dx / gridSize) * gridSize;
                    const snappedDy = Math.round(dy / gridSize) * gridSize;
                    const finalX = x + snappedDx;
                    const finalY = y + snappedDy;

                    frameCoords.push({ x: finalX, y: finalY });
                }

                // Construct polygon path
                for (let i = 0; i < stepsPerFrame; i++) {
                    const prevIndex = (i - 1 + stepsPerFrame) % stepsPerFrame;
                    const curr = frameCoords[i];
                    const prev = frameCoords[prevIndex];
                    framePoints.push(`${curr.x}px ${prev.y}px`);
                    framePoints.push(`${curr.x}px ${curr.y}px`);
                }

                keyframes.push({
                    clipPath: `polygon(${framePoints.join(", ")})`,
                    easing: "step-end",
                });
            }

            document.documentElement.animate(keyframes, {
                duration: duration,
                easing: "linear",
                pseudoElement: "::view-transition-new(root)",
            });
        });
    }

    // Apply theme changes to the document
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
            <span class="name gradient-text">Andrei Elias</span>
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
                    <!-- Pixelated Sun Icon -->
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                        style="image-rendering: pixelated;"
                    >
                        <path
                            d="M8 8H16V16H8V8ZM10 2H14V6H10V2ZM10 18H14V22H10V18ZM2 10H6V14H2V10ZM18 10H22V14H18V10ZM5 5H7V7H5V5ZM17 5H19V7H17V5ZM17 17H19V19H17V17ZM5 17H7V19H5V17Z"
                        />
                    </svg>
                {:else}
                    <!-- Pixelated Moon Icon -->
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                        style="image-rendering: pixelated;"
                    >
                        <!-- Chunky Pixel Moon (Long Horizontal Tips) -->
                        <rect x="6" y="8" width="6" height="8" />
                        <rect x="8" y="5" width="6" height="3" />
                        <rect x="8" y="16" width="6" height="3" />
                        <rect x="11" y="3" width="8" height="2" />
                        <rect x="11" y="19" width="8" height="2" />
                    </svg>
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
        text-shadow: 0 0 10px rgba(var(--color-primary-rgb), 0.3);
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
