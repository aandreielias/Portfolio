<script>
  import { cubicInOut } from "svelte/easing";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let items = [];
  export let mode = "education"; // 'education', 'work', or 'combined'

  // For single-column modes
  $: filteredItems =
    mode === "combined"
      ? [] // Not used in combined split view
      : items.filter((item) => item.type === mode);

  // For combined split view
  $: leftItems =
    mode === "combined"
      ? items
          .filter((item) => item.type === "education")
          .sort((a, b) => b.start - a.start)
      : [];
  $: rightItems =
    mode === "combined"
      ? items
          .filter((item) => item.type === "work")
          .sort((a, b) => b.start - a.start)
      : [];

  function hinge(node, { duration, delay = 0, type = null, side = null }) {
    return {
      duration,
      delay,
      css: (t) => {
        const eased = cubicInOut(t);
        let rotate;
        // If explicitly left (Education in combined) or just standard mode
        const isLeft = side === "left" || (mode === "education" && !side);

        if (isLeft) {
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

<div
  class="timeline-container"
  class:mode-work={mode === "work"}
  class:mode-combined={mode === "combined"}
>
  <div class="line"></div>

  {#if mode === "combined"}
    <div class="timeline-split">
      <!-- Left Column (Education) -->
      <div class="column left-col">
        {#each leftItems as item (item)}
          <div
            class="item-wrapper is-left"
            in:hinge={{ duration: 600, delay: 300, side: "left" }}
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
              {#if item.skills}
                <div class="timeline-skills">
                  {#each item.skills as skill}
                    <span class="timeline-skill-tag">{skill}</span>
                  {/each}
                </div>
              {/if}
              {#if item.action}
                <button
                  class="timeline-action-btn"
                  on:click={() =>
                    dispatch("viewProject", item.action.projectId)}
                >
                  {item.action.label}
                </button>
              {/if}
            </div>
          </div>
        {/each}
      </div>

      <!-- Right Column (Work) -->
      <div class="column right-col">
        {#each rightItems as item (item)}
          <div
            class="item-wrapper is-right"
            in:hinge={{ duration: 600, delay: 300, side: "right" }}
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
  {:else}
    <!-- Original Single Column View -->
    <div class="items">
      {#each filteredItems as item (item)}
        <div
          class="item-wrapper"
          in:hinge={{ duration: 600, delay: 300, type: item.type }}
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
            {#if item.skills}
              <div class="timeline-skills">
                {#each item.skills as skill}
                  <span class="timeline-skill-tag">{skill}</span>
                {/each}
              </div>
            {/if}
            {#if item.action}
              <button
                class="timeline-action-btn"
                on:click={() => dispatch("viewProject", item.action.projectId)}
              >
                {item.action.label}
              </button>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .timeline-container {
    position: relative;
    padding: 2rem 0;
    min-height: 300px;
    perspective: 2000px;
  }

  .line {
    position: absolute;
    top: 2rem;
    bottom: 2rem;
    width: 6px;
    background: linear-gradient(
      to bottom,
      var(--color-primary),
      var(--color-secondary)
    );
    left: 30px;
    border-radius: 3px;
    transition: left 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 10;
    box-shadow: 0 0 10px rgba(79, 70, 229, 0.3);
  }

  .mode-work .line {
    left: calc(100% - 30px);
  }

  .mode-combined .line {
    left: 50%;
    transform: translateX(-50%);
  }

  /* Split View Layout */
  .timeline-split {
    display: flex;
    width: 100%;
    justify-content: center;
  }

  .column {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    min-width: 0; /* Prevent flex overflow */
  }

  /* Single Column Items (Legacy) */
  .items {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  /* Item Wrappers */
  .item-wrapper {
    position: relative;
    display: flex;
    align-items: flex-start;
    padding-left: 60px;
    transform-style: preserve-3d;
    transform-origin: 33px center;
  }

  /* Single Mode: Work (Right Hinge) */
  .mode-work .item-wrapper {
    flex-direction: row-reverse;
    padding-left: 0;
    padding-right: 60px;
    text-align: right;
    transform-origin: calc(100% - 33px) center;
  }

  /* Combined Mode Specifics */
  .mode-combined .item-wrapper.is-left {
    margin-right: 0;
    padding-right: 40px;
    padding-left: 0;
    text-align: right;
    flex-direction: row-reverse;
    transform-origin: right center;
  }

  .mode-combined .item-wrapper.is-right {
    margin-left: 0;
    padding-left: 40px;
    padding-right: 0;
    text-align: left;
    flex-direction: row;
    transform-origin: left center;
  }

  /* Knot Positioning */
  .knot-container {
    position: absolute;
    left: 33px;
    top: 1.5rem;
    width: 0;
    height: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .mode-work .knot-container {
    left: auto;
    right: 33px;
  }

  .mode-combined .is-left .knot-container {
    right: -3px; /* Center of the line (width 6px) implies center is 3px inward from edge? 
                        Actually line occupies center screen. 
                        Left column ends at 50%. Line is at 50%. 
                        So padding-right is space to line. 
                        We need knot at right edge of this container.
                     */
    right: -3px; /* Half of line width */
    left: auto;
    top: 1.5rem;
  }

  .mode-combined .is-right .knot-container {
    left: -3px;
    right: auto;
    top: 1.5rem;
  }

  .knot {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--gradient-heading);
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
    z-index: 11;
    transform: translateX(-50%);
  }

  .mode-work .knot {
    transform: translateX(50%);
  }

  .mode-combined .is-left .knot {
    transform: translateX(50%);
  }

  .mode-combined .is-right .knot {
    transform: translateX(-50%);
  }

  /* Content Box */
  .content {
    background: var(--glass-panel-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    width: 100%;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
  }

  /* Only lift the card if we are NOT hovering the action button */
  .content:hover:not(:has(.timeline-action-btn:hover)) {
    transform: translateY(-2px) scale(1.01);
    box-shadow: var(--shadow-md);
    background: rgba(255, 255, 255, 0.1);
  }

  /* When hovering the button, we can still highlight the card background slightly if desired,
     or just leave it relative to the button.
     Let's keep the card static (original position) but maybe keep the background for "active" state
  */
  .content:has(.timeline-action-btn:hover) {
    background: rgba(255, 255, 255, 0.05);
  }

  /* ... existing styles ... */

  .header {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    margin-bottom: 0.8rem;
  }

  /* ... */

  .timeline-skills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.75rem;
  }

  .timeline-skill-tag {
    font-size: 0.75rem;
    padding: 0.2rem 0.6rem;
    border-radius: 99px;
    background: rgba(var(--color-primary-rgb), 0.05);
    border: 1px solid rgba(var(--color-primary-rgb), 0.15);
    color: var(--color-text-muted);
    white-space: nowrap;
  }

  .timeline-action-btn {
    display: block;
    width: 100%;
    margin-top: 1rem;
    padding: 0.6rem;
    background: rgba(var(--color-primary-rgb), 0.1);
    border: 1px solid rgba(var(--color-primary-rgb), 0.2);
    color: var(--color-primary);
    border-radius: var(--radius);
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); /* Smooth transition */
    text-align: center;
  }

  .timeline-action-btn:hover {
    background: rgba(var(--color-primary-rgb), 0.2);
    transform: translateY(-4px) scale(1.02); /* Move forward/up significantly */
    box-shadow: 0 4px 12px rgba(var(--color-primary-rgb), 0.3);
  }

  @media (max-width: 768px) {
    .line {
      left: 30px !important;
      transform: none !important;
    }

    .timeline-split {
      flex-direction: column;
    }

    .column {
      gap: 2rem;
    }

    /* Reset wrappers to strict left-aligned stack on mobile */
    .item-wrapper,
    .mode-work .item-wrapper,
    .mode-combined .item-wrapper,
    .mode-combined .item-wrapper.is-left,
    .mode-combined .item-wrapper.is-right {
      width: 100% !important;
      padding-left: 60px !important;
      padding-right: 0 !important;
      flex-direction: row !important;
      text-align: left !important;
      transform-origin: 33px center !important;
      margin: 0 !important;
    }

    .knot-container,
    .mode-combined .is-left .knot-container,
    .mode-combined .is-right .knot-container {
      left: 33px !important; /* 30px line + 3px center */
      right: auto !important;
    }

    .knot,
    .mode-combined .is-left .knot,
    .mode-combined .is-right .knot {
      transform: translateX(-50%) !important;
    }
  }
</style>
