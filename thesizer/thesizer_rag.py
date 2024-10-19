# the following code is collected from this hugging face tutorial
# https://huggingface.co/learn/cookbook/rag_zephyr_langchain
# langchain
from typing import TypedDict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFacePipeline
# huggingface
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers import pipeline
# pytorch
import torch
# gradio
import gradio as gr
# stdlib
from asyncio import sleep
import copy
# local
from vector_store import get_document_database

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

# creating the prompt template in the shape of a chat prompt
# this is done so that it could be easily expanded
# https://www.mirascope.com/post/langchain-prompt-template
prompt_template = ChatPromptTemplate([
    ("system", """You are 'thesizer', a HAMK thesis assistant.
    You will help the user with technicalities on writing a thesis
    for hamk. If you can't find the answer from the context given to you,
    you will tell the user that you cannot assist with the specific topic.
    You answer with only a single message."""),
    ("system", "{context}"),
    ("assistant", "Hei! Kuinka voin auttaa opinnäytetyösi kanssa?"),
    ("assistant", "Hello! How can I help you with authoring your thesis?"),
    ("user", "{user_input}"),
])


async def generate_answer(message_history: list[HumanMessage | AIMessage]):
    print(f"message history: {message_history}")
    # generate a vector store
    db = await get_document_database("learning_material/*/*")

    # initialize the similarity search
    n_of_best_results = 4
    retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"k": n_of_best_results})

    retrieved_docs = retriever.get_relevant_documents(message_history[-1].content)
    context_string = "\n".join([
        doc.page_content
        for doc in retrieved_docs
    ])

    chat_template = [
        SystemMessage(
            content="""You are 'thesizer', a HAMK thesis assistant.
                You will help the user with technicalities on writing a thesis
                for hamk. If you can't find the answer from the context given
                to you, you will tell the user that you cannot assist with the
                specific topic. You answer with only a single message."""
        ),
        SystemMessage(content=context_string),
        MessagesPlaceholder(variable_name="messages"),
    ]

    prompt = ChatPromptTemplate.from_messages(chat_template)

    # create the pipeline for generating a response
    # RunnablePassthrough handles the invoke parameters
    retrieval_chain = (
        prompt
        | llm
    )

    response = retrieval_chain.invoke({"messages": message_history[-2:]})

    # debugging
    print("=====raw response=====")
    print(response)

    # get only the last response from the ai
    parsed_answer = response.split("## Thesizer Response").pop().strip()
    return parsed_answer


def update_chat(user_message: str, history: list):
    return "", history + [{"role": "user", "content": user_message}]


class ChatMessage(TypedDict):
    role: str
    metadata: dict
    content: str


def parse_history(
    message_history: list[ChatMessage]
) -> list[AIMessage | HumanMessage]:
    parsed = []
    for message in message_history:
        if message["role"] == "assistant":
            parsed.append(AIMessage(message["content"]))
        else:
            parsed.append(HumanMessage(message["content"]))
    return parsed


async def handle_conversation(
    history: list[ChatMessage],
    characters_per_second=80
):
    print("history:")
    print(history)
    bot_message = await generate_answer(parse_history(history))
    new_message: ChatMessage = {"role": "assistant",
                                "metadata": {"title": None},
                                "content": ""}
    history.append(new_message)
    for character in bot_message:
        history[-1]['content'] += character
        yield history
        await sleep(1 / characters_per_second)


def create_interface():
    with gr.Blocks() as interface:
        gr.Markdown("# 📄 Thesizer: HAMK Thesis Assistant")
        gr.Markdown("Ask for help with authoring the HAMK thesis!")

        gr.Markdown("## Chat interface")

        with gr.Column():
            chatbot = gr.Chatbot(type="messages")

            with gr.Row():
                user_input = gr.Textbox(
                    label="You:",
                    placeholder="Type your message here...",
                    show_label=False
                )
                send_button = gr.Button("Send")

        # handle the messages being sent
        send_button.click(
            fn=update_chat,
            inputs=[user_input, chatbot],
            outputs=[user_input, chatbot],
            queue=False
        ).then(
            fn=handle_conversation,
            inputs=chatbot,
            outputs=chatbot
        )

        # pressing enter instead of the button
        user_input.submit(
            fn=update_chat,
            inputs=[user_input, chatbot],
            outputs=[user_input, chatbot],
            queue=False
        ).then(
            fn=handle_conversation,
            inputs=chatbot,
            outputs=chatbot
        )

    return interface


if __name__ == "__main__":
    create_interface().launch()
