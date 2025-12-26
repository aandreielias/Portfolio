<script>
  export let name = "ANDREI ELIAS";
  export let helloText = "HELLO";
  export let introText = "MY NAME IS";

  // Split name into rows
  $: parts = name.split(" ");
  // Ensure we have strings to work with even if name is empty
  $: firstName = parts[0] || "ANDREI";
  $: lastName = parts.slice(1).join(" ") || "ELIAS";
</script>

<div class="kinetic-container">
  <div class="grid">
    <!-- COLUMN 1: HELLO (Vertical) -->
    <div class="cell col-vertical col-1">
      <svg viewBox="15 0 75 100" preserveAspectRatio="none">
        {#each helloText.split("") as char, i}
          <text
            x={(i * 100) / helloText.length + 50 / helloText.length}
            y="50"
            font-size="100"
            text-anchor="middle"
            dominant-baseline="central"
            textLength={100 / helloText.length}
            lengthAdjust="spacingAndGlyphs"
            transform="rotate(-90, 50, 50)">{char}</text
          >
        {/each}
      </svg>
    </div>

    <!-- COLUMN 2: MY NAME IS (Vertical) -->
    <div class="cell col-vertical col-2">
      <svg viewBox="15 0 75 100" preserveAspectRatio="none">
        {#each introText.split("") as char, i}
          <text
            x={(i * 100) / introText.length + 50 / introText.length}
            y="50"
            font-size="100"
            text-anchor="middle"
            dominant-baseline="central"
            textLength={100 / introText.length}
            lengthAdjust="spacingAndGlyphs"
            transform="rotate(-90, 50, 50)">{char}</text
          >
        {/each}
      </svg>
    </div>

    <!-- COLUMN 3, ROW 1: NAME (Horizontal) -->
    <div class="cell row-horizontal row-1">
      <svg viewBox="0 15 100 75" preserveAspectRatio="none">
        {#each firstName.split("") as char, i}
          <text
            x={(i * 100) / firstName.length + 50 / firstName.length}
            y="50"
            font-size="100"
            text-anchor="middle"
            dominant-baseline="central"
            textLength={100 / firstName.length}
            lengthAdjust="spacingAndGlyphs">{char}</text
          >
        {/each}
      </svg>
    </div>

    <!-- COLUMN 3, ROW 2: SURNAME (Horizontal) -->
    <div class="cell row-horizontal row-2">
      <svg viewBox="0 15 100 75" preserveAspectRatio="none">
        {#each lastName.split("") as char, i}
          <text
            x={(i * 100) / lastName.length + 50 / lastName.length}
            y="50"
            font-size="100"
            text-anchor="middle"
            dominant-baseline="central"
            textLength={100 / lastName.length}
            lengthAdjust="spacingAndGlyphs">{char}</text
          >
        {/each}
      </svg>
    </div>
  </div>
</div>

<style>
  .kinetic-container {
    width: 100%;
    height: 100%;
    /* Ensure the container itself can be centered or sized by parent */
    box-sizing: border-box;
    /* Maintain mix-blend-mode if needed */
    mix-blend-mode: difference;
    color: white;
  }

  .grid {
    display: grid;
    /* 
       Columns: 
       1: HELLO (Vertical) -> 15%
       2: MY NAME IS (Vertical) -> 15%
       3: Name (Horizontal) -> Remaining (1fr)
    */
    grid-template-columns: 15% 15% 1fr;
    grid-template-rows: 1fr 1fr; /* Equal height horizontal rows */
    width: 100%;
    height: 100%;
    gap: 0;
  }

  .cell {
    width: 100%;
    height: 100%;
    overflow: hidden;
    position: relative;
    line-height: 0; /* Remove potential inline spacing */
  }

  /* Grid Placement */
  .col-1 {
    grid-column: 1;
    grid-row: 1 / span 2;
  }

  .col-2 {
    grid-column: 2;
    grid-row: 1 / span 2;
  }

  .row-1 {
    grid-column: 3;
    grid-row: 1;
  }

  .row-2 {
    grid-column: 3;
    grid-row: 2;
  }

  /* SVG Styling */
  svg {
    width: 100%;
    height: 100%;
    display: block;
  }

  text {
    fill: #fff;
    font-family: var(--font-mono, monospace);
    font-weight: 700;
    text-transform: uppercase;
  }

  @media (max-width: 768px) {
    .grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, 1fr);
    }

    .col-1 {
      grid-column: 1;
      grid-row: 1;
    }
    .col-2 {
      grid-column: 1;
      grid-row: 2;
    }
    .row-1 {
      grid-column: 1;
      grid-row: 3;
    }
    .row-2 {
      grid-column: 1;
      grid-row: 4;
    }

    /* Un-rotate vertical text for stacked mobile view */
    .col-vertical text {
      transform: none;
    }
  }
</style>
