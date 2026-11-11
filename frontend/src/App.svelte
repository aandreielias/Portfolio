<script>
  import { fly } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import { name, projects, text } from "./content.js";
  import { lang, setLang } from "./lib/lang.svelte.js";
  import { imageViewerStore, closeImage } from "./lib/stores/imageViewerStore.js";
  import Section from "./lib/components/Section.svelte";
  import ProjectModal from "./lib/components/project/ProjectModal.svelte";
  import ImageViewer from "./lib/components/common/ImageViewer.svelte";

  const base = import.meta.env.BASE_URL;
  const roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"];

  let t = $derived(text[lang.current]);
  let index = $derived([{ id: "profil", title: t.profile.title, kind: "profile" }, ...t.sections]);
  let current = $state(location.hash.slice(1));
  let section = $derived(index.find((s) => s.id === current));
  let pinned = $state(false);
  let projectId = $state(null);
  let project = $derived(projects.find((p) => p.id === projectId));

  $effect(() => setLang(lang.current));
  $effect(() => {
    document.title = section ? `${section.title} · ${name}` : name;
  });
  $effect(() => {
    current;
    window.scrollTo(0, 0);
  });

  function home() {
    history.pushState(null, "", location.pathname);
    current = "";
    pinned = false;
  }

  // One Esc handler for every layer, so a single press closes only the topmost one.
  function onkeydown(e) {
    if (e.key !== "Escape") return;
    if ($imageViewerStore.isOpen) closeImage();
    else if (project) projectId = null;
    else if (section) home();
  }
</script>

<svelte:window onhashchange={() => (current = location.hash.slice(1))} {onkeydown} />

<div class="desk" class:open={section}>
  <div class="lang" role="group" aria-label="Language">
    {#each ["de", "en"] as l}
      <button aria-pressed={lang.current === l} onclick={() => setLang(l)}>{l.toUpperCase()}</button>
    {/each}
  </div>

  <main class="hero" class:pinned inert={section ? true : undefined}>
    <h1>
      <button aria-expanded={pinned} aria-controls="index" aria-label={name} onclick={() => (pinned = !pinned)}>
        {#each name as ch, i}<span style="--i:{i}" aria-hidden="true">{ch}</span>{/each}<span class="caret" aria-hidden="true"></span>
      </button>
    </h1>
    <span class="rule" aria-hidden="true"></span>
    <nav aria-label={t.ui.index}>
      <ol id="index">
        {#each index as s, i}
          <li style="--i:{i}"><a href="#{s.id}"><span class="num">{roman[i]}</span>{s.title}</a></li>
        {/each}
        <li style="--i:{index.length}">
          <a href={base + t.cv.href} target="_blank" rel="noopener"><span class="num">↗</span>{t.cv.label}</a>
        </li>
      </ol>
    </nav>
  </main>

  {#if section}
    <header class="bar" in:fly={{ y: -16, duration: 400 }}>
      <button class="mini" onclick={home} title={t.ui.back}>{name}</button>
      <nav aria-label={t.ui.index}>
        {#each index as s}
          <a href="#{s.id}" aria-current={s.id === current ? "page" : undefined}>{s.title}</a>
        {/each}
      </nav>
    </header>

    {#key section.id}
      <article class="sheet" in:fly={{ y: 80, duration: 700, easing: cubicOut }}>
        <h2>{section.title}</h2>
        <Section {section} {t} lang={lang.current} onproject={(id) => (projectId = id)} />
        <footer>
          <span>{name}</span>
          <a href={base + t.cv.href} target="_blank" rel="noopener">{t.cv.label}</a>
        </footer>
      </article>
    {/key}
  {/if}
</div>

{#if project}
  <ProjectModal {project} {t} lang={lang.current} onclose={() => (projectId = null)} />
{/if}
<ImageViewer />

<style>
  .desk {
    min-height: 100vh;
    min-height: 100dvh;
    transition: background-color 0.6s var(--ease);
  }
  .desk.open { background: #eeebe5; }

  .lang {
    position: fixed;
    top: 1.25rem;
    right: 1.25rem;
    z-index: 20;
    display: flex;
    gap: 0.25rem;
    font-size: 0.8125rem;
    letter-spacing: 0.06em;
  }
  .lang button { padding: 0.25rem 0.35rem; color: var(--muted); }
  .lang button[aria-pressed="true"] { color: var(--ink); text-decoration: underline; text-underline-offset: 0.3em; }

  /* Landing: only the name. The index typesets out on hover, focus or tap. */
  .hero {
    position: fixed;
    inset: 0;
    display: grid;
    place-content: center;
    justify-items: start;
    padding: 0 1rem;
    pointer-events: none; /* only the name, rule and index react to hover, not the whole page */
    transition: opacity 0.5s var(--ease), transform 0.6s var(--ease);
  }
  .desk.open .hero { opacity: 0; transform: translateY(-3rem); pointer-events: none; }

  /* Printer's crop marks: the landing page is a blank sheet. */
  .hero::before, .hero::after {
    content: "";
    position: absolute;
    width: 1.5rem;
    height: 1.5rem;
    border: solid var(--rule);
    pointer-events: none;
    animation: fade 1.2s 1.2s both;
  }
  .hero::before { top: 2.5rem; left: 2.5rem; border-width: 1px 0 0 1px; }
  .hero::after { bottom: 2.5rem; right: 2.5rem; border-width: 0 1px 1px 0; }

  .hero > * { pointer-events: auto; }
  h1 button { text-align: left; }
  h1 {
    font-size: clamp(2.75rem, 10vw, 7.5rem);
    font-weight: 400;
    line-height: 1;
    letter-spacing: -0.02em;
    white-space: nowrap;
  }
  h1 span:not(.caret) {
    display: inline-block;
    white-space: pre;
    animation: rise 0.9s calc(var(--i) * 45ms) var(--ease) both;
  }
  .caret {
    display: inline-block;
    width: 0.06em;
    height: 0.8em;
    margin-left: 0.08em;
    background: var(--ink);
    vertical-align: -0.02em;
    animation: blink 1.1s 1s steps(1) infinite;
  }
  .hero:hover .caret, .hero:focus-within .caret, .hero.pinned .caret { animation: none; opacity: 0; }

  .rule {
    display: block;
    width: 100%;
    height: 1px;
    box-sizing: content-box;
    padding: 1.25rem 0 1.5rem; /* padding, not margin: keeps hover alive between name and index */
    background: var(--ink) content-box;
    transform-origin: left;
    animation: draw 1s 0.6s var(--ease) both;
  }

  ol { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.35rem; min-height: 15rem; }
  li {
    clip-path: inset(0 100% 0 0);
    transition: clip-path 0.45s steps(14) calc(var(--i) * 60ms);
  }
  .hero:hover li, .hero:focus-within li, .hero.pinned li { clip-path: inset(0 0 0 0); }
  ol a {
    display: inline-flex;
    gap: 1rem;
    font-size: 1.375rem;
    color: var(--ink);
    text-decoration: none;
  }
  ol a:hover { text-decoration: underline; text-decoration-thickness: 1px; }
  .num { width: 2.25rem; color: var(--muted); font-size: 0.875rem; padding-top: 0.45rem; }

  /* Section view */
  .bar {
    position: sticky;
    top: 0;
    z-index: 10;
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.5rem 1.75rem;
    padding: 1.1rem 5.5rem 0.9rem 1.5rem;
    background: color-mix(in srgb, #eeebe5 88%, transparent);
    backdrop-filter: blur(6px);
  }
  .mini { font-size: 1.25rem; }
  .mini:hover { text-decoration: underline; text-underline-offset: 0.2em; }
  .bar nav { display: flex; flex-wrap: wrap; gap: 0.25rem 1.1rem; font-size: 0.9375rem; }
  .bar nav a { color: var(--muted); text-decoration: none; }
  .bar nav a:hover, .bar nav a[aria-current] { color: var(--ink); }
  .bar nav a[aria-current] { text-decoration: underline; text-underline-offset: 0.3em; }

  .sheet {
    max-width: 52rem;
    margin: 1.5rem auto 4rem;
    padding: clamp(1.5rem, 6vw, 4.5rem) clamp(1rem, 7vw, 5rem) 2rem;
    background: var(--paper);
    box-shadow: 0 1px 2px rgb(0 0 0 / 0.06), 0 12px 40px -12px rgb(0 0 0 / 0.18);
  }
  .sheet h2 { font-size: 1.75rem; font-weight: 700; margin-bottom: 1.75rem; }
  .sheet footer {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-top: 3.5rem;
    font-size: 0.8125rem;
    color: var(--muted);
  }
  .sheet footer a { color: inherit; }

  @media (max-width: 640px) {
    .bar { padding: 0.9rem 4.5rem 0.75rem 1rem; }
    .sheet { margin: 0 0 2rem; }
    .hero::before { top: 1.25rem; left: 1.25rem; }
    .hero::after { bottom: 1.25rem; right: 1.25rem; }
  }

  @keyframes rise { from { opacity: 0; transform: translateY(0.35em); } }
  @keyframes draw { from { transform: scaleX(0); } }
  @keyframes fade { from { opacity: 0; } }
  @keyframes blink { 50% { opacity: 0; } }
</style>
