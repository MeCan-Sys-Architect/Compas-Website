import os
import re

def get_html_files():
    files = []
    if os.path.exists('index.html'):
        files.append('index.html')
    for entry in sorted(os.listdir('.')):
        if os.path.isdir(entry):
            idx = os.path.join(entry, 'index.html')
            if os.path.exists(idx):
                files.append(idx)
    return files

html_files = get_html_files()

missing = []
for file in html_files:
    base_dir = os.path.dirname(file) or '.'
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Check local src attributes
    for src in re.findall(r'src=["\']([^"\']+)["\']', content):
        if src.startswith(('http://', 'https://', '//')):
            continue
        resolved = os.path.normpath(os.path.join(base_dir, src))
        if not os.path.exists(resolved):
            missing.append((file, 'src', src, resolved))
    # Check local href attributes
    for href in re.findall(r'href=["\']([^"\']+)["\']', content):
        if href.startswith(('http://', 'https://', 'mailto:', '#', '/index.css')):
            continue
        clean_href = href.split('?')[0].split('#')[0]
        if not clean_href:
            continue
        resolved = os.path.normpath(os.path.join(base_dir, clean_href))
        if not (os.path.exists(resolved) or os.path.exists(os.path.join(resolved, 'index.html'))):
            missing.append((file, 'href', href, resolved))

if missing:
    print("Found missing links/assets:")
    for item in missing:
        print(" ", item)
else:
    print("All HTML links, images, videos, icons, and downloads resolve to existing files!")
