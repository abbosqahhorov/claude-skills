#!/usr/bin/env python3
"""graphview — render a folder of notes, or graphify-out/ data, as one standalone
Obsidian-style interactive HTML knowledge graph. No dependencies, no network.

Usage:
  python -I build_graph.py <source> [-o out.html] [--title "..."]

<source> is either:
  - a directory of Markdown notes (parses YAML frontmatter + [[wikilinks]] + [](x.md) links), or
  - a graphify-out directory or a JSON file shaped {"nodes":[{id,label,type,desc,body,path,links[]}], "links":[[a,b],...]}.

The HTML template lives next to this script as template.html.
"""
import sys, os, re, json, argparse

def parse_md_dir(root):
    nodes, idset = [], set()
    files = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in (".git", "node_modules", ".obsidian")]
        for fn in fns:
            if fn.lower().endswith((".md", ".markdown")):
                files.append(os.path.join(dp, fn))
    for fp in sorted(files):
        rel = os.path.relpath(fp, root).replace("\\", "/")
        nid = os.path.splitext(os.path.basename(fp))[0]
        txt = open(fp, encoding="utf-8", errors="replace").read().replace("\r", "")
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", txt, re.S)
        fm, body = (m.group(1), m.group(2)) if m else ("", txt)
        def fld(k):
            mm = re.search(r"^%s:\s*(.+)$" % k, fm, re.M)
            return mm.group(1).strip().strip('"').strip("'") if mm else ""
        typ = fld("type") or fld("node_type") or "note"
        label = fld("title") or fld("name") or nid.replace("-", " ")
        desc = fld("description")
        wl = set(re.findall(r"\[\[([^\]|#]+)", body))                       # [[wikilink]]
        for _, tgt in re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", body):     # [text](file.md)
            wl.add(os.path.splitext(os.path.basename(tgt))[0])
        nodes.append({"id": nid, "label": label, "type": typ, "desc": desc,
                      "path": rel, "body": body.strip()[:4000], "links": sorted(wl)})
        idset.add(nid)
    links = []
    for n in nodes:
        for t in n["links"]:
            if t in idset and t != n["id"]:
                links.append([n["id"], t])
    return {"nodes": nodes, "links": links}

def load_json_source(src):
    if os.path.isdir(src):
        for cand in ("graph.json", "nodes.json", "knowledge-graph.json"):
            p = os.path.join(src, cand)
            if os.path.isfile(p):
                src = p; break
        else:
            return None
    try:
        data = json.load(open(src, encoding="utf-8"))
    except Exception:
        return None
    if isinstance(data, dict) and "nodes" in data:
        return data
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("-o", "--out")
    ap.add_argument("--title", default="Bilim Grafigi")
    a = ap.parse_args()

    g = load_json_source(a.source)
    if g is None:
        if not os.path.isdir(a.source):
            sys.exit(f"Source not found or unsupported: {a.source}")
        g = parse_md_dir(a.source)
    if not g.get("nodes"):
        sys.exit("No nodes found. Point at a folder of .md notes or a graph JSON.")

    here = os.path.dirname(os.path.abspath(__file__))
    tpl = open(os.path.join(here, "template.html"), encoding="utf-8").read()
    html = (tpl.replace("__GRAPH__", json.dumps(g, ensure_ascii=False).replace("</", "<\\/"))
               .replace("__TITLE__", a.title))

    out = a.out or os.path.join(a.source if os.path.isdir(a.source) else os.path.dirname(a.source) or ".",
                                "knowledge-graph.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"{len(g['nodes'])} nodes, {len(g.get('links', []))} links -> {out}")

if __name__ == "__main__":
    main()
