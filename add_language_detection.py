import os

with open('language.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

def get_html_files():
    files = []
    if os.path.exists('index.html'):
        files.append(('index.html', False))
    for entry in os.listdir('.'):
        if os.path.isdir(entry):
            idx = os.path.join(entry, 'index.html')
            if os.path.exists(idx):
                files.append((idx, True))
    return files

for file, is_sub in get_html_files():
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    script_src = '../language.js' if is_sub else 'language.js'
    if f'<script src="{script_src}"></script>' not in content:
        content = content.replace('</head>', f'  <script src="{script_src}"></script>\n</head>')
    
    if 'onchange="location = this.value;"' in content:
        content = content.replace('onchange="location = this.value;"', 'onchange="changeLanguage(this.value);"')
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Language detection implemented in all HTML files.")
