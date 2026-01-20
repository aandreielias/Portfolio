<script>
  export let name = "ANDREI ELIAS";
  export let helloText = "HELLO";
  export let introText = "MY NAME IS";

  // Split name into rows
  $: parts = name.split(" ");
  // Ensure we have strings to work with even if name is empty
  $: firstName = parts[0] || "ANDREI";
  $: lastName = parts.slice(1).join(" ") || "ELIAS";

  // Scale factor to compensate for the original viewBox cropping (75/100 -> 1.333 zoom)
  const SCALE = 100 / 75;
  const STROKE_WIDTH_LG = 0.04 * SCALE;
  const STROKE_WIDTH_SM = 0.04 * SCALE;
</script>

<div class="kinetic-container">
  <div class="outer-backdrop">
    <div class="outer-circle"></div>
    <svg width="0" height="0" class="mask-def">
      <defs>
        <mask id="mask-hole" maskContentUnits="objectBoundingBox">
          <rect width="1" height="1" fill="white" />
          <rect x="0.17" y="0.17" width="0.66" height="0.66" fill="black" />
        </mask>
      </defs>
    </svg>
  </div>
  <div class="grid">
    <!-- COLUMN 1: HELLO (Vertical) -->
    <div
      class="cell col-vertical col-1"
      style="--x: 0; --w: 0.15; --y: 0; --h: 1;"
    >
      <svg width="0" height="0" class="mask-def">
        <defs>
          <mask id="mask-hello" maskContentUnits="objectBoundingBox">
            {#each helloText.split("") as char, i}
              <text
                x={(i * 1.0) / helloText.length + 0.5 / helloText.length}
                y="0.5"
                font-size={SCALE}
                text-anchor="middle"
                dominant-baseline="central"
                textLength={1.0 / helloText.length}
                lengthAdjust="spacingAndGlyphs"
                transform="rotate(-90, 0.5, 0.5)"
                fill="white"
                stroke="white"
                stroke-width={STROKE_WIDTH_LG}>{char}</text
              >
            {/each}
          </mask>
          <mask id="mask-hello-inverse" maskContentUnits="objectBoundingBox">
            <rect width="1" height="1" fill="white" />
            {#each helloText.split("") as char, i}
              <text
                x={(i * 1.0) / helloText.length + 0.5 / helloText.length}
                y="0.5"
                font-size={SCALE}
                text-anchor="middle"
                dominant-baseline="central"
                textLength={1.0 / helloText.length}
                lengthAdjust="spacingAndGlyphs"
                transform="rotate(-90, 0.5, 0.5)"
                fill="black"
                stroke="black"
                stroke-width={STROKE_WIDTH_LG}>{char}</text
              >
            {/each}
          </mask>
        </defs>
      </svg>
      <div
        class="bg-layer masked-layer"
        style="mask: url(#mask-hello-inverse); -webkit-mask: url(#mask-hello-inverse);"
      >
        <!-- Solid Rectangle Filling the Cell -->
        <div class="bg-rect"></div>
      </div>
      <div
        class="inversionMask masked-layer"
        style="mask: url(#mask-hello); -webkit-mask: url(#mask-hello);"
      ></div>
    </div>

    <!-- COLUMN 2: MY NAME IS (Vertical) -->
    <div
      class="cell col-vertical col-2"
      style="--x: 0.15; --w: 0.15; --y: 0; --h: 1;"
    >
      <svg width="0" height="0" class="mask-def">
        <defs>
          <mask id="mask-intro" maskContentUnits="objectBoundingBox">
            {#each introText.split("") as char, i}
              <text
                x={(i * 1.0) / introText.length + 0.5 / introText.length}
                y="0.5"
                font-size={SCALE}
                text-anchor="middle"
                dominant-baseline="central"
                textLength={1.0 / introText.length}
                lengthAdjust="spacingAndGlyphs"
                transform="rotate(-90, 0.5, 0.5)"
                fill="white"
                stroke="white"
                stroke-width={STROKE_WIDTH_LG}>{char}</text
              >
            {/each}
          </mask>
          <mask id="mask-intro-inverse" maskContentUnits="objectBoundingBox">
            <rect width="1" height="1" fill="white" />
            {#each introText.split("") as char, i}
              <text
                x={(i * 1.0) / introText.length + 0.5 / introText.length}
                y="0.5"
                font-size={SCALE}
                text-anchor="middle"
                dominant-baseline="central"
                textLength={1.0 / introText.length}
                lengthAdjust="spacingAndGlyphs"
                transform="rotate(-90, 0.5, 0.5)"
                fill="black"
                stroke="black"
                stroke-width={STROKE_WIDTH_LG}>{char}</text
              >
            {/each}
          </mask>
        </defs>
      </svg>
      <div
        class="bg-layer masked-layer"
        style="mask: url(#mask-intro-inverse); -webkit-mask: url(#mask-intro-inverse);"
      >
        <div class="bg-rect"></div>
      </div>
      <div
        class="inversionMask masked-layer"
        style="mask: url(#mask-intro); -webkit-mask: url(#mask-intro);"
      ></div>
    </div>

    <!-- COLUMN 3, ROW 1: NAME (Horizontal) -->
    <div
      class="cell row-horizontal row-1"
      style="--x: 0.3; --w: 0.7; --y: 0; --h: 0.5;"
    >
      <svg width="0" height="0" class="mask-def">
        <defs>
          <mask id="mask-first" maskContentUnits="objectBoundingBox">
            {#each firstName.split("") as char, i}
              <text
                x={(i * 1.0) / firstName.length + 0.5 / firstName.length}
                y="0.5"
                font-size={SCALE}
                text-anchor="middle"
                dominant-baseline="central"
                textLength={1.0 / firstName.length}
                lengthAdjust="spacingAndGlyphs"
                fill="white"
                stroke="white"
                stroke-width={STROKE_WIDTH_LG}>{char}</text
              >
            {/each}
          </mask>
          <mask id="mask-first-inverse" maskContentUnits="objectBoundingBox">
            <rect width="1" height="1" fill="white" />
            {#each firstName.split("") as char, i}
              <text
                x={(i * 1.0) / firstName.length + 0.5 / firstName.length}
                y="0.5"
                font-size={SCALE}
                text-anchor="middle"
                dominant-baseline="central"
                textLength={1.0 / firstName.length}
                lengthAdjust="spacingAndGlyphs"
                fill="black"
                stroke="black"
                stroke-width={STROKE_WIDTH_LG}>{char}</text
              >
            {/each}
          </mask>
        </defs>
      </svg>
      <div
        class="bg-layer masked-layer"
        style="mask: url(#mask-first-inverse); -webkit-mask: url(#mask-first-inverse);"
      >
        <div class="bg-rect"></div>
      </div>
      <div
        class="inversionMask masked-layer"
        style="mask: url(#mask-first); -webkit-mask: url(#mask-first);"
      ></div>
    </div>

    <!-- COLUMN 3, ROW 2: SURNAME (Horizontal) -->
    <div
      class="cell row-horizontal row-2"
      style="--x: 0.3; --w: 0.7; --y: 0.5; --h: 0.5;"
    >
      <svg width="0" height="0" class="mask-def">
        <defs>
          <mask id="mask-last" maskContentUnits="objectBoundingBox">
            {#each lastName.split("") as char, i}
              <text
                x={(i * 1.0) / lastName.length + 0.5 / lastName.length}
                y="0.5"
                font-size={SCALE}
                text-anchor="middle"
                dominant-baseline="central"
                textLength={1.0 / lastName.length}
                lengthAdjust="spacingAndGlyphs"
                fill="white"
                stroke="white"
                stroke-width={STROKE_WIDTH_SM}>{char}</text
              >
            {/each}
          </mask>
          <mask id="mask-last-inverse" maskContentUnits="objectBoundingBox">
            <rect width="1" height="1" fill="white" />
            {#each lastName.split("") as char, i}
              <text
                x={(i * 1.0) / lastName.length + 0.5 / lastName.length}
                y="0.5"
                font-size={SCALE}
                text-anchor="middle"
                dominant-baseline="central"
                textLength={1.0 / lastName.length}
                lengthAdjust="spacingAndGlyphs"
                fill="black"
                stroke="black"
                stroke-width={STROKE_WIDTH_SM}>{char}</text
              >
            {/each}
          </mask>
        </defs>
      </svg>
      <div
        class="bg-layer masked-layer"
        style="mask: url(#mask-last-inverse); -webkit-mask: url(#mask-last-inverse);"
      >
        <div class="bg-rect"></div>
      </div>
      <div
        class="inversionMask masked-layer"
        style="mask: url(#mask-last); -webkit-mask: url(#mask-last);"
      ></div>
    </div>
  </div>
</div>

<style>
  .kinetic-container {
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    /* Removed mix-blend-mode: difference to allow inversionMask to handle the effect directly */
    color: white;
    /* Ensure overflow is visible so the outer backdrop can extend */
    overflow: visible;
    position: relative; /* For absolute positioning of children */
  }

  .outer-backdrop {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 150%;
    height: 150%;
    pointer-events: none;
    z-index: 0; /* Behind Grid */
    /* Apply mask to cut out the center (where the grid is) */
    mask: url(#mask-hole);
    -webkit-mask: url(#mask-hole);
    mask-repeat: no-repeat;
    -webkit-mask-repeat: no-repeat;
    mask-size: 100% 100%;
    -webkit-mask-size: 100% 100%;
  }

  .outer-circle {
    width: 100%;
    height: 100%;
    background-color: black;
    border-radius: 50%;
  }

  .inversionMask {
    backdrop-filter: invert(1) brightness(0.7) sepia(1) hue-rotate(195deg)
      saturate(500%) !important;
    -webkit-backdrop-filter: invert(1) brightness(0.7) sepia(1)
      hue-rotate(190deg) saturate(500%) !important;
  }

  .grid {
    display: grid;
    grid-template-columns: 15% 15% 1fr;
    grid-template-rows: 1fr 1fr;
    width: 100%;
    height: 100%;
    gap: 0;
  }

  .cell {
    width: 100%;
    height: 100%;
    overflow: hidden;
    position: relative;
    line-height: 0;
  }

  .mask-def {
    position: absolute;
    width: 0;
    height: 0;
    pointer-events: none;
  }

  .masked-layer {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    /* Ensure mask repeats/sizing are correct (default is repeat, match element box) */
    mask-repeat: no-repeat;
    -webkit-mask-repeat: no-repeat;
    mask-size: 100% 100%;
    -webkit-mask-size: 100% 100%;
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

  text {
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

    .col-vertical text {
      transform: none;
    }
  }

  /* Simplified Background Logic */
  .bg-layer {
    z-index: 0; /* Behind inversionMask */
    top: -1px;
    left: -1px;
    width: calc(100% + 2px);
    height: calc(100% + 2px);
  }

  .inversionMask {
    z-index: 1; /* On top */
  }

  .bg-rect {
    width: 100%;
    height: 100%;
    background-color: black;
    transform: scale(1.02); /* Slight overlap to prevent sub-pixel gaps */
  }
</style>
