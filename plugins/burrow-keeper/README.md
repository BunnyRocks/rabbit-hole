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

This plugin collects practical maintenance workflows for digital artifacts that benefit from precise command or format reconstruction. It provides yt-dlp guidance for archiving YouTube videos and playlists, with detailed coverage of output templates, playlist variables, format selection, and common command mistakes. It also supports converting rendered SVG flowcharts and Mermaid-like diagram exports back into pasteable Mermaid source while preserving layout direction, node shapes, edge labels, renderer config, and ambiguity notes. Its main strengths are compact references for error-prone syntax and repeatable workflows where guessing creates broken output.

## Skills

### archiving-youtube

Use when downloading or archiving YouTube videos/playlists with yt-dlp, constructing output templates, selecting formats, or troubleshooting yt-dlp commands

### converting-svg-to-mermaid

Use when converting SVG flowcharts, diagram exports, or rendered Mermaid-like graphics back into Mermaid source code

## Info

- **Author:** BunnyRocks
- **License:** MIT
- **Keywords:** chores, archiving, youtube, yt-dlp, svg, mermaid, diagrams, flowcharts, media, maintenance, backup
<!--[[[end]]]-->
