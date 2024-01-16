import os
import re

def replace_url(old_url, new_url, reverse=False):
    if reverse:
        old_url, new_url = new_url, old_url
    folder_path = os.path.dirname(os.path.realpath(__file__))
    print(folder_path)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('html', 'js', 'css')):
                file_path = os.path.join(root, file)
                print("file: ", file)
                with open(file_path, 'r') as f:
                    content = f.read()
                
                new_content = re.sub(re.escape(old_url) + r'(?=/)', new_url, content)

                with open(file_path, 'w') as f:
                    f.write(new_content)

# Usage example
replace_url('http://127.0.0.1:5500', 'https://silver-goldfish-7xg65j5rx5xhww4g-5500.app.github.dev', False)
#replace_url('https://silver-goldfish-7xg65j5rx5xhww4g-5500.app.github.dev', 'http://127.0.0.1:5500', True)