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

This plugin provides comprehensive guidance for archiving YouTube videos and playlists using yt-dlp, focusing on constructing accurate output templates and selecting optimal download formats. It covers key yt-dlp command patterns, template syntax, variable usage, common flags, and error-prone areas specific to output template construction and playlist handling. Designed as a troubleshooting and reference tool, the plugin helps users avoid common mistakes, supports advanced filename logic, playlist variable handling, and format selection, and provides concise examples for practical archiving workflows. Its main strengths are precise output template documentation, format selection guidance, and detailed flag explanations for efficient YouTube archiving.

## Skills

### archiving-youtube

Use when downloading or archiving YouTube videos/playlists with yt-dlp, constructing output templates, selecting formats, or troubleshooting yt-dlp commands

## Info

- **Author:** BunnyRocks
- **License:** MIT
- **Keywords:** chores, archiving, youtube, yt-dlp, media, maintenance, backup
<!--[[[end]]]-->
