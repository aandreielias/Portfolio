<script>
  import { fade, fly } from "svelte/transition";
  import { cubicOut } from "svelte/easing";

  let { title, onclose, labels, actions, children } = $props();

  const MIN_W = 300;
  const MIN_H = 200;
  const handles = ["n", "s", "e", "w", "ne", "nw", "se", "sw"];

  const w0 = Math.min(860, innerWidth - 32);
  const h0 = Math.min(innerHeight * 0.85, 780);
  let w = $state(w0);
  let h = $state(h0);
  let x = $state((innerWidth - w0) / 2);
  let y = $state((innerHeight - h0) / 2);
  let maximized = $state(false);
  let drag = null;

  $effect(() => {
    document.body.style.overflow = "hidden";
    return () => (document.body.style.overflow = "");
  });

  function start(e, mode) {
    if (maximized || e.button !== 0 || e.target.closest("button, a")) return;
    drag = { mode, px: e.clientX, py: e.clientY, x, y, w, h };
    e.currentTarget.setPointerCapture(e.pointerId);
    e.preventDefault();
  }

  function move(e) {
    if (!drag) return;
    const dx = e.clientX - drag.px;
    const dy = e.clientY - drag.py;
    const m = drag.mode;
    if (m === "move") {
      x = Math.min(Math.max(drag.x + dx, 0), innerWidth - w);
      y = Math.min(Math.max(drag.y + dy, 0), innerHeight - 48);
      return;
    }
    if (m.includes("e")) w = Math.max(MIN_W, drag.w + dx);
    if (m.includes("s")) h = Math.max(MIN_H, drag.h + dy);
    if (m.includes("w")) { w = Math.max(MIN_W, drag.w - dx); x = drag.x + drag.w - w; }
    if (m.includes("n")) { h = Math.max(MIN_H, drag.h - dy); y = drag.y + drag.h - h; }
  }
</script>

<div class="backdrop" onclick={onclose} transition:fade={{ duration: 250 }} aria-hidden="true"></div>

<div
  class="window"
  class:maximized
  role="dialog"
  aria-modal="true"
  aria-label={title}
  style="left:{x}px; top:{y}px; width:{w}px; height:{h}px"
  transition:fly={{ y: 40, duration: 450, easing: cubicOut }}
  onpointermove={move}
  onpointerup={() => (drag = null)}
>
  <!-- svelte-ignore a11y_no_static_element_interactions (double-click is a shortcut; the maximize button is the accessible path) -->
  <header onpointerdown={(e) => start(e, "move")} ondblclick={() => (maximized = !maximized)}>
    <h2>{title}</h2>
    <div class="actions">
      {@render actions?.()}
      <button class="max" onclick={() => (maximized = !maximized)}>{maximized ? labels.restore : labels.maximize}</button>
      <button onclick={onclose} aria-label={labels.close}>✕</button>
    </div>
  </header>
  <div class="body">{@render children()}</div>
  {#if !maximized}
    {#each handles as d}
      <span class="handle {d}" onpointerdown={(e) => start(e, d)} aria-hidden="true"></span>
    {/each}
  {/if}
</div>

<style>
  .backdrop { position: fixed; inset: 0; z-index: 40; background: rgb(20 20 20 / 0.28); }

  .window {
    position: fixed;
    z-index: 41;
    display: flex;
    flex-direction: column;
    background: var(--paper);
    box-shadow: 0 2px 4px rgb(0 0 0 / 0.08), 0 30px 80px -20px rgb(0 0 0 / 0.45);
  }
  .window.maximized { inset: 0 !important; width: auto !important; height: auto !important; }

  header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem 1.5rem 0.8rem;
    border-bottom: 1px solid var(--ink);
    cursor: grab;
    user-select: none;
    touch-action: none;
  }
  header:active { cursor: grabbing; }
  h2 { font-size: 1.25rem; font-weight: 700; }
  .actions { display: flex; align-items: baseline; gap: 1.1rem; font-size: 0.875rem; flex-shrink: 0; }
  .actions :global(a), .actions button { color: var(--muted); }
  .actions :global(a:hover), .actions button:hover { color: var(--ink); }

  .body { flex: 1; overflow-y: auto; padding: 1.5rem clamp(1rem, 5vw, 3rem) 3rem; }

  .handle { position: absolute; touch-action: none; }
  .n, .s { left: 0.5rem; right: 0.5rem; height: 0.5rem; cursor: ns-resize; }
  .e, .w { top: 0.5rem; bottom: 0.5rem; width: 0.5rem; cursor: ew-resize; }
  .n { top: -0.25rem; } .s { bottom: -0.25rem; } .e { right: -0.25rem; } .w { left: -0.25rem; }
  .ne, .nw, .se, .sw { width: 0.9rem; height: 0.9rem; }
  .ne { top: -0.3rem; right: -0.3rem; cursor: nesw-resize; }
  .sw { bottom: -0.3rem; left: -0.3rem; cursor: nesw-resize; }
  .nw { top: -0.3rem; left: -0.3rem; cursor: nwse-resize; }
  .se { bottom: -0.3rem; right: -0.3rem; cursor: nwse-resize; }

  /* Phones: always full screen, nothing to drag. */
  @media (max-width: 640px) {
    .window { inset: 0 !important; width: auto !important; height: auto !important; }
    .handle, .max { display: none; }
    header { cursor: default; padding: 0.9rem 1rem 0.7rem; }
  }
</style>
