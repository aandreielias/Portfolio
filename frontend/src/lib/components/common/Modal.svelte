<script>
  import { fade, fly } from "svelte/transition";
  import { cubicOut } from "svelte/easing";

  let { title, onclose, labels, actions, children, width = 860 } = $props();

  const MIN_W = 300;
  const MIN_H = 200;
  const handles = ["n", "s", "e", "w", "ne", "nw", "se", "sw"];

  const w0 = Math.min(width, innerWidth - 32);
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
      <button class="icon max" onclick={() => (maximized = !maximized)} aria-label={maximized ? labels.restore : labels.maximize} title={maximized ? labels.restore : labels.maximize}>
        <svg viewBox="0 0 16 16" aria-hidden="true">{#if maximized}<path d="M5.5 3.5h7v7M3.5 5.5h7v7h-7z" />{:else}<rect x="3.5" y="3.5" width="9" height="9" rx="1.5" />{/if}</svg>
      </button>
      <button class="icon" onclick={onclose} aria-label={labels.close} title={labels.close}>
        <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" /></svg>
      </button>
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
  .backdrop { position: fixed; inset: 0; z-index: 40; background: rgba(12, 13, 18, 0.28); }

  .window {
    position: fixed;
    z-index: 41;
    display: flex;
    flex-direction: column;
    background: var(--elevated);
    border-radius: var(--r-lg);
    box-shadow: var(--shadow-window);
  }
  .window.maximized { inset: 0 !important; width: auto !important; height: auto !important; border-radius: 0; }

  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--s4);
    padding: var(--s3) var(--s3) var(--s3) var(--s5);
    border-bottom: 1px solid var(--border);
    cursor: grab;
    user-select: none;
    touch-action: none;
  }
  header:active { cursor: grabbing; }
  h2 { font-size: 16px; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .actions { display: flex; align-items: center; gap: var(--s2); flex-shrink: 0; }

  .icon { display: grid; place-items: center; width: 28px; height: 28px; color: var(--muted); border-radius: var(--r-sm); }
  .icon:hover { background: var(--hover); color: var(--text); }
  .icon svg { width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }

  .body { flex: 1; overflow-y: auto; padding: var(--s5) var(--s6) var(--s6); }

  .handle { position: absolute; touch-action: none; }
  .n, .s { left: 8px; right: 8px; height: 8px; cursor: ns-resize; }
  .e, .w { top: 8px; bottom: 8px; width: 8px; cursor: ew-resize; }
  .n { top: -4px; } .s { bottom: -4px; } .e { right: -4px; } .w { left: -4px; }
  .ne, .nw, .se, .sw { width: 14px; height: 14px; }
  .ne { top: -5px; right: -5px; cursor: nesw-resize; }
  .sw { bottom: -5px; left: -5px; cursor: nesw-resize; }
  .nw { top: -5px; left: -5px; cursor: nwse-resize; }
  .se { bottom: -5px; right: -5px; cursor: nwse-resize; }

  /* Phones: always full screen, nothing to drag. */
  @media (max-width: 720px) {
    .window { inset: 0 !important; width: auto !important; height: auto !important; border-radius: 0; }
    .handle, .max { display: none; }
    header { cursor: default; padding-left: var(--s4); }
    .body { padding: var(--s4) var(--s4) var(--s5); }
  }
</style>
