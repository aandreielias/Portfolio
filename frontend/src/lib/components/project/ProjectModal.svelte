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

  {#if p.arch}
    <h3>{p.arch.title}</h3>
    <div class="arch">
      {#each p.arch.layers as l}
        <section class="layer" class:accent={l.accent}>
          <h4>{l.name}</h4>
          <ul>{#each l.items as item}<li>{item}</li>{/each}</ul>
          {#if l.note}<p class="note">{l.note}</p>{/if}
        </section>
        {#if l.via}<p class="via">{l.via}</p>{/if}
      {/each}
    </div>
    <h3>{p.arch.flowTitle}</h3>
    <ol class="flow">{#each p.arch.flow as step}<li>{step}</li>{/each}</ol>
  {/if}

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
  h3 { margin-top: var(--s6); font-size: 15px; }

  /* Architecture: stacked layers joined by labelled connectors. */
  .arch { margin-top: var(--s3); }
  .layer { padding: var(--s3) var(--s4); background: var(--surface); border-radius: var(--r-md); box-shadow: inset 0 0 0 1px var(--border); }
  .layer.accent { background: color-mix(in srgb, var(--accent) 7%, var(--elevated)); box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--accent) 30%, transparent); }
  h4 { margin: 0; font-size: 13.5px; font-weight: 600; }
  .layer ul { display: flex; flex-wrap: wrap; gap: var(--s1); margin: var(--s2) 0 0; padding: 0; list-style: none; }
  .layer li { padding: 1px var(--s2); font-size: 12.5px; background: var(--elevated); border-radius: var(--r-sm); box-shadow: var(--shadow-raised); }
  .note { margin-top: var(--s2); font-size: 12.5px; color: var(--muted); }
  .via {
    position: relative;
    margin: 0;
    padding: var(--s2) 0 var(--s2) var(--s6);
    font-size: 12.5px;
    color: var(--muted);
  }
  .via::before { content: ""; position: absolute; left: var(--s5); top: 0; bottom: 0; border-left: 1.5px solid var(--border-strong); }

  .flow { max-width: 68ch; margin: var(--s3) 0 0; padding-left: var(--s5); color: #3d3f47; }
  .flow li + li { margin-top: var(--s2); }
  .flow li::marker { color: var(--muted); font-variant-numeric: tabular-nums; }

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
