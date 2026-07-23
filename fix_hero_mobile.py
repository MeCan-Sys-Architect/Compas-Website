import os

files = ['index.html', 'index_DE.html', 'index_TR.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the block:
    #       .hero {
    #         height: 100vh;
    #         min-height: 0; /* Override previous setting */
    #         padding-bottom: 120px; /* 2 * 60px header */
    #       }
    # and replace with:
    #       .hero {
    #         height: 60vh;
    #         min-height: 400px;
    #         padding-bottom: 80px;
    #       }
    #       .hero-video {
    #         object-fit: cover;
    #         object-position: 25% 50%;
    #       }

    target = """      .hero {
        height: 100vh;
        min-height: 0; /* Override previous setting */
        padding-bottom: 120px; /* 2 * 60px header */
      }"""
    
    replacement = """      .hero {
        height: 65vh;
        min-height: 400px;
        padding-bottom: 80px;
      }
      .hero-video {
        object-fit: cover;
        object-position: center;
      }"""
      
    if target in content:
        content = content.replace(target, replacement)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
    else:
        print(f"Target not found in {file}")
