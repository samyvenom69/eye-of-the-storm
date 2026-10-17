"""Eye of the Storm — Banner & display helpers."""

from rich.console import Console
from rich.text    import Text
from rich.panel   import Panel
from rich         import box

console = Console()

BANNER = r"""
  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
"""

PHASES = "[ 1-RECON ] → [ 2-INVESTIGATE ] → [ 3-ANALYSE ] → [ 4-INTELLIGENCE ]"
TAGLINE = "Stay vigilant. Follow the trace of everything."

PHASE_COLORS = {
    "whois":     "cyan",   "subdomain": "cyan",   "ip":      "cyan",
    "portscan":  "cyan",   "metadata":  "cyan",
    "username":  "blue",   "email":     "blue",   "phone":   "blue",
    "exif":      "blue",   "dork":      "blue",
    "scrape":    "yellow", "wayback":   "yellow", "revimg":  "yellow",
    "geoint":    "yellow",
    "threat":    "red",    "social":    "red",    "report":  "green",
}


def print_banner():
    t = Text(BANNER, style="bold cyan")
    console.print(t)
    console.print(f"  [bold white]{PHASES}[/bold white]")
    console.print(f"  [dim italic]{TAGLINE}[/dim italic]\n")


def print_phase(module_name: str):
    color = PHASE_COLORS.get(module_name, "white")
    panel = Panel(
        f"[bold {color}]Running module:[/bold {color}] [white]{module_name.upper()}[/white]",
        box=box.SIMPLE_HEAD,
        border_style=color,
    )
    console.print(panel)


def print_result(label: str, value, color: str = "white"):
    console.print(f"  [dim]{'─'*4}[/dim] [bold]{label}:[/bold] [{color}]{value}[/{color}]")


def print_section(title: str):
    console.rule(f"[bold cyan] {title} [/bold cyan]")
