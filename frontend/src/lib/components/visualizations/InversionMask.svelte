<script>
  function generateTable() {
    // 0-127 -> 0
    // 128 -> 0.5 (approx 128/255)
    // 129-255 -> 1
    const t = [];
    for (let i = 0; i < 256; i++) {
      if (i < 128) t.push(0);
      else if (i === 128) t.push(0.5);
      else t.push(1);
    }
    return t.join(" ");
  }
</script>

<svg style="position: absolute; width: 0; height: 0; pointer-events: none;">
  <defs>
    <filter id="quantize3" color-interpolation-filters="sRGB">
      <feComponentTransfer>
        <feFuncR type="discrete" tableValues={generateTable()} />
        <feFuncG type="discrete" tableValues={generateTable()} />
        <feFuncB type="discrete" tableValues={generateTable()} />
      </feComponentTransfer>
    </filter>
  </defs>
</svg>

<style>
  :global(.inversionMask) {
    /* Apply quantization then inversion to satisfy "128 remains" + "Inversion" */
    backdrop-filter: url(#quantize3) invert(1);
    -webkit-backdrop-filter: url(#quantize3) invert(1);

    /* Ensure it has a layer impact */
    background-color: transparent;
  }
</style>
