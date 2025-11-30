// Prognosis AI - Compute Essay Visualizations
// Author: Antigravity
// Date: Nov 2025
// Style: Professional Data-Viz (Think Tank / Consulting)

(function () {
    // --- Global Style Constants ---
    const COLORS = {
        paper: '#F2F0E6',
        ink: '#1A1C1B',
        inkSoft: '#4A4D4B',
        accent: '#D64000',
        grid: '#D1CEC4',
        blue: '#0056b3',
        purple: '#6f42c1',
        green: '#28a745',
        red: '#dc3545',
        orange: '#fd7e14'
    };

    const FONTS = {
        label: '11px "JetBrains Mono", monospace',
        title: 'bold 12px "JetBrains Mono", monospace',
        axis: '10px "JetBrains Mono", monospace'
    };

    // Utility: Setup Canvas with Dynamic Height
    function setupCanvas(id, aspectRatio = 2) {
        const canvas = document.getElementById(id);
        if (!canvas) {
            // console.warn(`Canvas with ID '${id}' not found.`); // Suppress warning for removed Fig 9
            return null;
        }
        const ctx = canvas.getContext('2d');
        const dpr = window.devicePixelRatio || 1;

        const rect = canvas.getBoundingClientRect();
        const width = rect.width;
        const height = width / aspectRatio;

        canvas.style.width = `${width}px`;
        canvas.style.height = `${height}px`;

        canvas.width = width * dpr;
        canvas.height = height * dpr;

        ctx.scale(dpr, dpr);

        return { canvas, ctx, width, height };
    }

    // --- Visualization 1: The Ladder of Oomph ---
    // Fix: Remove empty space. Tighter log scale.
    // Aspect: Short (2.5)
    function initLadderOfOomph() {
        const setup = setupCanvas('viz-oomph', 2.5);
        if (!setup) return;
        const { ctx, width, height } = setup;

        const data = [
            { label: 'Human Brain', sub: '~20W', val: 16 },
            { label: 'H100 Cluster', sub: '100k (30MW)', val: 24 },
            { label: 'GPT-4 Train', sub: 'Est.', val: 25 },
            { label: 'Blackwell', sub: '100k (120MW)', val: 27 },
            { label: 'Stargate', sub: '5GW', val: 29 }
        ];

        // Tight bounds
        const minLog = 15;
        const maxLog = 30;

        function draw() {
            ctx.clearRect(0, 0, width, height);

            const yBase = height - 25;
            const chartH = height - 50;

            // Axis
            ctx.beginPath(); ctx.moveTo(50, yBase); ctx.lineTo(width - 20, yBase);
            ctx.strokeStyle = COLORS.ink; ctx.lineWidth = 1; ctx.stroke();

            // Ticks
            for (let i = minLog; i <= maxLog; i += 2) {
                const x = 50 + ((i - minLog) / (maxLog - minLog)) * (width - 70);
                ctx.fillStyle = COLORS.inkSoft; ctx.font = FONTS.axis;
                ctx.fillText(`10^${i}`, x, yBase + 15);
                ctx.beginPath(); ctx.moveTo(x, yBase); ctx.lineTo(x, yBase + 4); ctx.stroke();
            }

            // Bars
            const barHeight = 18; // Thinner bars
            const gap = 12;

            data.forEach((d, i) => {
                const x = 50 + ((d.val - minLog) / (maxLog - minLog)) * (width - 70);
                const y = yBase - 30 - (i * (barHeight + gap));

                ctx.fillStyle = i === data.length - 1 ? COLORS.accent : COLORS.inkSoft;
                ctx.fillRect(50, y, x - 50, barHeight);

                ctx.fillStyle = COLORS.ink; ctx.font = FONTS.title;
                ctx.fillText(d.label, 50, y - 4);

                ctx.fillStyle = COLORS.inkSoft; ctx.font = FONTS.label;
                ctx.fillText(d.sub, 200, y - 4);
            });
        }
        draw();
    }

    // --- Visualization 2: Exploded Blackwell ---
    function initExplodedBlackwell() {
        const setup = setupCanvas('viz-blackwell', 1.8);
        if (!setup) return;
        const { ctx, width, height } = setup;
        let time = 0;

        function draw() {
            ctx.clearRect(0, 0, width, height);
            const cx = width / 2;
            const cy = height / 2 + 30;
            const t = (Math.sin(time * 0.02) + 1) / 2;

            const layers = [
                { name: 'Organic Substrate', w: 240, h: 140, yBase: 80, yMove: 0, color: '#e0e0e0' },
                { name: 'CoWoS-L Interposer', w: 220, h: 120, yBase: 40, yMove: 20, color: '#d0d0d0' },
                { name: 'LSI Bridge (Stitch)', w: 40, h: 100, yBase: 40, yMove: 20, color: '#d0d0d0' },
                { name: 'GPU Die 1', w: 100, h: 90, yBase: 0, yMove: 50, xOffset: -55, color: '#1A1C1B' },
                { name: 'GPU Die 2', w: 100, h: 90, yBase: 0, yMove: 50, xOffset: 55, color: '#1A1C1B' },
                { name: 'HBM3e Stacks', w: 200, h: 40, yBase: -40, yMove: 80, color: '#4A4D4B' }
            ];

            layers.forEach((l) => {
                const y = cy + l.yBase - (l.yMove * t);
                const x = cx + (l.xOffset || 0);
                ctx.fillStyle = l.highlight ? COLORS.accent : (l.color || '#fff');
                ctx.fillRect(x - l.w / 2, y - l.h / 2, l.w, l.h);
                ctx.strokeStyle = COLORS.ink; ctx.strokeRect(x - l.w / 2, y - l.h / 2, l.w, l.h);

                const isDark = l.color === '#1A1C1B' || l.color === '#4A4D4B' || l.highlight;
                if (t > 0.1 || l.yMove === 0) {
                    ctx.fillStyle = isDark ? '#fff' : COLORS.ink;
                    ctx.textAlign = 'center'; ctx.font = FONTS.label;
                    ctx.fillText(l.name, x, y + 4);
                }
            });

            if (t > 0.5) {
                ctx.beginPath(); ctx.moveTo(cx, cy + 40 - (20 * t)); ctx.lineTo(cx + 140, cy + 40 - (20 * t));
                ctx.strokeStyle = COLORS.accent; ctx.setLineDash([2, 2]); ctx.stroke(); ctx.setLineDash([]);
                ctx.fillStyle = COLORS.accent; ctx.textAlign = 'left'; ctx.font = FONTS.title;
                ctx.fillText("10 TB/s NV-HBI", cx + 145, cy + 44 - (20 * t));
            }
            time++; requestAnimationFrame(draw);
        }
        draw();
    }

    // --- Visualization 3: ASML Schematic ---
    function initASMLSchematic() {
        const setup = setupCanvas('viz-asml', 2);
        if (!setup) return;
        const { ctx, width, height } = setup;
        let highNA = false;
        let time = 0;

        const btnLow = document.getElementById('btn-low-na');
        const btnHigh = document.getElementById('btn-high-na');
        if (btnLow && btnHigh) {
            btnLow.onclick = () => { highNA = false; updateBtns(); };
            btnHigh.onclick = () => { highNA = true; updateBtns(); };
        }
        function updateBtns() {
            if (btnLow) btnLow.classList.toggle('active', !highNA);
            if (btnHigh) btnHigh.classList.toggle('active', highNA);
        }

        function draw() {
            ctx.clearRect(0, 0, width, height);
            const cx = width / 2;
            const ySource = 30, yMask = 80, yLens = 140, yWafer = 200;

            ctx.fillStyle = COLORS.accent; ctx.beginPath(); ctx.arc(cx, ySource, 8, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = COLORS.ink; ctx.textAlign = 'right'; ctx.font = FONTS.label; ctx.fillText("EUV Source", cx - 20, ySource + 4);

            ctx.fillStyle = COLORS.inkSoft; ctx.fillRect(cx - 30, yMask, 60, 6);
            ctx.textAlign = 'right'; ctx.fillText("Mask", cx - 40, yMask + 4);

            const lensWidth = highNA ? 120 : 80;
            ctx.fillStyle = 'rgba(0, 86, 179, 0.1)'; ctx.strokeStyle = COLORS.blue;
            ctx.beginPath(); ctx.ellipse(cx, yLens, lensWidth / 2, 15, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            ctx.textAlign = 'right'; ctx.fillStyle = COLORS.ink; ctx.fillText(highNA ? "High-NA (0.55)" : "Low-NA (0.33)", cx - 80, yLens + 4);

            ctx.fillStyle = COLORS.ink; ctx.fillRect(cx - 80, yWafer, 160, 4);
            ctx.textAlign = 'right'; ctx.fillText("Wafer", cx - 90, yWafer + 6);

            const coneWidth = highNA ? 60 : 30;
            ctx.fillStyle = 'rgba(214, 0, 0, 0.1)';
            ctx.beginPath(); ctx.moveTo(cx, ySource); ctx.lineTo(cx - 15, yMask); ctx.lineTo(cx + 15, yMask); ctx.fill();
            ctx.beginPath(); ctx.moveTo(cx, yMask + 6); ctx.lineTo(cx - lensWidth / 2, yLens); ctx.lineTo(cx + lensWidth / 2, yLens); ctx.fill();
            ctx.beginPath(); ctx.moveTo(cx, yLens); ctx.lineTo(cx - coneWidth, yWafer); ctx.lineTo(cx + coneWidth, yWafer); ctx.fill();

            time++; requestAnimationFrame(draw);
        }
        draw();
    }

    // --- Visualization 4: Memory Funnel (Schematic) ---
    // Fix: Clean schematic, no noise.
    // Aspect: Standard (2)
    function initMemoryFunnel() {
        const setup = setupCanvas('viz-memory', 2);
        if (!setup) return;
        const { ctx, width, height } = setup;

        function draw() {
            ctx.clearRect(0, 0, width, height);
            const cx = width / 2;
            const cy = height / 2;

            // Funnel Shape
            ctx.beginPath();
            ctx.moveTo(cx - 150, cy - 80); // Top Left
            ctx.lineTo(cx + 150, cy - 80); // Top Right
            ctx.lineTo(cx + 20, cy + 20);  // Neck Right
            ctx.lineTo(cx + 20, cy + 80);  // Bottom Right
            ctx.lineTo(cx - 20, cy + 80);  // Bottom Left
            ctx.lineTo(cx - 20, cy + 20);  // Neck Left
            ctx.closePath();

            ctx.fillStyle = 'rgba(26, 28, 27, 0.05)';
            ctx.fill();
            ctx.strokeStyle = COLORS.ink;
            ctx.lineWidth = 2;
            ctx.stroke();

            // Labels
            ctx.fillStyle = COLORS.ink;
            ctx.textAlign = 'center';

            // Top: Compute
            ctx.font = FONTS.title;
            ctx.fillText("Potential Compute", cx, cy - 90);
            ctx.font = FONTS.label;
            ctx.fillText("4 PetaFLOPS (Ready)", cx, cy - 60);

            // Neck: Bandwidth
            ctx.fillStyle = COLORS.accent;
            ctx.fillText("Memory Bandwidth Wall", cx + 120, cy + 20);
            ctx.beginPath(); ctx.moveTo(cx + 25, cy + 15); ctx.lineTo(cx + 60, cy + 15); ctx.stroke();

            // Bottom: Throughput
            ctx.fillStyle = COLORS.ink;
            ctx.fillText("Actual Throughput", cx, cy + 100);
            ctx.font = FONTS.label;
            ctx.fillText("~10% Utilization", cx, cy + 115);
        }
        draw();
    }

    // --- Visualization 5: SRAM Race Track ---
    function initSRAMRaceTrack() {
        const setup = setupCanvas('viz-sram', 3.5);
        if (!setup) return;
        const { ctx, width, height } = setup;
        let groqX = 50, nvidiaX = 50;

        function draw() {
            ctx.clearRect(0, 0, width, height);
            const yGroq = 40, yNvidia = 80;

            ctx.strokeStyle = COLORS.grid;
            ctx.beginPath();
            ctx.moveTo(50, yGroq); ctx.lineTo(width - 50, yGroq);
            ctx.moveTo(50, yNvidia); ctx.lineTo(width - 50, yNvidia);
            ctx.stroke();

            ctx.fillStyle = COLORS.ink; ctx.textAlign = 'left'; ctx.font = FONTS.label;
            ctx.fillText("Groq (SRAM) - 0.5ns", 50, yGroq - 10);
            ctx.fillText("NVIDIA (HBM) - 50ns", 50, yNvidia - 10);

            groqX += 15; if (groqX > width - 50) groqX = 50;
            nvidiaX += 1; if (nvidiaX > width - 50) nvidiaX = 50;

            ctx.fillStyle = COLORS.accent; ctx.fillRect(groqX, yGroq - 5, 20, 10);
            ctx.fillStyle = COLORS.inkSoft; ctx.fillRect(nvidiaX, yNvidia - 5, 20, 10);
            requestAnimationFrame(draw);
        }
        draw();
    }

    // --- Visualization 6: Networking (Visible Spraying) ---
    // Fix: Thicker lines, wider spread.
    function initNetworkingComparison() {
        const setup = setupCanvas('viz-networking', 2.5);
        if (!setup) return;
        const { ctx, width, height } = setup;

        const packetsLeft = [];
        const packetsRight = [];

        function draw() {
            ctx.clearRect(0, 0, width, height);
            const mid = width / 2;

            ctx.strokeStyle = COLORS.grid; ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(mid, 10); ctx.lineTo(mid, height - 10); ctx.stroke();

            ctx.fillStyle = COLORS.ink; ctx.textAlign = 'center'; ctx.font = FONTS.title;
            ctx.fillText("Traditional ECMP", mid / 2, 20);
            ctx.fillText("UEC Packet Spraying", mid + mid / 2, 20);

            // Left (Collision)
            const yStart = height / 2 + 10;
            ctx.strokeStyle = COLORS.inkSoft; ctx.lineWidth = 2; // Thicker
            ctx.beginPath(); ctx.moveTo(50, yStart); ctx.lineTo(mid - 50, yStart); ctx.stroke();

            if (Math.random() < 0.1) packetsLeft.push({ x: 50 });
            packetsLeft.forEach((p, i) => {
                p.x += 2; if (p.x > mid - 50) packetsLeft.splice(i, 1);
                ctx.fillStyle = COLORS.ink; ctx.beginPath(); ctx.arc(p.x, yStart, 4, 0, Math.PI * 2); ctx.fill();
            });

            // Right (Spraying)
            // Wider spread: -40 to +40
            const paths = [-40, -20, 0, 20, 40];
            if (Math.random() < 0.2) packetsRight.push({ t: 0, path: Math.floor(Math.random() * 5) });

            packetsRight.forEach((p, i) => {
                p.t += 0.02; if (p.t > 1) packetsRight.splice(i, 1);
                const offset = paths[p.path];
                const x = (1 - p.t) * (1 - p.t) * (mid + 50) + 2 * (1 - p.t) * p.t * (mid + mid / 2) + p.t * p.t * (width - 50);
                const y = (1 - p.t) * (1 - p.t) * yStart + 2 * (1 - p.t) * p.t * (yStart + offset * 2) + p.t * p.t * yStart;

                // Draw Path Trace
                ctx.strokeStyle = 'rgba(214, 0, 0, 0.1)'; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(mid + 50, yStart);
                ctx.quadraticCurveTo(mid + mid / 2, yStart + offset * 2, width - 50, yStart);
                ctx.stroke();

                ctx.fillStyle = COLORS.accent; ctx.beginPath(); ctx.arc(x, y, 3, 0, Math.PI * 2); ctx.fill();
            });

            requestAnimationFrame(draw);
        }
        draw();
    }

    // --- Visualization 7: Optical Mesh ---
    function initOpticalMesh() {
        const setup = setupCanvas('viz-google', 2);
        if (!setup) return;
        const { ctx, width, height } = setup;
        const cols = 6, rows = 3;
        const cellW = (width - 100) / cols;
        const cellH = (height - 80) / rows;
        let frame = 0, failureState = 0;

        function draw() {
            ctx.clearRect(0, 0, width, height);
            if (frame % 300 === 0) failureState = 0;
            else if (frame % 300 === 60) failureState = 1;
            else if (frame % 300 === 120) failureState = 2;
            else if (frame % 300 === 180) failureState = 3;

            ctx.fillStyle = COLORS.ink; ctx.textAlign = 'center'; ctx.font = FONTS.title;
            let status = "Normal Operation";
            if (failureState === 1) status = "Node Failure Detected";
            if (failureState === 2) status = "Traffic Blocked (Red)";
            if (failureState === 3) status = "OCS Reconfiguration (Bypass)";
            ctx.fillText(status, width / 2, 20);

            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    const x = 50 + c * cellW, y = 50 + r * cellH;
                    const isFailNode = r === 1 && c === 2;
                    const isNeighbor = (r === 1 && c === 1) || (r === 1 && c === 3);

                    ctx.strokeStyle = COLORS.grid; ctx.lineWidth = 1;
                    ctx.beginPath();
                    if (c < cols - 1) { ctx.moveTo(x, y); ctx.lineTo(x + cellW, y); }
                    if (r < rows - 1) { ctx.moveTo(x, y); ctx.lineTo(x, y + cellH); }
                    ctx.stroke();

                    if (failureState === 3 && isNeighbor && c === 1) {
                        ctx.strokeStyle = COLORS.green; ctx.lineWidth = 2;
                        ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(x + cellW, y - 40, x + cellW * 2, y); ctx.stroke();
                    }

                    let color = COLORS.ink;
                    if (isFailNode && failureState >= 1) color = COLORS.red;
                    if (isNeighbor && failureState === 2) color = COLORS.orange;
                    if (isNeighbor && failureState === 3) color = COLORS.green;
                    ctx.fillStyle = color; ctx.beginPath(); ctx.arc(x, y, 5, 0, Math.PI * 2); ctx.fill();
                }
            }
            frame++; requestAnimationFrame(draw);
        }
        draw();
    }

    // --- Visualization 8: Cost Breakdown (Stacked) ---
    // Fix: Stacked Bar (CapEx + OpEx)
    function initCostBreakdown() {
        const setup = setupCanvas('viz-trainium', 2);
        if (!setup) return;
        const { ctx, width, height } = setup;

        const data = [
            { name: 'NVIDIA H100', capex: 70, opex: 30 }, // Total 100
            { name: 'AWS Trainium 2', capex: 25, opex: 30 } // Total 55
        ];

        function draw() {
            ctx.clearRect(0, 0, width, height);

            const barWidth = 80;
            const spacing = 100;
            const startX = width / 2 - (barWidth * 2 + spacing) / 2;
            const bottomY = height - 40;

            // Axis
            ctx.beginPath(); ctx.moveTo(50, bottomY); ctx.lineTo(width - 50, bottomY);
            ctx.strokeStyle = COLORS.ink; ctx.stroke();

            // Bars
            data.forEach((d, i) => {
                const x = startX + i * (barWidth + spacing);

                // CapEx (Bottom)
                const hCapex = (d.capex / 100) * (height - 80);
                // OpEx (Top)
                const hOpex = (d.opex / 100) * (height - 80);

                // Draw CapEx
                ctx.fillStyle = COLORS.inkSoft;
                ctx.fillRect(x, bottomY - hCapex, barWidth, hCapex);

                // Draw OpEx
                ctx.fillStyle = COLORS.accent;
                ctx.fillRect(x, bottomY - hCapex - hOpex, barWidth, hOpex);

                // Labels
                ctx.fillStyle = COLORS.ink; ctx.textAlign = 'center'; ctx.font = FONTS.label;
                ctx.fillText(d.name, x + barWidth / 2, bottomY + 20);

                // Values
                ctx.fillStyle = '#fff';
                if (hCapex > 20) ctx.fillText("CapEx", x + barWidth / 2, bottomY - hCapex / 2 + 4);
                if (hOpex > 20) ctx.fillText("OpEx", x + barWidth / 2, bottomY - hCapex - hOpex / 2 + 4);

                // Total
                ctx.fillStyle = COLORS.ink; ctx.font = 'bold 14px "JetBrains Mono"';
                ctx.fillText(`${d.capex + d.opex}%`, x + barWidth / 2, bottomY - hCapex - hOpex - 10);
            });

            ctx.fillStyle = COLORS.ink; ctx.textAlign = 'center'; ctx.font = FONTS.title;
            ctx.fillText("TCO Breakdown: Hardware vs Energy", width / 2, 20);
        }
        draw();
    }

    // --- Visualization 10: Pipeline Bubble ---
    function initPipelineBubble() {
        const setup = setupCanvas('viz-orchestra', 2);
        if (!setup) return;
        const { ctx, width, height } = setup;
        let offset = 0;

        function draw() {
            ctx.clearRect(0, 0, width, height);
            const rows = 4, cols = 8;
            const cellW = (width - 100) / cols;
            const cellH = (height - 60) / rows;
            offset += 0.02; if (offset > 1) offset = 0;

            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    const x = 50 + c * cellW, y = 30 + r * cellH;
                    const isBubble = (c - r) < 0;
                    ctx.strokeStyle = COLORS.grid; ctx.strokeRect(x, y, cellW, cellH);
                    if (!isBubble) {
                        ctx.fillStyle = COLORS.ink;
                        const fillH = cellH * ((Math.sin(offset * Math.PI * 2 + c) + 1) / 2);
                        ctx.fillRect(x, y + (cellH - fillH), cellW, fillH);
                    } else {
                        ctx.fillStyle = 'rgba(214, 0, 0, 0.1)'; ctx.fillRect(x, y, cellW, cellH);
                    }
                }
            }
            ctx.fillStyle = COLORS.accent; ctx.textAlign = 'center'; ctx.font = FONTS.title;
            ctx.fillText("Pipeline Bubbles (Red) = Idle Cash", width / 2, height - 10);
            requestAnimationFrame(draw);
        }
        draw();
    }

    // Initialize
    document.addEventListener('DOMContentLoaded', () => {
        initLadderOfOomph();
        initExplodedBlackwell();
        initASMLSchematic();
        initMemoryFunnel();
        initSRAMRaceTrack();
        initNetworkingComparison();
        initOpticalMesh();
        initCostBreakdown();
        // initInferenceIceberg(); // Removed
        initPipelineBubble();
    });

})();
