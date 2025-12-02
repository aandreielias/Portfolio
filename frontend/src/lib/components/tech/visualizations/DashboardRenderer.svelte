<script>
    import { onMount, onDestroy } from "svelte";

    export let sim;

    let canvas;
    let ctx;
    let animationId;
    let lastTime;

    // Inputs
    let gasMouse = false;
    let brakeMouse = false;
    let gasKey = false;
    let brakeKey = false;

    // Constants
    const WIDTH = 1280;
    const HEIGHT = 450; // Reduced from 550
    const PEDAL_HEIGHT = 170;

    // MFD State
    let pageIndex = 0;
    const pages = ["MAIN", "TRIP", "PERFORMANCE", "DIAGNOSTICS"];

    function togglePage() {
        pageIndex = (pageIndex + 1) % pages.length;
    }

    function handleKeyDown(e) {
        if (e.key === "ArrowUp") gasKey = true;
        if (e.key === "ArrowDown") brakeKey = true;
        if (e.key === " ") {
            e.preventDefault();
            togglePage();
        }
    }

    function handleKeyUp(e) {
        if (e.key === "ArrowUp") gasKey = false;
        if (e.key === "ArrowDown") brakeKey = false;
    }

    function drawPedal(ctx, x, y, w, h, text, color) {
        ctx.fillStyle = color;
        ctx.strokeStyle = "#aaaaaa";
        ctx.lineWidth = 2;
        ctx.fillRect(x + 5, y + 5, w - 10, h - 10);
        ctx.strokeRect(x + 5, y + 5, w - 10, h - 10);
        ctx.fillStyle = "white";
        ctx.font = "bold 14px Arial";
        ctx.textAlign = "center";
        const lines = text.split("\n");
        lines.forEach((line, i) =>
            ctx.fillText(line, x + w / 2, y + h / 2 + i * 15),
        );
    }

    function drawGaugeBackground(
        ctx,
        x,
        y,
        r,
        minVal,
        maxVal,
        title,
        majorTicks,
        unit = "",
        iconType = null,
    ) {
        // Bezel
        ctx.beginPath();
        ctx.arc(x, y, r + 2, 0, 2 * Math.PI);
        ctx.strokeStyle = "#888";
        ctx.lineWidth = 3;
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(x, y, r, 0, 2 * Math.PI);
        ctx.strokeStyle = "#555";
        ctx.lineWidth = 5;
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(x, y, r - 5, 0, 2 * Math.PI);
        ctx.fillStyle = "#050505";
        ctx.fill();

        // Ticks
        for (let i = 0; i <= majorTicks; i++) {
            const val = minVal + (maxVal - minVal) * (i / majorTicks);
            const simAngle = 225 - 270 * (i / majorTicks);
            const rad = (simAngle * Math.PI) / 180;
            const tx1 = x + (r - 25) * Math.cos(rad);
            const ty1 = y - (r - 25) * Math.sin(rad);
            const tx2 = x + (r - 10) * Math.cos(rad);
            const ty2 = y - (r - 10) * Math.sin(rad);
            ctx.beginPath();
            ctx.moveTo(tx1, ty1);
            ctx.lineTo(tx2, ty2);
            ctx.strokeStyle = "white";
            ctx.lineWidth = 2;
            ctx.stroke();

            const tx = x + (r - 40) * Math.cos(rad);
            const ty = y - (r - 40) * Math.sin(rad);
            ctx.fillStyle = "white";
            ctx.font = (r > 80 ? 14 : 10) + "px Arial";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(Math.floor(val).toString(), tx, ty);
        }

        if (iconType) {
            ctx.fillStyle = "#888";
            ctx.font = "bold 12px Arial";
            ctx.fillText(iconType.toUpperCase(), x, y - r / 2.5);
        } else {
            ctx.fillStyle = "#aaa";
            ctx.font = "bold 16px Arial";
            ctx.fillText(title, x, y + r / 2 + 5);
            ctx.fillStyle = "#888";
            ctx.font = "12px Arial";
            ctx.fillText(unit, x, y + r / 2 + 25);
        }
    }

    function updateNeedle(ctx, x, y, r, val, minVal, maxVal) {
        val = Math.max(minVal, Math.min(maxVal, val));
        const pct = (val - minVal) / (maxVal - minVal);
        const rad = ((225 - 270 * pct) * Math.PI) / 180;
        const tx = x + (r - 15) * Math.cos(rad);
        const ty = y - (r - 15) * Math.sin(rad);
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(tx, ty);
        ctx.strokeStyle = "#ff2222";
        ctx.lineWidth = 4;
        ctx.lineCap = "round";
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(x, y, 7, 0, 2 * Math.PI);
        ctx.fillStyle = "#111";
        ctx.fill();
        ctx.strokeStyle = "#555";
        ctx.lineWidth = 1;
        ctx.stroke();
    }

    let needle_values = {
        rpm: 0.8,
        speed: 0.0,
        oil: 15.0,
        coolant: 20.0,
        fuel: 1.0,
        batt: 12.0,
    };
    function smooth_value(key, target, max_change_rate, dt) {
        let current =
            needle_values[key] !== undefined ? needle_values[key] : target;
        const diff = target - current;
        const max_step = max_change_rate * dt;
        needle_values[key] =
            Math.abs(diff) <= max_step
                ? target
                : current + Math.sign(diff) * max_step;
        return needle_values[key];
    }

    function drawCenterScreen(ctx, stats) {
        const x1 = 540,
            y1 = 50, // 150 - 100
            x2 = 740,
            y2 = 250; // 350 - 100
        ctx.strokeStyle = "#444";
        ctx.lineWidth = 3;
        ctx.strokeRect(x1 - 4, y1 - 4, 208, 208);
        ctx.fillStyle = "black";
        ctx.fillRect(x1, y1, 200, 200);
        ctx.fillStyle = "#555";
        ctx.font = "bold 16px Courier";
        ctx.textAlign = "center";
        ctx.fillText("PRNDS", 640, y1 + 20);
        ctx.beginPath();
        ctx.moveTo(x1 + 10, y1 + 35);
        ctx.lineTo(x2 - 10, y1 + 35);
        ctx.strokeStyle = "#333";
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.fillStyle = "#555";
        ctx.font = "8px Arial";
        ctx.fillText("[SPACE] Change Page", 640, y2 + 15);

        const page = pages[pageIndex];
        ctx.fillStyle = "#888";
        ctx.font = "bold 9px Arial";
        ctx.fillText(`- ${page} -`, 640, y1 + 45);

        if (page === "MAIN") {
            ctx.fillStyle = "orange";
            ctx.font = "bold 45px Courier";
            ctx.fillText(stats.gear, 640, 130); // y-100
            ctx.fillStyle = "#555";
            ctx.font = "8px Arial";
            ctx.fillText("GEAR", 640, 105); // y-100
            ctx.fillStyle = "white";
            ctx.font = "bold 26px Courier";
            ctx.fillText(stats.speed_kmh, 640, 180); // y-100
            ctx.fillStyle = "#aaa";
            ctx.font = "8px Arial";
            ctx.fillText("km/h", 640, 200); // y-100
            ctx.fillStyle = "#aaa";
            ctx.font = "10px Courier";
            ctx.fillText(
                stats.speed_kmh > 5
                    ? `${stats.fuel_usage_l_100km} L/100`
                    : "--.- L/100",
                640,
                230, // y-100
            );
        } else if (page === "TRIP") {
            ctx.fillStyle = "#555";
            ctx.font = "8px Arial";
            ctx.fillText("RANGE", 640, 115); // y-100
            ctx.fillStyle = "#4f4";
            ctx.font = "bold 16px Courier";
            ctx.fillText(`${stats.range_km} km`, 640, 130); // y-100
            ctx.fillStyle = "#555";
            ctx.font = "8px Arial";
            ctx.fillText("ODOMETER", 640, 160); // y-100
            ctx.fillStyle = "white";
            ctx.font = "12px Courier";
            ctx.fillText(`${stats.odometer_km} km`, 640, 175); // y-100
            ctx.fillStyle = "#555";
            ctx.font = "8px Arial";
            ctx.fillText("AFR", 640, 205); // y-100
            ctx.fillStyle = "cyan";
            ctx.font = "12px Courier";
            ctx.fillText(`${stats.afr}:1`, 640, 220); // y-100
        } else if (page === "PERFORMANCE") {
            ctx.fillStyle = "#555";
            ctx.font = "8px Arial";
            ctx.fillText("HP", 600, 120); // y-100
            ctx.fillStyle = "orange";
            ctx.font = "bold 14px Courier";
            ctx.fillText(stats.power_hp, 600, 135); // y-100
            ctx.fillStyle = "#555";
            ctx.font = "8px Arial";
            ctx.fillText("TRQ", 680, 120); // y-100
            ctx.fillStyle = "orange";
            ctx.font = "bold 14px Courier";
            ctx.fillText(stats.torque_nm, 680, 135); // y-100
            ctx.fillStyle = "white";
            ctx.font = "12px Courier";
            ctx.fillText(`G-FORCE: ${stats.accel_g} G`, 640, 165); // y-100
            ctx.fillStyle = "#555";
            ctx.font = "8px Arial";
            ctx.fillText("0-100 km/h", 640, 200); // y-100
            ctx.fillStyle =
                stats.timer_0_100 > 0
                    ? "red"
                    : stats.best_0_100 > 0
                      ? "#4f4"
                      : "#444";
            ctx.font = "bold 14px Courier";
            ctx.fillText(
                `${stats.timer_0_100 > 0 ? stats.timer_0_100 : stats.best_0_100} s`,
                640,
                215, // y-100
            );
        } else if (page === "DIAGNOSTICS") {
            ctx.fillStyle = "#555";
            ctx.font = "7px Arial";
            ctx.fillText("TRANS TEMP", 590, 120); // y-100
            ctx.fillStyle = "white";
            ctx.font = "11px Courier";
            ctx.fillText(`${stats.trans_temp}°C`, 590, 135); // y-100
            ctx.fillStyle = "#555";
            ctx.font = "7px Arial";
            ctx.fillText("INTAKE AIR", 690, 120); // y-100
            ctx.fillStyle = "white";
            ctx.font = "11px Courier";
            ctx.fillText(`${stats.iat_temp}°C`, 690, 135); // y-100
            ctx.fillStyle = "#555";
            ctx.font = "7px Arial";
            ctx.fillText("CONV. SLIP", 590, 170); // y-100
            ctx.fillStyle = "orange";
            ctx.font = "11px Courier";
            ctx.fillText(stats.slip_rpm, 590, 185); // y-100
            ctx.fillStyle = "#555";
            ctx.font = "7px Arial";
            ctx.fillText("LOCKUP", 690, 170); // y-100
            ctx.fillStyle = stats.lockup ? "#4f4" : "#f44";
            ctx.font = "bold 10px Courier";
            ctx.fillText(stats.lockup ? "CLOSED" : "OPEN", 690, 185); // y-100
            ctx.fillStyle = "#aaa";
            ctx.font = "10px Courier";
            ctx.fillText(`OIL P: ${stats.oil_pressure} bar`, 640, 215); // y-100
        }
    }

    function loop(timestamp) {
        if (!sim) return;
        if (!lastTime) lastTime = timestamp;
        const dt = (timestamp - lastTime) / 1000;
        lastTime = timestamp;

        sim.set_inputs(
            gasMouse || gasKey ? 1.0 : 0.0,
            brakeMouse || brakeKey ? 1.0 : 0.0,
        );
        const statsProxy = sim.update(dt);
        const stats = statsProxy.toJs({ dict_converter: Object.fromEntries });
        statsProxy.destroy();

        ctx.fillStyle = "#2a2a2a";
        ctx.fillRect(0, 0, WIDTH, HEIGHT + PEDAL_HEIGHT);
        // Shifted all Y by -100
        drawGaugeBackground(ctx, 360, 180, 140, 0, 8, "x1000", 8, "RPM");
        drawGaugeBackground(ctx, 920, 180, 140, 0, 320, "km/h", 8);
        drawGaugeBackground(ctx, 140, 260, 75, 50, 150, "OIL", 2, "°C", "oil");
        drawGaugeBackground(ctx, 1140, 260, 75, 8, 16, "BATT", 2, "V", "batt");
        drawGaugeBackground(
            ctx,
            570,
            330,
            45,
            50,
            130,
            "ENGINE",
            2,
            "",
            "temp",
        );
        drawGaugeBackground(ctx, 710, 330, 45, 0, 1, "FUEL", 2, "", "fuel");
        drawCenterScreen(ctx, stats);

        updateNeedle(
            ctx,
            360,
            180,
            140,
            smooth_value("rpm", stats.rpm / 1000, 8.0, dt),
            0,
            8,
        );
        updateNeedle(
            ctx,
            920,
            180,
            140,
            smooth_value("speed", stats.speed_kmh, 160.0, dt),
            0,
            320,
        );
        updateNeedle(
            ctx,
            140,
            260,
            75,
            smooth_value("oil", parseFloat(stats.oil_temp), 10.0, dt),
            50,
            150,
        );
        updateNeedle(
            ctx,
            1140,
            260,
            75,
            smooth_value(
                "batt",
                11.5 + (parseFloat(stats.battery_pct) / 100) * 3.0,
                2.0,
                dt,
            ),
            8,
            16,
        );
        updateNeedle(
            ctx,
            570,
            330,
            45,
            smooth_value("coolant", parseFloat(stats.engine_temp), 10.0, dt),
            50,
            130,
        );
        updateNeedle(
            ctx,
            710,
            330,
            45,
            smooth_value("fuel", parseFloat(stats.fuel_ltr) / 90.0, 0.05, dt),
            0,
            1,
        );

        ctx.fillStyle = "#151515";
        ctx.fillRect(0, HEIGHT, WIDTH, PEDAL_HEIGHT);
        drawPedal(
            ctx,
            200,
            HEIGHT + 15,
            120,
            140,
            "BRAKE\n(Down Arrow)",
            brakeMouse || brakeKey ? "#ff4444" : "#882222",
        );
        drawPedal(
            ctx,
            WIDTH - 300,
            HEIGHT + 15,
            100,
            140,
            "GAS\n(Up Arrow)",
            gasMouse || gasKey ? "#44ff44" : "#228822",
        );

        animationId = requestAnimationFrame(loop);
    }

    function handleMouseDown(e) {
        const rect = canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) * (WIDTH / rect.width);
        const y =
            (e.clientY - rect.top) * ((HEIGHT + PEDAL_HEIGHT) / rect.height);
        if (y > HEIGHT + 15 && y < HEIGHT + 155) {
            if (x > 200 && x < 320) brakeMouse = true;
            if (x > WIDTH - 300 && x < WIDTH - 200) gasMouse = true;
        }
    }
    function handleMouseUp() {
        brakeMouse = false;
        gasMouse = false;
    }

    onMount(() => {
        ctx = canvas.getContext("2d");
        window.addEventListener("keydown", handleKeyDown);
        window.addEventListener("keyup", handleKeyUp);
        animationId = requestAnimationFrame(loop);
    });

    onDestroy(() => {
        window.removeEventListener("keydown", handleKeyDown);
        window.removeEventListener("keyup", handleKeyUp);
        cancelAnimationFrame(animationId);
    });
</script>

<div class="sim-container">
    <canvas
        bind:this={canvas}
        width={WIDTH}
        height={HEIGHT + PEDAL_HEIGHT}
        on:mousedown={handleMouseDown}
        on:mouseup={handleMouseUp}
        on:mouseleave={handleMouseUp}
    ></canvas>
</div>

<style>
    .sim-container {
        width: 100%;
        display: flex;
        justify-content: center;
        background-color: #2a2a2a;
        border-radius: 4px;
        overflow: hidden;
    }
    canvas {
        max-width: 100%;
        height: auto;
    }
</style>
