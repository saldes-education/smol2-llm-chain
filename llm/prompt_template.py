from pydantic import BeforeValidator
from typing import Annotated
from agentic.runnable.runnable import Runnable
from json.decoder import JSONDecodeError
from agentic.utils.logging import log
import json
import inspect

class SafeDict(dict):
    def __missing__(self, key):
        return f"{{{key}}}" 

class PromptTemplate(Runnable[dict | str, str]):
    name: str = "prompt_template"
    template_str: Annotated[str, BeforeValidator(inspect.cleandoc)]
    
    def invoke(self, data: dict | str) -> str:
        """ Takes either a str or a dict and returns a formatted string """
        log(data)
        if isinstance(data, str):
            try:
                parsed = json.loads(data)
                if isinstance(parsed, dict):
                    data = SafeDict(parsed)
                else:
                    log("Valid JSON but not an object, treating as raw text")
                    return self.template_str.format(text=data)
            except (JSONDecodeError):
                log("Not valid json returning raw string")
                return self.template_str.format(text=data)
        try:
            return self.template_str.format(**data)
        except TypeError:
            log(f"Expected a dictionary for keyword unpacking, got {type(data)}")
            return self.template_str
    
    def format(self, **kwargs):
        return self.template_str.format(**kwargs)
