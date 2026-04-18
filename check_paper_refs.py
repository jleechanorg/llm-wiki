import os
import re

sources_dir = 'wiki/sources'
concepts_dir = 'wiki/concepts'

# Get all papers
papers = [f for f in os.listdir(sources_dir) if f.endswith('-paper.md')]
# Slug in concept files usually includes '-paper' if it's there
paper_slugs = [f.replace('.md', '') for f in papers]

# Map slug to full filename
slug_to_file = dict(zip(paper_slugs, papers))

# Check references in concepts
referenced_slugs = set()
for concept_file in os.listdir(concepts_dir):
    if not concept_file.endswith('.md'):
        continue
    with open(os.path.join(concepts_dir, concept_file), 'r') as f:
        content = f.read()
        # Find [[slug]] or sources: [slug, ...]
        refs = re.findall(r'\[\[(.*?)\]\]', content)
        referenced_slugs.update(refs)
        
        # Also check sources: [paper1, paper2]
        sources_match = re.search(r'sources:\s*\[(.*?)\]', content)
        if sources_match:
            sources_list = [s.strip() for s in sources_match.group(1).split(',')]
            referenced_slugs.update(sources_list)

unreferenced = []
for slug in paper_slugs:
    if slug not in referenced_slugs:
        unreferenced.append(slug)

print(f"Total papers: {len(paper_slugs)}")
print(f"Unreferenced: {len(unreferenced)}")
for slug in sorted(unreferenced):
    print(f"  - {slug} ({slug_to_file[slug]})")
