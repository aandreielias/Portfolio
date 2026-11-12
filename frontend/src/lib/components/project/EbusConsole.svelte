<script>
  import { tick } from "svelte";
  import { createBus } from "../../ebus.js";

  let { lang } = $props();

  const text = {
    de: { intro: "Event-Bus im Browser, mit denselben Regeln wie die Java-Bibliothek. subscribe und publish stehen für Anwendungscode, ebus liest den Zustand wie das echte Werkzeug.", examples: "Beispiele", input: "Befehl eingeben" },
    en: { intro: "Event bus in the browser, with the same rules as the Java library. subscribe and publish stand for application code, ebus reads the state like the real tool.", examples: "Examples", input: "Enter a command" },
  };
  const examples = ["publish orders/eu/de ORD-1042", "ebus subscribers", "ebus channels", "ebus history", "publish members/joined anna", "publish orders/eu! x", "subscribe orders/eu MONITOR", "ebus info", "ebus help"];

  const bus = createBus();
  let lines = $state([]);
  let input = $state("");
  let past = [];
  let back = 0;
  let log;

  async function run(cmd) {
    cmd = cmd.trim();
    if (!cmd) return;
    lines.push({ cmd, out: bus.run(cmd) });
    past.push(cmd);
    back = 0;
    input = "";
    await tick();
    log.scrollTop = log.scrollHeight;
  }

  function key(e) {
    if (e.key === "Enter") run(input);
    else if (e.key === "ArrowUp" && back < past.length) input = past[past.length - ++back];
    else if (e.key === "ArrowDown" && back > 0) input = --back ? past[past.length - back] : "";
    else return;
    e.preventDefault();
  }

  run("subscribe orders HIGH");
  run("subscribe orders/eu");
</script>

<div class="console">
  <p class="intro">{text[lang].intro}</p>
  <div class="log" bind:this={log}>
    {#each lines as l}
      <code class="cmd">$ {l.cmd}</code>
      <pre>{l.out}</pre>
    {/each}
    <label class="prompt">
      <span>$</span>
      <input bind:value={input} onkeydown={key} aria-label={text[lang].input} placeholder={text[lang].input} spellcheck="false" autocomplete="off" />
    </label>
  </div>
  <p class="label">{text[lang].examples}</p>
  <div class="examples">
    {#each examples as ex}<button onclick={() => run(ex)}><code>{ex}</code></button>{/each}
  </div>
</div>

<style>
  .console { display: flex; flex-direction: column; gap: var(--s3); min-height: 0; }
  .intro { font-size: 13px; color: var(--muted); }
  .log {
    height: 360px;
    overflow: auto;
    padding: var(--s3) var(--s4);
    font: 12px/1.55 var(--mono);
    background: var(--surface);
    border-radius: var(--r-md);
    box-shadow: inset 0 0 0 1px var(--border);
  }
  .cmd { display: block; font: inherit; color: var(--muted); }
  .cmd:not(:first-child) { margin-top: var(--s2); }
  pre { margin: 0; font: inherit; white-space: pre; color: var(--text); }
  .prompt { display: flex; gap: var(--s2); margin-top: var(--s2); color: var(--muted); }
  input { flex: 1; min-width: 0; font: inherit; color: var(--text); background: none; border: 0; outline: 0; }
  .label { font-size: 12px; font-weight: 600; color: var(--muted); }
  .examples { display: flex; flex-wrap: wrap; gap: var(--s1); }
  .examples code { font: inherit; }
  .examples button {
    padding: 2px var(--s2);
    font: 11.5px var(--mono);
    color: var(--text);
    background: var(--elevated);
    border-radius: var(--r-sm);
    box-shadow: var(--shadow-raised);
  }
  .examples button:hover { background: var(--surface); }
</style>
