#!/usr/bin/env python3
"""
Security cleanup script for GitHub Pages blog.
Cleans WordPress-legacy HTML files and Jekyll pages.
"""

import os
import re
import glob
import sys

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
WP_DIR = os.path.join(REPO_ROOT, "wordpress-pages")

# Stats
stats = {
    "files_processed": 0,
    "scripts_removed": 0,
    "links_removed": 0,
    "http_converted": 0,
    "ie_conditionals_removed": 0,
    "comments_html_preserved": 0,
}


def remove_script_tags(html):
    """Remove all <script> tags (inline and external) from HTML."""
    count = len(re.findall(r'<script[\s>]', html, re.IGNORECASE))
    # Remove script tags including their content (handles multiline)
    cleaned = re.sub(
        r'<script[^>]*>[\s\S]*?</script>\s*',
        '',
        html,
        flags=re.IGNORECASE
    )
    # Also remove self-closing script tags
    cleaned = re.sub(
        r'<script[^>]*/>\s*',
        '',
        cleaned,
        flags=re.IGNORECASE
    )
    stats["scripts_removed"] += count
    return cleaned


def remove_wp_meta_links(html):
    """Remove WordPress-specific <link> tags that serve no purpose on a static site."""
    patterns = [
        # EditURI / RSD
        r'<link[^>]*rel="EditURI"[^>]*/?>[ \t]*\n?',
        # wlwmanifest
        r'<link[^>]*rel="wlwmanifest"[^>]*/?>[ \t]*\n?',
        # pingback
        r'<link[^>]*rel="pingback"[^>]*/?>[ \t]*\n?',
        # WordPress generator meta
        r'<meta[^>]*name="generator"[^>]*content="WordPress[^"]*"[^>]*/?>[ \t]*\n?',
        # Google Analytics comment
        r'<!-- Google Analytics Tracking[^>]*-->\s*\n?',
    ]
    for pattern in patterns:
        count = len(re.findall(pattern, html, re.IGNORECASE))
        stats["links_removed"] += count
        html = re.sub(pattern, '', html, flags=re.IGNORECASE)
    return html


def remove_ie_conditionals_with_external_refs(html):
    """Remove IE conditional comments that reference sharing-nicely.net."""
    pattern = r'<!--\[if[^\]]*\]>[\s\S]*?sharing-nicely\.net[\s\S]*?<!\[endif\]-->\s*\n?'
    count = len(re.findall(pattern, html, re.IGNORECASE))
    stats["ie_conditionals_removed"] += count
    html = re.sub(pattern, '', html, flags=re.IGNORECASE)
    return html


def convert_http_to_https_in_tags(html):
    """Convert http:// to https:// in <link> and <a> href attributes, and <img> src attributes.
    Only converts in HTML tags, not in body text content."""
    def replace_http(match):
        tag = match.group(0)
        # Don't convert w3.org DTD/namespace URLs (they're identifiers, not fetched resources)
        if 'w3.org' in tag:
            return tag
        new_tag = tag.replace('http://', 'https://')
        if new_tag != tag:
            stats["http_converted"] += 1
        return new_tag

    # Convert in link tags
    html = re.sub(r'<link[^>]*>', replace_http, html, flags=re.IGNORECASE)
    # Convert in img src (but not in body text)
    html = re.sub(r'<img[^>]*>', replace_http, html, flags=re.IGNORECASE)
    # Convert Google Fonts link specifically
    html = re.sub(
        r"http://fonts\.googleapis\.com",
        "https://fonts.googleapis.com",
        html
    )
    return html


def has_disqus_comments(html):
    """Check if the file contains actual Disqus comment content (not just the embed script)."""
    return 'dsq-comment-message' in html or 'dsq-comment-body' in html


def clean_wordpress_html(filepath):
    """Clean a WordPress-legacy HTML file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    original = html

    if has_disqus_comments(html):
        stats["comments_html_preserved"] += 1

    # 1. Remove all script tags
    html = remove_script_tags(html)

    # 2. Remove WordPress-specific meta/link tags
    html = remove_wp_meta_links(html)

    # 3. Remove IE conditionals referencing sharing-nicely.net
    html = remove_ie_conditionals_with_external_refs(html)

    # 4. Remove link tags referencing sharing-nicely.net (CSS etc)
    sharing_link_count = len(re.findall(r'<link[^>]*sharing-nicely\.net[^>]*/?>',
                                         html, re.IGNORECASE))
    stats["links_removed"] += sharing_link_count
    html = re.sub(r'<link[^>]*sharing-nicely\.net[^>]*/?>[ \t]*\n?', '', html,
                  flags=re.IGNORECASE)

    # 5. Convert http:// to https:// in remaining tags
    html = convert_http_to_https_in_tags(html)

    # 6. Clean up excessive blank lines (more than 2 in a row)
    html = re.sub(r'\n{4,}', '\n\n\n', html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def clean_jekyll_page(filepath):
    """Clean a Jekyll page (remove jQuery, Modernizr, etc. that aren't used)."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    original = html

    # Remove the script block (jQuery, Modernizr, plugins, main.js)
    # These are not used - main.js is empty, plugins.js is just a console polyfill
    html = re.sub(
        r'<script src="javascripts/vendor/modernizr[^"]*"></script>\s*\n?',
        '', html, flags=re.IGNORECASE
    )
    html = re.sub(
        r'<script src="//ajax\.googleapis\.com/ajax/libs/jquery/[^"]*"></script>\s*\n?',
        '', html, flags=re.IGNORECASE
    )
    html = re.sub(
        r"<script>window\.jQuery[^<]*</script>\s*\n?",
        '', html, flags=re.IGNORECASE
    )
    html = re.sub(
        r'<script src="javascripts/plugins\.js"></script>\s*\n?',
        '', html, flags=re.IGNORECASE
    )
    html = re.sub(
        r'<script src="javascripts/main\.js"></script>\s*\n?',
        '', html, flags=re.IGNORECASE
    )

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def find_wordpress_html_files():
    """Find all WordPress-legacy HTML files."""
    files = []
    for root, dirs, filenames in os.walk(WP_DIR):
        for fname in filenames:
            if fname.endswith('.html'):
                files.append(os.path.join(root, fname))
    return files


def main():
    print("=" * 60)
    print("Security Cleanup Script")
    print("=" * 60)

    # Process WordPress legacy files
    wp_files = find_wordpress_html_files()
    print(f"\nFound {len(wp_files)} WordPress HTML files in wordpress-pages/")

    modified_count = 0
    for filepath in wp_files:
        stats["files_processed"] += 1
        if clean_wordpress_html(filepath):
            modified_count += 1

    print(f"Modified: {modified_count} files")

    # Process Jekyll pages
    jekyll_pages = [
        os.path.join(REPO_ROOT, "index.html"),
        os.path.join(REPO_ROOT, "blog.html"),
        os.path.join(REPO_ROOT, "food.html"),
    ]

    print(f"\nProcessing {len(jekyll_pages)} Jekyll pages...")
    for filepath in jekyll_pages:
        if os.path.exists(filepath):
            stats["files_processed"] += 1
            if clean_jekyll_page(filepath):
                print(f"  Cleaned: {os.path.basename(filepath)}")

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Files processed:              {stats['files_processed']}")
    print(f"Script tags removed:          {stats['scripts_removed']}")
    print(f"WP meta/link tags removed:    {stats['links_removed']}")
    print(f"IE conditionals removed:      {stats['ie_conditionals_removed']}")
    print(f"HTTP→HTTPS conversions:       {stats['http_converted']}")
    print(f"Files with comments preserved:{stats['comments_html_preserved']}")


if __name__ == "__main__":
    main()
