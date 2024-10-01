# Instructions for the project

As the very first thing you do, install the required packages with pip.
Follow these steps or check it out from `./assignment/Exercise_01.ipynb`.

1. Create a virtual env

```bash
# linux
python3 -m venv my_venv
# windows 
python -m venv my_venv
```

NOTE: if you use a custom folder name for your virtual env, remember
to add it to the `.gitignore` file in either the root or this folder.

2. Activate virtual environment

```bash
# linux
source my_venv/bin/activate
# windows
.\my_venv\bin\activate.exe # or something, you can figure it out if you use windows
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

# Codellama example

You can use the codellama example as well if you would like. It uses the 7B parameter version,
so make sure that your machine can run it, or use the 3B version instead.

You also need to add an .env file for logging into huggingface.

```bash
echo "HF_TOKEN=hf_abcdefg..." > .env
```

### Example prompt

Codellama needs a surrounding code context for it to work, so you need to add a FILL_ME mark.

```go
func GreetUser(user string) {
    <FILL_ME>
}

func main() {
    GreetUser("Raino")
}
```
