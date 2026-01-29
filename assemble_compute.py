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

# Header Template
header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compute-Centric Scaling: The Engine of AI</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="article-theme.css">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="index.html">Prognosis AI</a></li>
                <li><a href="models.html">Models</a></li>
                <li><a href="compute.html" class="active">Compute</a></li>
                <li><a href="energy.html">Energy</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <article>
            <h1>Compute-Centric Scaling</h1>
            <p class="byline">By Ramesh | November 26, 2025 | Deep Dive</p>
"""

footer = """
        </article>
    </main>

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
