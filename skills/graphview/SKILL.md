---
name: graphview
description: Render notes, docs, or a codebase as a beautiful, interactive Obsidian-style knowledge graph — a standalone HTML page with a force-directed graph, search, hover-to-highlight neighbours, and a slide-in note panel. Use when the user wants to SEE or explore how things connect (not just query them): "visualize this", "make a graph like Obsidian", "knowledge graph", "bilim grafigi", "obsidiandek", "grafik qilib ber", or to put a prettier visual layer on top of a graph extractor's output. An extractor (e.g. graphify, or domain-modeling) finds the structure; graphview makes it explorable and good-looking.
---

# graphview

Turns structure into one self-contained, dependency-free HTML page that looks and behaves like Obsidian's graph view: draggable force-directed nodes, hover highlights a node's neighbours, click opens the note's full text in a side panel with clickable links, search dims the rest, wheel zooms, drag-empty pans. Works offline, light + dark.

This skill is the **view**. For the **structure** underneath, prefer an extractor first:
- A codebase → run a code-graph tool (e.g. `graphify`) that writes a graph, then render it here.
- Code terms / decisions → a domain-modeling pass (GLOSSARY.md, ADRs), then render the folder.
- A notes/docs folder with `[[wikilinks]]` or `[text](file.md)` links → render directly.

## Use

1. Pick the source:
   - a folder of Markdown notes (frontmatter `title`/`name`, `type`/`node_type`, `description`; links via `[[name]]` or `[](file.md)`), **or**
   - a graph JSON / directory shaped `{"nodes":[{id,label,type,desc,body,path,links:[]}],"links":[[a,b],…]}`.
2. Run the generator from your working directory (don't cd into the source), passing paths. The script sits next to this SKILL.md:
   ```
   python -I "<path-to-this-skill>/build_graph.py" "<source>" -o "<out>.html" --title "<name>"
   ```
   (When installed globally this is typically `~/.claude/skills/graphview/build_graph.py`.)
3. It writes a standalone `knowledge-graph.html`. Open it in the browser, or publish it as a shareable page.
4. Tell the user in one line what was graphed (N nodes, M links) and where the file is.

## Notes
- Node colour = `type`; the legend builds itself from the types present (palette auto-assigns).
- Node size = number of links. An unlinked note still appears (isolated dot).
- Bodies are trimmed to ~4000 chars per note so the page stays light.
- Everything is inline in one file; no server, no internet. `examples/knowledge-graph.html` is a prebuilt sample.

## Make it a repeatable local project
Copy `build_graph.py` + `template.html` into the target repo (e.g. `tools/graphview/`) and add a one-line script/task that re-runs it on save, so the graph refreshes as notes or the extracted graph change.
