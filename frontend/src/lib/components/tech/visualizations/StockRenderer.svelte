<script>
    import { onMount, onDestroy } from "svelte";

    // Default Symbols (Fallback)
    let selectedId = "bitcoin";
    let selectedSymbol = "BTC";
    let selectedName = "Bitcoin";

    let price = 0;
    let change24h = 0;
    let history = []; // Array of [timestamp, price]
    let loading = true;
    let error = null;
    let intervalId;

    // Search State
    let searchQuery = "";
    let searchResults = [];
    let isSearching = false;
    let showResults = false;
    let searchTimeout;

    // Chart State
    let chartWidth;
    let hoverInfo = null;

    async function fetchMarketData() {
        if (!selectedId) return;

        try {
            // Fetch current price and 24h change
            const priceRes = await fetch(
                `https://api.coingecko.com/api/v3/simple/price?ids=${selectedId}&vs_currencies=usd&include_24hr_change=true`,
            );
            const priceData = await priceRes.json();

            if (priceData[selectedId]) {
                price = priceData[selectedId].usd;
                change24h = priceData[selectedId].usd_24h_change;
            }

            // Fetch chart history (24h)
            const historyRes = await fetch(
                `https://api.coingecko.com/api/v3/coins/${selectedId}/market_chart?vs_currency=usd&days=1`,
            );
            const historyData = await historyRes.json();

            if (historyData.prices) {
                history = historyData.prices;
            }

            error = null;
            loading = false;
        } catch (e) {
            console.error("Failed to fetch market data:", e);
            error = "Failed to load data";
            loading = false;
        }
    }

    function handleSearchInput() {
        clearTimeout(searchTimeout);
        if (searchQuery.length < 2) {
            searchResults = [];
            showResults = false;
            return;
        }

        searchTimeout = setTimeout(() => {
            performSearch();
        }, 500);
    }

    async function performSearch() {
        if (!searchQuery) return;

        isSearching = true;
        showResults = true;

        try {
            const res = await fetch(
                `https://api.coingecko.com/api/v3/search?query=${encodeURIComponent(searchQuery)}`,
            );
            const data = await res.json();
            searchResults = data.coins || [];
        } catch (e) {
            console.error("Search failed:", e);
            searchResults = [];
        } finally {
            isSearching = false;
        }
    }

    function selectCoin(coin) {
        selectedId = coin.id;
        selectedSymbol = coin.symbol;
        selectedName = coin.name;

        searchQuery = "";
        showResults = false;
        loading = true;
        history = [];
        fetchMarketData();
    }

    function formatTick(val) {
        if (val >= 1000) {
            return val.toLocaleString(undefined, {
                notation: "compact",
                compactDisplay: "short",
                maximumFractionDigits: 1,
            });
        }
        return Math.round(val).toLocaleString();
    }

    onMount(() => {
        fetchMarketData();
        // Refresh every 60s
        intervalId = setInterval(fetchMarketData, 60000);
    });

    onDestroy(() => {
        clearInterval(intervalId);
        clearTimeout(searchTimeout);
    });

    // Chart Helpers
    $: prices = history.map((p) => p[1]);
    $: minVal = prices.length ? Math.min(...prices) : 0;
    $: maxVal = prices.length ? Math.max(...prices) : 0;
    $: range = maxVal - minVal || 1;

    // Scale X and Y to percentage (10-90% for Y padding)
    $: getY = (val) => 100 - ((val - minVal) / range) * 80 - 10;
    $: getX = (i) => (i / (prices.length - 1)) * 100;

    // Y Axis Ticks (5 steps)
    $: yTicks = [0, 0.25, 0.5, 0.75, 1].map((p) => {
        const val = minVal + range * p;
        return {
            val,
            y: getY(val),
        };
    });

    // SVG Path Generation
    $: linePoints = history.map((p, i) => `${getX(i)},${getY(p[1])}`).join(" ");
    $: areaPoints = `${linePoints} 100,100 0,100`;

    // Interaction Handlers
    function handleMouseMove(e) {
        if (!history.length || !chartWidth) return;

        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const width = rect.width;

        // Find closest index
        const index = Math.min(
            Math.max(Math.round((x / width) * (history.length - 1)), 0),
            history.length - 1,
        );
        const point = history[index];

        if (point) {
            hoverInfo = {
                time: new Date(point[0]).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                }),
                price: point[1],
                x: (index / (history.length - 1)) * 100, // percentage for positioning
                y: ((e.clientY - rect.top) / rect.height) * 100, // Use cursor Y position
            };
        }
    }

    function handleMouseLeave() {
        hoverInfo = null;
    }
</script>

<div class="stock-viewer">
    <!-- Click Outside Backdrop -->
    {#if showResults}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div class="backdrop" on:click={() => (showResults = false)}></div>
    {/if}

    <!-- Header with Search -->
    <div class="header">
        <div class="title-section">
            <div class="coin-info">
                <h2>{selectedName}</h2>
                <span class="symbol">{selectedSymbol}</span>
            </div>
            <div class="live-indicator">
                <div class="live-dot"></div>
                <span>LIVE</span>
            </div>
        </div>

        <div class="search-container">
            <div class="search-input-wrapper">
                <svg
                    class="search-icon"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    ><circle cx="11" cy="11" r="8"></circle><line
                        x1="21"
                        y1="21"
                        x2="16.65"
                        y2="16.65"
                    ></line></svg
                >
                <input
                    type="text"
                    placeholder="Search market..."
                    bind:value={searchQuery}
                    on:input={handleSearchInput}
                    on:focus={() => {
                        if (searchQuery.length > 1) {
                            if (searchResults.length > 0) showResults = true;
                            else performSearch();
                        }
                    }}
                />
            </div>
            {#if showResults}
                <div class="search-results glass-panel">
                    {#if isSearching}
                        <div class="p-4 text-center text-sm text-gray-400">
                            Searching...
                        </div>
                    {:else if searchResults.length > 0}
                        {#each searchResults.slice(0, 8) as coin}
                            <!-- svelte-ignore a11y-click-events-have-key-events -->
                            <!-- svelte-ignore a11y-no-static-element-interactions -->
                            <div
                                class="search-item"
                                on:click={() => selectCoin(coin)}
                            >
                                <img src={coin.thumb} alt={coin.symbol} />
                                <div class="item-text">
                                    <span class="name">{coin.name}</span>
                                    <span class="sym">{coin.symbol}</span>
                                </div>
                            </div>
                        {/each}
                    {:else if searchQuery.length > 1}
                        <div class="p-4 text-center text-sm text-gray-400">
                            No results found
                        </div>
                    {/if}
                </div>
            {/if}
        </div>
    </div>

    {#if loading && !prices.length}
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Fetching market data...</p>
        </div>
    {:else if error}
        <div class="error-state">
            <span>⚠️</span>
            {error}
        </div>
    {:else}
        <div class="price-row">
            <div class="main-price">
                ${price.toLocaleString(undefined, {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                })}
            </div>
            <div
                class="change-badge"
                class:positive={change24h >= 0}
                class:negative={change24h < 0}
            >
                {change24h >= 0 ? "▲" : "▼"}
                {Math.abs(change24h).toFixed(2)}%
                <span class="interval">24h</span>
            </div>
        </div>

        <div
            class="chart-wrapper"
            bind:clientWidth={chartWidth}
            on:mousemove={handleMouseMove}
            on:mouseleave={handleMouseLeave}
            role="application"
        >
            <div class="chart-stats">
                <span class="stat high">H: ${maxVal.toLocaleString()}</span>
                <span class="stat low">L: ${minVal.toLocaleString()}</span>
            </div>

            <!-- Y-Axis Labels -->
            <div class="y-axis">
                {#each yTicks as tick}
                    <div class="tick-label" style="top: {tick.y}%;">
                        ${formatTick(tick.val)}
                    </div>
                    <!-- Optional grid line -->
                    <div class="grid-line" style="top: {tick.y}%;"></div>
                {/each}
            </div>

            <svg viewBox="0 0 100 100" preserveAspectRatio="none">
                <defs>
                    <linearGradient
                        id="gradient-{change24h >= 0 ? 'up' : 'down'}"
                        x1="0"
                        x2="0"
                        y1="0"
                        y2="1"
                    >
                        <stop
                            offset="0%"
                            stop-color={change24h >= 0 ? "#4ade80" : "#f87171"}
                            stop-opacity="0.2"
                        />
                        <stop
                            offset="100%"
                            stop-color={change24h >= 0 ? "#4ade80" : "#f87171"}
                            stop-opacity="0"
                        />
                    </linearGradient>
                </defs>

                <!-- Fill Area -->
                <polygon
                    points={areaPoints}
                    fill={`url(#gradient-${change24h >= 0 ? "up" : "down"})`}
                />

                <!-- Line -->
                <polyline
                    points={linePoints}
                    fill="none"
                    stroke={change24h >= 0 ? "#4ade80" : "#f87171"}
                    stroke-width="1.5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    vector-effect="non-scaling-stroke"
                />

                <!-- Hover Intersect Lines -->
                {#if hoverInfo}
                    <!-- Vertical Line (Darker for visibility) -->
                    <line
                        x1={hoverInfo.x}
                        y1="0"
                        x2={hoverInfo.x}
                        y2="100"
                        stroke="rgba(0,0,0,0.5)"
                        stroke-width="2"
                        stroke-dasharray="4"
                        vector-effect="non-scaling-stroke"
                    />
                {/if}
            </svg>

            <!-- Tooltip -->
            {#if hoverInfo}
                <div
                    class="tooltip glass-panel"
                    style="left: {hoverInfo.x}%; top: {hoverInfo.y}%;"
                >
                    <span class="time">{hoverInfo.time}</span>
                    <span class="hover-price"
                        >${hoverInfo.price.toLocaleString(undefined, {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                        })}</span
                    >
                </div>
            {/if}
        </div>
    {/if}
</div>

<style>
    .stock-viewer {
        width: 100%;
        height: 100%; /* Fill container */
        max-width: 100%; /* Remove 600px cap */
        min-height: 400px;
        padding: 2rem;
        /* Changed background to lighter gray as requested */
        background: rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .title-section {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .coin-info {
        display: flex;
        align-items: baseline;
        gap: 0.5rem;
    }

    h2 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--color-text);
    }

    .symbol {
        font-size: 0.9rem;
        color: var(--color-text-muted);
        text-transform: uppercase;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
    }

    .live-indicator {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.75rem;
        color: #16a34a; /* Darker green (green-600) */
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    .live-dot {
        width: 6px;
        height: 6px;
        background-color: #16a34a; /* Darker green */
        border-radius: 50%;
        box-shadow: 0 0 6px rgba(22, 163, 74, 0.6);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* Fixed Backdrop for Click Outside */
    .backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 40; /* Lower than search results, higher than page */
        cursor: default;
    }

    /* Search */
    .search-container {
        position: relative;
        min-width: 280px;
        z-index: 50; /* Above backdrop */
    }

    .search-input-wrapper {
        position: relative;
        width: 100%;
        display: flex;
        align-items: center;
    }

    .search-icon {
        position: absolute;
        left: 0.75rem;
        width: 16px;
        height: 16px;
        color: var(--color-text-muted);
        pointer-events: none;
    }

    input {
        width: 100%;
        padding: 0.6rem 1rem 0.6rem 2.5rem; /* Left padding for icon */
        background: rgba(255, 255, 255, 0.03); /* Lighter glass */
        border: 1px solid var(--glass-border);
        color: var(--color-text);
        border-radius: 50px; /* Fully rounded pill */
        outline: none;
        font-size: 0.9rem;
        transition: all 0.2s;
    }

    input::placeholder {
        color: var(--color-text-muted);
        opacity: 0.7;
    }

    input:focus {
        background: rgba(255, 255, 255, 0.08); /* Slightly lighter on focus */
        border-color: rgba(255, 255, 255, 0.2);
    }

    .search-results {
        position: absolute;
        top: calc(100% + 8px);
        right: 0;
        left: 0;
        max-height: 280px;
        overflow-y: auto;
        /* Glossy Background utilizing theme variable or fallback to dark glass */
        background: var(--glass-panel-bg, rgba(10, 10, 12, 0.85));
        border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
        border-radius: 12px;
        z-index: 100;
        box-shadow:
            0 4px 6px -1px rgba(0, 0, 0, 0.1),
            0 2px 4px -1px rgba(0, 0, 0, 0.06),
            0 20px 25px -5px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px);
        padding: 4px;
        /* Scrollbar styling */
        scrollbar-width: thin;
        scrollbar-color: var(--glass-border, rgba(255, 255, 255, 0.2))
            transparent;
        color: var(--color-text);
    }

    /* Custom Scrollbar for Webkit */
    .search-results::-webkit-scrollbar {
        width: 6px;
    }
    .search-results::-webkit-scrollbar-track {
        background: transparent;
    }
    .search-results::-webkit-scrollbar-thumb {
        background-color: var(--glass-border, rgba(255, 255, 255, 0.2));
        border-radius: 20px;
    }

    .search-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.6rem 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border-radius: 8px;
        border-bottom: none;
        margin-bottom: 2px;
    }

    .search-item:hover {
        background: var(--glass-border, rgba(255, 255, 255, 0.1));
        transform: translateX(4px);
    }

    .search-item img {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        object-fit: cover;
    }

    .item-text {
        display: flex;
        flex-direction: column;
        line-height: 1.2;
    }

    .item-text .name {
        font-size: 0.9rem;
        color: var(--color-text);
        font-weight: 500;
        margin-bottom: 2px;
    }

    .item-text .sym {
        font-size: 0.75rem;
        color: var(--color-text-muted);
        font-weight: 500;
        text-transform: uppercase;
    }

    .p-4 {
        padding: 1rem;
    }
    .text-center {
        text-align: center;
    }
    .text-sm {
        font-size: 0.875rem;
    }
    .text-gray-400 {
        color: var(--color-text-muted);
    }

    /* Price Section */
    .price-row {
        display: flex;
        align-items: flex-end;
        gap: 1rem;
    }

    .main-price {
        font-family: "Inter", sans-serif;
        font-weight: 700;
        font-size: 3.5rem; /* Larger price */
        color: var(--color-text);
        letter-spacing: -2px;
        line-height: 1;
    }

    .change-badge {
        font-size: 1rem;
        font-weight: 600;
        padding: 0.35rem 0.85rem;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        margin-bottom: 0.5rem;
    }

    .interval {
        opacity: 0.6;
        font-weight: 400;
        font-size: 0.8rem;
        margin-left: 0.25rem;
    }

    .change-badge.positive {
        color: #4ade80;
        background: rgba(74, 222, 128, 0.1);
        border: 1px solid rgba(74, 222, 128, 0.2);
    }

    .change-badge.negative {
        color: #f87171;
        background: rgba(248, 113, 113, 0.1);
        border: 1px solid rgba(248, 113, 113, 0.2);
    }

    /* Chart */
    .chart-wrapper {
        position: relative;
        flex: 1; /* Take remaining vertical space */
        min-height: 0; /* Flex fix */
        width: 100%;
        background: rgba(0, 0, 0, 0.1);
        border-radius: var(--radius);
        overflow: hidden;
        border: 1px solid var(--glass-border);
        cursor: crosshair;
    }

    .chart-stats {
        position: absolute;
        top: 1rem;
        left: 1rem;
        right: 1rem;
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: var(--color-text-muted);
        pointer-events: none;
    }

    svg {
        width: 100%;
        height: 100%;
        display: block;
    }

    /* Tooltip */
    .tooltip {
        position: absolute;
        pointer-events: none;
        padding: 0.6rem 0.8rem;
        border-radius: 8px;

        /* Light Mode Defaults */
        background: rgba(245, 245, 245, 0.95);
        border: 1px solid rgba(0, 0, 0, 0.1);
        color: #1a1a1a;

        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        z-index: 10;
        /* Position below the cursor: center horizontally, push down vertically (25px offset) */
        transform: translate(-50%, 25px);
        white-space: nowrap;
    }

    /* Dark Mode Override */
    :global([data-theme="dark"]) .tooltip {
        background: rgba(46, 46, 46, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .tooltip .time {
        font-size: 0.75rem;
        color: var(--color-text-muted);
    }
    .tooltip .hover-price {
        font-size: 0.95rem;
        font-weight: 700;
        color: inherit;
    }

    .loading-state,
    .error-state {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: var(--color-text-muted);
        gap: 1rem;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-top-color: var(--color-primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    .search-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.6rem 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border-radius: 8px;
        border-bottom: none;
        margin-bottom: 2px;
    }

    .search-item:hover {
        background: var(--glass-border, rgba(255, 255, 255, 0.1));
        transform: translateX(4px);
    }

    .search-item img {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        object-fit: cover;
    }

    .item-text {
        display: flex;
        flex-direction: column;
        line-height: 1.2;
    }

    .item-text .name {
        font-size: 0.9rem;
        color: var(--color-text);
        font-weight: 500;
        margin-bottom: 2px;
    }

    .item-text .sym {
        font-size: 0.75rem;
        color: var(--color-text-muted);
        font-weight: 500;
        text-transform: uppercase;
    }

    .p-4 {
        padding: 1rem;
    }
    .text-center {
        text-align: center;
    }
    .text-sm {
        font-size: 0.875rem;
    }
    .text-gray-400 {
        color: var(--color-text-muted);
    }

    /* Price Section */
    .price-row {
        display: flex;
        align-items: flex-end;
        gap: 1rem;
    }

    .main-price {
        font-family: "Inter", sans-serif;
        font-weight: 700;
        font-size: 3.5rem; /* Larger price */
        color: var(--color-text);
        letter-spacing: -2px;
        line-height: 1;
    }

    .change-badge {
        font-size: 1rem;
        font-weight: 600;
        padding: 0.35rem 0.85rem;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        margin-bottom: 0.5rem;
    }

    .interval {
        opacity: 0.6;
        font-weight: 400;
        font-size: 0.8rem;
        margin-left: 0.25rem;
    }

    .change-badge.positive {
        color: #4ade80;
        background: rgba(74, 222, 128, 0.1);
        border: 1px solid rgba(74, 222, 128, 0.2);
    }

    .change-badge.negative {
        color: #f87171;
        background: rgba(248, 113, 113, 0.1);
        border: 1px solid rgba(248, 113, 113, 0.2);
    }

    /* Chart */
    .chart-wrapper {
        position: relative;
        flex: 1; /* Take remaining vertical space */
        min-height: 0; /* Flex fix */
        width: 100%;
        background: rgba(0, 0, 0, 0.1);
        border-radius: var(--radius);
        overflow: hidden;
        border: 1px solid var(--glass-border);
        cursor: crosshair;
    }

    .chart-stats {
        position: absolute;
        top: 1rem;
        left: 1rem;
        right: 1rem;
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: var(--color-text-muted);
        pointer-events: none;
    }

    svg {
        width: 100%;
        height: 100%;
        display: block;
    }

    /* Tooltip */
    .tooltip {
        position: absolute;
        pointer-events: none;
        padding: 0.6rem 0.8rem;
        border-radius: 8px;

        /* Light Mode Defaults */
        background: rgba(245, 245, 245, 0.95);
        border: 1px solid rgba(0, 0, 0, 0.1);
        color: #1a1a1a;

        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        z-index: 10;
        /* Position below the cursor: center horizontally, push down vertically (25px offset) */
        transform: translate(-50%, 25px);
        white-space: nowrap;
    }

    /* Dark Mode Override */
    :global([data-theme="dark"]) .tooltip {
        background: rgba(46, 46, 46, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .tooltip .time {
        font-size: 0.75rem;
        color: var(--color-text-muted);
    }
    .tooltip .hover-price {
        font-size: 0.95rem;
        font-weight: 700;
        color: inherit;
    }

    .loading-state,
    .error-state {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: var(--color-text-muted);
        gap: 1rem;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-top-color: var(--color-primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    /* Y-Axis Styles */
    .y-axis {
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        width: 100%;
        pointer-events: none;
        z-index: 1;
    }

    .tick-label {
        position: absolute;
        left: 0.5rem;
        transform: translateY(-50%);
        font-size: 0.7rem;
        color: var(--color-text-muted);
        font-weight: 500;
        text-align: left;
        opacity: 0.5;
    }

    .grid-line {
        position: absolute;
        left: 3rem; /* Start after labels */
        right: 0;
        height: 1px;
        background: transparent;
        /* Visible in Light Mode */
        border-top: 1px solid rgba(0, 0, 0, 0.05);
    }

    /* Dark Mode Grid Override */
    :global([data-theme="dark"]) .grid-line {
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
