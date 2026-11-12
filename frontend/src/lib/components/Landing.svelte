<script>
  import { email, github, name, projects } from "../../content.js";
  import { openImage } from "../stores/imageViewerStore.js";

  let { t, lang, index, onproject, langToggle } = $props();
  const base = import.meta.env.BASE_URL;
  const lines = name.toUpperCase().split(" ");
  const covers = { eventbus: "EventBus/architektur-{lang}.png", eroots: "ERoots/eroots-client-ui.png", portfolio: "Portfolio/landing.png" };
  let L = $derived(t.landing);
  const short = (title) => title.split(":").at(-1).trim();

  // Main project: screenshots first, diagrams last.
  const main = projects[0];
  let slides = $derived([...main.images.map((i) => ({ src: i.src, caption: i[lang] })), ...main[lang].diagrams]);
  let work;
  let shown = $state(0);
  let slide = $derived(slides[shown]);

  // Timeline in months since 01/2019; the top is the end of the current year, newest on top.
  const START = 2019;
  const year = new Date().getFullYear();
  const TOP = (year - START + 1) * 12;
  const years = Array.from({ length: year - START + 1 }, (_, i) => year - i);
  function month(d, end) {
    if (/laufend|present/.test(d)) return TOP;
    const [mm, yy] = d.includes("/") ? d.split("/").map(Number) : [end ? 12 : 1, Number(d)];
    return (yy - START) * 12 + mm - 1 + (end ? 1 : 0);
  }
  function range(date) {
    const [a, b = a] = date.split("–").map((x) => x.trim());
    return { from: month(a, false), to: month(b, true), open: /laufend|present/.test(b) };
  }
  const chapter = (id) => t.sections.find((s) => s.id === id);
  let rows = $derived(
    ["ausbildung", "erfahrung", "ehrenamt"].map((id) => ({
      id,
      title: chapter(id).title,
      items: chapter(id).entries.map((e) => ({ ...e, ...range(e.date), where: e.place.split(",")[0] })),
    })),
  );
  let others = $derived(index.filter((s) => !["ausbildung", "erfahrung", "ehrenamt", "kenntnisse"].includes(s.id)));
  let skills = $derived(chapter("kenntnisse"));
  // The first four rows are lists of tools (chips); the rest are sentences.
  const CHIPS = 4;

  // Sections rise in once as they enter; without the observer everything stays visible.
  // Contact bar shows once the hero has scrolled away.
  let pastHero = $state(false);
  function watchHero(node) {
    const io = new IntersectionObserver(([e]) => (pastHero = !e.isIntersecting));
    io.observe(node);
    return { destroy: () => io.disconnect() };
  }

  function reveal(node) {
    if (!("IntersectionObserver" in window)) return;
    node.classList.add("wait");
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) { node.classList.remove("wait"); io.disconnect(); }
    }, { threshold: 0.15 });
    io.observe(node);
    return { destroy: () => io.disconnect() };
  }
</script>

<div class="ground"><div class="page">
<header class="hero" use:watchHero>
  <div class="top">
    {@render langToggle()}
    <a class="cvbtn" href={base + t.cv.href} target="_blank" rel="noopener">{t.cv.label}</a>
  </div>
  <h1>
    <span class="sr">{name}</span>
    {#each ["over", "under"] as layer}
      <span class="copy {layer}" aria-hidden="true">
        {#each lines as l, n}<span class="line"><span style="--n:{n}">{l}</span></span>{/each}
      </span>
    {/each}
  </h1>
  <p class="who">{L.who}</p>
</header>

<section class="intro" use:reveal>
  <p class="statement">{L.intro}</p>
  <img class="portrait" src="{base}uploads/portrait.jpg" alt={name} width="600" height="800" />
</section>

<section class="work" bind:this={work} use:reveal>
  <h2>{L.work}</h2>
  <div class="main">
    <button class="big" onclick={() => openImage(base + slide.src, slide.caption)}>
      <img src={base + slide.src} alt={slide.caption} />
    </button>
    <div class="about">
      <h3>{main[lang].title}</h3>
      <p class="meta">{main.year} · {main.tech}</p>
      <p>{main[lang].summary}.</p>
      <p class="caption">{slide.caption}</p>
      <button class="btn primary" onclick={() => onproject(main.id)}>{t.ui.details}</button>
    </div>
  </div>
  <div class="thumbs">
    {#each slides as s, n}
      <button class:on={n === shown} onclick={() => (shown = n)} aria-label={s.caption} title={s.caption}>
        <img src={base + s.src} alt="" loading="lazy" />
      </button>
    {/each}
  </div>
</section>

<div class="trio">
  {#each projects.slice(1) as p, n}
    <button class="card" style="--i:{n}" use:reveal onclick={() => onproject(p.id)}>
      <span class="cover"><img src="{base}uploads/projects/{covers[p.id].replace('{lang}', lang)}" alt="" /></span>
      <span class="name">{short(p[lang].title)}</span>
      <span class="meta">{p.year}</span>
      <span class="sum">{p[lang].summary}</span>
    </button>
  {/each}
</div>

<section class="skills" use:reveal>
  <h2>{skills.title}</h2>
  <dl>
    {#each skills.rows as [label, value], i}
      <div>
        <dt>{label}</dt>
        <dd>{#if i < CHIPS}{#each value.split(", ") as v}<span class="chip">{v}</span>{/each}{:else}{value}{/if}</dd>
      </div>
    {/each}
  </dl>
</section>

<section class="cv" use:reveal>
  <h2>{L.cv}</h2>
  <div class="heads">
    {#each rows as r}<a href="#{r.id}">{r.title}</a>{/each}
  </div>
  <div class="tl" style="--top:{TOP}">
    <div class="col edu">
      {#each rows[0].items as e}
        <a class="block" class:open={e.open} href="#ausbildung" style="--a:{TOP - e.to}; --h:{e.to - e.from}">
          <strong>{e.where}</strong><span>{e.title}</span><span class="d">{e.date}</span>
        </a>
      {/each}
    </div>
    <div class="axis" aria-hidden="true">
      {#each years as y}<span style="--a:{TOP - (y - START + 1) * 12}">{y}</span>{/each}
    </div>
    <div class="col exp">
      {#each rows[1].items as e}
        <a class="block" href="#erfahrung" title={e.title} style="--a:{TOP - e.to}; --h:{e.to - e.from}">
          <strong>{e.where}</strong><span class="d">{e.date}</span>
        </a>
      {/each}
    </div>
    <div class="col vol">
      {#each rows[2].items.toSorted((a, b) => a.from - b.from) as e, n}
        <a class="rail" href="#ehrenamt" title={e.title} style="--a:{TOP - e.to}; --h:{e.to - e.from}; --lane:{n}"></a>
        <a class="tag" href="#ehrenamt" title={e.title} style="--a:{TOP - e.from}"><strong>{e.where}</strong><span class="d">{e.date}</span></a>
      {/each}
    </div>
  </div>
  <ul class="vol-list" aria-label={rows[2].title}>
    {#each rows[2].items as e}<li><a href="#ehrenamt"><strong>{e.where}</strong> {e.date}</a></li>{/each}
  </ul>
  <nav class="more" aria-label={t.ui.index}>
    {#each others as s}
      {#if s.id === "projekte"}<button class="btn" onclick={() => work.scrollIntoView({ behavior: "smooth" })}>{s.title}</button>
      {:else}<a class="btn" href="#{s.id}">{s.title}</a>{/if}
    {/each}
    <a class="btn primary" href={base + t.cv.href} target="_blank" rel="noopener">{t.cv.label}</a>
  </nav>
</section>

<section class="music" use:reveal>
  <h2>{L.music.title}</h2>
  <div class="split">
    <video controls preload="none" poster="{base}uploads/harfe/fantasia.jpg" src="{base}uploads/harfe/fantasia.mp4"></video>
    <div>
      <h3>{L.music.piece}</h3>
      <p class="meta">{L.music.by}</p>
      <p>{L.music.text}</p>
    </div>
  </div>
</section>

<footer class:on={pastHero}>
  <strong>{name}</strong>
  <a href="mailto:{email}">{email}</a>
  <a href={github} target="_blank" rel="noopener">GitHub</a>
</footer>
</div></div>

<style>
  /* Hero: white field over an accent field; the seam runs through the second line of the name. */
  /* Every part is a rounded panel of the same width on the grey page, like the section pages. */
  .page { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--s5); max-width: 1120px; margin: 0 auto; padding: var(--s5); }
  .ground { min-height: 100svh; background: var(--surface); }
  .hero, section { border-radius: var(--r-lg); background: var(--elevated); }

  .hero {
    --seam: 50%;
    position: relative;
    height: min(86svh, 760px);
    min-height: 480px;
    container-type: inline-size;
    display: grid;
    grid-template-rows: auto 1fr auto;
    padding: var(--s6);
    overflow: hidden;
  }
  .hero::before { content: ""; position: absolute; inset: var(--seam) 0 0; background: var(--accent); }
  .top { position: relative; display: flex; justify-content: space-between; align-items: center; }
  .cvbtn {
    padding: 10px var(--s4);
    font-weight: 600;
    color: #fff;
    text-decoration: none;
    background: var(--accent);
    border-radius: var(--r-sm);
    transition: background-color 120ms, translate 200ms var(--ease);
  }
  .cvbtn:hover { background: var(--accent-hover); translate: 0 -2px; }

  /* Name sits so the seam (hero 50%) crosses its second line at 75% of its height. */
  h1 {
    position: absolute;
    left: 0;
    right: 0;
    top: var(--seam);
    translate: 0 -75%;
    display: grid;
    font-family: "Source Serif 4", "Liberation Serif", "Times New Roman", serif;
    font-size: min(17cqi, 200px);
    font-weight: 900;
    line-height: 0.86;
    letter-spacing: -0.02em;
    text-align: center;
  }
  .sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
  .copy { grid-area: 1 / 1; display: flex; flex-direction: column; align-items: center; }
  .over { color: var(--accent); clip-path: inset(0 0 25% 0); }
  .under { color: #fff; clip-path: inset(75% 0 0 0); }
  .line { display: block; overflow: hidden; padding-inline: 0.05em; }
  .line span { display: block; animation: rise 1s var(--ease) both; animation-delay: calc(var(--n) * 90ms + 100ms); }

  .who {
    position: relative;
    grid-row: 3;
    max-width: 34ch;
    font-size: clamp(18px, 1.6vw, 22px);
    line-height: 1.45;
    color: #fff;
    background: var(--accent);
    animation: fade 0.8s 0.5s var(--ease) both;
  }

  section { padding: var(--s6); }
  section > * { transition: opacity 0.7s var(--ease), translate 0.7s var(--ease); }
  section > :nth-child(2) { transition-delay: 80ms; }
  section > :nth-child(3) { transition-delay: 160ms; }
  section:global(.wait) > * { opacity: 0; translate: 0 24px; }

  /* Intro continues the accent field. */
  .intro {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: center;
    gap: var(--s6);
    background: var(--accent);
    color: #fff;
  }
  .statement { max-width: 34ch; font-size: clamp(24px, 2.6vw, 36px); line-height: 1.3; font-weight: 500; letter-spacing: -0.02em; text-wrap: balance; }
  .portrait { width: clamp(140px, 16vw, 220px); height: auto; border-radius: var(--r-lg); }

  h2, h3, .name { font-family: "Source Serif 4", "Liberation Serif", serif; font-weight: 900; letter-spacing: -0.01em; }
  h2 { font-size: clamp(28px, 3vw, 40px); line-height: 1.1; margin-bottom: var(--s5); }
  .meta { font-size: 14px; color: var(--muted); }

  /* Main project: large picture, text beside it, all pictures as a strip below. */
  .main { display: grid; grid-template-columns: minmax(0, 1.7fr) minmax(0, 1fr); gap: var(--s6); align-items: start; }
  .big { display: block; width: 100%; aspect-ratio: 16 / 10; border-radius: var(--r-md); overflow: hidden; background: var(--surface); cursor: zoom-in; }
  .big img { width: 100%; height: 100%; object-fit: contain; }
  .about { display: flex; flex-direction: column; gap: var(--s3); align-items: start; font-size: 16px; }
  .about h3 { font-size: clamp(24px, 2.4vw, 32px); line-height: 1.15; }
  .caption { font-size: 14px; color: var(--muted); }
  .about .btn { margin-top: var(--s2); }
  .thumbs { display: flex; gap: var(--s2); margin-top: var(--s4); overflow-x: auto; padding-bottom: var(--s1); }
  .thumbs button { flex: 0 0 104px; height: 66px; border-radius: var(--r-sm); overflow: hidden; background: var(--surface); opacity: 0.55; outline: 2px solid transparent; outline-offset: -2px; transition: opacity 160ms, outline-color 160ms; }
  .thumbs button:hover { opacity: 1; }
  .thumbs button.on { opacity: 1; outline-color: var(--text); }
  .thumbs img { width: 100%; height: 100%; object-fit: cover; object-position: top left; }

  /* The other three projects as equal panels. */
  .trio { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--s5); }
  .card { display: flex; flex-direction: column; gap: var(--s1); padding: var(--s5); text-align: left; background: var(--elevated); border-radius: var(--r-lg); transition: opacity 0.7s var(--ease), translate 0.7s var(--ease); transition-delay: calc(var(--i) * 80ms); }
  .card:global(.wait) { opacity: 0; translate: 0 24px; }
  .cover { display: block; aspect-ratio: 16 / 10; margin-bottom: var(--s3); border-radius: var(--r-md); overflow: hidden; background: var(--surface); }
  .cover img { width: 100%; height: 100%; object-fit: cover; object-position: top left; transition: scale 500ms var(--ease); }
  .card:hover .cover img { scale: 1.03; }
  .name { font-size: 24px; line-height: 1.15; }
  .sum { margin-top: var(--s1); color: var(--text); }

  /* CV timeline: one axis, newest on top, block height = duration. */
  .cv { --m: 6px; }
  .heads, .tl { display: grid; grid-template-columns: minmax(0, 1fr) 64px minmax(0, 1fr) minmax(0, 1fr); column-gap: var(--s4); }
  .heads { margin-bottom: var(--s3); font-weight: 600; }
  .heads a { text-decoration: none; }
  .heads a:first-child { grid-column: 1; }
  .heads a:nth-child(2) { grid-column: 3; }
  .tl { height: calc(var(--m) * var(--top)); }
  .col, .axis { position: relative; }
  .axis::before { content: ""; position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; translate: -1px 0; background: var(--text); }
  .axis span { position: absolute; left: 50%; top: calc(var(--m) * var(--a)); height: calc(var(--m) * 12); translate: -50% 0; display: grid; place-items: center; font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums; }
  .axis span::after { content: ""; position: absolute; inset: auto -4px; height: 22px; z-index: -1; background: var(--elevated); }
  .axis span { z-index: 0; }
  .block {
    position: absolute;
    left: 0;
    right: 0;
    top: calc(var(--m) * var(--a));
    min-height: calc(var(--m) * var(--h) - 4px);
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: var(--s2) var(--s3);
    overflow: hidden;
    font-size: 14px;
    line-height: 1.3;
    color: #fff;
    text-decoration: none;
    background: var(--text);
    border-radius: var(--r-md);
    transition: background-color 160ms;
  }
  .block:hover { background: #000; }
  .block.open { border-top-left-radius: 0; border-top-right-radius: 0; }
  .block strong { font-weight: 600; }
  .block .d { color: rgba(255, 255, 255, 0.7); font-size: 13px; }
  .edu .block { padding: var(--s3) var(--s4); font-size: 15px; }
  .rail { position: absolute; left: calc(var(--lane) * 14px); top: calc(var(--m) * var(--a)); width: 8px; height: max(calc(var(--m) * var(--h)), 12px); background: var(--border-strong); border-radius: 4px; transition: background-color 160ms; }
  .rail:hover { background: var(--muted); }
  .tag { position: absolute; left: 52px; right: 0; top: max(calc(var(--m) * var(--a)), 40px); translate: 0 -100%; display: flex; flex-direction: column; font-size: 14px; line-height: 1.3; text-decoration: none; }
  .tag strong { font-weight: 600; }
  .tag .d { font-size: 13px; color: var(--muted); }
  .tag:hover strong { text-decoration: underline; }
  .vol-list { display: none; }
  .music .split { display: grid; grid-template-columns: minmax(0, 1.7fr) minmax(0, 1fr); gap: var(--s5); align-items: start; }
  .music video { display: block; width: 100%; aspect-ratio: 16 / 9; background: #000; border-radius: var(--r-md); }
  .music h3 { margin-bottom: var(--s1); }
  .music .meta { margin-bottom: var(--s3); }
  footer {
    position: fixed; z-index: 30; left: 0; right: 0; bottom: var(--s3); margin: 0 auto;
    width: min(1120px - 2 * var(--s5), 100% - 2 * var(--s3));
    display: flex; flex-wrap: wrap; align-items: center; gap: var(--s2) var(--s5);
    padding: var(--s3) var(--s5); font-size: 14px; color: #c9cad1;
    background: var(--accent); border-radius: var(--r-lg);
    opacity: 0; translate: 0 calc(100% + var(--s3)); visibility: hidden;
    transition: opacity 240ms var(--ease), translate 240ms var(--ease), visibility 0s 240ms;
  }
  footer.on { opacity: 1; translate: 0 0; visibility: visible; transition-delay: 0s; }
  footer strong { margin-right: auto; color: #fff; font-weight: 600; }
  footer a { text-decoration: none; }
  footer a:hover { color: #fff; }
  .page { padding-bottom: 96px; }
  .skills dl { margin: var(--s5) 0 0; }
  .skills dl div { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: var(--s5); padding: var(--s3) 0; }
  .skills dt { font-weight: 600; padding-top: 4px; }
  .skills dd { margin: 0; display: flex; flex-wrap: wrap; gap: var(--s2); align-items: center; }
  .chip { padding: 4px 10px; font-size: 14px; background: var(--surface); border-radius: var(--r-sm); }
  .more { display: flex; flex-wrap: wrap; gap: var(--s2); margin-top: var(--s6); }
  .more .btn:not(.primary) { background: var(--surface); box-shadow: none; }
  .more .btn:not(.primary):hover { background: var(--hover); }

  @media (max-width: 720px) {
    .music .split { grid-template-columns: minmax(0, 1fr); }
    .page { gap: var(--s3); padding: var(--s3) var(--s3) 88px; }
    footer { padding: var(--s3) var(--s4); gap: var(--s4); }
    footer strong { display: none; }
    .skills dl div { grid-template-columns: minmax(0, 1fr); gap: var(--s2); }
    .hero { --seam: 46%; padding: var(--s5); }
    h1 { font-size: 25cqi; }
    section { padding: var(--s5); }
    .intro { grid-template-columns: minmax(0, 1fr); }
    .main, .trio { grid-template-columns: minmax(0, 1fr); }
    .cv { --m: 9px; }
    .heads, .tl { grid-template-columns: minmax(0, 1fr) 40px minmax(0, 1fr) 44px; column-gap: var(--s2); }
    .heads a:nth-child(3) { display: none; }
    .tag { display: none; }
    .block, .edu .block { padding: var(--s2); font-size: 13px; hyphens: auto; }
    .block .d { font-size: 13px; }
    .edu .block span:not(.d) { display: none; }
    .vol-list { display: grid; gap: var(--s1); margin: var(--s4) 0 0; padding: 0; list-style: none; font-size: 14px; color: var(--muted); }
    .vol-list a { text-decoration: none; }
    .vol-list strong { color: var(--text); font-weight: 600; }
    .rail { left: calc(var(--lane) * 12px); }
  }

  @keyframes rise { from { translate: 0 105%; } }
  @keyframes fade { from { opacity: 0; translate: 0 12px; } }
  @media (prefers-reduced-motion: reduce) {
    .line span, .who { animation: none; }
    section > * { transition: none; }
    .card { transition: none; }
    section:global(.wait) > *, .card:global(.wait) { opacity: 1; translate: 0; }
  }
</style>
