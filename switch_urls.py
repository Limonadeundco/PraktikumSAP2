import os

def replace_url(folder_path, old_url, new_url):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.html', '.css', '.js')):
                file_path = os.path.join(root, file)
                #read lines and replace old_url with new_url
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                with open(file_path, 'w') as f:
                    for line in lines:
                        f.write(line.replace(old_url, new_url))    

# Usage example
replace_url('/', 'http://127.0.0.1:5000', 'https://silver-goldfish-7xg65j5rx5xhww4g-5500.app.github.dev/')