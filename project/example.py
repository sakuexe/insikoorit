import gradio as gr
from transformers import pipeline
import sys


def greet(name: str):
    return f"Hello, {name}!"


# Example 2
def gpt2(prompt: str) -> None:
    generator = pipeline('text-generation', model='gpt2', device="cuda")
    result = generator(prompt, max_length=50, num_return_sequences=1,
                       clean_up_tokenization_spaces=True, truncation=True)
    response: str = result[0]["generated_text"]
    print("=" * 32)
    print(response)
    print("=" * 32)


if sys.argv[1] is not None and sys.argv[1] == "gpt":
    if sys.argv[2] is None:
        print("pass a prompt after the gpt parameter")
        print("e.g. python3 example.py gpt 'As a large language model, I'")
    gpt2(sys.argv[2])
else:
    # Example 1
    iface = gr.Interface(fn=greet, inputs="text", outputs="text")
    iface.launch()
