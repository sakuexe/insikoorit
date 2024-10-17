import numpy as np

import torch
import sys
from numpy import resize
from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, Resize, ToTensor

from sklearn.multioutput import MultiOutputClassifier
import matplotlib.pyplot as plt
from self_taught_model import cnn_model

from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay


from sklearn.metrics import recall_score

#from app.routing.evaluation import
TRAINING_ROOT = "trees_training/resized"
VALIDATION_ROOT = "trees_valuation"
LEARNING_RATE = 0.01
# = 128?
IMAGE_RESIZE = 64

# transformations, like resizing
transform = Compose([Resize((IMAGE_RESIZE, IMAGE_RESIZE)), ToTensor()])
# load the dataset
train_data = ImageFolder(root=TRAINING_ROOT, transform=transform)
validation_data = ImageFolder(root=VALIDATION_ROOT, transform=transform)
global accu
accu = []
global pred
pred = []
global losses
losses  = []
global EPOCHS
EPOCHS = 40
global scoreall
scoreall = []
global f1all
f1all = []
global lsall
lasll = []
global recal
recal = []
confmatall =[]
global cmx
cmx = np.zeros((8,8), dtype=int)
global cmpr
cmpr =np.zeros((8,8), dtype=int)
global cofusmatsum
cofusmatsum = np.zeros((8,8),dtype =int)
def mini_batch(device, data_loader, test_loader, model):
    
    score = 0
    for x_batch, y_batch in zip(data_loader,test_loader):
       
        Y = y_batch[1]
        y_pred = y_batch[0].to(device)
    
        y_pred_idx=np.argmax(y_pred, axis=1)
        y_test_idx=np.argmax(Y)
        
        N_correct=(y_pred_idx==y_test_idx).sum()
        
        
        N_all=y_pred_idx.sum()
        
        acc=N_correct/N_all
      
        pr = y_batch[1]
        x =  x_batch[1]
        
        
        score = accuracy_score(x, pr, normalize= True)
        scoreall.append(score)


        accu.append(acc)
        la = Y
        op = x_batch[0][0][0][0]
        op = np.array(op)
      
        opp = []
        for n in range(4):
            opp.append(op[n*4:n*4+4])
        opp = np.array(opp)
        la = np.array(la)
       
        try:
            pre = average_precision_score(la,opp)
            pred.append(pre)
        except:
            pass

        f1 = f1_score(x, pr, average='weighted')
        f1all.append(f1)


       
        recal1 = recall_score(x_batch[1], y_batch[1], labels=None, pos_label=1, average="macro", sample_weight=None, zero_division=0.0)
        #recal2 = np.array(recal1)
        #scoreRec = recal1.sum()/len(recal2)
       
        scoreRec = recal1
        recal.append(scoreRec)    
        x1 = resize(x, (8,8))
        global cmx
        cmx = cmx + x1
        pr1 = resize(pr, (8,8))
        global cmpr
        cmpr = cmpr + pr1

    return accu, pred,scoreall, f1all, recal, cmx, cmpr


def main(model_path):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = cnn_model.TreeCNN(train_data.classes, IMAGE_RESIZE).to(device)
    model.load_state_dict(torch.load(model_path, map_location=torch.device(device), weights_only=True))
   
 
    scoreT = []
    lr = 0.1
    train_loader = None
    train_step = 1
    torch.manual_seed(42)

    #checkpoint = torch.load(model_path, map_location=torch.device(device), weights_only=True)
    print(model_path)
    print(model)
   
    #optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.9)
   
    print(device)
   
   
    #train_step = model.forward(td)
    losall = []
    accall =[]
    presall = []
    global EPOCHS
    model.eval()
    for epoch in range(EPOCHS):
        print("EPOCH: ", epoch + 1, "\nPlease wait")
        #train_step = model.forward
        train_loader = torch.utils.data.DataLoader(train_data, batch_size=4, shuffle=True)
        test_loader = torch.utils.data.DataLoader(validation_data, batch_size = 4, shuffle = True)
        train_accuracy, pres, scoreA, f1all, recA, cmx, cmpr = mini_batch(device, train_loader, test_loader, model) #train_step)
        summa =0.0
        k=0
        
        for p in train_accuracy:
            summa = summa+p
            k = k +1
        if k>0:
            summa = summa /k
        h = 0
        presi = 0
       
        for r in pres:
            presi = presi + r
            h=h+1
          
        if h>0:
            presi = presi / h
    
       
        AS = np.array(scoreA).sum()/len(np.array(scoreA))
        f1x = np.array(f1all).sum()/len(np.array(f1all))
        R = np.array(recA).sum()/len(np.array(recA))
        lsum = 0.0
        k2 = 0
     
        accall.append(summa)
        presall.append(presi)
        scoreT.append(AS)
        
        
        print(
        f'Epoch: {epoch+1}\n',
        '*100%\n',
        f'Mean Accuracy:{summa*100:0.2f}\n',
        f'Avarage precision:{presi*100:0.2f}\n',
        f'Accuracy score:{AS*100:0.2f}\n',
        f'f1 score: {f1x*100:0.2f}\n',
        f'Recall score: {R*100:0.2f}\n'
        )

        cmx1 = cmx[0]
        cmpr1 = cmpr[0]
        for r in range(7):
            cmx1 = cmx1 + cmx[r+1]
            cmpr1 = cmpr1 +cmpr[r+1]
        #print("Confussion matrix:", cmx1, cmpr1)
        confuss_mat = confusion_matrix(cmx1, cmpr1)
        confuss_mat.resize(8,8)
        global cofusmatsum
        cofusmatsum = cofusmatsum + confuss_mat
  
    x=0
    plt.title("accuracy")
    for acca in accall:
        plt.scatter(x, acca)
        x= x +1
    plt.show()
    x=0
    plt.title("Presision")
    for p in presall:
        plt.scatter(x, p)
        x= x +1
    plt.show()
   
    s = 0
    plt.title("Accurate score")
    for score1 in scoreT:
        plt.scatter(s,score1)
        s=s+1
    plt.show()
    p = 0
    plt.title("f1 score")
    for scoref in f1all:
        plt.scatter(p,scoref)
        p=p+1
    plt.show()
    
    r = 0

    plt.title("recall")
    for scorer in recal:
        plt.scatter(r,scorer)
        r=r+1
    plt.show()
    print(cofusmatsum)
    disp = ConfusionMatrixDisplay(cofusmatsum)   
    disp.plot()
    plt.show()

if __name__=="__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("No model path provided.")
        print("Path: self_taught_model/weights/best_model_weights.pth")
        main("self_taught_model/weights/best_model_weights.pth")
      
