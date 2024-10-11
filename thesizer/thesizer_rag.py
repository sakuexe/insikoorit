# the following code is collected from this hugging face tutorial
# https://huggingface.co/learn/cookbook/rag_zephyr_langchain
# langchain
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
# stdlib
import sys
import re
import textwrap
from asyncio import get_event_loop
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

prompt_template = """
<system>
You are 'thesizer', a HAMK thesis assistant.
you speak both finnish and english. You will help the user
with technicalities on writing a thesis for hamk.
If you do not know the answer based on the context given to you,
you will not answer and try to find a related link in you context.

Only include one reply from the assistant
</system>

<context>
{context}
</context>

<user>
{question}
</user>

<thesizer>
 """


async def main():
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    # get the documents
    db = await get_document_database("learning_material/*/*")
    retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"k": 4})

    llm_chain = prompt | llm | StrOutputParser()

    rag_chain = {"context": retriever,
                 "question": RunnablePassthrough()} | llm_chain

    question = "mitä tarkoittaa abstract sivu? Mitä siihen voi laittaa?"
    if sys.argv[1]:
        question = sys.argv[1]

    # raw_response = llm_chain.invoke({"context": "", "question": question})
    rag_response = rag_chain.invoke(question)

    print("raw response")
    print(rag_response)

    match = re.search(r"<thesizer>(.*?)</thesizer>", rag_response, re.DOTALL)
    parsed_answer = match.group(1).strip()

    print(f"User prompt: {question}")
    print(f"{'=' * 23}Thesizer answer{'=' * 23}")
    print(textwrap.fill(parsed_answer, 60))
    print('=' * 60)


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
