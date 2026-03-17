#!/usr/bin/env python3
import os, re

base = r'c:\Users\wan_f\Desktop\cursor\AI工作台\output\book-yellow-emperor\images'

files = [
    'ch00-fig1-book-architecture.svg',
    'ch03-fig1-neijing-plate-en.svg',
    'ch04-fig1-seven-emotions-organs-qi-en.svg',
    'ch06-fig1-prevention-layers-en.svg',
    'ch07-fig1-four-imbalances-en.svg',
    'ch09-fig1-five-pillars-en.svg',
]

for fname in files:
    path = os.path.join(base, fname)
    print(f'\n=== {fname} ===')
    if not os.path.exists(path):
        print('  ERROR: FILE NOT FOUND')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'  Size: {len(content)} chars')
    
    has_xml_decl = content.startswith('<?xml')
    print(f'  XML declaration: {has_xml_decl}')
    
    # Check for common corruption patterns
    issues = []
    if '<>' in content: issues.append('contains <> (corrupted emoji)')
    if '>l ' in content: issues.append('contains >l (corrupted emoji)')
    if '<N ' in content: issues.append('contains <N (corrupted emoji)')
    if '>i ' in content: issues.append('contains >i (corrupted emoji)')
    if chr(0x02C7) in content: issues.append('contains caron (corrupted middle dot)')  # ˇ
    if '3¢' in content or '4Z' in content: issues.append('contains corrupted Chinese')
    if '???' in content: issues.append('contains ??? (corrupted text)')
    if re.search(r'\? Yin-Yang', content): issues.append('contains ? (corrupted yin-yang)')
    
    if issues:
        for i in issues:
            print(f'  ISSUE: {i}')
    else:
        print('  No corruption found')
    
    # Show key text content
    texts = re.findall(r'>([^<]+)</text>', content)
    print(f'  Text elements: {len(texts)}')
    for t in texts[:3]:
        print(f'    "{t.strip()}"')
    if len(texts) > 3:
        print(f'    ... and {len(texts)-3} more')

print('\n=== DONE ===')
