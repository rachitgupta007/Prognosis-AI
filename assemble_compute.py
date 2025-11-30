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

base_dir = "/Users/ramesh/Desktop/Prognosis AI/compute_sections"
output_file = "/Users/ramesh/Desktop/Prognosis AI/compute.html"

# Header Template
header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compute-Centric Scaling: The Engine of AI</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0a0a0a;
            --text-color: #e0e0e0;
            --accent-color: #4CAF50;
            --card-bg: #111;
            --border-color: #333;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }
        header {
            background: rgba(10, 10, 10, 0.9);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 1rem 2rem;
        }
        nav ul {
            display: flex;
            list-style: none;
            gap: 2rem;
            margin: 0;
            padding: 0;
            justify-content: center;
        }
        nav a {
            color: #888;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }
        nav a:hover, nav a.active {
            color: #fff;
        }
        main {
            max-width: 800px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }
        article {
            animation: fadeIn 1s ease-out;
        }
        h1 {
            font-size: 3.5rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 0.5rem;
            background: linear-gradient(180deg, #fff, #666);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        h2 {
            font-size: 2rem;
            margin-top: 4rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid #333;
            padding-bottom: 0.5rem;
        }
        h3 {
            font-size: 1.5rem;
            margin-top: 2.5rem;
            color: #fff;
        }
        p {
            margin-bottom: 1.5rem;
            font-size: 1.125rem;
            color: #ccc;
        }
        .byline {
            color: #666;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 4rem;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .viz-container {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 3rem 0;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            position: relative;
            overflow: hidden;
        }
        canvas {
            width: 100%;
            height: 400px;
            display: block;
        }
        .caption {
            font-family: 'JetBrains Mono', monospace;
            color: #666;
            font-size: 0.85rem;
            margin-top: 1rem;
            text-align: center;
            border-top: 1px solid #222;
            padding-top: 0.5rem;
        }
        blockquote {
            border-left: 4px solid var(--accent-color);
            padding-left: 1.5rem;
            margin: 2rem 0;
            font-style: italic;
            color: #fff;
            background: rgba(255,255,255,0.05);
            padding: 1.5rem;
            border-radius: 0 8px 8px 0;
        }
        code {
            font-family: 'JetBrains Mono', monospace;
            background: #222;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-size: 0.9em;
            color: #ff9900;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
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
