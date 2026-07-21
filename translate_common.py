import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('_DE.html')]

translations = {
    r'<title>(.*?) \| Compas Solutions</title>': {
        "Contact": "Kontakt",
        "Industries": "Branchen",
        "Privacy Policy": "Datenschutzrichtlinie",
        "Resources": "Ressourcen",
        "Use Cases": "Fallstudien"
    },
    r'<a href="index_DE.html"(.*?)>Home</a>': r'<a href="index_DE.html"\1>Startseite</a>',
    r'<a href="aboutus_DE.html"(.*?)>About Us</a>': r'<a href="aboutus_DE.html"\1>Über uns</a>',
    r'<a href="Services_DE.html"(.*?)>Services</a>': r'<a href="Services_DE.html"\1>Dienstleistungen</a>',
    r'<a href="industries_DE.html"(.*?)>Industries</a>': r'<a href="industries_DE.html"\1>Branchen</a>',
    r'<a href="use-cases_DE.html"(.*?)>Use Cases</a>': r'<a href="use-cases_DE.html"\1>Fallstudien</a>',
    r'<a href="Contact_DE.html"(.*?)>Contact Us</a>': r'<a href="Contact_DE.html"\1>Kontakt</a>',
    r'<a href="Contact_DE.html"(.*?)>Contact</a>': r'<a href="Contact_DE.html"\1>Kontakt</a>',
    r'<a href="resources_DE.html"(.*?)>Resources</a>': r'<a href="resources_DE.html"\1>Ressourcen</a>',
    r'All rights reserved\.': r'Alle Rechte vorbehalten.',
    r'Privacy Policy': r'Datenschutzrichtlinie',
}

for filename in html_files:
    if filename in ["index_DE.html", "aboutus_DE.html", "Services_DE.html"]:
        continue # Already done manually

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Translate title
    def title_replace(match):
        title = match.group(1)
        return f'<title>{translations[r"<title>(.*?) \| Compas Solutions</title>"].get(title, title)} | Compas Solutions</title>'
    
    content = re.sub(r'<title>(.*?) \| Compas Solutions</title>', title_replace, content)

    # Translate links and footer
    for pattern, replacement in translations.items():
        if pattern != r'<title>(.*?) \| Compas Solutions</title>':
            content = re.sub(pattern, replacement, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Common components translated.")
