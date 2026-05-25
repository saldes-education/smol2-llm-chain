from transformers import pipeline
from pprint import pprint

class SmolLLM:
    def __init__(self, model_name="HuggingFaceTB/SmolLM2-135M-Instruct"):
        print(f"Loading {model_name} into memory. This may take a while...")
        self.pipe = pipeline("text-generation", model=model_name)
        print("Model loaded successful!")
    
    def invoke(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        output = self.pipe(messages, max_new_tokens=150)
        return output[0]['generated_text'][-1]['content'].strip()
    
class PromptTemplate:
    def __init__(self, template_str: str):
        self.template_str = template_str
        
    def format(self, **kwargs):
        return self.template_str.format(**kwargs)
    
    def __or__(self, other):
        if isinstance(other, SmolLLM):
            return LLMChain(prompt_template=self, llm=other)
        raise TypeError("A PromptTemplate can only be piped into LLMChain.")
    
class LLMChain:
    def __init__(self, prompt_template: PromptTemplate, llm: SmolLLM):
        self.prompt_template = prompt_template
        self.llm = llm
        
    def invoke(self, **kwargs) -> str:
        formatted_prompt = self.prompt_template.format(**kwargs)
        return self.llm.invoke(formatted_prompt)

llm = SmolLLM()

recipe_prompt = PromptTemplate(
    template_str="Give me a quick 2-step recipe for a {dish} using only {ingredients_count} integredients. Think it through step by step and explain your reasoning."
)

recipe_chain = recipe_prompt | llm

result = recipe_chain.invoke(dish="mud cake", ingredients_count="four")

pprint(result)
