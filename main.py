from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, track
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.live import Live
from rich.prompt import Prompt

import random
import time

console = Console()

def ask_name() -> str:
    """Ask for a name and keep asking until it's not empty."""
    while True:
        name = Prompt.ask("[bold cyan]What is your name?[/]")
        if name.strip():
            return name.strip()
        console.print("[red]Name cannot be empty![/]", style="bold")

def ask_age() -> int:
    """Ask for age and validate it's a positive integer."""
    while True:
        age_str = Prompt.ask("[bold cyan]How old are you?[/]")
        try:
            age = int(age_str)
            if age <= 0:
                raise ValueError
            return age
        except ValueError:
            console.print("[red]Please enter a valid positive integer.[/]", style="bold")

name = ask_name()
age = ask_age()

panel_narrow = Panel(
    f"[bold green]Your Name is: {name}[/bold green]\n"
    f"[blue]And you are {age} Years Old.[/blue]",
    title="About You",
    subtitle="The info you gave",
    expand=False,
)

console.print(panel_narrow)
