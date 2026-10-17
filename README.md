# claude-skills

Open-source [Agent Skills](https://docs.anthropic.com/en/docs/claude-code/skills) by [Abbos Qahhorov](https://github.com/abbosqahhorov). Small, focused skills that work in Claude Code (and other agents that read `SKILL.md`). More to come — this repo is the home for them.

## Skills

| Skill | What it does |
|-------|--------------|
| **[graphview](skills/graphview/)** | Turn notes, docs, or a codebase into an interactive, Obsidian-style knowledge graph — one standalone HTML file, no dependencies, no server, light + dark. |

## graphview

You give it a folder of Markdown notes (linked with `[[wikilinks]]` or `[text](file.md)`) or a graph JSON, and it builds a single HTML page you can open in any browser:

- force-directed graph you can drag, zoom (wheel) and pan
- hover a node to highlight its neighbours; everything else dims
- click a node to read the full note in a side panel, with clickable links to connected notes
- search to spotlight matching nodes
- node colour = type (legend builds itself), node size = number of links

It's the **view**. For the **structure** underneath a codebase, run a graph extractor first (for example [graphify](https://github.com/snarktank/graphify) or a domain-modeling pass), then point graphview at its output. A sample output is in [`skills/graphview/examples/`](skills/graphview/examples/).

### Run it directly

```bash
python -I skills/graphview/build_graph.py <source> -o knowledge-graph.html --title "My Graph"
```

`<source>` is a folder of `.md` notes, or a JSON file / directory shaped
`{"nodes":[{id,label,type,desc,body,path,links:[]}], "links":[[a,b],...]}`.

## Install as a skill

**Copy it in** (simplest, works in any agent that reads `SKILL.md`):

```bash
cp -r skills/graphview ~/.claude/skills/graphview
```

**Or as a Claude Code plugin:**

```
/plugin marketplace add abbosqahhorov/claude-skills
/plugin install graphview
```

Then just ask, e.g. *"make an Obsidian-style graph of this docs folder"* or *"bu papkani bilim grafigi qilib ber"*.

## License

[MIT](LICENSE) © Abbos Qahhorov. Contributions welcome — open an issue or a PR.
