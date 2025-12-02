<script>
    import { cubicInOut } from "svelte/easing";

    export let items = [];
    export let mode = "education"; // 'education' or 'work'

    $: filteredItems = items.filter((item) => item.type === mode);

    function hinge(node, { duration, delay = 0, type }) {
        return {
            duration,
            delay,
            css: (t) => {
                const eased = cubicInOut(t);
                // Education (type='education'): Hinge is on Left.
                // In: Rotate from -90 to 0. Out: Rotate from 0 to -90.
                // Work (type='work'): Hinge is on Right.
                // In: Rotate from 90 to 0. Out: Rotate from 0 to 90.

                let rotate;
                if (type === "education") {
                    rotate = -90 + eased * 90; // -90 -> 0
                } else {
                    rotate = 90 - eased * 90; // 90 -> 0
                }

                return `
                    transform: rotateY(${rotate}deg);
                    opacity: ${eased};
                `;
            },
        };
    }
</script>

<div class="timeline-container" class:mode-work={mode === "work"}>
    <div class="line"></div>

    <div class="items">
        {#each filteredItems as item (item)}
            <div
                class="item-wrapper"
                in:hinge={{ duration: 600, delay: 300, type: item.type }}
                out:hinge={{ duration: 600, delay: 0, type: item.type }}
            >
                <div class="knot-container">
                    <div class="knot"></div>
                </div>
                <div class="content">
                    <div class="header">
                        <span class="title">{item.title}</span>
                        <span class="date">{item.displayDate}</span>
                    </div>
                    <div class="description">{item.description}</div>
                </div>
            </div>
        {/each}
    </div>
</div>

<style>
    .timeline-container {
        position: relative;
        padding: 2rem 0;
        min-height: 300px;
        perspective: 2000px; /* Deep perspective */
    }

    .line {
        position: absolute;
        top: 2rem;
        bottom: 2rem;
        width: 6px; /* Thicker spine */
        background: linear-gradient(
            to bottom,
            var(--color-primary),
            var(--color-secondary)
        );
        left: 30px;
        border-radius: 3px;
        transition: left 0.8s cubic-bezier(0.4, 0, 0.2, 1); /* Slower slide */
        z-index: 10;
        box-shadow: 0 0 10px rgba(79, 70, 229, 0.3);
    }

    .mode-work .line {
        left: calc(100% - 30px);
    }
    .items {
        display: flex;
        flex-direction: column;
        gap: 3rem;
    }

    .item-wrapper {
        position: relative;
        display: flex;
        align-items: flex-start;
        padding-left: 60px; /* Space for line */
        transform-style: preserve-3d;
        transform-origin: 33px center; /* Hinge point (30px line + 3px half-width) */
    }

    .mode-work .item-wrapper {
        flex-direction: row-reverse;
        padding-left: 0;
        padding-right: 60px;
        text-align: right;
        transform-origin: calc(100% - 33px) center; /* Hinge point on right */
    }

    .knot-container {
        position: absolute;
        left: 33px; /* Center on line */
        top: 1.5rem;
        width: 0;
        height: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        /* Knot moves with the wrapper, no separate transition needed if wrapper hinges */
    }

    .mode-work .knot-container {
        left: auto;
        right: 33px;
    }

    .knot {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: var(--gradient-heading);
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
        z-index: 11;
        transform: translateX(-50%); /* Center the dot */
    }

    .mode-work .knot {
        transform: translateX(50%);
    }

    .content {
        background: var(--glass-panel-bg);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        width: 100%;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
        /* Content is flat on the "page" */
    }

    .content:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: var(--shadow-md);
        background: rgba(255, 255, 255, 0.1);
    }

    .header {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
        margin-bottom: 0.8rem;
    }

    .title {
        font-weight: 700;
        color: var(--color-text);
        font-size: 1.2rem;
    }

    .date {
        font-size: 0.9rem;
        color: var(--color-primary);
        font-weight: 600;
    }

    .description {
        font-size: 1rem;
        color: var(--color-text-muted);
        line-height: 1.6;
    }

    @media (max-width: 768px) {
        .line {
            left: 30px !important;
        }

        .mode-work .line {
            left: 30px !important;
        }

        .item-wrapper {
            padding-left: 60px !important;
            padding-right: 0 !important;
            flex-direction: row !important;
            text-align: left !important;
            transform-origin: 33px center !important;
        }

        .knot-container {
            left: 33px !important;
            right: auto !important;
        }

        .knot {
            transform: translateX(-50%) !important;
        }
    }
</style>
