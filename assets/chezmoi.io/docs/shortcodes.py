# Copyright (c) 2016-2023 Martin Donath <martin.donath@squidfunk.com>
# Modified for chezmoi by Austin Ziegler <halostatue@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from __future__ import annotations

import posixpath
import re
from re import Match

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page

# -----------------------------------------------------------------------------
# Hooks
# -----------------------------------------------------------------------------


# @todo
def on_page_markdown(
    markdown: str,
    *,
    page: Page,
    config: MkDocsConfig,
    files: Files,
) -> str:
    # Replace callback
    def replace(match: Match) -> str:
        tag_type, args = match.groups()
        args = args.strip()
        if tag_type == 'version':
            return _badge_for_version(args, page, files)

        # Otherwise, raise an error
        raise RuntimeError(f'Unknown shortcode: {tag_type}')

    # Find and replace all external asset URLs in current page
    return re.sub(r'<!-- md:(\w+)(.*?) -->', replace, markdown, flags=re.I | re.M)


# Resolve path of file relative to given page - the posixpath always includes
# one additional level of `..` which we need to remove
def _resolve_path(path: str, page: Page, files: Files) -> str:
    path, anchor, *_ = f'{path}#'.split('#')
    path = _resolve(files.get_file_from_path(path), page)
    return '#'.join([path, anchor]) if anchor else path


# Resolve path of file relative to given page - the posixpath always includes
# one additional level of `..` which we need to remove
def _resolve(file: File, page: Page) -> str:
    path = posixpath.relpath(file.src_uri, page.file.src_uri)
    return posixpath.sep.join(path.split(posixpath.sep)[1:])


# -----------------------------------------------------------------------------


# Create badge
def _badge(icon: str, text: str = '', tag_type: str = '') -> str:
    classes = f'mdx-badge mdx-badge--{tag_type}' if tag_type else 'mdx-badge'
    return ''.join(
        [
            f'<span class="{classes}">',
            *([f'<span class="mdx-badge__icon">{icon}</span>'] if icon else []),
            *([f'<span class="mdx-badge__text">{text}</span>'] if text else []),
            '</span>',
        ],
    )


# Create badge for version
def _badge_for_version(text: str, page: Page, files: Files) -> str:
    spec = text
    path = f'reference/release-history.md#{spec}'

    # Return badge
    # icon_name = "material-tag-outline"
    icon_name = 'material-update'
    icon = f':{icon_name}:{"{"} title="Since" {"}"}'
    return _badge(
        icon=icon,
        text=f' Since [{text}]({_resolve_path(path, page, files)})' if spec else '',
    )
