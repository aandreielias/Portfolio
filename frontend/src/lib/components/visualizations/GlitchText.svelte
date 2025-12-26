<script>
  import { onMount, onDestroy } from "svelte";
  import { glitchChars } from "../../utils/glitchCharacters.js";

  export let text = "Hello, my name is";
  export let speed = 16; // 60fps ~= 16.67ms

  let displayedChars = text
    .split("")
    .map((char) => ({ char, isGlitch: false }));
  let frameId;
  let lastUpdate = 0;

  function animate(timestamp) {
    if (timestamp - lastUpdate >= speed) {
      lastUpdate = timestamp;

      // Update logic:
      // We want to keep most text readable but chaotic.
      // Re-generate the array occasionally or just modify in place?
      // To satisfy "separate letters updated each", we treat them individually.

      const newChars = text.split("").map((original, i) => {
        // 5% chance to glitch each character per frame
        if (original !== " " && Math.random() < 0.05) {
          return {
            char: glitchChars[Math.floor(Math.random() * glitchChars.length)],
            isGlitch: true,
          };
        }
        return { char: original, isGlitch: false };
      });

      displayedChars = newChars;
    }

    frameId = requestAnimationFrame(animate);
  }

  onMount(() => {
    frameId = requestAnimationFrame(animate);
  });

  onDestroy(() => {
    if (frameId) cancelAnimationFrame(frameId);
  });
</script>

<span class="glitch-wrapper">
  {displayedText}
</span>

<style>
  .glitch-wrapper {
    display: inline-block;
    font-family: var(--font-mono);
    font-weight: 500;
  }
</style>
