# from transformers import pipeline
from transformers import CodeLlamaTokenizer, LlamaForCausalLM
from huggingface_hub import login
import torch
import gradio as gr
from dotenv import load_dotenv
from os import getenv

model_id = "meta-llama/CodeLlama-7b-hf"

load_dotenv()
TOKEN = getenv("HF_TOKEN")
login(TOKEN)

tokenizer = CodeLlamaTokenizer.from_pretrained("meta-llama/CodeLlama-7b-hf")
model = LlamaForCausalLM.from_pretrained(
    "meta-llama/CodeLlama-7b-hf", device_map="auto")


def generate_text(prompt, max_length=50, temperature=1.0):
    # Tokenize the input prompt
    # generated_text = generator(prompt, max_new_tokens=128)
    # answer = generated_text[0]["generated_text"]

    input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]
    input_ids = input_ids.to("cuda" if torch.cuda.is_available() else "cpu")
    generated_ids = model.generate(input_ids,
                                   max_new_tokens=max_length,
                                   temperature=temperature)
    filling = tokenizer.batch_decode(generated_ids[:, input_ids.shape[1]:],
                                     skip_special_tokens=True)[0]
    return prompt.replace("<FILL_ME>", filling)


# Create the Gradio interface
def generate_interface(prompt, max_length, temperature):
    return generate_text(prompt, max_length=max_length, temperature=temperature)


interface = gr.Interface(
    fn=generate_interface,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter your prompt here",
                   label="Prompt"),
        gr.Slider(10, 512, value=128, label="Max Length"),
        gr.Slider(0.7, 1.3, value=1.0, label="Temperature")
    ],
    outputs="text",
    title="Text Generation with Codellama",
    description="Enter a prompt and experiment with different parameters to generate text."
)

interface.launch()
