<script>
  import { email, github, name, projects } from "../../content.js";

  let { section, t, lang, onproject } = $props();
  const base = import.meta.env.BASE_URL;
</script>

{#if section.kind === "profile"}
  <div class="profile item">
    <img src="{base}uploads/portrait.jpg" alt={name} width="600" height="800" />
    <p>{t.profile.summary}</p>
  </div>
  <dl>
    {#each t.profile.rows as [label, value], i}
      <div class="item" style="--i:{i + 1}"><dt>{label}</dt><dd>{value}</dd></div>
    {/each}
  </dl>
{:else if section.kind === "projects"}
  {#each projects as p, i}
    <div class="entry item" style="--i:{i}">
      <span class="date">{p.year}</span>
      <div>
        <button class="title link" onclick={() => onproject(p.id)}>{p[lang].title}</button>
        <p class="text">{p[lang].summary}</p>
        <p class="tech">{t.ui.technologies}: {p.tech}</p>
        <button class="more" onclick={() => onproject(p.id)}>{t.ui.details} →</button>
      </div>
    </div>
  {/each}
{:else if section.kind === "contact"}
  <dl>
    <div class="item"><dt>E-Mail</dt><dd><a href="mailto:{email}">{email}</a></dd></div>
    <div class="item" style="--i:1"><dt>GitHub</dt><dd><a href={github} target="_blank" rel="noopener">github.com/aandreielias</a></dd></div>
    <div class="item" style="--i:2"><dt>PDF</dt><dd><a href={base + t.cv.href} target="_blank" rel="noopener">{t.cv.label}</a></dd></div>
  </dl>
{:else if section.rows}
  <dl>
    {#each section.rows as [label, value], i}
      <div class="item" style="--i:{i}"><dt>{label}</dt><dd>{value}</dd></div>
    {/each}
  </dl>
{:else}
  {#each section.entries as e, i}
    <div class="entry item" style="--i:{i}">
      <span class="date">{e.date}</span>
      <div>
        <p>{e.place}</p>
        <h3>{e.title}</h3>
        {#each e.text ?? [] as line}<p class="text">{line}</p>{/each}
        {#if e.tech}<p class="tech">{e.techLabel ?? t.ui.technologies}: {e.tech}</p>{/if}
        {#if e.project}
          {@const p = projects.find((x) => x.id === e.project)}
          <button class="more" onclick={() => onproject(p.id)}>{p[lang].title} →</button>
        {/if}
      </div>
    </div>
  {/each}
{/if}

<style>
  .item { animation: rise 0.7s calc(0.15s + var(--i, 0) * 70ms) var(--ease) both; }

  .entry {
    display: grid;
    grid-template-columns: 9.5rem 1fr;
    gap: 0 1.5rem;
    padding: 1.1rem 0;
  }
  .entry + .entry { border-top: 1px solid var(--rule); }
  .date { font-size: 0.875rem; padding-top: 0.2rem; }
  h3 { font-size: 1.125rem; font-weight: 700; line-height: 1.35; }
  .title { font-size: 1.25rem; text-align: left; line-height: 1.35; }
  .title:hover { text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 0.2em; }
  .text { font-size: 0.9375rem; margin-top: 0.5rem; }
  .tech { font-size: 0.9375rem; font-weight: 700; margin-top: 0.6rem; }
  .more { margin-top: 0.7rem; font-size: 0.9375rem; color: var(--link); }
  .more:hover { text-decoration: underline; text-underline-offset: 0.2em; }

  .profile { display: grid; grid-template-columns: 8.5rem 1fr; gap: 1.75rem; align-items: start; margin-bottom: 1.75rem; }
  .profile img { width: 100%; height: auto; display: block; }
  .profile p { font-size: 1.125rem; }

  dl { margin: 0; }
  dl div { display: grid; grid-template-columns: 11rem 1fr; gap: 0 1.5rem; padding: 0.65rem 0; }
  dl div + div { border-top: 1px solid var(--rule); }
  dt { font-size: 0.875rem; padding-top: 0.15rem; }
  dd { margin: 0; }

  @media (max-width: 640px) {
    .entry, dl div { grid-template-columns: 1fr; }
    .date, dt { color: var(--muted); }
    .profile { grid-template-columns: 6rem 1fr; gap: 1rem; }
    .profile p { font-size: 1rem; }
  }

  @keyframes rise { from { opacity: 0; transform: translateY(0.75rem); } }
</style>
