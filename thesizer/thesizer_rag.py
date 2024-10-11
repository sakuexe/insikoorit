# the following code is collected from this hugging face tutorial
# https://huggingface.co/learn/cookbook/rag_zephyr_langchain
# langchain
from langchain_core.prompts import ChatPromptTemplate
from transformers import pipeline
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
# stdlib
from asyncio import get_event_loop
import sys
import os

# local
from utils.documents import get_document_database

# MODEL_NAME = "meta-llama/Llama-3.2-3B"
# MODEL_NAME = "google/gemma-7b"
MODEL_NAME = "google/gemma-2-2b-it"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.bfloat16
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

text_generation_pipeline = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.2,
    do_sample=True,
    repetition_penalty=1.1,
    return_full_text=True,
    max_new_tokens=400,
)

llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

# https://www.mirascope.com/post/langchain-prompt-template
prompt_template = ChatPromptTemplate([
    ("system", """You are 'thesizer', a HAMK thesis assistant.
    You will help the user with technicalities on writing a thesis
    for hamk. If you can't find the answer from the context given to you,
    you will not answer. You answer with only a single message."""),
    ("system", "{context}"),
    ("assistant", "Hei! Kuinka voin auttaa opinnäytetyösi kanssa?"),
    ("user", "{user_input}"),
])


async def main():
    # get the documents
    db = await get_document_database("learning_material/*/*")
    n_of_best_results = 4
    retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"k": n_of_best_results})

    question = "mitä tarkoittaa abstract sivu? Mitä siihen voi laittaa?"
    cli_question = sys.argv.pop()
    if cli_question != os.path.basename(__file__):
        question = sys.argv[1]

    retrieval_chain = (
        {"context": retriever, "user_input": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )

    response = retrieval_chain.invoke(question)

    # debugging
    # print("=====raw response=====")
    # print(response)

    parsed_answer = response.split("AI:").pop().strip()

    print(f"User prompt: {question}")
    print(f"{'=' * 23}Thesizer answer{'=' * 23}")
    print(parsed_answer)


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
