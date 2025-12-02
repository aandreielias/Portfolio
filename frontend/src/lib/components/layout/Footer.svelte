<script>
    const year = new Date().getFullYear();
</script>

<footer>
    <div class="container">
        <p>&copy; {year} Built with Svelte & Spring Boot.</p>
    </div>
</footer>

<style>
    footer {
        padding: 4rem 0;
        margin-top: 4rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        color: var(--color-text-muted);
        text-align: center;
        font-size: 0.9rem;
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
</style>
