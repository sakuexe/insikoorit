# Instructions for the project

As the very first thing you do, install the required packages with pip.
Follow these steps or check it out from `./assignment/Exercise_01.ipynb`.

1. create a virtual env

```bash
# linux
python3 -m venv venv
# windows 
python -m venv venv
```

2. activate virtual environment

```bash
# linux
source venv/bin/activate
# windows
.\venv\bin\activate.exe # or something, you can figure it out if you use windows
```

3. install requirements

```bash
# if you have a cuda 12.4 gpu
pip install -r requirements_cuda.txt
# if you do not
pip install transformers gradio diffusers numpy
# install the pytorch version for you
# https://pytorch.org/get-started/locally/
# for example linux, no gpu:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

4. go for it

```bash
python3 example.py
# gpt2 version
python3 gpt 'my prompt is'
```
