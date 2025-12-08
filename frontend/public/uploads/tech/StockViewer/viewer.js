// Market Viewer Logic - Handles data fetching from Yahoo Finance via CORS proxy

const CORS_PROXY = "https://corsproxy.io/?";

class MarketViewer {
    constructor() {
        this.baseUrl = "https://query1.finance.yahoo.com/v8/finance/chart";
        this.searchUrl = "https://query2.finance.yahoo.com/v1/finance/search";
    }

    // Search for stocks, crypto, or ETFs
    async search(query) {
        if (!query || query.length < 2) return [];
        try {
            const res = await fetch(`${CORS_PROXY}${this.searchUrl}?q=${encodeURIComponent(query)}`);
            const data = await res.json();

            // Filter for valid Yahoo Finance quotes and Map to simple objects
            return (data.quotes || [])
                .filter(q => q.isYahooFinance)
                .map(q => ({
                    symbol: q.symbol,
                    name: q.shortname || q.longname,
                    type: q.typeDisp
                }));
        } catch (error) {
            console.error("Search failed:", error);
            return [];
        }
    }

    // Fetch historical chart data and current price
    async fetchMarketData(symbol) {
        try {
            // Request 1 day of data with 5-minute intervals
            const url = `${CORS_PROXY}${this.baseUrl}/${symbol}?range=1d&interval=5m`;
            const response = await fetch(url);
            const data = await response.json();

            const result = data.chart.result[0];
            const meta = result.meta;
            const quotes = result.indicators.quote[0];

            // Calculate percentage change from previous close
            const price = meta.regularMarketPrice;
            const prevClose = meta.previousClose;
            const change = prevClose ? ((price - prevClose) / prevClose) * 100 : 0;

            return {
                price: price,
                change24h: change,
                history: result.timestamp.map((t, i) => [t * 1000, quotes.close[i]])
            };
        } catch (error) {
            console.error("Data fetch failed:", error);
            return null;
        }
    }
}
