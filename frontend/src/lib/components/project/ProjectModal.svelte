<script>
  import Modal from "../common/Modal.svelte";
  import { openImage } from "../../stores/imageViewerStore.js";

  let { project, t, lang, onclose } = $props();
  const base = import.meta.env.BASE_URL;
  let p = $derived(project[lang]);
</script>

<Modal title={p.title} {onclose} labels={t.ui}>
  {#snippet actions()}
    {#if project.link}<a class="btn" href={project.link} target="_blank" rel="noopener">{t.ui.source}</a>{/if}
    {#if project.pdf}<a class="btn" href={base + project.pdf} target="_blank" rel="noopener">{t.ui.openPdf}</a>{/if}
  {/snippet}

  <p class="year">{project.year}</p>
  {#each p.body as para}<p class="para">{para}</p>{/each}
  <p class="tech"><span>{t.ui.technologies}</span> {project.tech}</p>

  {#if project.code}<pre><code>{project.code}</code></pre>{/if}

  {#each project.images ?? [] as img}
    <figure>
      <button onclick={() => openImage(base + img.src, img[lang])}>
        <img src={base + img.src} alt={img[lang]} loading="lazy" />
      </button>
      <figcaption>{img[lang]}</figcaption>
    </figure>
  {/each}
</Modal>

<style>
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
  figure { margin: var(--s5) 0 0; }
  figure button { display: block; width: 100%; cursor: zoom-in; border-radius: var(--r-md); }
  figure img { display: block; width: 100%; height: auto; border-radius: var(--r-md); box-shadow: var(--shadow-raised); }
  figcaption { font-size: 13px; color: var(--muted); margin-top: var(--s2); }
</style>
