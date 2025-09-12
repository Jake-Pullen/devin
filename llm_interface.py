import config
from tools import ToolExecutor
import requests
from rich import print
from rich.prompt import Prompt

#TODO: context squish when it gets big

class llm():
    def __init__(self, logger) -> None:
        self.logger = logger
        self.first_prompt = 1
        self.context = {
            "history": [],
            "summary": None,
            "metadata": {
                "created_at": None,
                "token_budget": 8000,
            }
        }

    def summarise_context(self):
        # add ai summary & created at time
        pass

    def add_to_history(self, history_object):
        self.context['history'].append(history_object)
        self.logger.debug(self.context['history'])

    def ask_model(self, prompt: str, url=config.LM_STUDIO_URL) -> str:
        # prompt = config.PRE_PROMPT + prompt
        payload = {
        "model": 'qwen/qwen3-coder-30b',
        "messages": [],
        "temperature": 0.7,
        "max_tokens": 2048,
        }
        self.add_to_history({"role": "user", "content": prompt})

        payload["messages"] = [
                {"role": "system", "content": config.SYSTEM_MESSAGE}
            ] + self.context['history']
        self.logger.debug(f'json payload: {payload}')
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        self.logger.debug(resp.json())
        self.add_to_history(resp.json()["choices"][0]["message"])
        return resp.json()["choices"][0]["message"]["content"].strip()
    
    def tool_response(self, prompt: str, url=config.LM_STUDIO_URL) -> str:
        payload = {
        "model": 'qwen/qwen3-coder-30b',
        "messages": [],
        "temperature": 0.7,
        "max_tokens": 2048,
        }
        payload["messages"] =  [{"role": "tool", "content": prompt}]
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        self.logger.debug(resp.json())
        return resp.json()["choices"][0]["message"]["content"].strip()

    def get_llm_prompt(self):
        while True:
            llm_prompt = Prompt.ask("[bold cyan]Ask your local llm[/]")
            self.logger.debug(f'prompt is: {llm_prompt}')
            if llm_prompt == '':
                self.logger.error("Cannot be empty!")
            return llm_prompt

    def handle_llm_reply(self, llm_reply:str):
        architect = ToolExecutor(self.logger)
        return architect.process_llm_response(llm_output=llm_reply)