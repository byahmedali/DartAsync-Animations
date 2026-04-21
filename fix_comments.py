import glob
import re

for file in glob.glob(r'c:\Users\aa304\Downloads\AsyncIO-Animations\js\*.js'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # The python script already did something, but let's replace '# ' with '// ' IF it appears inside <span class="line...
    content = re.sub(r'(<span class="line-\d+">)\s*#\s*(.*?</span>)', r'\1// \2', content)
    content = re.sub(r'#\s*Could be awaited directly', r'// Starts immediately', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
