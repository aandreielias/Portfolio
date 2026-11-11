<script>
  import Modal from "../common/Modal.svelte";
  import { openImage } from "../../stores/imageViewerStore.js";

  let { project, t, lang, onclose } = $props();
  const base = import.meta.env.BASE_URL;
  let p = $derived(project[lang]);
</script>

<Modal title={p.title} {onclose} labels={t.ui}>
  {#snippet actions()}
    {#if project.link}<a href={project.link} target="_blank" rel="noopener">{t.ui.source}</a>{/if}
    {#if project.pdf}<a href={base + project.pdf} target="_blank" rel="noopener">{t.ui.openPdf}</a>{/if}
  {/snippet}

  <p class="year">{project.year}</p>
  {#each p.body as para}<p class="para">{para}</p>{/each}
  <p class="tech">{t.ui.technologies}: {project.tech}</p>

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
  .year { font-size: 0.875rem; color: var(--muted); margin-bottom: 1rem; }
  .para { max-width: 40rem; }
  .para + .para { margin-top: 0.75rem; }
  .tech { font-weight: 700; margin-top: 1rem; }
  pre {
    margin: 1.5rem 0 0;
    padding: 1rem 1.25rem;
    overflow-x: auto;
    font: 0.8125rem/1.6 var(--mono);
    background: #f4f2ee;
    border-left: 2px solid var(--ink);
  }
  figure { margin: 2rem 0 0; }
  figure button { display: block; width: 100%; cursor: zoom-in; }
  figure img { display: block; width: 100%; height: auto; border: 1px solid var(--rule); }
  figcaption { font-size: 0.8125rem; color: var(--muted); margin-top: 0.5rem; }
</style>
