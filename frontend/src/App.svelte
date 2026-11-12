<script>
  import { fade, fly } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import { name, projects, text } from "./content.js";
  import { lang, setLang } from "./lib/lang.svelte.js";
  import { imageViewerStore, closeImage } from "./lib/stores/imageViewerStore.js";
  import Section from "./lib/components/Section.svelte";
  import Modal from "./lib/components/common/Modal.svelte";
  import Landing from "./lib/components/Landing.svelte";
  import ProjectModal from "./lib/components/project/ProjectModal.svelte";
  import ImageViewer from "./lib/components/common/ImageViewer.svelte";

  let t = $derived(text[lang.current]);
  let index = $derived([{ id: "profil", title: t.profile.title, kind: "profile" }, ...t.sections]);
  let current = $state(location.hash.slice(1));
  let section = $derived(index.find((s) => s.id === current && s.kind !== "projects"));
  let projectId = $state(null);
  let project = $derived(projects.find((p) => p.id === projectId));

  $effect(() => setLang(lang.current));
  $effect(() => {
    document.title = section ? `${section.title} · ${name}` : name;
  });

  function home() {
    history.pushState(null, "", location.pathname);
    current = "";
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

<Landing {t} lang={lang.current} {index} {langToggle} onproject={(id) => (projectId = id)} />

{#if section}
  <Modal title={section.title} onclose={home} labels={t.ui}>
    <Section {section} {t} lang={lang.current} onproject={(id) => (projectId = id)} />
  </Modal>
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

</style>
