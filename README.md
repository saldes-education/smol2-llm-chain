# SmolLLM2 LLM Chain
To start the project run these:
```console
uv init
uv add transformers torch pydantic
uv run main.py
```

I've added `ovarload.py` as an example for how overloading works and `union.py` to show how discriminating union types work.

## Read more
- Read about [Generics](https://pydantic.dev/docs/validation/latest/concepts/models/#generic-models) 
- Read about [overloading](https://typing.python.org/en/latest/spec/overload.html)
- **BONUS:** [union](https://pydantic.dev/docs/validation/latest/concepts/unions/) types and [serialization](https://pydantic.dev/docs/validation/latest/concepts/serialization/)