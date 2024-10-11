# HAMK Thesis Assistant (Thesizer)

AI Project - 10.2024

```
              .----.
  .---------. | == |
  |.-"""""-.| |----|
  ||  A I  || | == |
  ||       || |----|
  |'-.....-'| |::::|
  `"")---(""` |___.|
 /:::::::::::\" _  "
/:::=======:::\`\`\
`"""""""""""""`  '-'
```

**Thesizer** is a fine-tuned LLM that is trained to assist with authoring Thesis'.
It is specifically trained and tuned to guide the user using HAMK's thesis 
standards and guidelines [Thesis - HAMK](https://www.hamk.fi/en/student-pages/planning-your-studies/thesis/).
The goal of this is to make the process of writing a thesis easier, by helping
the user using spoken language, so that it will be easier for the user to find
help on the more technical aspects of writing a thesis. This way the user can
focus on what is the most important. The actual content of the Thesis.

This project is part of HAMK's `Development of AI Applications` -course. The
idea for the project spawned from the overwhelming feeling that all of the
different guidelines and learning documents there are for writing a thesis using
the standards of HAMK. Thesizer takes those documents and fine-tunes itself so
that it will be able to provide useful information and help the user. It is kind
of like a spoken language search engine for thesis writing technicalities.

## Documentation

### 1. The development process

The development process started after we had come to an agreement on the project.
We then tasked everyone to go and research what Hugging Face transformers would
be suitable as a base for our Fine-Tuned model.

Some of the models considered:

**General LLMs**

- [google-bert/bert-base-multilingual-cased](https://huggingface.co/google-bert/bert-base-multilingual-cased)
- [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)
- [google/gemma-2-2b](https://huggingface.co/google/gemma-2-2b)

**Translation models**

- [facebook/mbart-large-50-one-to-many-mmt](https://huggingface.co/facebook/mbart-large-50-one-to-many-mmt) 

### 2. Tools used

We ended up going with \[INSERT MODEL HERE\], because \[INSERT EXPLANATION HERE\]...

### 3. Challenges

## Dependencies

If the requirements.txt does not work, you can try installing the dependcies 
using the following commands.

0. **Create a virtual environment**

```bash
# linux
python3 -m venv venv
source venv/bin/activate
# windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

1. **Install Pytorch that matches your machine**

Get the installation command from this website: [Start Locally | PyTorch](https://pytorch.org/get-started/locally/)

2. **Install FAISS**

```bash
# if you have a gpu
pip install faiss-gpu-cu12 # CUDA 12.x
pip install faiss-gpu-cu11 # CUDA 11.x
# if you only have a cpu
pip install faiss-cpu
```

3. **Install universal pip packages**

```bash
pip install transformers accelerate bitsandbytes sentence-transformers langchain \
langchain-community langchain-huggingface pypdf bs4 lxml
```

4. **Log into your Hugging Face account**

If you are prompted to log in, follow the instructions of the prompt.
You can figure it out.

> [!NOTE]
> If there are problems or the process feels complicated, add your own
> guide right here and replace this note.
