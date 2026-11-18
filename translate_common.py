import os
import re

de_folders = [f for f in os.listdir('.') if os.path.isdir(f) and f.endswith('_DE')]

translations = {
    r'<title>(.*?) \| Compas Solutions</title>': {
        "Contact": "Kontakt",
        "Industries": "Branchen",
        "Privacy Policy": "Datenschutzrichtlinie",
        "Resources": "Ressourcen",
        "Use Cases": "Fallstudien"
    },
    r'<a href="\.\./index_DE"(.*?)>Home</a>': r'<a href="../index_DE"\1>Startseite</a>',
    r'<a href="\.\./aboutus_DE"(.*?)>About Us</a>': r'<a href="../aboutus_DE"\1>Über uns</a>',
    r'<a href="\.\./Services_DE"(.*?)>Services</a>': r'<a href="../Services_DE"\1>Dienstleistungen</a>',
    r'<a href="\.\./industries_DE"(.*?)>Industries</a>': r'<a href="../industries_DE"\1>Branchen</a>',
    r'<a href="\.\./use-cases_DE"(.*?)>Use Cases</a>': r'<a href="../use-cases_DE"\1>Fallstudien</a>',
    r'<a href="\.\./Contact_DE"(.*?)>Contact Us</a>': r'<a href="../Contact_DE"\1>Kontakt</a>',
    r'<a href="\.\./Contact_DE"(.*?)>Contact</a>': r'<a href="../Contact_DE"\1>Kontakt</a>',
    r'<a href="\.\./resources_DE"(.*?)>Resources</a>': r'<a href="../resources_DE"\1>Ressourcen</a>',
    r'All rights reserved\.': r'Alle Rechte vorbehalten.',
    r'Privacy Policy': r'Datenschutzrichtlinie',
}

for folder in de_folders:
    if folder in ["index_DE", "aboutus_DE", "Services_DE"]:
        continue

    filepath = os.path.join(folder, 'index.html')
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def title_replace(match):
        title = match.group(1)
        return f'<title>{translations[r"<title>(.*?) \| Compas Solutions</title>"].get(title, title)} | Compas Solutions</title>'
    
    content = re.sub(r'<title>(.*?) \| Compas Solutions</title>', title_replace, content)

    for pattern, replacement in translations.items():
        if pattern != r'<title>(.*?) \| Compas Solutions</title>':
            content = re.sub(pattern, replacement, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Common components translated.")
