from fastapi import FastAPI
import os
from PIL import Image

app = FastAPI()
    
   
@app.post("/several_items/")
async def several_images(path: str="\\tree_recognition\\koe\\", whichTree: str = "maple"):
    os.chdir("..")
    directory = os.path.dirname(os.getcwd())+ "\\tree_recognition\\trees_training\\edited\\"+whichTree+"\\"
    lst = os.listdir(directory)
    number_files = len(lst)
    for id in range(number_files):
        if id <=9:
            N = "_00"
        else:
            N = "_0"
        names = os.path.dirname(os.getcwd()) + path + whichTree + str(id)+".jpg"
        fileName = whichTree+N+str(id)+".jpg"
        fileName2 = whichTree+N+str(id)+".jpeg"
        file = os.path.dirname(os.getcwd()) + "\\tree_recognition\\trees_training\\edited\\"+whichTree+"\\"+ fileName
        file2 = os.path.dirname(os.getcwd()) + "\\tree_recognition\\trees_training\\edited\\"+whichTree+"\\" + fileName2
        if os.path.isfile(file):
            image = Image.open(file)
        elif os.path.isfile(file2):
            image = Image.open(file2)
        else:
            id = id + 1
            continue
        image.show()
        image.save(names)
        image.close()
    return file
