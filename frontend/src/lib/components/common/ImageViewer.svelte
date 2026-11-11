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
    <button class="close" onclick={closeImage} aria-label="✕">✕</button>
  </div>
{/if}

<style>
  .viewer { position: fixed; inset: 0; z-index: 60; display: grid; place-items: center; overflow: hidden; }
  .backdrop { position: absolute; inset: 0; background: rgb(253 252 250 / 0.96); cursor: zoom-out; }
  img {
    position: relative;
    max-width: 92vw;
    max-height: 84vh;
    box-shadow: 0 20px 60px -20px rgb(0 0 0 / 0.35);
    cursor: zoom-in;
    touch-action: none;
    transition: transform 0.15s ease-out;
  }
  img.zoomed { cursor: grab; transition: none; }
  p, .close { position: absolute; background: var(--paper); }
  p { bottom: 1.25rem; left: 50%; translate: -50%; max-width: 90vw; padding: 0.2rem 0.6rem; text-align: center; font-size: 0.875rem; color: var(--muted); pointer-events: none; }
  .close { top: 1rem; right: 1.25rem; font-size: 1.25rem; padding: 0.25rem 0.6rem; }
</style>
