import re

# Read the SVG file
with open(r'c:\Users\VICTUS\Downloads\geminioddo\Dayflow - Human Resource Management System - 8 hours.svg', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all text content
texts = re.findall(r'>([^<]+)</text>', content)

# Filter and clean
unique_texts = sorted(set([t.strip() for t in texts if len(t.strip()) > 2]))

# Print all unique text elements
for text in unique_texts:
    print(text)
