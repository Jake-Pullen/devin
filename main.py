from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, track
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.live import Live
from rich.prompt import Prompt
import requests
import sys
from tools import ToolExecutor
import random
import time

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
EXIT_STRINGS = ['exit','goodbye','go away','fuck off']

console = Console()

PRE_PROMPT = '''You have the following tools available, only use the tools if you need to.
please reply with only the tool call if you need to
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "examples": [
    {
      "input": {"tool": "get_weather", "parameters":{"city":"New York"}},
      "output": {"temperature": 22, "condition": "partly cloudy", "humidity": 65}
    },
    {
      "input": {"tool": "get_weather", "parameters":{"city":"London"}},
      "output": {"temperature": 18, "condition": "rainy", "humidity": 80}
    }
  ]
}'''

def ask_model(prompt: str, url=LM_STUDIO_URL) -> str:
    payload = {
        "model": 'qwen/qwen3-coder-30b',
        "messages": [{"role": "user", "content": PRE_PROMPT+prompt}],
        "temperature": 0.7,
        "max_tokens": 2048,
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()

def ask_model_no_pre(prompt: str, url=LM_STUDIO_URL) -> str:
    payload = {
        #"model": 'qwen/qwen3-coder-30b',
        "model": 'openai/gpt-oss-20b',
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2048,
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()

def get_llm_prompt():
    while True:
        llm_prompt = Prompt.ask("[bold cyan]Ask your local llm[/]")
        if llm_prompt.strip():
            return llm_prompt.strip()
        console.print("[red]Cannot be empty![/]", style="bold")
        return llm_prompt

def handle_llm_reply(llm_reply:str):
    architect = ToolExecutor()
    return architect.process_llm_response(llm_output=llm_reply)

def main():
    while True:
        llm_prompt = get_llm_prompt()
        if llm_prompt.lower() in EXIT_STRINGS:
            sys.exit()
        start = time.time()
          
        llm_reply = ask_model(llm_prompt)
        print(llm_reply)
        handled_response = handle_llm_reply(llm_reply)
        print(handled_response)
        print(handled_response == llm_reply)

        if handled_response != llm_reply:
            output = ask_model_no_pre(prompt=f'Make this lovely markdown, use fun emojis {handled_response}')

        elif handled_response == llm_reply:
            output = handled_response

        elapsed = time.time() - start
        panel_narrow = Panel(Markdown(output),
            title="LLM Reply",
            subtitle=f"Response time: {elapsed:.2f}s",
            expand=False,
        )

        console.print(panel_narrow)

if __name__ == "__main__":
    main()

