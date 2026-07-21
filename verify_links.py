import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# Extract all links
all_links = set()
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        links = re.findall(r'href="([^"]+\.html)"', content)
        for link in links:
            all_links.add(link)
        links = re.findall(r'value="([^"]+\.html)"', content)
        for link in links:
            all_links.add(link)

missing = []
for link in all_links:
    if not os.path.exists(link):
        missing.append(link)

if missing:
    print("Found missing links:", missing)
else:
    print("All HTML links point to existing files.")
