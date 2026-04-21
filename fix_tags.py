import glob

for file in glob.glob(r'c:\Users\aa304\Downloads\AsyncIO-Animations\js\*.js'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replacing unescaped generic tags in Dart code blocks
    content = content.replace('Future<String>', 'Future&lt;String&gt;')
    content = content.replace('Future<List<String>>', 'Future&lt;List&lt;String&gt;&gt;')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
