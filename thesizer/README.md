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

If the requirements.txt does not work, you can try installing the depended on
packages using the following command.

```bash
pip install gradio
```

You also need to install pytorch. You can get the right command for your machine
from the following link: [Start Locally | PyTorch](https://pytorch.org/get-started/locally/)
