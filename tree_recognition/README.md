# Tree Recognition Project

```
     .\^/.
   . |`|/| .
   |\|\|'|/|
.--'-\`|/-''--.
 \`-._\|./.-'/
  >`-._|/.-'<
 '~|/~~|~~\|~'
       |
```

## Tree name translations

The english names, finnish names and the amount of pictures taken.

- **Alder**: leppä (0)
- **Birch**: koivu (34)
- **Juniper**: kataja (29)
- **Linden**: lehmus (34)
- **Maple**: vaahtera (25)
- **Oak**: tammi (22)
- **Pine**: mänty (26)
- **Rowan**: pihlaja (35)
- **Spruce**: kuusi (25)

<hr>

**Overall**: 230 images

## Running The Project

1. Set up the virtual environment

> [!NOTE]
> If you make a venv directory with a custom name,
> remember to add it into the .gitignore file!

```bash
# linux / wsl
python3 -m venv venv
source venv/bin/activate
# windows (powershell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install the required packages

```bash
pip install -r requirements.txt
```

3. Install pytorch to your virutal environment based on your specs

[Pytorch - Get Started Locally](https://pytorch.org/get-started/locally/)

## Learning about FastAPI

Getting started with FastAPI basics:

- [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/)

Using Templates with FastAPI (The frontend code):

- [https://fastapi.tiangolo.com/advanced/templates/](https://fastapi.tiangolo.com/advanced/templates/)

> [!NOTE]
> All of the packages that are needed by these tutorials are already inside
> `requirements.txt`. Install them using `pip install -r requirements`!
> Therefore, you don't need to follow the installation steps in the tutorials.


## Helpful commands

Re-preprocess the training images:

```bash
# linux
python3 image_preprocessing.py
# windows
python image_preprocessing.py
```

Find the number of images in total:

```bash
# linux
find tree_recognition/images/ -mindepth 2 -maxdepth 2 | wc -l
# windows (powershell)
Get-ChildItem -Path tree_recognition/images/ -Directory | ForEach-Object {$sum += (Get-ChildItem -Path $_.FullName | Measure-Object).Count} | Write-Host $sum
```

Reshuffle the tree images

```bash
# remove the image folders
rm -rf trees_training/ trees_valuation/
# get the base image folder
git checkout 047d5f0977f23ee910fe20e903eb45c8c1d78b68 -- trees_training
# run the python script
python3 organize_training.py
# commit and push your reshuffle
```
