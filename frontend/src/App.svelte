<script>
  import { fade, fly } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import { name, projects, text } from "./content.js";
  import { lang, setLang } from "./lib/lang.svelte.js";
  import { imageViewerStore, closeImage } from "./lib/stores/imageViewerStore.js";
  import Section from "./lib/components/Section.svelte";
  import ProjectModal from "./lib/components/project/ProjectModal.svelte";
  import ImageViewer from "./lib/components/common/ImageViewer.svelte";

  const base = import.meta.env.BASE_URL;

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

{#snippet langToggle()}
  <div class="lang" role="group" aria-label="Language">
    {#each ["de", "en"] as l}
      <button aria-pressed={lang.current === l} onclick={() => setLang(l)}>{l.toUpperCase()}</button>
    {/each}
  </div>
{/snippet}

{#if !section}
  <div class="landing">
    <div class="corner">{@render langToggle()}</div>
    <main class="hero" class:pinned>
      <h1>
        <button aria-expanded={pinned} aria-controls="index" onclick={() => (pinned = !pinned)}>{name}</button>
      </h1>
      <nav id="index" aria-label={t.ui.index}>
        {#each index as s}<a href="#{s.id}">{s.title}</a>{/each}
        <a class="btn primary" href={base + t.cv.href} target="_blank" rel="noopener">{t.cv.label}</a>
      </nav>
    </main>
  </div>
{:else}
  <div class="app" in:fade={{ duration: 200 }}>
    <aside class="side">
      <button class="name" onclick={home} title={t.ui.back}>{name}</button>
      {@render langToggle()}
      <nav aria-label={t.ui.index}>
        {#each index as s}
          <a href="#{s.id}" aria-current={s.id === current ? "page" : undefined}>{s.title}</a>
        {/each}
      </nav>
      <a class="btn primary cv" href={base + t.cv.href} target="_blank" rel="noopener">{t.cv.label}</a>
    </aside>

    <main class="content">
      {#key section.id}
        <article class="panel" in:fly={{ y: 8, duration: 280, easing: cubicOut }}>
          <h2>{section.title}</h2>
          <Section {section} {t} lang={lang.current} onproject={(id) => (projectId = id)} />
        </article>
      {/key}
    </main>
  </div>
{/if}

{#if project}
  <ProjectModal {project} {t} lang={lang.current} onclose={() => (projectId = null)} />
{/if}
<ImageViewer />

<style>
  /* Language switch: segmented control as in the club software. */
  .lang {
    display: inline-flex;
    gap: 2px;
    padding: 2px;
    background: var(--border);
    border-radius: var(--r-sm);
  }
  .lang button {
    padding: 2px var(--s2);
    font-size: 12.5px;
    font-weight: 500;
    color: var(--muted);
    border-radius: 4px;
  }
  .lang button[aria-pressed="true"] { background: var(--elevated); color: var(--text); box-shadow: var(--shadow-raised); }

  /* Landing: only the name. The chapters appear together on hover, focus or tap. */
  .landing {
    min-height: 100vh;
    min-height: 100dvh;
    display: grid;
    place-items: center;
    padding: var(--s6) var(--s4);
  }
  .corner { position: fixed; top: var(--s4); right: var(--s4); }

  .hero { max-width: 100%; }
  h1 {
    font-size: clamp(48px, 10vw, 120px);
    font-weight: 600;
    line-height: 1;
    letter-spacing: -0.045em;
    animation: enter 0.8s var(--ease) both;
  }
  h1 button { text-align: left; border-radius: var(--r-md); }

  #index {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: var(--s1);
    margin: var(--s5) 0 0 calc(-1 * var(--s3));
    opacity: 0;
    visibility: hidden;
    translate: 0 6px;
    transition: opacity 240ms var(--ease), translate 240ms var(--ease), visibility 0s 240ms;
  }
  .hero:hover #index, .hero:focus-within #index, .hero.pinned #index {
    opacity: 1;
    visibility: visible;
    translate: 0;
    transition-delay: 0s;
  }
  #index a:not(.btn) {
    padding: 5px var(--s3);
    font-size: 15px;
    font-weight: 500;
    color: var(--muted);
    text-decoration: none;
    border-radius: var(--r-sm);
    transition: background-color 120ms, color 120ms;
  }
  #index a:not(.btn):hover { background: var(--hover); color: var(--text); }
  #index .btn { margin-left: var(--s2); }

  /* Section view: sidebar and one panel, like the club software. */
  .app {
    display: grid;
    grid-template-columns: 232px minmax(0, 1fr);
    min-height: 100vh;
    min-height: 100dvh;
  }
  .side {
    position: sticky;
    top: 0;
    height: 100vh;
    height: 100dvh;
    display: grid;
    grid-template: "name lang" auto "nav nav" auto "cv cv" 1fr / 1fr auto;
    align-items: center;
    gap: var(--s5) var(--s2);
    padding: var(--s5) var(--s4);
    background: var(--surface);
    border-right: 1px solid var(--border);
  }
  .name { grid-area: name; justify-self: start; padding: 2px var(--s2); font-weight: 600; letter-spacing: -0.015em; border-radius: var(--r-sm); }
  .name:hover { background: var(--hover); }
  .side .lang { grid-area: lang; }
  .side nav { grid-area: nav; display: flex; flex-direction: column; gap: 2px; align-self: start; }
  .side nav a {
    padding: 5px var(--s2);
    font-size: 14px;
    font-weight: 500;
    color: var(--muted);
    text-decoration: none;
    border-radius: var(--r-sm);
    transition: background-color 120ms, color 120ms;
  }
  .side nav a:hover { background: var(--hover); color: var(--text); }
  .side nav a[aria-current] { background: var(--elevated); color: var(--text); box-shadow: var(--shadow-raised); }
  .cv { grid-area: cv; align-self: end; justify-self: start; }

  .content { padding: var(--s5); }
  .panel {
    max-width: 800px;
    margin: 0 auto;
    padding: var(--s6);
    background: var(--elevated);
    border-radius: var(--r-lg);
    box-shadow: var(--shadow-raised);
  }
  .panel h2 { font-size: 22px; margin-bottom: var(--s5); }

  @media (max-width: 720px) {
    .app { grid-template: auto 1fr / minmax(0, 1fr); }
    .side {
      z-index: 10;
      height: auto;
      grid-template: "name cv lang" auto "nav nav nav" auto / 1fr auto auto;
      gap: var(--s3) var(--s2);
      padding: var(--s3) var(--s4) var(--s2);
      border-right: 0;
      border-bottom: 1px solid var(--border);
    }
    .side nav {
      flex-direction: row;
      overflow-x: auto;
      margin: 0 calc(-1 * var(--s4));
      padding: 0 var(--s4) var(--s1);
      scrollbar-width: none;
    }
    .side nav a { white-space: nowrap; }
    .cv { align-self: center; }
    .content { padding: var(--s3); }
    .panel { padding: var(--s5) var(--s4); }
  }

  @keyframes enter { from { opacity: 0; translate: 0 12px; } }
</style>
