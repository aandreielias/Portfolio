<script>
    import { createEventDispatcher } from "svelte";
    import Modal from "./Modal.svelte";
    import Timeline from "./Timeline.svelte";

    const dispatch = createEventDispatcher();

    const name = import.meta.env.VITE_NAME;
    const email = import.meta.env.VITE_EMAIL;
    const phone = import.meta.env.VITE_PHONE;

    let activeTab = "about";
    let activeCategory = "education";

    const timelineItems = [
        {
            start: 2025.0,
            end: 2026.0,
            title: "FH Wiener Neustadt",
            description: "Software Engineering and System Design",
            type: "education",
            displayDate: "2025 - Present",
        },
        {
            start: 2024.6, // Aug
            end: 2025.1, // Feb
            title: "Österreichisches Bundesheer",
            description: "Basic Military Service",
            type: "work",
            displayDate: "Aug 2024 - Feb 2025",
        },
        {
            start: 2019.7, // Sept
            end: 2024.5, // June
            title: "HTL Spengergasse",
            description: "Biomedicine and Health Informatics",
            type: "education",
            displayDate: "2019 - 2024",
        },
        {
            start: 2022.6, // Aug
            end: 2022.7, // Aug
            title: "Rehab Zentrum Stadlau",
            description: "Research Internship",
            type: "work",
            displayDate: "Aug 2022",
        },
        {
            start: 2021.6, // Aug
            end: 2021.7, // Aug
            title: "Rehab Zentrum Stadlau",
            description: "Research Internship",
            type: "work",
            displayDate: "Aug 2021",
        },
    ];

    function close() {
        dispatch("close");
    }
</script>

<Modal
    title={activeTab === "about" ? "About Me" : "Contact Me"}
    on:close={close}
    height="600px"
>
    <div class="modal-content-grid">
        <div class="main-column">
            <div class="tabs">
                <button
                    class="tab-btn"
                    class:active={activeTab === "about"}
                    on:click={() => (activeTab = "about")}
                >
                    About Me
                </button>
                <button
                    class="tab-btn"
                    class:active={activeTab === "contact"}
                    on:click={() => (activeTab = "contact")}
                >
                    Contact Me
                </button>
            </div>

            <div class="content-area">
                {#if activeTab === "about"}
                    <div class="about-container">
                        <div class="about-text">
                            <p>
                                I'm {name}, a student for System Engineering and
                                System Design and a passion for programming.
                            </p>
                            <p>
                                I have a strong foundation in software
                                development and a keen interest in creating
                                innovative solutions.
                            </p>
                        </div>

                        <div class="category-tabs">
                            <button
                                class="category-btn"
                                class:active={activeCategory === "education"}
                                on:click={() => (activeCategory = "education")}
                            >
                                Education
                            </button>
                            <button
                                class="category-btn"
                                class:active={activeCategory === "work"}
                                on:click={() => (activeCategory = "work")}
                            >
                                Work Experience
                            </button>
                        </div>

                        <Timeline items={timelineItems} mode={activeCategory} />
                    </div>
                {:else}
                    <div class="contact-info">
                        <div class="contact-item">
                            <span class="label">Name</span>
                            <span class="value">{name}</span>
                        </div>
                        <div class="contact-item">
                            <span class="label">Email</span>
                            <a href="mailto:{email}" class="value link"
                                >{email}</a
                            >
                        </div>
                        <div class="contact-item">
                            <span class="label">Phone</span>
                            <a href="tel:{phone}" class="value link">{phone}</a>
                        </div>
                    </div>
                {/if}
            </div>
        </div>

        {#if activeTab === "about"}
            <div class="side-column">
                <img src="/api/self" alt={name} class="profile-image" />
                <div class="interests-section">
                    <h3>Personal Interests</h3>
                    <p>
                        I have studied classical harp for 11 years and bassoon
                        for 7 years and participated in various concerts over
                        the years.
                    </p>
                </div>
            </div>
        {/if}
    </div>
</Modal>

<style>
    .modal-content-grid {
        display: flex;
        gap: 2rem;
        height: 100%;
        overflow: hidden; /* Prevent double scrollbars */
    }

    .main-column {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-width: 0; /* Important for flex children */
    }

    .side-column {
        flex-shrink: 0;
        width: 250px;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        overflow-y: auto;
        max-height: 100%;
        padding-right: 0.5rem; /* Space for scrollbar */
    }

    /* Side Column Scrollbar */
    .side-column::-webkit-scrollbar {
        width: 4px;
    }

    .side-column::-webkit-scrollbar-track {
        background: transparent;
    }

    .side-column::-webkit-scrollbar-thumb {
        background: var(--glass-border);
        border-radius: 2px;
    }

    .side-column::-webkit-scrollbar-thumb:hover {
        background: var(--color-text-muted);
    }

    .interests-section {
        background: var(--glass-panel-bg);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 1rem;
        font-size: 0.9rem;
        color: var(--color-text-muted);
        line-height: 1.5;
    }

    .interests-section h3 {
        font-size: 1rem;
        color: var(--color-text);
        margin-bottom: 0.5rem;
        font-weight: 600;
    }

    .tabs {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--color-border);
        padding-bottom: 0.5rem;
        flex-shrink: 0;
    }

    .tab-btn {
        background: none;
        border: none;
        color: var(--color-text-muted);
        font-size: 1.1rem;
        cursor: pointer;
        padding: 0.5rem 1rem;
        border-radius: var(--radius);
        transition: all 0.2s;
    }

    .tab-btn:hover {
        color: var(--color-text);
        background: var(--color-bg-secondary);
    }

    .tab-btn.active {
        color: var(--color-primary);
        font-weight: 600;
        background: rgba(99, 102, 241, 0.1);
    }

    .content-area {
        flex: 1;
        overflow-y: auto;
        padding-right: 1rem;
        min-height: 0;
    }

    /* Custom Scrollbar */
    .content-area::-webkit-scrollbar {
        width: 6px;
    }

    .content-area::-webkit-scrollbar-track {
        background: transparent;
    }

    .content-area::-webkit-scrollbar-thumb {
        background: var(--glass-border);
        border-radius: 3px;
    }

    .content-area::-webkit-scrollbar-thumb:hover {
        background: var(--color-text-muted);
    }

    .category-tabs {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
        margin-top: 1rem;
        background: var(--glass-panel-bg);
        padding: 0.5rem;
        border-radius: 50px;
        border: 1px solid var(--glass-border);
        width: fit-content;
        margin-left: auto; /* Center horizontally if container allows */
        margin-right: auto;
    }

    .category-btn {
        background: transparent;
        color: var(--color-text-muted);
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 0.9rem;
        border: none; /* Remove border from buttons as container has it */
        cursor: pointer;
        transition: all 0.2s;
    }

    .category-btn:hover {
        color: var(--color-text);
    }

    .category-btn.active {
        background: var(--color-primary);
        color: white;
        font-weight: 600;
    }

    .about-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .about-text {
        flex-direction: column;
        gap: 0.5rem;
    }

    .label {
        font-size: 0.9rem;
        color: var(--color-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    .value {
        font-size: 1.2rem;
        color: var(--color-text);
    }

    .link {
        color: var(--color-primary);
        text-decoration: none;
        transition: color 0.2s;
    }

    .link:hover {
        color: #818cf8;
        text-decoration: underline;
    }

    .profile-image {
        width: 100%;
        height: auto;
        border-radius: var(--radius);
        object-fit: cover;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        /* Align with tabs? The tabs have margin-bottom 1rem. 
           The image is in side-column. 
           If we want the top of the image to align with the top of the tabs, 
           we just need to ensure they start at the same y-position.
           Since they are flex siblings, they start at the top.
        */
    }

    @media (max-width: 768px) {
        .modal-content-grid {
            flex-direction: column-reverse; /* Image on top? Or bottom? */
            /* User said "pictures top should begin in the row where you can switch tabs" */
            /* On mobile, maybe stack image on top of tabs? */
            overflow-y: auto;
        }

        .side-column {
            width: 100%; /* Full width on mobile */
            margin: 0 auto;
            flex-shrink: 0;
        }

        .main-column {
            overflow: visible; /* Let the whole modal scroll */
        }

        .content-area {
            overflow: visible;
        }
    }
</style>
