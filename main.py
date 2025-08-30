from rich import print, pretty
from rich.panel import Panel

def main():
    print("Hello from devin!")
    print("[italic red]Hello[/italic red] World!", locals())
    print(["Rich and pretty", True])
    print(Panel.fit("[bold yellow]Hi, I'm a Panel", border_style="red"))


if __name__ == "__main__":
    main()
