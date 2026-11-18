import os
import re

base_names = [
    "index", "aboutus", "Services", "Contact", 
    "industries", "privacy_pol", "resources", "use-cases"
]

def get_page_files():
    pages = []
    for base in base_names:
        en_path = "index.html" if base == "index" else os.path.join(base, "index.html")
        if os.path.exists(en_path):
            pages.append((en_path, base, "EN", base != "index"))
        tr_path = os.path.join(f"{base}_TR", "index.html")
        if os.path.exists(tr_path):
            pages.append((tr_path, base, "TR", True))
        de_path = os.path.join(f"{base}_DE", "index.html")
        if os.path.exists(de_path):
            pages.append((de_path, base, "DE", True))
    return pages

for filepath, base, lang, is_sub in get_page_files():
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lang_select_pattern = re.compile(r'<select class="language-select" onchange="(?:location = this\.value|changeLanguage\(this\.value\));">.*?</select>', re.DOTALL)
    
    tr_selected = " selected" if lang == "TR" else ""
    de_selected = " selected" if lang == "DE" else ""
    en_selected = " selected" if lang == "EN" else ""
    
    prefix = "../" if is_sub else ""
    en_val = ("../" if is_sub else "./") if base == "index" else f"{prefix}{base}"
    tr_val = f"{prefix}{base}_TR"
    de_val = f"{prefix}{base}_DE"
    
    new_lang_select = f'''<select class="language-select" onchange="changeLanguage(this.value);">
      <option value="{tr_val}"{tr_selected}>Türkçe</option>
      <option value="{de_val}"{de_selected}>Deutsch</option>
      <option value="{en_val}"{en_selected}>English</option>
    </select>'''
    
    content = lang_select_pattern.sub(new_lang_select, content)
    
    if lang == "DE":
        for b in base_names:
            en_href = "../" if b == "index" else f"../{b}"
            content = re.sub(rf'href="{re.escape(en_href)}"', f'href="../{b}_DE"', content)
            content = re.sub(rf'href="\.\./{b}_TR"', f'href="../{b}_DE"', content)
            content = re.sub(rf'href="{re.escape(en_href)}#([^"]+)"', rf'href="../{b}_DE#\1"', content)
            content = re.sub(rf'href="\.\./{b}_TR#([^"]+)"', rf'href="../{b}_DE#\1"', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Language switchers and DE navigation links updated successfully.")
