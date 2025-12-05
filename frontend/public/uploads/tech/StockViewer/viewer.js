// Live Market Viewer - Logic
// Uses CoinGecko API for real-time market data & 24h history
// Version 2.0 - Added Universal Search & Interactive Graph

class MarketViewer {
    constructor() {
        this.baseUrl = "https://api.coingecko.com/api/v3";
        this.selectedSymbol = "bitcoin";
    }

    // New: Universal Search Function
    async search(query) {
        if (!query || query.length < 2) return [];
        try {
            const res = await fetch(`${this.baseUrl}/search?query=${query}`);
            const data = await res.json();
            return data.coins || [];
        } catch (error) {
            console.error("Search Error:", error);
            return [];
        }
    }

    // Fetch 24-hour historical data for the chart
    async fetchChart(id) {
        try {
            const response = await fetch(
                `${this.baseUrl}/coins/${id}/market_chart?vs_currency=usd&days=1`
            );
            if (!response.ok) throw new Error("API Limit Reached");

            const data = await response.json();
            // Data format: [[timestamp, price], [timestamp, price], ...]
            return data.prices || [];
        } catch (error) {
            console.error("Chart Fetch Error:", error);
            return [];
        }
    }

    // Fetch current price and 24h stats
    async fetchCurrentStats(id) {
        try {
            const response = await fetch(
                `${this.baseUrl}/simple/price?ids=${id}&vs_currencies=usd&include_24hr_change=true`
            );
            const data = await response.json();
            return data[id] || null;
        } catch (error) {
            console.error("Stats Fetch Error:", error);
            return null;
        }
    }

    // Main refresh loop
    async refresh(id) {
        const [history, stats] = await Promise.all([
            this.fetchChart(id),
            this.fetchCurrentStats(id)
        ]);

        return {
            history,
            currentPrice: stats.usd,
            change24h: stats.usd_24h_change
        };
    }
}
