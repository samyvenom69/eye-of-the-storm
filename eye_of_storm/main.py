#!/usr/bin/env python3
import asyncio
import argparse
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint

# Initialisation de la console Rich pour un affichage pro
console = Console()

def print_banner():
    banner_text = """[bold cyan]
  _____               _      _____ _                 
 |  ___|             | |    /  ___| |                
 | |__ _   _  ___    | |    \ `--.| |_ ___  _ __ _ __ ___  
 |  __| | | |/ _ \   | |     `--. \ __/ _ \| '__| '_ ` _ \ 
 | |__| |_| |  __/   | |____/\__/ / || (_) | |  | | | | | |
 \____/\__, |\___|   \_____/\____/ \__\___/|_|  |_| |_| |_|
        __/ |                                            
       |___/ [/bold cyan][bold yellow]Advanced OSINT Reconnaissance Framework[/bold yellow]
       
[bold white]STAY VIGILANT, TRACE EVERYTHING.[/bold white]
    """
    console.print(Panel(banner_text, title="[bold red]v2.0 Asynchronous Edition[/bold red]", expand=False))

async def simulate_async_recon(target: str, module_name: str) -> dict:
    """
    Simulation d'une tâche asynchrone (ex: ping un serveur, vérifier un pseudo).
    C'est ici que les vrais modules feront leurs requêtes sans bloquer le programme.
    """
    # Simule un délai réseau (entre 0.5 et 2 secondes)
    import random
    await asyncio.sleep(random.uniform(0.5, 2.0))
    
    # Simulation d'un résultat
    status = "FOUND" if random.choice([True, False]) else "NOT FOUND"
    return {"module": module_name, "target": target, "status": status}

async def run_one_click_async(target: str):
    """
    Moteur d'exécution asynchrone massif.
    """
    start_time = time.time()
    console.print(f"\n[bold green][*][/bold green] Initiating Deep Recon on: [bold yellow]{target}[/bold yellow]")
    
    # Liste des modules à exécuter en parallèle
    modules_to_run = [
        "DNS_Enumeration", "DarkNet_Breach_Check", "Username_Sherlock", 
        "Global_Phone_Intel", "Email_Verification", "Threat_Intel_Feed"
    ]

    results = []

    # Utilisation de Rich pour une barre de progression stylée
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        
        task_id = progress.add_task("[cyan]Executing modules asynchronously...", total=len(modules_to_run))
        
        # Création des tâches asynchrones
        tasks = [simulate_async_recon(target, mod) for mod in modules_to_run]
        
        # Exécution en parallèle (C'est ici que la magie de la vitesse opère)
        for completed_task in asyncio.as_completed(tasks):
            result = await completed_task
            results.append(result)
            progress.update(task_id, advance=1)
            # Affichage en temps réel dans le terminal
            color = "green" if result["status"] == "FOUND" else "red"
            progress.console.print(f"  ↳ [{color}]{result['module']}[/{color}] completed.")

    elapsed_time = time.time() - start_time

    # Affichage du rapport final dans un tableau propre
    console.print("\n[bold green][*] Reconnaissance Complete![/bold green]")
    
    table = Table(title=f"OSINT Intelligence Report: {target}")
    table.add_column("Module", justify="left", style="cyan", no_wrap=True)
    table.add_column("Target", style="magenta")
    table.add_column("Status", justify="right", style="green")

    for res in results:
        status_style = "[bold green]FOUND[/bold green]" if res["status"] == "FOUND" else "[bold red]NOT FOUND[/bold red]"
        table.add_row(res["module"], res["target"], status_style)

    console.print(table)
    console.print(f"[bold blue]Total execution time: {elapsed_time:.2f} seconds[/bold blue]\n")

def main():
    parser = argparse.ArgumentParser(description="Eye of the Storm: Advanced OSINT Framework")
    parser.add_argument('--target', type=str, required=True, help='The target for the operation (domain, username, phone)')
    
    args = parser.parse_args()

    print_banner()
    
    # Lancement de la boucle asynchrone principale
    try:
        asyncio.run(run_one_click_async(args.target))
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Operation aborted by user. Shutting down gracefully...[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()