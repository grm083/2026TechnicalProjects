#!/usr/bin/env python3
"""
Convert Confluence HTML export .doc files to clean Markdown
"""
import html2text
import re
from pathlib import Path

def extract_html_content(file_path):
    """Extract HTML content from the Confluence export file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the HTML body content
    # Look for the <body> tag and extract everything inside it
    body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
    if body_match:
        html_content = body_match.group(1)
    else:
        # If no body tag, try to find the main content section
        section_match = re.search(r'<div class="Section1">(.*?)</div>\s*</body>', content, re.DOTALL)
        if section_match:
            html_content = section_match.group(1)
        else:
            html_content = content

    return html_content

def convert_to_markdown(html_content):
    """Convert HTML to Markdown using html2text"""
    import quopri

    # Decode quoted-printable encoding
    try:
        html_content = quopri.decodestring(html_content.encode()).decode('utf-8')
    except:
        pass  # If decoding fails, continue with original content

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    h.unicode_snob = True
    h.ignore_tables = False

    markdown = h.handle(html_content)

    # Clean up the markdown
    # Remove excessive blank lines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)

    # Remove any remaining HTML entities
    markdown = markdown.replace('=3D', '=')
    markdown = markdown.replace('&amp;', '&')
    markdown = markdown.replace('&lt;', '<')
    markdown = markdown.replace('&gt;', '>')
    markdown = markdown.replace('&quot;', '"')

    # Clean up broken links
    markdown = re.sub(r'\]\(3D"[^"]*"\)', '](#)', markdown)
    markdown = re.sub(r'\[([^\]]+)\]\(#\)', r'\1', markdown)

    return markdown.strip()

def main():
    base_path = Path(__file__).parent

    files = [
        'Quote+Network+Modernization+Charter.doc',
        'Quote+Network+Modernization+QA+Test+Plan.doc',
        'Quote+Network+Modernization+UAT+Test+Plan.doc'
    ]

    for doc_file in files:
        doc_path = base_path / doc_file
        if not doc_path.exists():
            print(f"Warning: {doc_file} not found")
            continue

        print(f"Converting {doc_file}...")

        # Extract HTML content
        html_content = extract_html_content(doc_path)

        # Convert to Markdown
        markdown = convert_to_markdown(html_content)

        # Create output filename
        md_file = doc_file.replace('+', ' ').replace('.doc', '.md')
        md_path = base_path / md_file

        # Write markdown file
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"  ✓ Created {md_file}")

    print("\nConversion complete!")

if __name__ == '__main__':
    main()
