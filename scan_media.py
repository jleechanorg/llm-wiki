#!/usr/bin/env python3
"""Scan for media files and generate wiki entries."""
import os
import re
from pathlib import Path
from datetime import datetime

EXCLUDE_DIRS = {'node_modules', '.git', 'build', 'target', 'dist', '__pycache__', '.cache', 'Library', '.Trash', '.cursor'}

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico'}
VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
AUDIO_EXTS = {'.mp3', '.wav', '.aac', '.m4a', '.ogg'}
DOC_EXTS = {'.pdf'}

def get_media_type(path):
    ext = path.suffix.lower()
    if ext in IMAGE_EXTS:
        return 'image'
    elif ext in VIDEO_EXTS:
        return 'video'
    elif ext in AUDIO_EXTS:
        return 'audio'
    elif ext in DOC_EXTS:
        return 'document'
    return 'unknown'

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def should_exclude(path):
    parts = path.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
    return False

def scan_media(root):
    root_path = Path(root)
    media_files = []
    
    patterns = [
        '**/*.png', '**/*.jpg', '**/*.jpeg', '**/*.gif', '**/*.svg', '**/*.webp', '**/*.ico',
        '**/*.mp4', '**/*.mov', '**/*.avi', '**/*.mkv', '**/*.webm',
        '**/*.mp3', '**/*.wav', '**/*.aac', '**/*.m4a', '**/*.ogg',
        '**/*.pdf', '**/Screenshot*'
    ]
    
    for pattern in patterns:
        for path in root_path.glob(pattern):
            if should_exclude(path):
                continue
            try:
                stat = path.stat()
                media_files.append({
                    'path': str(path),
                    'name': path.name,
                    'type': get_media_type(path),
                    'size': format_size(stat.st_size),
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d'),
                    'size_bytes': stat.st_size
                })
            except OSError:
                continue
    
    # Sort by size descending, then name
    media_files.sort(key=lambda x: (-x['size_bytes'], x['name']))
    return media_files

def generate_wiki(media_files, output_path):
    lines = ['# Media Wiki\n']
    
    if not media_files:
        lines.append('\nNo media files found.\n')
        return '\n'.join(lines)
    
    # Group by type
    by_type = {}
    for f in media_files:
        t = f['type']
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(f)
    
    for media_type in ['image', 'video', 'audio', 'document']:
        files = by_type.get(media_type, [])
        if not files:
            continue
        
        lines.append(f'\n## {media_type.capitalize()}s\n')
        for f in files:
            lines.append(f'### Media: {f["name"]}')
            lines.append(f'- **Path**: {f["path"]}')
            lines.append(f'- **Type**: {f["type"]}')
            lines.append(f'- **Size**: {f["size"]}')
            lines.append(f'- **Modified**: {f["modified"]}')
            lines.append('')
    
    return '\n'.join(lines)

if __name__ == '__main__':
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    output = sys.argv[2] if len(sys.argv) > 2 else 'media.md'
    
    files = scan_media(root)
    wiki = generate_wiki(files, output)
    
    with open(output, 'w') as f:
        f.write(wiki)
    
    print(f'Found {len(files)} media files, wrote to {output}')
