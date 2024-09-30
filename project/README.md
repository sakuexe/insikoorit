# Instructions for the project

As the very first thing you do, install the required packages with pip.
Follow these steps or check it out from `./assignment/Exercise_01.ipynb`.

1. Create a virtual env

```bash
# linux
python3 -m venv venv
# windows 
python -m venv venv
```

2. Activate virtual environment

```bash
# linux
source venv/bin/activate
# windows
.\venv\bin\activate.exe # or something, you can figure it out if you use windows
```

3. Install requirements

Link to the pytorch install guide: [Get Started - Pytorch](https://pytorch.org/get-started/locally/).

Use the link to generate a pytorch installation command if needed.

```bash
# if you have a cuda 12.4 gpu
pip install -r requirements_cuda.txt
# if you do not
pip install transformers gradio diffusers numpy
# install the pytorch version for you
# for example linux, no gpu:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

4. Run it

```bash
python3 example.py
# gpt2 version
python3 example.py gpt 'my prompt is'
```
