<script>
  import { name, projects } from "../../content.js";

  let { section, t, lang, onproject } = $props();
  const base = import.meta.env.BASE_URL;
</script>

{#if section.kind === "profile"}
  <div class="profile">
    <img src="{base}uploads/portrait.jpg" alt={name} width="600" height="800" />
    <p>{t.profile.summary}</p>
  </div>
  <dl>
    {#each t.profile.rows as [label, value]}
      <div><dt>{label}</dt><dd>{value}</dd></div>
    {/each}
  </dl>
{:else if section.rows}
  <dl>
    {#each section.rows as [label, value]}
      <div><dt>{label}</dt><dd>{value}</dd></div>
    {/each}
  </dl>
{:else}
  {#each section.entries as e}
    <div class="entry">
      <span class="date">{e.date}</span>
      <div>
        <p class="place">{e.place}</p>
        <h3>{e.title}</h3>
        {#each e.text ?? [] as line}<p class="text">{line}</p>{/each}
        {#if e.tech}<p class="tech"><span>{e.techLabel ?? t.ui.technologies}</span> {e.tech}</p>{/if}
        {#if e.project}
          {@const p = projects.find((x) => x.id === e.project)}
          <button class="btn" onclick={() => onproject(p.id)}>{p[lang].title}</button>
        {/if}
      </div>
    </div>
  {/each}
{/if}

<style>
  /* Rows, not cards: one panel, hairlines between entries. */
  .entry {
    display: grid;
    grid-template-columns: 136px minmax(0, 1fr);
    gap: var(--s5);
    padding: var(--s5) 0;
  }
  .entry:first-child { padding-top: 0; }
  .entry:last-child { padding-bottom: 0; }
  .entry + .entry { border-top: 1px solid var(--border); }

  .date { font-size: 13.5px; color: var(--muted); font-variant-numeric: tabular-nums; padding-top: 2px; }
  .place { font-size: 13.5px; color: var(--muted); margin-bottom: 2px; }
  h3 { font-size: 16px; }
  .text { margin-top: var(--s2); color: #3d3f47; }
  .tech { margin-top: var(--s3); font-size: 13.5px; color: var(--muted); }
  .tech span { font-weight: 600; color: var(--text); }
  .btn { margin-top: var(--s4); }

  .profile {
    display: grid;
    grid-template-columns: 136px minmax(0, 1fr);
    gap: var(--s5);
    align-items: start;
    padding-bottom: var(--s5);
    border-bottom: 1px solid var(--border);
  }
  .profile img { width: 100%; height: auto; display: block; border-radius: var(--r-md); }
  .profile p { font-size: 16px; line-height: 1.65; }

  dl { margin: 0; }
  dl div {
    display: grid;
    grid-template-columns: 136px minmax(0, 1fr);
    gap: var(--s5);
    padding: var(--s3) 0;
  }
  dl div + div { border-top: 1px solid var(--border); }
  dt { font-size: 13.5px; color: var(--muted); padding-top: 1px; }
  dd { margin: 0; }

  @media (max-width: 720px) {
    .entry, dl div { grid-template-columns: minmax(0, 1fr); gap: var(--s1); }
    .profile { grid-template-columns: 96px minmax(0, 1fr); gap: var(--s4); }
    .profile p { font-size: 15px; }
  }
</style>
