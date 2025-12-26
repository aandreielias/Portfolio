<script context="module">
  import { glitchChars } from "../../utils/glitchCharacters.js";

  export class GlitchString {
    constructor(originalText) {
      this.originalText = originalText;
      this.chars = originalText.split("").map((char) => ({
        original: char,
        current: char,
        glitchType: null, // null, 'random', '?', 'block'
        glitchTimeout: 0,
        nextGlitchAvailable: 0,
      }));
      this.glitchHistory = []; // Track timestamps of started glitches
      this.lastCheck = Date.now();
    }

    update() {
      const now = Date.now();
      const dt = now - this.lastCheck;
      this.lastCheck = now;

      // Clean up glitch history older than 5 seconds
      this.glitchHistory = this.glitchHistory.filter((t) => now - t < 5000);

      this.chars.forEach((char) => {
        if (char.glitchType) {
          char.glitchTimeout -= dt;
          if (char.glitchTimeout <= 0) {
            if (char.glitchType === "random") {
              char.glitchType = "?";
              char.current = "?";
              char.glitchTimeout = 100;
            } else if (char.glitchType === "?") {
              char.glitchType = "block";
              char.current = "▮";
              char.glitchTimeout = 100;
            } else {
              char.glitchType = null;
              char.current = char.original;
              char.nextGlitchAvailable = now + 5000;
            }
          }
        } else if (
          this.glitchHistory.length < 3 &&
          now >= char.nextGlitchAvailable &&
          char.original !== " "
        ) {
          // Lower chance to start glitching (0.1% per frame ≈ 0.06 per char/sec)
          if (Math.random() < 0.001) {
            char.glitchType = "random";
            char.glitchTimeout = 200;
            char.current =
              glitchChars[Math.floor(Math.random() * glitchChars.length)];
            this.glitchHistory.push(now);
          }
        }
      });

      return this.chars.map((c) => c.current).join("");
    }
  }
</script>

<script>
  import { onMount, onDestroy } from "svelte";

  export let text = "Hello, my name is";
  export let speed = 16;

  let glitcher = new GlitchString(text);
  let displayedText = text;
  let frameId;
  let lastUpdate = 0;

  $: if (text !== glitcher.originalText) {
    glitcher = new GlitchString(text);
  }

  function animate(timestamp) {
    if (timestamp - lastUpdate >= speed) {
      lastUpdate = timestamp;
      displayedText = glitcher.update();
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
