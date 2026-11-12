// In-browser copy of the EventBus rules (validation, hierarchical routing, priorities, dead letter)
// plus the read side of the ebus CLI, with the same table format as ae.eventbus.cli.TextTable.
const PRIORITY = { HIGHEST: 100, HIGH: 75, NORMAL: 50, LOW: 25, MONITOR: 0 };
const SEGMENT = /^[a-zA-Z0-9_\-.]+$/;
const MAX_DEPTH = 16;

const pad = (n) => String(n).padStart(2, "0");
const stamp = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
// shortcut: 8 hex chars instead of a full UUID, so tables fit the panel
const id = () => crypto.getRandomValues(new Uint32Array(1))[0].toString(16).padStart(8, "0");
const within = (channel, parent) => channel === parent || channel.startsWith(parent + "/");

function table(headers, rows) {
  if (!rows.length) return "(none)";
  const cells = rows.map((r) => r.map((c) => (c == null ? "-" : String(c))));
  const widths = headers.map((h, i) => Math.max(h.length, ...cells.map((r) => r[i].length)));
  const line = (r) => r.map((c, i) => (i === r.length - 1 ? c : c.padEnd(widths[i]))).join("  ");
  return [line(headers), ...cells.map(line)].join("\n");
}

function validate(channel) {
  const segments = channel.split("/");
  if (segments.length > MAX_DEPTH) throw new Error(`Channel depth ${segments.length} exceeds maximum allowed depth of ${MAX_DEPTH}: ${channel}`);
  const bad = segments.find((s) => !SEGMENT.test(s));
  if (bad !== undefined) throw new Error(`Channel segment '${bad}' in channel '${channel}' contains illegal characters. Only alphanumeric, dashes, dots, and underscores are allowed, and never the separator '/'.`);
}

export function createBus() {
  const subs = [];
  const channels = new Map(); // name -> { publications, lastFired }
  const history = [];
  let seq = 0;

  const known = (c) => channels.has(c) || channels.set(c, { publications: 0, lastFired: null });

  function subscribe(channel, priority = "NORMAL") {
    priority = priority.toUpperCase();
    if (!(priority in PRIORITY)) return `Unknown priority '${priority}'. Use ${Object.keys(PRIORITY).join(", ")}.`;
    validate(channel);
    known(channel);
    const s = { id: id(), channel, priority, delivered: 0, failed: 0, since: new Date() };
    subs.push(s);
    return `Subscribed ${s.id} to ${channel} (${priority}, SYNCHRONOUS, hierarchical).`;
  }

  function publish(channel, payload) {
    validate(channel);
    known(channel);
    const matched = subs.filter((s) => within(channel, s.channel)).sort((a, b) => PRIORITY[b.priority] - PRIORITY[a.priority]);
    const info = channels.get(channel);
    info.publications++;
    info.lastFired = new Date();
    history.push({ seq: ++seq, time: info.lastFired, channel, recipients: matched.length, id: id() });
    if (history.length > 1000) history.shift();
    if (!matched.length) return `No subscriber for ${channel}: the dead-letter handler received "${payload}".`;
    return matched.map((s, i) => {
      s.delivered++;
      return `${i + 1}. ${s.id}  ${s.channel}  (${s.priority} ${PRIORITY[s.priority]})  received "${payload}"`;
    }).join("\n");
  }

  function ebus(args) {
    const [cmd, ...rest] = args;
    switch (cmd) {
      case "info":
        return [
          "Bus:            demo",
          "Access:         READ_WRITE",
          "State:          OPEN",
          "Separator:      /",
          `Channels:       ${channels.size}`,
          `Subscribers:    ${subs.length}`,
          `Publications:   ${[...channels.values()].reduce((n, c) => n + c.publications, 0)}`,
          `History:        ${history.length} records (last seq ${history.at(-1)?.seq ?? 0})`,
        ].join("\n");
      case "channels":
        return table(["CHANNEL", "SUBSCRIBERS", "PUBLICATIONS", "LAST FIRED"],
          [...channels].sort(([a], [b]) => a.localeCompare(b)).map(([c, i]) => [c, subs.filter((s) => s.channel === c).length, i.publications, i.lastFired && stamp(i.lastFired)]));
      case "subscribers":
        return table(["ID", "CHANNEL", "PRIORITY", "DELIVERED", "FAILED"],
          subs.filter((s) => !rest[0] || s.channel === rest[0]).map((s) => [s.id, s.channel, s.priority, s.delivered, s.failed]));
      case "history": {
        let n = 20, ch;
        for (let i = 0; i < rest.length; i++) {
          if (rest[i] === "-n") {
            n = Number(rest[++i]);
            if (!(n > 0)) return `Option -n needs a positive number, got '${rest[i] ?? ""}'.`;
          } else ch = rest[i];
        }
        return table(["SEQ", "TIME", "CHANNEL", "RECIPIENTS"],
          history.filter((e) => !ch || within(e.channel, ch)).slice(-n).map((e) => [e.seq, stamp(e.time), e.channel, e.recipients]));
      }
      case "unsubscribe": {
        if (!rest[0]) return "Usage: unsubscribe <subscription-id>";
        const i = subs.findIndex((s) => s.id === rest[0]);
        if (i < 0) return `No live subscription with id ${rest[0]}.`;
        subs.splice(i, 1);
        return `Subscription ${rest[0]} ended.`;
      }
      case "clear-history":
        history.length = 0;
        return "History cleared.";
      case "help":
      case undefined:
        return table(["COMMAND", "DESCRIPTION"], [
          ["info", "Show bus summary and configuration"],
          ["channels", "List channels with subscriber and publication counts"],
          ["subscribers [channel]", "List live subscribers, optionally of one channel"],
          ["history [-n <count>] [channel]", "Show recent publications (channel includes descendants)"],
          ["unsubscribe <subscription-id>", "End a subscription (needs READ_WRITE access)"],
          ["clear-history", "Clear the publication history (needs READ_WRITE access)"],
        ]);
      default:
        return `Unknown command '${cmd}'. Type 'help' for the list of commands.`;
    }
  }

  // One input line -> output text. Errors from the bus are shown as the exception the caller would get.
  function run(line) {
    const [cmd, ...args] = line.trim().split(/\s+/);
    try {
      if (cmd === "subscribe") return args[0] ? subscribe(args[0], args[1]) : "Usage: subscribe <channel> [HIGHEST|HIGH|NORMAL|LOW|MONITOR]";
      if (cmd === "publish") return args[0] ? publish(args[0], args.slice(1).join(" ") || "hello") : "Usage: publish <channel> <message>";
      if (cmd === "ebus") return ebus(args);
      return `Unknown command '${cmd}'. Use subscribe, publish or ebus <command>.`;
    } catch (e) {
      return `ValidationException: ${e.message}`;
    }
  }

  return { run };
}
