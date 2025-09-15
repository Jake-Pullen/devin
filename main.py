from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

import sys

import time
import config
from llm_interface import llm

import logging

#TODO: add context for llm calls so we have history and can chain messages

console = Console()

class RichConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        if record.levelno >= logging.CRITICAL:
            console.print(f"[bold magenta]CRITICAL:[/bold magenta] {record.getMessage()}")
        elif record.levelno >= logging.ERROR:
            console.print(f"[bold red]ERROR:[/bold red] {record.getMessage()}")
        elif record.levelno >= logging.WARNING:
            console.print(f"[bold yellow]WARNING:[/bold yellow] {record.getMessage()}")
        # elif record.levelno >= logging.INFO:
        #     console.print(f"[bold blue]INFO:[/bold blue] {record.getMessage()}")
        # elif record.levelno >= logging.DEBUG:
        #     console.print(f"[bold green]DEBUG:[/bold green] {record.getMessage()}")


def main(logger):
    logger.info('Application Started')
    language_model = llm(logger)
    while True:
        llm_prompt = language_model.get_llm_prompt()
        if llm_prompt.lower() in config.EXIT_STRINGS:
            sys.exit()
        start = time.time()

        llm_reply = language_model.ask_model(llm_prompt)
        logger.info(f"LLM Reply: {llm_reply}")
        handled_response = language_model.handle_llm_reply(llm_reply)
        logger.info(f"Handled Response: {handled_response}")
        logger.info(f"Response equals original: {handled_response == llm_reply}")

        if handled_response != llm_reply:
            output = language_model.tool_response(prompt=f'Make this lovely markdown, use fun emojis {handled_response}')
            #TODO: Make sure to pass the history into the this so that if we ask additional questions it has context
            # For example get weather AND suggest clothing based on weather.
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
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log')
        ]
    )

    logger = logging.getLogger(__name__)
    logger.addHandler(RichConsoleHandler())
    logger.info("Logging Instantiated")

    main(logger)
