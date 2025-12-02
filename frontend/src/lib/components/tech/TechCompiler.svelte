<script>
    import { createEventDispatcher } from "svelte";

    export let files = {};
    export let language = "python";

    const dispatch = createEventDispatcher();
    let pyodide;

    async function loadPyodide() {
        if (window.loadPyodide) {
            return await window.loadPyodide({
                indexURL: "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/",
            });
        }
        return new Promise((resolve, reject) => {
            const script = document.createElement("script");
            script.src =
                "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js";
            script.async = true;
            script.onload = async () => {
                try {
                    const py = await window.loadPyodide({
                        indexURL:
                            "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/",
                    });
                    resolve(py);
                } catch (e) {
                    reject(e);
                }
            };
            script.onerror = reject;
            document.body.appendChild(script);
        });
    }

    async function compile() {
        if (language === "python") {
            try {
                if (!pyodide) {
                    pyodide = await loadPyodide();
                }

                // Load all python files
                // We'll try to run them. If one fails (e.g. imports tkinter), we log it and continue.
                // Ideally we should run 'simulator.py' or dependency files first.
                // For now, we just iterate.
                for (const [filename, content] of Object.entries(files)) {
                    if (filename.endsWith(".py")) {
                        try {
                            await pyodide.runPythonAsync(content);
                        } catch (e) {
                            console.warn(`Failed to run ${filename}:`, e);
                        }
                    }
                }

                // Instantiate Simulator if it exists
                try {
                    // Check if Simulator class exists
                    // We can try to run it.
                    const sim = pyodide.runPython("Simulator()");
                    dispatch("compiled", { sim, pyodide });
                } catch (e) {
                    console.log(
                        "No Simulator class found or instantiation failed",
                        e,
                    );
                    // Even if sim failed, we return pyodide so we can maybe debug or show something
                    dispatch("compiled", { pyodide });
                }
            } catch (err) {
                console.error("Compilation error:", err);
                dispatch("error", err);
            }
        } else {
            // For other languages, just pass through or handle differently
            dispatch("compiled", { files });
        }
    }

    $: if (files && language) {
        compile();
    }
</script>
