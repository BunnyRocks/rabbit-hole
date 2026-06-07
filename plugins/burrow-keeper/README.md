<!--[[[cog
import readme_gen

plugin_dir = readme_gen.this_plugin_dir(cog.inFile)
meta = readme_gen.load_plugin_meta(plugin_dir)
skills = readme_gen.discover_skills(plugin_dir)
summary = readme_gen.get_or_create_summary(plugin_dir)

print(f"# {meta['name']}\n")
print(f"{meta['description']}\n")
print(f"{summary}\n")
print("## Skills\n")
for skill in skills:
    print(f"### {skill['name']}\n")
    print(f"{skill['description']}\n")

print("## Info\n")
print(f"- **Author:** {meta['author']['name']}")
print(f"- **License:** {meta['license']}")
if meta.get('keywords'):
    print(f"- **Keywords:** {', '.join(meta['keywords'])}")
]]]-->
# burrow-keeper

Skills for routine digital chores and maintenance

This plugin collects practical maintenance workflows for digital artifacts that benefit from precise command or format reconstruction. It provides yt-dlp guidance for archiving YouTube videos and playlists, localizes external media from private clippings into local assets, and supports converting rendered SVG flowcharts or Mermaid-like diagram exports back into pasteable Mermaid source. Its main strengths are compact references for error-prone syntax, asset-preserving archive workflows, and repeatable maintenance tasks where guessing creates broken output.

## Skills

### archiving-clipping-media

Use when localizing external media (images, videos, audio) in a private clipping to archive them as local assets. Triggers when user wants to download, archive, or localize media from content/private/clippers/ files.

### archiving-youtube

Use when downloading or archiving YouTube videos/playlists with yt-dlp, constructing output templates, selecting formats, or troubleshooting yt-dlp commands

### converting-svg-to-mermaid

Use when converting SVG flowcharts, diagram exports, or rendered Mermaid-like graphics back into Mermaid source code

## Info

- **Author:** BunnyRocks
- **License:** MIT
- **Keywords:** chores, archiving, youtube, yt-dlp, clippings, svg, mermaid, diagrams, flowcharts, media, maintenance, backup
<!--[[[end]]]-->
