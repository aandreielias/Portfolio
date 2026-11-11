<script>
  import { fade } from "svelte/transition";
  import { imageViewerStore, closeImage } from "../../stores/imageViewerStore.js";

  let zoom = $state(1);
  let tx = $state(0);
  let ty = $state(0);
  let drag = null;

  // Reset the view whenever a new image opens or the viewer closes.
  $effect(() => {
    $imageViewerStore.src;
    zoom = 1; tx = 0; ty = 0;
  });

  function onwheel(e) {
    e.preventDefault();
    zoom = Math.min(Math.max(1, zoom - e.deltaY * 0.001), 5);
    if (zoom === 1) tx = ty = 0;
  }

  function down(e) {
    if (zoom === 1) return;
    drag = { x: e.clientX - tx, y: e.clientY - ty };
    e.currentTarget.setPointerCapture(e.pointerId);
    e.preventDefault();
  }

  function move(e) {
    if (!drag) return;
    tx = e.clientX - drag.x;
    ty = e.clientY - drag.y;
  }
</script>

{#if $imageViewerStore.isOpen}
  <div class="viewer" role="dialog" aria-modal="true" aria-label={$imageViewerStore.alt} transition:fade={{ duration: 200 }}>
    <button class="backdrop" onclick={closeImage} aria-label="✕"></button>
    <img
      src={$imageViewerStore.src}
      alt={$imageViewerStore.alt}
      class:zoomed={zoom > 1}
      style="transform: translate({tx}px, {ty}px) scale({zoom})"
      {onwheel}
      onpointerdown={down}
      onpointermove={move}
      onpointerup={() => (drag = null)}
      ondblclick={() => { zoom = zoom > 1 ? 1 : 2.5; tx = ty = 0; }}
      draggable="false"
    />
    {#if $imageViewerStore.alt}<p>{$imageViewerStore.alt}</p>{/if}
    <button class="close" onclick={closeImage} aria-label="✕"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" /></svg></button>
  </div>
{/if}

<style>
  .viewer { position: fixed; inset: 0; z-index: 60; display: grid; place-items: center; overflow: hidden; }
  .backdrop { position: absolute; inset: 0; background: rgba(12, 13, 18, 0.72); cursor: zoom-out; }
  img {
    position: relative;
    max-width: 92vw;
    max-height: 84vh;
    border-radius: var(--r-md);
    box-shadow: var(--shadow-window);
    cursor: zoom-in;
    touch-action: none;
    transition: transform 0.15s ease-out;
  }
  img.zoomed { cursor: grab; transition: none; }
  p, .close { position: absolute; background: var(--elevated); box-shadow: var(--shadow-raised); border-radius: var(--r-sm); }
  p { bottom: var(--s4); left: 50%; translate: -50%; max-width: 90vw; padding: var(--s1) var(--s3); font-size: 13px; color: var(--muted); pointer-events: none; }
  .close { top: var(--s4); right: var(--s4); display: grid; place-items: center; width: 32px; height: 32px; }
  .close svg { width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 1.5; stroke-linecap: round; }
</style>
