<script>
    import JSZip from "jszip";
    import { saveAs } from "file-saver";
    import { fade } from "svelte/transition";

    export let files = {};
    export let title = "project";
    export let description = "";
    export let id = "";

    let activeTab = "simulator";
    let activeEquationTab = "aero";
    let activeSpecsTab = "vehicle";
    let activeOutputTab = "engine";
    let expandedEquation = null;

    async function downloadProject() {
        const zip = new JSZip();
        for (const [filename, content] of Object.entries(files)) {
            zip.file(filename, content);
        }
        const blob = await zip.generateAsync({ type: "blob" });
        saveAs(blob, `${title}.zip`);
    }
</script>

<div class="tech-description">
    <div class="header-row">
        <h3>Description</h3>
        <button on:click={downloadProject}>Download Project</button>
    </div>

    {#if id === "DashboardSim"}
        <div class="general-desc">
            <p>
                A high-fidelity Python simulation of a 2005 VW Phaeton W12 LWB.
                This project models the complex interaction between the 6.0L W12
                engine, ZF 5HP24A automatic transmission, and the vehicle's
                chassis dynamics. It includes a real-time thermodynamic system,
                fluid dynamics for the torque converter, and a fully functional
                digital dashboard interface built with Tkinter.
            </p>
        </div>

        <div class="desc-tabs">
            <button
                class:active={activeTab === "simulator"}
                on:click={() => (activeTab = "simulator")}
            >
                Simulator Logic
            </button>
            <div class="divider">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    ><polyline points="16 18 22 12 16 6"></polyline><polyline
                        points="8 6 2 12 8 18"
                    ></polyline></svg
                >
            </div>
            <button
                class:active={activeTab === "dashboard"}
                on:click={() => (activeTab = "dashboard")}
            >
                Dashboard UI
            </button>
        </div>

        <div class="desc-content">
            {#if activeTab === "simulator"}
                <div class="tab-pane" in:fade={{ duration: 200 }}>
                    <div class="section">
                        <h4>Physical Model Architecture</h4>
                        <p>
                            The simulation utilizes a <strong
                                >discrete-time Euler integration model</strong
                            > to approximate the continuous physics of the vehicle.
                            This approach was chosen for its balance between computational
                            efficiency and accuracy suitable for real-time visualization
                            (30+ FPS). By breaking down the complex differential
                            equations of motion into small time steps (dt), the system
                            can dynamically respond to user inputs and changing environmental
                            conditions without the overhead of a full physics engine.
                        </p>

                        <h4>Core Physics Equations</h4>

                        <div class="sub-tabs">
                            <button
                                class:active={activeEquationTab === "aero"}
                                on:click={() => (activeEquationTab = "aero")}
                                >Aerodynamics</button
                            >
                            <button
                                class:active={activeEquationTab === "engine"}
                                on:click={() => (activeEquationTab = "engine")}
                                >Engine</button
                            >
                            <button
                                class:active={activeEquationTab === "drive"}
                                on:click={() => (activeEquationTab = "drive")}
                                >Drivetrain</button
                            >
                            <button
                                class:active={activeEquationTab === "thermo"}
                                on:click={() => (activeEquationTab = "thermo")}
                                >Thermodynamics</button
                            >
                        </div>

                        <div class="math-block">
                            {#if activeEquationTab === "aero"}
                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>Aerodynamic Drag</h5>
                                        <div class="equation">
                                            <span class="var"
                                                >F<sub>aero</sub></span
                                            >
                                            =
                                            <span class="num">0.5</span> ·
                                            <span class="var">ρ</span>
                                            ·
                                            <span class="var"
                                                >C<sub>d</sub></span
                                            >
                                            · <span class="var">A</span> ·
                                            <span class="var"
                                                >v<sup>2</sup></span
                                            >
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var"
                                                        >F<sub>aero</sub></span
                                                    >: Drag force opposing
                                                    motion (Newtons).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var">ρ</span>:
                                                    Air density (kg/m³).
                                                    Calculated dynamically based
                                                    on temperature.
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >C<sub>d</sub></span
                                                    >: Drag coefficient (0.32).
                                                    Measures aerodynamic
                                                    resistance.
                                                </div>
                                                <div class="var-item">
                                                    <span class="var">A</span>:
                                                    Frontal area (2.40 m²). The
                                                    cross-sectional area of the
                                                    car.
                                                </div>
                                                <div class="var-item">
                                                    <span class="var">v</span>:
                                                    Vehicle velocity (m/s).
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>Rolling Resistance</h5>
                                        <div class="equation">
                                            <span class="var"
                                                >F<sub>roll</sub></span
                                            >
                                            =
                                            <span class="var"
                                                >C<sub>rr</sub></span
                                            >
                                            · <span class="var">m</span> ·
                                            <span class="var">g</span>
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var"
                                                        >F<sub>roll</sub></span
                                                    >: Force resisting tire
                                                    rotation (Newtons).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >C<sub>rr</sub></span
                                                    >: Rolling resistance
                                                    coefficient (0.012). Typical
                                                    for passenger tires.
                                                </div>
                                                <div class="var-item">
                                                    <span class="var">m</span>:
                                                    Vehicle mass (2450 kg).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var">g</span>:
                                                    Gravitational acceleration
                                                    (9.81 m/s²).
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>
                                            Air Density (Ideal Gas Law approx.)
                                        </h5>
                                        <div class="equation">
                                            <span class="var">ρ</span> =
                                            <span class="num">1.225</span> · (<span
                                                class="num">288.15</span
                                            >
                                            /
                                            <span class="var"
                                                >T<sub>intake_K</sub></span
                                            >)
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var"
                                                        >1.225</span
                                                    >: Standard air density at
                                                    sea level (15°C).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >T<sub>intake_K</sub
                                                        ></span
                                                    >: Intake air temperature in
                                                    Kelvin.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {:else if activeEquationTab === "engine"}
                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>Net Engine Torque</h5>
                                        <div class="equation">
                                            <span class="var"
                                                >T<sub>net</sub></span
                                            >
                                            =
                                            <span class="var"
                                                >T<sub>combustion</sub></span
                                            >(<span class="var">rpm</span>) ·
                                            <span class="var">throttle</span>
                                            -
                                            <span class="var"
                                                >T<sub>friction</sub></span
                                            >
                                            -
                                            <span class="var"
                                                >T<sub>load</sub></span
                                            >
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var"
                                                        >T<sub>net</sub></span
                                                    >: The final torque
                                                    available to accelerate the
                                                    flywheel (Nm).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >T<sub>combustion</sub
                                                        ></span
                                                    >: Max torque at current RPM
                                                    (from lookup table).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >throttle</span
                                                    >: Pedal input (0.0 to 1.0).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >T<sub>friction</sub
                                                        ></span
                                                    >: Internal friction losses,
                                                    increases with RPM.
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >T<sub>load</sub></span
                                                    >: Resistance from the
                                                    torque
                                                    converter/transmission.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>Angular Acceleration</h5>
                                        <div class="equation">
                                            <span class="var">α</span> =
                                            <span class="var"
                                                >T<sub>net</sub></span
                                            >
                                            /
                                            <span class="var"
                                                >I<sub>engine</sub></span
                                            >
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var">α</span>:
                                                    Angular acceleration
                                                    (radians/s²).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >I<sub>engine</sub
                                                        ></span
                                                    >: Rotational inertia of
                                                    engine internals + flywheel
                                                    (0.65 kg·m²).
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>RPM Integration</h5>
                                        <div class="equation">
                                            <span class="var"
                                                >RPM<sub>new</sub></span
                                            >
                                            =
                                            <span class="var"
                                                >RPM<sub>old</sub></span
                                            >
                                            + <span class="var">α</span> ·
                                            <span class="var">dt</span>
                                            · <span class="num">9.549</span>
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var">dt</span>:
                                                    Time step (seconds).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >9.549</span
                                                    >: Conversion factor from
                                                    rad/s to RPM (60 / 2π).
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {:else if activeEquationTab === "drive"}
                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>Wheel Force</h5>
                                        <div class="equation">
                                            <span class="var"
                                                >F<sub>drive</sub></span
                                            >
                                            = (<span class="var"
                                                >T<sub>load</sub></span
                                            >
                                            ·
                                            <span class="var"
                                                >Ratio<sub>gear</sub></span
                                            >
                                            ·
                                            <span class="var"
                                                >Ratio<sub>final</sub></span
                                            >) /
                                            <span class="var"
                                                >r<sub>tire</sub></span
                                            >
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var"
                                                        >F<sub>drive</sub></span
                                                    >: Linear force applied to
                                                    the road (Newtons).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >T<sub>load</sub></span
                                                    >: Torque transmitted
                                                    through the transmission.
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >Ratio<sub>gear</sub
                                                        ></span
                                                    >: Current transmission gear
                                                    ratio (e.g., 3.57 for 1st).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >Ratio<sub>final</sub
                                                        ></span
                                                    >: Differential gear ratio
                                                    (3.07).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >r<sub>tire</sub></span
                                                    >: Tire radius (0.35 m).
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>
                                            Vehicle Acceleration (Newton's 2nd
                                            Law)
                                        </h5>
                                        <div class="equation">
                                            <span class="var">a</span> = (<span
                                                class="var"
                                                >F<sub>drive</sub></span
                                            >
                                            -
                                            <span class="var"
                                                >F<sub>aero</sub></span
                                            >
                                            -
                                            <span class="var"
                                                >F<sub>roll</sub></span
                                            >) / <span class="var">m</span>
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var">a</span>:
                                                    Linear acceleration (m/s²).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var">m</span>:
                                                    Total vehicle mass (2450
                                                    kg).
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>Velocity Integration</h5>
                                        <div class="equation">
                                            <span class="var"
                                                >v<sub>new</sub></span
                                            >
                                            =
                                            <span class="var"
                                                >v<sub>old</sub></span
                                            >
                                            + <span class="var">a</span> ·
                                            <span class="var">dt</span>
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var">v</span>:
                                                    Velocity (m/s). Converted to
                                                    km/h for display (v * 3.6).
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {:else if activeEquationTab === "thermo"}
                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>
                                            Heat Transfer Rate (Newton's Law of
                                            Cooling)
                                        </h5>
                                        <div class="equation">
                                            <span class="var">Q</span> =
                                            <span class="var">k</span> · (<span
                                                class="var"
                                                >T<sub>source</sub></span
                                            >
                                            -
                                            <span class="var"
                                                >T<sub>target</sub></span
                                            >)
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var">Q</span>:
                                                    Heat energy transfer rate
                                                    (Watts or Joules/s).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var">k</span>:
                                                    Thermal conductivity
                                                    coefficient (W/K). Varies by
                                                    component and airflow.
                                                </div>
                                                <div class="var-item">
                                                    <span class="var">T</span>:
                                                    Temperature (Celsius).
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="math-group">
                                    <div class="math-content">
                                        <h5>Temperature Change</h5>
                                        <div class="equation">
                                            <span class="var">ΔT</span> = ((<span
                                                class="var">Q<sub>in</sub></span
                                            >
                                            -
                                            <span class="var"
                                                >Q<sub>out</sub></span
                                            >) / (<span class="var">m</span> ·
                                            <span class="var">c</span>)) ·
                                            <span class="var">dt</span>
                                        </div>
                                    </div>
                                    <div class="slide-panel">
                                        <div class="panel-trigger">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><polyline
                                                    points="15 18 9 12 15 6"
                                                ></polyline></svg
                                            >
                                        </div>
                                        <div class="panel-content">
                                            <div class="var-list">
                                                <div class="var-item">
                                                    <span class="var">m</span>:
                                                    Mass of the component (e.g.,
                                                    200kg for Engine Block).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var">c</span>:
                                                    Specific heat capacity
                                                    (e.g., 450 J/kgK for Iron).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >Q<sub>in</sub></span
                                                    >: Heat generated (e.g.,
                                                    from combustion).
                                                </div>
                                                <div class="var-item">
                                                    <span class="var"
                                                        >Q<sub>out</sub></span
                                                    >: Heat lost (e.g., to
                                                    coolant).
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {/if}
                        </div>
                    </div>

                    <div class="section">
                        <h4>Simulation Constants & Start Values</h4>

                        <div class="sub-tabs">
                            <button
                                class:active={activeSpecsTab === "vehicle"}
                                on:click={() => (activeSpecsTab = "vehicle")}
                                >Vehicle</button
                            >
                            <button
                                class:active={activeSpecsTab === "engine"}
                                on:click={() => (activeSpecsTab = "engine")}
                                >Engine</button
                            >
                            <button
                                class:active={activeSpecsTab === "trans"}
                                on:click={() => (activeSpecsTab = "trans")}
                                >Transmission</button
                            >
                            <button
                                class:active={activeSpecsTab === "thermo"}
                                on:click={() => (activeSpecsTab = "thermo")}
                                >Thermodynamics</button
                            >
                            <button
                                class:active={activeSpecsTab === "outputs"}
                                on:click={() => (activeSpecsTab = "outputs")}
                                >Outputs</button
                            >
                        </div>

                        <div class="table-container">
                            <table class="specs-table">
                                <thead>
                                    <tr>
                                        <th>Symbol</th>
                                        <th>Parameter</th>
                                        <th>Value</th>
                                        <th>Unit</th>
                                        <th>Description / Source</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {#if activeSpecsTab === "vehicle"}
                                        <tr
                                            ><td class="var">m</td><td>Mass</td
                                            ><td>2450</td><td>kg</td><td
                                                >Curb weight of W12 LWB model
                                                (approx).</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">C<sub>d</sub></td
                                            ><td>Drag Coeff</td><td>0.32</td><td
                                                >-</td
                                            ><td
                                                >Official drag coefficient for
                                                Phaeton.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">A</td><td
                                                >Frontal Area</td
                                            ><td>2.40</td><td>m²</td><td
                                                >Estimated from width (1.9m) *
                                                height (1.45m) * form factor.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >r<sub>tire</sub></td
                                            ><td>Tire Radius</td><td>0.35</td
                                            ><td>m</td><td
                                                >Based on 255/45 R18 tires.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">C<sub>rr</sub></td
                                            ><td>Rolling Res.</td><td>0.012</td
                                            ><td>-</td><td
                                                >Standard value for passenger
                                                car tires on asphalt.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">g</td><td
                                                >Gravity</td
                                            ><td>9.81</td><td>m/s²</td><td
                                                >Standard gravitational
                                                acceleration.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">ρ<sub>std</sub></td
                                            ><td>Air Density</td><td>1.225</td
                                            ><td>kg/m³</td><td
                                                >Standard sea level air density
                                                at 15°C.</td
                                            ></tr
                                        >
                                    {:else if activeSpecsTab === "engine"}
                                        <tr
                                            ><td class="var">V<sub>d</sub></td
                                            ><td>Displacement</td><td>6.0</td
                                            ><td>L</td><td
                                                >Total volume of all 12
                                                cylinders.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >RPM<sub>idle</sub></td
                                            ><td>Idle RPM</td><td>600</td><td
                                                >rpm</td
                                            ><td
                                                >Target idle speed when warm.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >RPM<sub>max</sub></td
                                            ><td>Redline</td><td>6200</td><td
                                                >rpm</td
                                            ><td
                                                >Maximum recommended engine
                                                speed.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >I<sub>engine</sub></td
                                            ><td>Inertia</td><td>0.65</td><td
                                                >kg·m²</td
                                            ><td
                                                >Estimated rotational inertia of
                                                crankshaft, flywheel, and torque
                                                converter fluid.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">dt</td><td
                                                >Time Step</td
                                            ><td>0.016</td><td>s</td><td
                                                >Simulation update interval
                                                (approx 60Hz).</td
                                            ></tr
                                        >
                                    {:else if activeSpecsTab === "trans"}
                                        <tr
                                            ><td class="var"
                                                >Ratio<sub>final</sub></td
                                            ><td>Final Drive</td><td>3.07</td
                                            ><td>ratio</td><td
                                                >Differential gear ratio.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >Ratio<sub>1</sub></td
                                            ><td>1st Gear</td><td>3.57</td><td
                                                >ratio</td
                                            ><td>ZF 5HP24A 1st gear ratio.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >Ratio<sub>2</sub></td
                                            ><td>2nd Gear</td><td>2.20</td><td
                                                >ratio</td
                                            ><td>ZF 5HP24A 2nd gear ratio.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >Ratio<sub>3</sub></td
                                            ><td>3rd Gear</td><td>1.51</td><td
                                                >ratio</td
                                            ><td>ZF 5HP24A 3rd gear ratio.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >Ratio<sub>4</sub></td
                                            ><td>4th Gear</td><td>1.00</td><td
                                                >ratio</td
                                            ><td
                                                >ZF 5HP24A 4th gear ratio
                                                (Direct drive).</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >Ratio<sub>5</sub></td
                                            ><td>5th Gear</td><td>0.80</td><td
                                                >ratio</td
                                            ><td
                                                >ZF 5HP24A 5th gear ratio
                                                (Overdrive).</td
                                            ></tr
                                        >
                                    {:else if activeSpecsTab === "thermo"}
                                        <tr
                                            ><td class="var"
                                                >m<sub>block</sub></td
                                            ><td>Block Mass</td><td>200</td><td
                                                >kg</td
                                            ><td
                                                >Approx. mass of W12 block
                                                (Alu/Iron mix).</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >c<sub>block</sub></td
                                            ><td>Block Cp</td><td>450</td><td
                                                >J/kgK</td
                                            ><td
                                                >Specific Heat of Iron/Alu mix.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >m<sub>coolant</sub></td
                                            ><td>Coolant Mass</td><td>15</td><td
                                                >kg</td
                                            ><td
                                                >Cooling system capacity (approx
                                                15L).</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >c<sub>coolant</sub></td
                                            ><td>Coolant Cp</td><td>4184</td><td
                                                >J/kgK</td
                                            ><td
                                                >Specific Heat of Water/Glycol.</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">m<sub>oil</sub></td
                                            ><td>Oil Mass</td><td>12</td><td
                                                >kg</td
                                            ><td
                                                >Oil capacity (approx 12L for
                                                W12).</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">c<sub>oil</sub></td
                                            ><td>Oil Cp</td><td>1800</td><td
                                                >J/kgK</td
                                            ><td>Specific Heat of Oil.</td></tr
                                        >
                                    {/if}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="section">
                        <h4>Real-time Telemetry Outputs</h4>
                        <p>
                            The simulation runs at approximately 60Hz, but
                            telemetry data is sent to the frontend at 30Hz for
                            visualization. The following values are available in
                            the <code>outputs</code> object.
                        </p>

                        <div class="sub-tabs">
                            <button
                                class:active={activeOutputTab === "engine"}
                                on:click={() => (activeOutputTab = "engine")}
                                >Engine & Power</button
                            >
                            <button
                                class:active={activeOutputTab === "drive"}
                                on:click={() => (activeOutputTab = "drive")}
                                >Drivetrain</button
                            >
                            <button
                                class:active={activeOutputTab === "dynamics"}
                                on:click={() => (activeOutputTab = "dynamics")}
                                >Dynamics</button
                            >
                            <button
                                class:active={activeOutputTab === "vital"}
                                on:click={() => (activeOutputTab = "vital")}
                                >Vital Signs</button
                            >
                            <button
                                class:active={activeOutputTab === "trip"}
                                on:click={() => (activeOutputTab = "trip")}
                                >Trip & Fuel</button
                            >
                        </div>

                        <div class="table-container">
                            <table class="specs-table">
                                <thead>
                                    <tr>
                                        <th>Variable</th>
                                        <th>Description</th>
                                        <th>Unit</th>
                                        <th>Type</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {#if activeOutputTab === "engine"}
                                        <tr
                                            ><td class="var">rpm</td><td
                                                >Engine Speed</td
                                            ><td>rpm</td><td>Integer</td></tr
                                        >
                                        <tr
                                            ><td class="var">power_hp</td><td
                                                >Engine Power</td
                                            ><td>hp</td><td>Integer</td></tr
                                        >
                                        <tr
                                            ><td class="var">torque_nm</td><td
                                                >Engine Torque</td
                                            ><td>Nm</td><td>Integer</td></tr
                                        >
                                        <tr
                                            ><td class="var">ve_pct</td><td
                                                >Volumetric Efficiency</td
                                            ><td>%</td><td>Integer</td></tr
                                        >
                                        <tr
                                            ><td class="var">afr</td><td
                                                >Air-Fuel Ratio</td
                                            ><td>ratio</td><td>Float (1 dec)</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">iat_temp</td><td
                                                >Intake Air Temp</td
                                            ><td>°C</td><td>Float (1 dec)</td
                                            ></tr
                                        >
                                    {:else if activeOutputTab === "drive"}
                                        <tr
                                            ><td class="var">gear</td><td
                                                >Current Gear</td
                                            ><td>-</td><td>Integer (1-5)</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">slip_rpm</td><td
                                                >Torque Converter Slip</td
                                            ><td>rpm</td><td>Integer</td></tr
                                        >
                                        <tr
                                            ><td class="var">lockup</td><td
                                                >TCC Lockup State</td
                                            ><td>-</td><td>Boolean</td></tr
                                        >
                                        <tr
                                            ><td class="var">trans_temp</td><td
                                                >Transmission Fluid Temp</td
                                            ><td>°C</td><td>Float (1 dec)</td
                                            ></tr
                                        >
                                    {:else if activeOutputTab === "dynamics"}
                                        <tr
                                            ><td class="var">speed_kmh</td><td
                                                >Vehicle Speed</td
                                            ><td>km/h</td><td>Integer</td></tr
                                        >
                                        <tr
                                            ><td class="var">accel_g</td><td
                                                >Longitudinal G-Force</td
                                            ><td>g</td><td>Float (2 dec)</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">timer_0_100</td><td
                                                >Current 0-100km/h Time</td
                                            ><td>s</td><td>Float (1 dec)</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">best_0_100</td><td
                                                >Best 0-100km/h Time</td
                                            ><td>s</td><td>Float (2 dec)</td
                                            ></tr
                                        >
                                    {:else if activeOutputTab === "vital"}
                                        <tr
                                            ><td class="var">engine_temp</td><td
                                                >Coolant Temperature</td
                                            ><td>°C</td><td>Float (1 dec)</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">oil_temp</td><td
                                                >Engine Oil Temperature</td
                                            ><td>°C</td><td>Float (1 dec)</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var">oil_pressure</td
                                            ><td>Oil Pressure</td><td>bar</td
                                            ><td>Float (2 dec)</td></tr
                                        >
                                        <tr
                                            ><td class="var">battery_pct</td><td
                                                >Battery Level</td
                                            ><td>%</td><td>Float (1 dec)</td
                                            ></tr
                                        >
                                    {:else if activeOutputTab === "trip"}
                                        <tr
                                            ><td class="var">fuel_ltr</td><td
                                                >Fuel Remaining</td
                                            ><td>L</td><td>Float (2 dec)</td
                                            ></tr
                                        >
                                        <tr
                                            ><td class="var"
                                                >fuel_usage_l_100km</td
                                            ><td>Instant Consumption</td><td
                                                >L/100km</td
                                            ><td>Float (1 dec)</td></tr
                                        >
                                        <tr
                                            ><td class="var">range_km</td><td
                                                >Estimated Range</td
                                            ><td>km</td><td>Integer</td></tr
                                        >
                                        <tr
                                            ><td class="var">odometer_km</td><td
                                                >Total Distance</td
                                            ><td>km</td><td>Float (1 dec)</td
                                            ></tr
                                        >
                                    {/if}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            {/if}
            {#if activeTab === "dashboard"}
                <div class="tab-pane" in:fade={{ duration: 200 }}>
                    <div class="section">
                        <h4>Dashboard Interface</h4>
                        <p>
                            The visualization is built using Python's <strong
                                >Tkinter</strong
                            > library. It renders a vector-based instrument cluster
                            that updates in real-time (approx. 30 FPS). The needles
                            use a smoothing algorithm (linear interpolation with
                            a max step) to simulate the physical damping of real
                            gauges.
                        </p>
                    </div>

                    <div class="section">
                        <h4>Multi-Function Display (MFD)</h4>
                        <p>The center screen features 4 switchable pages:</p>
                        <ul>
                            <li>
                                <strong>MAIN:</strong> Current Gear, Speed, Instant
                                Fuel Consumption.
                            </li>
                            <li>
                                <strong>TRIP:</strong> Range (km), Odometer, Air-Fuel
                                Ratio (AFR).
                            </li>
                            <li>
                                <strong>PERFORMANCE:</strong> Live HP/Torque, G-Force,
                                0-100 km/h Timer.
                            </li>
                            <li>
                                <strong>DIAGNOSTICS:</strong> Trans Temp, Intake
                                Temp, Converter Slip, Oil Pressure.
                            </li>
                        </ul>
                    </div>

                    <div class="section">
                        <h4>Controls</h4>
                        <div class="controls-list">
                            <div class="control-item">
                                <span class="key">↑ / Gas</span>
                                <span>Accelerate (Throttle)</span>
                            </div>
                            <div class="control-item">
                                <span class="key">↓ / Brake</span>
                                <span>Decelerate (Braking)</span>
                            </div>
                            <div class="control-item">
                                <span class="key">Space</span>
                                <span>Cycle MFD Pages</span>
                            </div>
                        </div>
                    </div>
                </div>
            {/if}
        </div>
    {:else}
        <div class="general-desc">
            {@html description || "No description available."}
        </div>
    {/if}
</div>

<style>
    .tech-description {
        padding: 2rem;
        font-size: 1rem;
        line-height: 1.6;
        display: flex;
        flex-direction: column;
        height: 100%;
        overflow-y: auto;
        color: var(--color-text);
    }
    .header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid var(--glass-border);
        padding-bottom: 1rem;
    }
    h3 {
        margin: 0;
        font-size: 1.5rem;
        color: var(--color-text);
    }
    button {
        background-color: var(--color-primary);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
        transition: background-color 0.2s;
    }
    button:hover {
        background-color: var(--color-secondary);
    }

    .general-desc {
        margin-bottom: 2rem;
        font-size: 1.1rem;
        color: var(--color-text-muted);
    }

    /* Tabs */
    .desc-tabs {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
        background: var(--glass-panel-bg);
        padding: 0.5rem;
        border-radius: 50px;
        border: 1px solid var(--glass-border);
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
    }

    .desc-tabs button {
        background: transparent;
        color: var(--color-text-muted);
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 0.9rem;
    }

    .desc-tabs button.active {
        background: var(--color-primary);
        color: white;
    }

    /* Sub Tabs */
    .sub-tabs {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }

    .sub-tabs button {
        background: var(--glass-panel-bg);
        color: var(--color-text-muted);
        padding: 0.4rem 1rem;
        border-radius: 8px;
        font-size: 0.85rem;
        border: 1px solid var(--glass-border);
    }

    .sub-tabs button.active {
        background: var(--color-primary);
        color: white;
        border-color: var(--color-primary);
    }

    .divider {
        color: var(--color-text-muted);
        opacity: 0.5;
        display: flex;
        align-items: center;
    }

    /* Content */
    .section {
        margin-bottom: 2rem;
    }

    h4 {
        font-size: 1.2rem;
        margin-bottom: 1rem;
        color: var(--color-primary);
        border-left: 3px solid var(--color-primary);
        padding-left: 0.8rem;
    }

    p {
        margin-bottom: 1rem;
        color: var(--color-text-muted);
    }

    ul {
        list-style-type: none;
        padding-left: 1rem;
    }

    li {
        margin-bottom: 0.5rem;
        position: relative;
        padding-left: 1.2rem;
        color: var(--color-text-muted);
    }

    li::before {
        content: "•";
        color: var(--color-primary);
        position: absolute;
        left: 0;
        font-weight: bold;
    }

    strong {
        color: var(--color-text);
    }

    /* Math Styles */
    .math-block {
        background: var(--code-bg);
        padding: 1.5rem;
        border-radius: var(--radius);
        border: 1px solid var(--glass-border);
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .equation {
        font-family: "Times New Roman", Times, serif;
        font-size: 1.3rem;
        color: var(--color-text);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .var {
        font-style: italic;
        color: var(--color-primary);
        font-weight: 500;
    }

    .num {
        color: var(--color-secondary);
        font-weight: 600;
    }

    /* Table Styles */
    .table-container {
        overflow-x: auto;
        border-radius: var(--radius);
        border: 1px solid var(--glass-border);
    }

    .specs-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
        background: var(--glass-panel-bg);
    }

    .specs-table th,
    .specs-table td {
        padding: 0.8rem 1rem;
        text-align: left;
        border-bottom: 1px solid var(--glass-border);
    }

    .specs-table th {
        background: rgba(127, 127, 127, 0.1);
        color: var(--color-text);
        font-weight: 600;
    }

    .specs-table td {
        color: var(--color-text-muted);
    }

    .specs-table tr:last-child td {
        border-bottom: none;
    }

    /* Controls List */
    .controls-list {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .control-item {
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 1;
        gap: 1rem;
        background: var(--glass-panel-bg);
        padding: 0.8rem;
        border-radius: var(--radius);
        border: 1px solid var(--glass-border);
        min-width: 200px;
    }

    .key {
        background: var(--color-text);
        color: var(--color-bg);
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        font-family: var(--font-mono);
        font-weight: bold;
        font-size: 0.9rem;
        min-width: 80px;
        text-align: center;
    }

    /* Variable Lists & Sliding Panel */
    .math-group {
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
        display: flex;
        /* Ensure the group has enough height/width context */
        background: var(--glass-panel-bg);
        border-radius: var(--radius);
        border: 1px solid var(--glass-border);
    }

    .math-group:last-child {
        margin-bottom: 0;
    }

    .math-content {
        flex: 1;
        padding: 1.5rem;
        /* Ensure content doesn't get hidden under the trigger initially */
        padding-right: 3.5rem;
    }

    /* The sliding container */
    .slide-panel {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        width: 65%; /* Adjust to keep equation visible */
        display: flex;
        transform: translateX(calc(100% - 40px)); /* Show only trigger */
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 10;
        pointer-events: auto; /* Ensure hover works */
    }

    /* Hovering the panel (which includes the trigger) slides it out */
    .slide-panel:hover {
        transform: translateX(0);
    }

    .panel-trigger {
        width: 40px;
        background: rgba(var(--color-primary-rgb), 0.1);
        border-left: 1px solid var(--glass-border);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: help;
        color: var(--color-primary);
        flex-shrink: 0;
        transition: background 0.2s;
    }

    .slide-panel:hover .panel-trigger {
        background: var(--color-primary);
        color: white;
    }

    .panel-trigger svg {
        transition: transform 0.3s;
        transform: rotate(180deg); /* Point left initially */
    }

    .slide-panel:hover .panel-trigger svg {
        transform: rotate(0deg); /* Point right when open */
    }

    .panel-content {
        flex: 1;
        background: var(
            --color-surface
        ); /* Solid background to cover content below */
        border-left: 1px solid var(--glass-border);
        padding: 1.5rem;
        overflow-y: auto;
        box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
    }

    .var-list {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .var-item {
        font-size: 0.9rem;
        color: var(--color-text-muted);
        line-height: 1.4;
    }
</style>
