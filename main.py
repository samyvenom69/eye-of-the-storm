#!/usr/bin/env python3
"""
Eye of the Storm (EOTS) — Main Orchestrator & CLI Engine
Connects all 16 OSINT/EASM modules across the 4 intelligence phases.
"""

import argparse
import importlib
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from rich.table import Table
from rich.prompt import Prompt
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from utils.config import Config
from utils.banner import (
    console,
    print_banner,
    print_phase,
    print_section,
)

__version__ = "2.0.0"

# Registry mapping CLI flags to (module path, class name, phase, description).
# Module classes are imported lazily so startup stays fast (e.g. spaCy is only
# loaded when the scrape module is actually executed).
MODULE_REGISTRY = {
    # Phase 1 — RECON
    "whois":     ("modules.whois_dns",      "WhoisDNSModule",      "1-RECON",        "WHOIS lookup & DNS records (A, MX, NS, TXT, CNAME)"),
    "subdomain": ("modules.subdomain",      "SubdomainModule",     "1-RECON",        "Subdomain enumeration (crt.sh + wordlist)"),
    "ip":        ("modules.ip_geo",         "IPGeoModule",         "1-RECON",        "IP geolocation, ASN, abuse score, reverse DNS"),
    "portscan":  ("modules.port_scan",      "PortScanModule",      "1-RECON",        "TCP/UDP port scanning via Nmap integration"),
    "metadata":  ("modules.file_metadata",  "FileMetadataModule",  "1-RECON",        "Extract metadata from PDF, DOCX, XLSX, images"),
    # Phase 2 — INVESTIGATE
    "username":  ("modules.username_recon", "UsernameReconModule", "2-INVESTIGATE",  "Username lookup across public platforms"),
    "email":     ("modules.email_breach",   "EmailBreachModule",   "2-INVESTIGATE",  "Breach detection, paste leaks, email validation"),
    "phone":     ("modules.phone_intel",    "PhoneIntelModule",    "2-INVESTIGATE",  "Carrier, region, timezone, number validation"),
    "exif":      ("modules.exif_gps",       "ExifGPSModule",       "2-INVESTIGATE",  "Extract GPS coordinates & EXIF from images"),
    "dork":      ("modules.google_dork",    "GoogleDorkModule",    "2-INVESTIGATE",  "Automated Google Dorking query templates"),
    # Phase 3 — ANALYSE
    "scrape":    ("modules.web_scraper",    "WebScraperModule",    "3-ANALYSE",      "Website crawling + spaCy NLP entity extraction"),
    "wayback":   ("modules.wayback",        "WaybackModule",       "3-ANALYSE",      "Wayback Machine historical snapshot analysis"),
    "revimg":    ("modules.reverse_image",  "ReverseImageModule",  "3-ANALYSE",      "Reverse image search correlation"),
    "geoint":    ("modules.geoint",         "GeointModule",        "3-ANALYSE",      "GEOINT coordinate analysis & satellite links"),
    # Phase 4 — INTELLIGENCE
    "threat":    ("modules.threat_intel",   "ThreatIntelModule",   "4-INTELLIGENCE", "Threat intelligence feeds (VirusTotal, AbuseIPDB)"),
    "social":    ("modules.social_intel",   "SocialIntelModule",   "4-INTELLIGENCE", "Reddit & GitHub public data intelligence"),
    "report":    ("modules.report",         "ReportModule",        "4-INTELLIGENCE", "HTML / JSON executive report generation"),
}

# Predefined pipelines
RECON_PIPELINE = ["whois", "subdomain", "ip", "portscan"]
FULL_PIPELINE  = [
    "whois", "subdomain", "ip", "portscan",
    "email", "dork", "scrape", "wayback",
    "threat", "social"
]


def load_module_class(mod_name: str):
    """Lazily import a module class on first use."""
    mod_path, class_name, _, _ = MODULE_REGISTRY[mod_name]
    return getattr(importlib.import_module(mod_path), class_name)


def list_modules_table():
    """Display all available modules in a formatted Rich table."""
    table = Table(title="🧩 Eye of the Storm — Available Modules")
    table.add_column("Flag (--module)", style="bold cyan", no_wrap=True)
    table.add_column("Phase", style="magenta", no_wrap=True)
    table.add_column("Description", style="white")

    for key, (_, _, phase, desc) in MODULE_REGISTRY.items():
        table.add_row(key, phase, desc)

    console.print(table)


def _run_one(mod_name: str, target: str, config: Config, verbose: bool):
    """Execute a single module and return (name, result, duration)."""
    started = time.time()
    mod_class = load_module_class(mod_name)
    instance = mod_class(target=target, config=config, verbose=verbose)
    result = instance.run()
    return mod_name, result, time.time() - started


def execute_pipeline(target: str, selected_modules: list, config: Config,
                     verbose: bool = False, report_fmt: str = None, jobs: int = 4):
    """Run selected modules (in parallel by default) and optionally generate a report."""
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    all_results = {
        "target": target,
        "timestamp": timestamp,
        "modules": {},
        "durations": {},
    }

    print_section(f"TARGET: {target}")

    runnable = [m for m in selected_modules if m != "report"]
    for mod_name in runnable:
        if mod_name not in MODULE_REGISTRY:
            console.print(f"  [bold red][!][/bold red] Unknown module '[yellow]{mod_name}[/yellow]'. Skipping.")
    runnable = [m for m in runnable if m in MODULE_REGISTRY]

    if not runnable:
        console.print("[bold red]No valid module to run.[/bold red]")
        return all_results

    if len(runnable) > 1 and jobs > 1:
        # Parallel engine: independent modules run concurrently.
        workers = min(jobs, len(runnable))
        console.print(f"  [dim]⚡ Parallel engine: {workers} workers for {len(runnable)} modules[/dim]")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:
            task_ids = {
                progress.add_task(f"[cyan]{m}[/cyan]", total=None): m
                for m in runnable
            }
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {
                    executor.submit(_run_one, m, target, config, verbose): m
                    for m in runnable
                }
                for future in as_completed(futures):
                    mod_name = futures[future]
                    try:
                        _, res, dur = future.result()
                        all_results["modules"][mod_name] = res
                    except Exception as exc:
                        console.print(f"  [bold red][ERROR][/bold red] Module '{mod_name}' failed: {exc}")
                        all_results["modules"][mod_name] = {"error": str(exc)}
                        dur = 0.0
                    all_results["durations"][mod_name] = round(dur, 2)
                    for task_id, name in task_ids.items():
                        if name == mod_name:
                            progress.update(task_id, description=f"[green]✓ {name}[/green] ({dur:.1f}s)", completed=100, total=100)
    else:
        # Sequential mode with a spinner per module.
        for mod_name in runnable:
            print_phase(mod_name)
            started = time.time()
            try:
                _, res, dur = _run_one(mod_name, target, config, verbose)
                all_results["modules"][mod_name] = res
            except Exception as exc:
                console.print(f"  [bold red][ERROR][/bold red] Module '{mod_name}' failed: {exc}")
                all_results["modules"][mod_name] = {"error": str(exc)}
                dur = time.time() - started
            all_results["durations"][mod_name] = round(dur, 2)

    elapsed = time.time() - start_time
    all_results["elapsed"] = round(elapsed, 2)

    # Summary Table
    print_section("EXECUTION SUMMARY")
    summary = Table(title=f"OSINT Assessment Summary — {target}")
    summary.add_column("Module", style="cyan")
    summary.add_column("Phase", style="magenta")
    summary.add_column("Status", justify="right")
    summary.add_column("Duration", justify="right", style="dim")

    for mod_name in runnable:
        if mod_name in all_results["modules"]:
            mod_data = all_results["modules"][mod_name]
            _, _, phase, _ = MODULE_REGISTRY[mod_name]
            has_err = isinstance(mod_data, dict) and "error" in mod_data
            status_str = "[bold red]ERROR[/bold red]" if has_err else "[bold green]COMPLETED[/bold green]"
            duration = f"{all_results['durations'].get(mod_name, 0):.2f}s"
            summary.add_row(mod_name, phase, status_str, duration)

    console.print(summary)
    console.print(f"  [bold blue]⏱ Total execution time: {elapsed:.2f} seconds[/bold blue]\n")

    # Report generation if requested
    if report_fmt:
        print_phase("report")
        reporter_cls = load_module_class("report")
        reporter = reporter_cls(target=target, config=config, verbose=verbose)
        out_path = reporter.generate(all_results, fmt=report_fmt, timestamp=timestamp)
        console.print(f"  [bold green][✓] Report exported to:[/bold green] [underline cyan]{out_path}[/underline cyan]\n")

    return all_results


def interactive_menu(config: Config):
    """Interactive CLI menu when launched without arguments."""
    list_modules_table()
    console.print("\n[bold cyan]Interactive Mode[/bold cyan] (Press Ctrl+C to exit)")
    target = Prompt.ask("\n[bold yellow]🎯 Enter Target[/bold yellow] (Domain, IP, +Phone, Email, or Username)")
    mod_choice = Prompt.ask(
        "[bold yellow]🧩 Enter Module flag[/bold yellow] (e.g., [cyan]phone[/cyan], [cyan]whois[/cyan], [cyan]username[/cyan], [cyan]email[/cyan], or [green]all[/green])",
        default="whois"
    )
    want_report = Prompt.ask("[bold yellow]📄 Generate HTML Report?[/bold yellow]", choices=["y", "n"], default="n")

    mods = FULL_PIPELINE if mod_choice.lower() == "all" else [m.strip() for m in mod_choice.split(",")]
    fmt = "html" if want_report == "y" else None
    execute_pipeline(target=target, selected_modules=mods, config=config, verbose=True, report_fmt=fmt)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eots.sh",
        description="👁️ Eye of the Storm (EOTS) — Advanced OSINT & EASM Reconnaissance Framework",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:
  ./eots.sh --module phone --target "+33617770590"
  ./eots.sh --module username --target "samyvenom69"
  ./eots.sh --module email --target "contact@jmmotors.fr"
  ./eots.sh --module whois --target jmmotors.fr
  ./eots.sh --target jmmotors.fr --modules whois,subdomain,ip
  ./eots.sh --target jmmotors.fr --full-recon --output html
  ./eots.sh --target jmmotors.fr --all --report --jobs 8
"""
    )
    parser.add_argument("-t", "--target", type=str, help="Target (Domain, IP, Email, +Phone, Username, or File path)")
    parser.add_argument("-m", "--module", type=str, help="Single module to run (e.g., phone, username, email, whois, ip)")
    parser.add_argument("--modules", type=str, help="Comma-separated list of modules (e.g., whois,subdomain,ip)")
    parser.add_argument("--full-recon", action="store_true", help="Run Phase 1 Recon pipeline (whois, subdomain, ip, portscan)")
    parser.add_argument("-a", "--all", action="store_true", help="Run full multi-phase OSINT pipeline")
    parser.add_argument("-r", "--report", action="store_true", help="Generate standalone HTML report in output/ directory")
    parser.add_argument("-o", "--output", type=str, choices=["html", "json"], help="Export results format (html or json)")
    parser.add_argument("-w", "--wordlist", type=str, help="Custom wordlist path for subdomain enumeration")
    parser.add_argument("-j", "--jobs", type=int, default=4, help="Max parallel workers when running several modules (default: 4, 1 = sequential)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug logging")
    parser.add_argument("--list", action="store_true", help="List all 16 available modules and exit")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    print_banner()
    config = Config()

    if args.wordlist:
        config.WORDLIST_PATH = args.wordlist

    if args.list:
        list_modules_table()
        sys.exit(0)

    # Launch interactive menu if no arguments provided
    if not args.target:
        try:
            interactive_menu(config)
        except KeyboardInterrupt:
            console.print("\n[bold red][!] Session terminated by user.[/bold red]")
        sys.exit(0)

    # Determine which modules to run
    selected = []
    if args.module:
        selected = [args.module.replace(".py", "").strip().lower()]
    elif args.modules:
        selected = [m.replace(".py", "").strip().lower() for m in args.modules.split(",") if m.strip()]
    elif args.full_recon:
        selected = RECON_PIPELINE
    elif args.all:
        selected = FULL_PIPELINE
    else:
        # Default fallback if only --target is passed: smart detection
        if args.target.startswith("+") or args.target.replace(" ", "").isdigit():
            selected = ["phone"]
        elif "@" in args.target:
            selected = ["email"]
        elif "." in args.target:
            selected = ["whois", "ip", "subdomain"]
        else:
            selected = ["username"]

    report_fmt = args.output if args.output else ("html" if args.report else None)

    try:
        execute_pipeline(
            target=args.target,
            selected_modules=selected,
            config=config,
            verbose=args.verbose,
            report_fmt=report_fmt,
            jobs=max(1, args.jobs),
        )
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Operation aborted by user. Shutting down gracefully...[/bold red]")
        sys.exit(0)


if __name__ == "__main__":
    main()
