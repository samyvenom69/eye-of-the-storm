"""HTML/JSON Report Generator — Phase: INTELLIGENCE"""
import json
from pathlib import Path
from datetime import datetime
from modules import BaseModule

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>Eye of the Storm — OSINT Report</title>
<style>
  body {{ font-family: monospace; background:#0a0e1a; color:#c0c8d8; padding:2rem; }}
  h1 {{ color:#00ccff; letter-spacing:4px; }}
  h2 {{ color:#0099bb; border-bottom:1px solid #0a3f6a; padding-bottom:4px; }}
  .meta {{ color:#446688; font-size:.85rem; }}
  pre {{ background:#060b14; border:1px solid #0a3f6a; padding:1rem;
         border-radius:6px; overflow-x:auto; color:#8fb8d0; font-size:.82rem; }}
  .badge {{ display:inline-block; padding:2px 8px; border-radius:4px;
            background:#0e2a4a; color:#00aadd; font-size:.75rem; margin:2px; }}
</style>
</head>
<body>
<h1>👁 EYE OF THE STORM</h1>
<p class="meta">Advanced OSINT Reconnaissance Framework | Educational Use Only</p>
<hr style="border-color:#0a3f6a"/>
<h2>Target: {target}</h2>
<p class="meta">Generated: {timestamp}</p>
{modules_html}
<hr style="border-color:#0a3f6a"/>
<p class="meta">Stay vigilant. Follow the trace of everything. — For authorized, ethical use only.</p>
</body>
</html>"""

class ReportModule(BaseModule):
    """Generate HTML/JSON/TXT reports from scan results."""
    def run(self) -> dict:
        return {"message": "Use generate() with full results dict."}

    def generate(self, all_results: dict, fmt: str = "html", timestamp: str = ""):
        ts       = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
        target   = all_results.get("target", "unknown")
        safe     = target.replace(".", "_").replace("@", "_at_")
        out_dir  = Path("output"); out_dir.mkdir(exist_ok=True)
        if fmt == "json":
            path = out_dir / f"{safe}_{ts}.json"
            path.write_text(json.dumps(all_results, indent=2, default=str))
        else:
            mods_html = ""
            for mod, data in all_results.get("modules", {}).items():
                mods_html += f"<h2>{mod.upper()}</h2><pre>{json.dumps(data, indent=2, default=str)}</pre>"
            html = HTML_TEMPLATE.format(target=target, timestamp=ts, modules_html=mods_html)
            path = out_dir / f"{safe}_{ts}.html"
            path.write_text(html)
        self.info(f"Report saved → {path}")
        return str(path)
