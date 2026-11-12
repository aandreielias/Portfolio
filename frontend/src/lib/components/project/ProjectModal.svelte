<script>
  import Modal from "../common/Modal.svelte";
  import EbusConsole from "./EbusConsole.svelte";
  import { openImage } from "../../stores/imageViewerStore.js";

  let { project, t, lang, onclose } = $props();
  const base = import.meta.env.BASE_URL;
  let p = $derived(project[lang]);

  // Diagrams, screenshots and the console share one panel next to the text.
  let slides = $derived([
    ...(project.images ?? []).map((img) => ({ src: img.src, caption: img[lang] })),
    ...(project.console ? [{ console: true, caption: t.ui.console }] : []),
    ...(p.diagrams ?? []),
  ]);
  let i = $state(0);
  let slide = $derived(slides[i]);
  const go = (d) => (i = (i + d + slides.length) % slides.length);
</script>

<Modal title={p.title} {onclose} labels={t.ui} width={slides.length ? 1280 : 860}>
  {#snippet actions()}
    {#if project.link}<a class="btn" href={project.link} target="_blank" rel="noopener">{t.ui.source}</a>{/if}
    {#if project.pdf}<a class="btn" href={base + project.pdf} target="_blank" rel="noopener">{t.ui.openPdf}</a>{/if}
  {/snippet}

  <div class="layout" class:split={slides.length}>
    <div class="text">
      <p class="year">{project.year}</p>
      {#each p.body as para}<p class="para">{para}</p>{/each}
      <p class="tech"><span>{t.ui.technologies}</span> {project.tech}</p>
      {#if project.code}<pre><code>{project.code}</code></pre>{/if}
    </div>

    {#if slide}
      <aside class="side">
        <div class="bar">
          <p class="caption">{slide.caption}</p>
          {#if slides.length > 1}
            <div class="nav">
              <button class="icon" onclick={() => go(-1)} aria-label={t.ui.prev} title={t.ui.prev}>
                <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3.5L5.5 8l4.5 4.5" /></svg>
              </button>
              <span class="count">{i + 1} / {slides.length}</span>
              <button class="icon" onclick={() => go(1)} aria-label={t.ui.next} title={t.ui.next}>
                <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3.5L10.5 8 6 12.5" /></svg>
              </button>
            </div>
          {/if}
        </div>
        {#if slide.console}
          <EbusConsole {lang} />
        {:else}
          <button class="shot" onclick={() => openImage(base + slide.src, slide.caption)}>
            <img src={base + slide.src} alt={slide.caption} />
          </button>
        {/if}
        {#if slides.length > 1}
          <div class="dots">
            {#each slides as s, n}
              <button class:on={n === i} onclick={() => (i = n)} aria-label={s.caption} title={s.caption}></button>
            {/each}
          </div>
        {/if}
      </aside>
    {/if}
  </div>
</Modal>

<style>
  .layout { container-type: inline-size; }
  .layout.split { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.25fr); gap: var(--s6); align-items: start; }
  /* Narrow window: panel goes below the text. */
  @container (max-width: 760px) { .layout.split { grid-template-columns: minmax(0, 1fr); gap: var(--s5); } }

  .year { font-size: 13.5px; color: var(--muted); margin-bottom: var(--s3); font-variant-numeric: tabular-nums; }
  .para { max-width: 68ch; color: #3d3f47; }
  .para + .para { margin-top: var(--s3); }
  .tech { margin-top: var(--s4); font-size: 13.5px; color: var(--muted); }
  .tech span { font-weight: 600; color: var(--text); }

  pre {
    margin: var(--s5) 0 0;
    padding: var(--s4);
    overflow-x: auto;
    font: 13px/1.6 var(--mono);
    background: var(--surface);
    border-radius: var(--r-md);
    box-shadow: inset 0 0 0 1px var(--border);
  }

  .side { position: sticky; top: 0; display: flex; flex-direction: column; gap: var(--s3); min-width: 0; }
  .bar { display: flex; align-items: center; justify-content: space-between; gap: var(--s3); min-height: 28px; }
  .caption { font-size: 13.5px; font-weight: 600; }
  .nav { display: flex; align-items: center; gap: var(--s1); flex-shrink: 0; }
  .count { font-size: 12.5px; color: var(--muted); font-variant-numeric: tabular-nums; min-width: 40px; text-align: center; }
  .icon { display: grid; place-items: center; width: 28px; height: 28px; color: var(--muted); border-radius: var(--r-sm); box-shadow: var(--shadow-raised); }
  .icon:hover { background: var(--hover); color: var(--text); }
  .icon svg { width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }

  .shot { display: block; width: 100%; cursor: zoom-in; border-radius: var(--r-md); }
  .shot img { display: block; width: 100%; height: auto; border-radius: var(--r-md); box-shadow: var(--shadow-raised); }

  .dots { display: flex; justify-content: center; gap: var(--s2); }
  .dots button { width: 8px; height: 8px; padding: 0; border-radius: 50%; background: var(--border-strong); }
  .dots button.on { background: var(--accent); }
</style>
