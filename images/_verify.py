import re

path = r'c:\Users\wan_f\Desktop\cursor\AI工作台\output\book-yellow-emperor\images\ch00-fig1-book-architecture.svg'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

texts = re.findall(r'>([^<]+)<', content)
for t in texts:
    t = t.strip()
    if t:
        print(repr(t))
