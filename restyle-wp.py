#!/usr/bin/env python3
"""
Restyle WordPress archive pages to match the Jekyll site's look and feel.
Replaces the WordPress theme structure with Jekyll-compatible markup and CSS.
"""

import os
import re
import glob

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
WP_DIR = os.path.join(REPO_ROOT, "wordpress-pages")

stats = {"processed": 0, "modified": 0, "footer_removed": 0}


def extract_title(html):
    """Extract the page title from the HTML."""
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    if m:
        # Clean up the title - remove " : Sharing Nicely" suffix
        title = m.group(1).strip()
        title = re.sub(r'\s*:\s*Sharing Nicely\s*$', '', title)
        return title
    return "Archive"


def build_new_head(title):
    """Build a new <head> section that loads the Jekyll CSS."""
    return f'''<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
  <link rel="stylesheet" href="/css/screen.css" type="text/css" />
  <style>
    /* WordPress archive page overrides */
    .entry-title {{ font-size: 130%; margin-bottom: 0.3em; }}
    .postMeta {{ color: #aaa; font-size: 85%; margin-top: 1em; margin-bottom: 2em; }}
    .postMeta span {{ font-weight: 500; }}
    .postDate, .categories {{ display: inline; margin-right: 1.5em; }}
    blockquote {{ border-left: 3px solid #ddd; margin-left: 0; padding-left: 1em; color: #555; }}
    img {{ max-width: 100%; height: auto; }}
    /* Comments */
    #dsq-comments {{ list-style: none; padding: 0; }}
    #dsq-comments li {{ margin-bottom: 1.5em; padding-bottom: 1em; border-bottom: 1px solid #eee; }}
    #dsq-comments .children {{ list-style: none; padding-left: 1.5em; }}
    .dsq-comment-header cite {{ font-style: normal; font-weight: 500; }}
    .dsq-comment-header cite span {{ color: #333; }}
    .dsq-comment-message {{ margin-top: 0.3em; }}
    .dsq-comment-header cite {{ display: block; }}
    /* Hide bare URLs in cite blocks, show only the author name span */
    .dsq-comment-header cite {{ font-size: 0; }}
    .dsq-comment-header cite span {{ font-size: 0.9rem; }}
    /* Navigation */
    .pageNav {{ overflow: hidden; margin: 2em 0; padding-top: 1em; border-top: 1px solid #eee; }}
    .pageNav .prev {{ float: left; }}
    .pageNav .next {{ float: right; }}
    /* Pingbacks */
    li.pingback {{ font-size: 85%; color: #888; }}
  </style>
</head>'''


def extract_body_content(html):
    """Extract the main content from the WordPress body."""
    # Get everything between <body...> and </body>
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    body = m.group(1)
    return body


def remove_wp_footer(html):
    """Remove the WordPress footer div."""
    original = html
    html = re.sub(
        r'<div id="footer">[\s\S]*?</div>\s*</div>',
        '',
        html,
        flags=re.IGNORECASE
    )
    if html != original:
        stats["footer_removed"] += 1
    return html


def remove_wp_nav_and_header(body):
    """Remove the old WordPress site header, nav, and description."""
    # Remove the h1 site title
    body = re.sub(r'<h1 class="vcard author">.*?</h1>\s*', '', body, flags=re.DOTALL)
    # Remove the mainNav div
    body = re.sub(r'<div id="mainNav">[\s\S]*?</div>\s*', '', body)
    # Remove siteDescription div
    body = re.sub(r'<div id="siteDescription">[\s\S]*?</div>\s*', '', body)
    return body


def remove_wp_search_form(body):
    """Remove the WordPress search form."""
    body = re.sub(r'<form[^>]*id="searchform"[^>]*>[\s\S]*?</form>', '', body)
    return body


def remove_footer_content(body):
    """Remove the entire footer div and its contents."""
    body = re.sub(
        r'<div id="footer">[\s\S]*$',
        '',
        body,
        flags=re.IGNORECASE
    )
    return body


def wrap_in_jekyll_structure(title, inner_content):
    """Wrap content in Jekyll-like site structure with nav and footer."""
    return f'''<body>
  <div class="site">
    <div class="nav">
      <a href="/">Home</a> | <a href="/about.html">About</a>
    </div>

{inner_content}

    <div class="footer">
      <div class="contact">
        <p>
          J. Philipp Schmidt<br />
        </p>
      </div>
      <div class="contact">
        <p>
          <a href="https://www.linkedin.com/in/schmidtjp/">LinkedIn</a> | <a href="/blog.html">Blog</a><br />
        </p>
      </div>
    </div>
  </div>
</body>
</html>'''


def restyle_file(filepath):
    """Restyle a single WordPress HTML file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    original = html

    title = extract_title(html)
    body = extract_body_content(html)
    if body is None:
        return False

    # Clean up the body content
    body = remove_wp_nav_and_header(body)
    body = remove_footer_content(body)
    body = remove_wp_search_form(body)

    # Remove empty siteWrapper and closing divs that are now orphaned
    # but keep coreContent and everything inside it
    body = re.sub(r'<div id="siteWrapper">\s*', '', body)
    # Remove trailing orphan </div> tags carefully
    # Strip excessive closing divs at the end
    body = body.rstrip()
    while body.endswith('</div>'):
        body = body[:-len('</div>')].rstrip()

    # Remove the disqus_thread wrapper div but keep comment content
    body = re.sub(r'<div id="disqus_thread">\s*', '', body)
    body = re.sub(r'<div id="dsq-content">\s*', '', body)

    # Add a "Comments" heading before the comments list if there are comments
    if 'id="dsq-comments"' in body:
        body = re.sub(
            r'(<ul id="dsq-comments">)',
            r'<h3>Comments</h3>\n\1',
            body
        )

    # Build new page
    new_head = build_new_head(title)
    new_html = new_head + '\n' + wrap_in_jekyll_structure(title, body)

    # Clean up excessive blank lines
    new_html = re.sub(r'\n{4,}', '\n\n\n', new_html)

    if new_html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return True
    return False


def find_html_files():
    """Find all HTML files in wordpress-pages."""
    files = []
    for root, dirs, filenames in os.walk(WP_DIR):
        for fname in filenames:
            if fname.endswith('.html'):
                files.append(os.path.join(root, fname))
    return files


def main():
    print("=" * 60)
    print("Restyle WordPress Pages")
    print("=" * 60)

    files = find_html_files()
    print(f"\nFound {len(files)} HTML files")

    for filepath in files:
        stats["processed"] += 1
        if restyle_file(filepath):
            stats["modified"] += 1

    print(f"Modified: {stats['modified']} files")
    print(f"Processed: {stats['processed']} files")


if __name__ == "__main__":
    main()
