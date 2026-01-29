import os
import re

# The ONE standard navigation bar
STANDARD_NAV = """<nav>
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
</nav>"""

# The ONE standard footer (Fixed dead clicks & added dynamic year class)
STANDARD_FOOTER = """<footer>
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
</script>"""

for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace varying navbars
        content = re.sub(r'<nav>.*?</nav>', STANDARD_NAV, content, flags=re.DOTALL)
        
        # Replace varying footers
        content = re.sub(r'<footer.*?</footer>', STANDARD_FOOTER, content, flags=re.DOTALL)
        
        # Replace hardcoded 2024 references in index.html text
        if filename == 'index.html':
            content = content.replace('Read the 2024 Executive Report', 'Read the <span class="dynamic-year">2026</span> Executive Report')
            content = content.replace('based on 2024 hardware', 'based on <span class="dynamic-year">2026</span> hardware')

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

print("Successfully unified Navigation, Footers, and Dates across all HTML files!")
