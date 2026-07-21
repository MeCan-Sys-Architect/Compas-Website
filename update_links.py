import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# List of the base names
base_names = [
    "index", "aboutus", "Services", "Contact", 
    "industries", "privacy_pol", "resources", "use-cases"
]

def get_base_name_and_lang(filename):
    for base in base_names:
        if filename == f"{base}.html":
            return base, "EN"
        elif filename == f"{base}_TR.html":
            return base, "TR"
        elif filename == f"{base}_DE.html":
            return base, "DE"
    return None, None

for filename in html_files:
    base, lang = get_base_name_and_lang(filename)
    if not base:
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Update language switcher
    # The existing language switcher block looks something like:
    # <select class="language-select" onchange="location = this.value;">
    #   <option value="...">Türkçe</option>
    #   <option value="...">Deutsch</option>
    #   <option value="...">English</option>
    # </select>
    
    # We will replace the entire block with a correctly formatted one
    lang_select_pattern = re.compile(r'<select class="language-select" onchange="location = this\.value;">.*?</select>', re.DOTALL)
    
    tr_selected = " selected" if lang == "TR" else ""
    de_selected = " selected" if lang == "DE" else ""
    en_selected = " selected" if lang == "EN" else ""
    
    new_lang_select = f'''<select class="language-select" onchange="location = this.value;">
      <option value="{base}_TR.html"{tr_selected}>Türkçe</option>
      <option value="{base}_DE.html"{de_selected}>Deutsch</option>
      <option value="{base}.html"{en_selected}>English</option>
    </select>'''
    
    content = lang_select_pattern.sub(new_lang_select, content)
    
    # 2. If it's a DE file, update all the navigation links to point to _DE versions.
    if lang == "DE":
        for b in base_names:
            # We want to replace href="base.html" and href="base_TR.html" (just in case) with href="base_DE.html"
            content = re.sub(rf'href="{b}\.html"', f'href="{b}_DE.html"', content)
            content = re.sub(rf'href="{b}_TR\.html"', f'href="{b}_DE.html"', content)
            # Also handle href="index.html#aerospace-case" etc.
            content = re.sub(rf'href="{b}\.html#([^"]+)"', rf'href="{b}_DE.html#\1"', content)
            content = re.sub(rf'href="{b}_TR\.html#([^"]+)"', rf'href="{b}_DE.html#\1"', content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Language switchers and DE navigation links updated successfully.")
