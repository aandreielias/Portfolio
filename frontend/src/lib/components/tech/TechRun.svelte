<script>
    import { onMount, onDestroy } from "svelte";
    import DashboardRenderer from "./visualizations/DashboardRenderer.svelte";
    import StockRenderer from "./visualizations/StockRenderer.svelte";
    import ModelRenderer from "./visualizations/ModelRenderer.svelte";

    export let techId;
    export let data; // { sim, pyodide }

    // Registry of visualizations
    const visualizations = {
        DashboardSim: DashboardRenderer,
        StockViewer: StockRenderer,
        "3d-viewer": ModelRenderer,
    };
</script>

<div class="tech-run">
    {#if visualizations[techId]}
        <svelte:component this={visualizations[techId]} sim={data.sim} />
    {:else}
        <div class="no-viz">
            <p>No visualization available for {techId}</p>
            <pre>Output: {JSON.stringify(data, null, 2)}</pre>
        </div>
    {/if}
</div>

<style>
    .tech-run {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: var(--code-view-bg);
    }
    .no-viz {
        color: var(--color-text);
        text-align: center;
    }
</style>
