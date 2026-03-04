import os
import re

# Order of sections
sections = [
    "part1_intro.html",
    "part2_blackwell.html",
    "part3_asml.html",
    "part4_memory.html",
    "part5_sram.html",
    "part6_networking.html",
    "part7_google.html",
    "part8_trainium.html",
    "part9_inference.html",
    "part10_orchestra.html",
    "part11_conclusion.html"
]

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, "compute_sections")
output_file = os.path.join(script_dir, "compute.html")

# UPDATED: Use the SAME standard nav/footer as standardize_layout.py
header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compute-Centric Scaling: The Engine of AI</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&display=swap" rel="stylesheet">
    <!-- MathJax -->
    <script>window.MathJax = { tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] }, svg: { fontCache: 'global' } };</script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <!-- Plotly -->
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    
    <link rel="stylesheet" href="article-theme.css">
</head>
<body>

<nav>
    <div class="nav-left" style="display: flex; gap: 2rem; align-items: baseline;">
        <a href="index.html" class="logo t-tight" style="font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 1.4rem; letter-spacing: -0.02em; color: var(--c-ink); text-decoration: none;">PROGNOSIS</a>
        <div class="nav-status mono caps" style="font-size: 0.7rem; color: var(--c-accent); display: flex; align-items: center; gap: 0.5rem;">
            <div class="status-dot" style="width: 6px; height: 6px; background: var(--c-accent); border-radius: 50%; animation: pulse 2s infinite;"></div>
            Live Model Inference
        </div>
    </div>
    <div class="nav-links" style="display: flex; gap: 2rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase;">
        <a href="index.html">Trends</a>
        <a href="research.html">Publications</a>
        <a href="models.html">Models</a>
        <a href="about.html">About</a>
    </div>
</nav>

    <div class="container fade-in">
        <article>
            <h1>Compute-Centric Scaling</h1>
            <div class="meta-block">
                <div class="meta-item"><label>Author</label><span>Ramesh</span></div>
                <div class="meta-item"><label>Date</label><span>November 26, 2025</span></div>
                <div class="meta-item"><label>Category</label><span>Deep Dive</span></div>
            </div>
"""

footer = """
        </article>
    </div>

<footer>
    <div class="footer-col" style="display: flex; flex-direction: column; gap: 1rem;">
        <div class="logo t-tight" style="font-size: 1rem; color: var(--c-ink); font-family: 'JetBrains Mono', monospace; font-weight: bold;">PROGNOSIS</div>
        <div>1200 17th St NW, Suite 500<br>Washington, DC 20036</div>
        <div>&copy; <span class="dynamic-year">2026</span> Prognosis Research Institute</div>
    </div>
    <div class="footer-col" style="align-items: flex-end; text-align: right; display: flex; flex-direction: column; gap: 1rem;">
        <div class="footer-links" style="display: flex; gap: 2rem;">
            <!-- REPLACED DEAD CLICKS WITH ACTUAL LINKS OR DISABLED SPANS -->
            <a href="https://twitter.com/yourhandle" target="_blank">Twitter / X</a>
            <a href="https://github.com/rachitgupta007/Prognosis-AI" target="_blank">GitHub</a>
            <span style="opacity: 0.5; cursor: not-allowed;" title="Coming Soon">Substack</span>
        </div>
        <div style="margin-top: 1rem;">
            <input type="email" class="newsletter-input" placeholder="Email for updates..." style="background: transparent; border: none; border-bottom: 1px solid var(--c-ink-soft); font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; padding: 0.5rem 0; width: 200px; color: var(--c-ink); outline: none;">
        </div>
        <div style="margin-top: 0.5rem; opacity: 0.6; font-size: 0.75rem;">501(c)(3) Non-Profit Organization</div>
    </div>
</footer>

<!-- Global Script to handle active nav states and dynamic years -->
<script>
    document.addEventListener('DOMContentLoaded', () => {
        // Dynamic Year Update
        const currentYear = new Date().getFullYear();
        document.querySelectorAll('.dynamic-year').forEach(el => el.textContent = currentYear);
        
        // Active Nav State Highlighting
        const currentPath = window.location.pathname.split('/').pop() || 'index.html';
        document.querySelectorAll('.nav-links a').forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
                link.style.opacity = '1';
                link.style.color = 'var(--c-accent)';
            }
        });
    });
</script>

    <script src="compute_viz.js"></script>
</body>
</html>
"""

def extract_body_content(html_content):
    # Regex to extract content between <body> and <script> or </body>
    # We want to ignore the <body> tag itself and the <script> tag at the end
    match = re.search(r'<body[^>]*>(.*?)<script', html_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback if no script tag
    match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return ""

full_content = header

for section_file in sections:
    path = os.path.join(base_dir, section_file)
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
            body_content = extract_body_content(content)
            # Remove the h1 title from individual sections if it duplicates the main title?
            # Actually, the sections use h1 for their section titles. 
            # Let's demote h1 to h2 in sections to maintain hierarchy, 
            # EXCEPT for the very first section if it's the main title.
            # But my sections have specific titles like "1. Thermodynamics".
            # So I will replace <h1> with <h2> in the extracted content.
            
            body_content = body_content.replace("<h1>", "<h2>").replace("</h1>", "</h2>")
            
            full_content += f"\n<!-- SECTION: {section_file} -->\n"
            full_content += body_content
            full_content += "\n"

full_content += footer

with open(output_file, 'w') as f:
    f.write(full_content)

print(f"Successfully assembled {output_file}")
