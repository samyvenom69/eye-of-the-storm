"""HTML/JSON Report Generator — Phase: INTELLIGENCE"""

import html
import json
from datetime import datetime
from pathlib import Path

from modules import BaseModule

CSS = """
:root {
  --bg: #070b14; --panel: #0d1424; --panel2: #111a2e; --border: #1d2c4a;
  --txt: #d5deef; --dim: #7d8fb3; --accent: #22d3ee; --accent2: #818cf8;
  --ok: #34d399; --err: #f87171;
}
* { box-sizing: border-box; }
body { margin: 0; background: radial-gradient(1200px 600px at 70% -10%, #14203d 0%, var(--bg) 55%);
       color: var(--txt); font: 15px/1.6 'Segoe UI', system-ui, sans-serif; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 2.5rem 1.5rem 4rem; }
header.hero { border: 1px solid var(--border); border-radius: 14px;
  background: linear-gradient(135deg, rgba(34,211,238,.10), rgba(129,140,248,.10));
  padding: 2rem 2.2rem; margin-bottom: 2rem; }
h1 { margin: 0 0 .3rem; font-size: 1.9rem; letter-spacing: 3px;
     background: linear-gradient(90deg, var(--accent), var(--accent2));
     -webkit-background-clip: text; background-clip: text; color: transparent; }
.tagline { color: var(--dim); font-size: .9rem; margin: 0; }
.meta { display: flex; flex-wrap: wrap; gap: .5rem 1.6rem; margin-top: 1.1rem;
        color: var(--dim); font-size: .88rem; }
.meta b { color: var(--txt); font-weight: 600; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
         gap: 1rem; margin-bottom: 2rem; }
.card { background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
        padding: 1rem 1.2rem; }
.card .num { font-size: 1.7rem; font-weight: 700; }
.card .lbl { color: var(--dim); font-size: .78rem; text-transform: uppercase; letter-spacing: 1px; }
.num.ok { color: var(--ok); } .num.err { color: var(--err); } .num.accent { color: var(--accent); }
h2 { font-size: 1.05rem; color: var(--accent); margin: 2.2rem 0 .8rem; letter-spacing: 1px; }
table.status { width: 100%; border-collapse: collapse; background: var(--panel);
               border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
table.status th, table.status td { padding: .6rem .9rem; text-align: left;
               border-bottom: 1px solid var(--border); font-size: .9rem; }
table.status th { background: var(--panel2); color: var(--dim); text-transform: uppercase;
                  font-size: .72rem; letter-spacing: 1px; }
table.status tr:last-child td { border-bottom: none; }
.badge { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: .75rem; font-weight: 600; }
.badge.ok { background: rgba(52,211,153,.12); color: var(--ok); border: 1px solid rgba(52,211,153,.35); }
.badge.err { background: rgba(248,113,113,.12); color: var(--err); border: 1px solid rgba(248,113,113,.35); }
.badge.phase { background: rgba(129,140,248,.12); color: var(--accent2); border: 1px solid rgba(129,140,248,.35); }
details { background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
          margin-bottom: .8rem; overflow: hidden; }
summary { cursor: pointer; padding: .8rem 1.1rem; font-weight: 600; list-style: none;
          display: flex; align-items: center; gap: .7rem; }
summary::-webkit-details-marker { display: none; }
summary::before { content: '▸'; color: var(--accent); transition: transform .15s; }
details[open] summary::before { transform: rotate(90deg); }
summary:hover { background: var(--panel2); }
pre { margin: 0; padding: 1rem 1.2rem; border-top: 1px solid var(--border);
      background: #05080f; color: #9fc3e8; font: .8rem/1.5 'Cascadia Code', Consolas, monospace;
      overflow-x: auto; white-space: pre-wrap; word-break: break-word; }
footer { margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--border);
         color: var(--dim); font-size: .82rem; text-align: center; }
@media print { body { background: #fff; color: #111; } .card, details, table.status { border-color: #ccc; } }
"""


class ReportModule(BaseModule):
    """Generate HTML/JSON reports from scan results."""

    def run(self) -> dict:
        return {"message": "Use generate() with full results dict."}

    def generate(self, all_results: dict, fmt: str = "html", timestamp: str = ""):
        ts = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
        target = all_results.get("target", "unknown")
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in target)
        out_dir = Path("output")
        out_dir.mkdir(exist_ok=True)

        if fmt == "json":
            path = out_dir / f"{safe}_{ts}.json"
            path.write_text(json.dumps(all_results, indent=2, default=str), encoding="utf-8")
        else:
            path = out_dir / f"{safe}_{ts}.html"
            path.write_text(self._render_html(all_results, ts), encoding="utf-8")

        self.info(f"Report saved → {path}")
        return str(path)

    # ------------------------------------------------------------------ #

    def _render_html(self, all_results: dict, ts: str) -> str:
        target = html.escape(str(all_results.get("target", "unknown")))
        modules = all_results.get("modules", {})
        durations = all_results.get("durations", {})
        elapsed = all_results.get("elapsed")

        total = len(modules)
        errors = sum(1 for d in modules.values() if isinstance(d, dict) and "error" in d)
        ok = total - errors

        # Summary cards
        cards = f"""
<div class="cards">
  <div class="card"><div class="num accent">{total}</div><div class="lbl">Modules run</div></div>
  <div class="card"><div class="num ok">{ok}</div><div class="lbl">Completed</div></div>
  <div class="card"><div class="num err">{errors}</div><div class="lbl">Errors</div></div>
  <div class="card"><div class="num accent">{elapsed if elapsed is not None else '—'}s</div><div class="lbl">Total time</div></div>
</div>"""

        # Status table
        rows = ""
        for name, data in modules.items():
            has_err = isinstance(data, dict) and "error" in data
            badge = '<span class="badge err">ERROR</span>' if has_err else '<span class="badge ok">COMPLETED</span>'
            dur = durations.get(name)
            dur = f"{dur:.2f}s" if isinstance(dur, (int, float)) else "—"
            rows += f"<tr><td><b>{html.escape(name)}</b></td><td>{badge}</td><td>{dur}</td></tr>"
        status_table = f"""
<h2>Execution summary</h2>
<table class="status">
  <tr><th>Module</th><th>Status</th><th>Duration</th></tr>
  {rows}
</table>"""

        # Collapsible per-module sections
        sections = ""
        for name, data in modules.items():
            has_err = isinstance(data, dict) and "error" in data
            badge = '<span class="badge err">ERROR</span>' if has_err else '<span class="badge ok">OK</span>'
            pretty = html.escape(json.dumps(data, indent=2, default=str))
            sections += f"""
<details>
  <summary>{html.escape(name.upper())} {badge}</summary>
  <pre>{pretty}</pre>
</details>"""

        generated = datetime.strptime(ts, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S") \
            if len(ts) == 15 else ts

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Eye of the Storm — OSINT Report — {target}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <h1>👁 EYE OF THE STORM</h1>
    <p class="tagline">Advanced OSINT Reconnaissance Framework — Executive Report</p>
    <div class="meta">
      <span>Target&nbsp;: <b>{target}</b></span>
      <span>Generated&nbsp;: <b>{generated}</b></span>
      <span>Engine&nbsp;: <b>EOTS v2</b></span>
    </div>
  </header>

  {cards}
  {status_table}

  <h2>Detailed findings</h2>
  {sections}

  <footer>
    Stay vigilant. Follow the trace of everything.<br/>
    For authorized, ethical use only.
  </footer>
</div>
</body>
</html>"""
