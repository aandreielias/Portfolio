function initial() {
  try {
    const saved = localStorage.getItem("lang");
    if (saved === "de" || saved === "en") return saved;
  } catch {}
  return navigator.language?.startsWith("de") ? "de" : "en";
}

export const lang = $state({ current: initial() });

export function setLang(value) {
  lang.current = value;
  document.documentElement.lang = value;
  try { localStorage.setItem("lang", value); } catch {}
}
