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
from sklearn.linear_model import LinearRegression

#from app.routing.evaluation import
TRAINING_ROOT = "trees_training/resized"
VALIDATION_ROOT = "trees_valuation"
#LEARNING_RATE = 0.01
# = 128?
IMAGE_RESIZE = 64

# transformations, like resizing
transform = Compose([Resize((IMAGE_RESIZE, IMAGE_RESIZE)), ToTensor()])
# load the datasets
train_data = ImageFolder(root=TRAINING_ROOT, transform=transform)
validation_data = ImageFolder(root=VALIDATION_ROOT, transform=transform)

global pred
pred = []
global lossess
lossess = []
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
#calculates the values
def mini_batch(device, data_loader, test_loader, model):
    #array of accrurate by epochs, values
    accurateall = []
    score = 0
    global cmx
    cmx = np.zeros((8,8), dtype=int)
    for data_batch, test_batch in zip(data_loader,test_loader):
        #data_batch= traing materral, test_batch= test material
        #Y = test y
        Y = test_batch[1]
        #y_pred: predicted value(predicated y) by test x
        y_pred = test_batch[0].to(device)
        #maximum value of predicted values
        y_pred_idx=np.argmax(y_pred, axis=1)
        #maximum value of data y values
        y_test_idx=np.argmax(Y)
        #number of correct, when predicted = data
        N_correct=(y_pred_idx==y_test_idx).sum()
        # of all predicted
        N_all=y_pred_idx.sum()
        # accuracy = correct from all
        accurate=N_correct/N_all

        #predicted and given values
        given2 = y_pred_idx[1][0]
        predicted2 =  test_batch[0][0][0][0]
        given1 = given2.numpy()
        givenn = np.array(given1)
        predicted1 = predicted2.numpy()
        predictedn = np.array(predicted1)
        #pere predicted values for confusion matrix
        pere = []
        for prr in predictedn:
            #round between 0 and 1 to 0 or 1
            pere.append(round(prr))
        pere = np.array(pere).reshape(8,8)

        given = givenn.reshape(16,4)
        predicted = predictedn.reshape(16,4)
        predictedbin = np.zeros((16,4), int)
        score = 0
        for a in range(4):
            for b in range(4):
                #print(predicted[a][b])
                score = score +predicted[a][b]
        score = score /(4*4)
    
        scoreall.append(score)

        accurateall.append(accurate)
        la = Y
        op = data_batch[0][0][0][0]
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
        #print("DATA", Y, data_batch[1])
        f1 = f1_score(Y, data_batch[1], average='weighted')
        
        #print("f1", f1)
        f1all.append(f1)


       
        #recal1 = recall_score(data_batch[1], test_batch[1], labels=None, pos_label=1, average="macro", sample_weight=None, zero_division=0.0)
        recal1 = recall_score(Y, data_batch[1], labels=None, pos_label=1, average="macro", sample_weight=None, zero_division=0.0)
       
       
        scoreRec = recal1
        recal.append(scoreRec)    
        x1 = resize(given, (8,8))
        
        cmx = cmx + x1
    
        pr1 = pere
        global cmpr
        cmpr = cmpr + pr1
        

    return accurateall, pred,scoreall, f1all, recal, cmx, cmpr


def main(model_path):
    #load model from model_path, train_data =ImageFolder(root=TRAINING_ROOT, transform=transform)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = cnn_model.TreeCNN(train_data.classes, IMAGE_RESIZE).to(device)
    model.load_state_dict(torch.load(model_path, map_location=torch.device(device), weights_only=True))
    #confusion_final sum of condusion_matrixes
    confusion_final =[]
    #AccuracyScores: array of accuracy scores
    AccuracyScores = []
    train_loader = None
    #Seed for random
    torch.manual_seed(42)
    #prints model_path and model parameters
    print(model_path)
    print(model)
    #print device cpu or gpu
    print(device)
    #all accuracys
    accuracy_all =[]
    #all predictions
    presall = []
    #epochs=number of shuffles
    #confusion_final_sum = confusion matrix in the end
    confusion_final_sum = np.zeros((8,8),int)
    global EPOCHS
    model.eval()
    for epoch in range(EPOCHS):
        
        print("EPOCH: ", epoch + 1, "\nPlease wait")
        confusionmatrx1 = np.zeros((8,8),int)
        #train_data = ImageFolder(root=TRAINING_ROOT, transform=transform)
        #validation_data = ImageFolder(root=VALIDATION_ROOT, transform=transform)
        #train_data traing
        #validation_data test data
        train_loader = torch.utils.data.DataLoader(train_data, batch_size=4, shuffle=True)
        test_loader = torch.utils.data.DataLoader(validation_data, batch_size = 4, shuffle = True)
        #train accuracy, presitioon, accuracy score, f1 score, recal score
        train_accuracy, presition, scoreAccuracy, f1all, recAll, confusionmatrix, confusionmatr1predicted = mini_batch(device, train_loader, test_loader, model) #train_step)
        summa =0.0
        k=0
        
        for p in train_accuracy:
            summa = summa+p
            k = k +1
        if k>0:
            summa = summa /k
            trainAccuracy = summa
        h = 0
        presi = 0
       
        for r in presition:
            presi = presi + r
            h=h+1
        if h>0:
            presi = presi / h
            #presition avarage
            presitionAvarage = presi
        #accuracy score avarage
        ASavarage = np.array(scoreAccuracy).sum()/len(np.array(scoreAccuracy))
        #f1 score avarage
        f1scoreavarage = np.array(f1all).sum()/len(np.array(f1all))
        #recaal score avarage
        recalscoreavarage = np.array(recAll).sum()/len(np.array(recAll))
       
        #accuracy array
        accuracy_all.append(trainAccuracy)
        #presition array
        presall.append(presitionAvarage)
        #accuracy score array
        AccuracyScores.append(ASavarage)
        
        
        print(
        f'Epoch: {epoch+1}\n',
        '*100%\n',
        f'Mean Accuracy:{trainAccuracy*100:0.2f}\n',
        f'Avarage precision:{presitionAvarage*100:0.2f}\n',
        f'Accuracy score:{ASavarage*100:0.2f}\n',
        f'f1 score: {f1scoreavarage*100:0.2f}\n',
        f'Recall score: {recalscoreavarage*100:0.2f}\n'
        )
        
    
        confuss_mat = confusionmatrix
        binary_times_confus_value = confuss_mat * confusionmatr1predicted
        
        confusion_final.append(binary_times_confus_value)
      
   
   
    x=0
    plt.title("accuracy")
    for acca in accuracy_all:
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
    for score1 in AccuracyScores:
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

    print(binary_times_confus_value)
    disp = ConfusionMatrixDisplay(binary_times_confus_value)   
    disp.plot()
    plt.show()


if __name__=="__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("No model path provided.")
        print("Path: self_taught_model/weights/best_model_weights.pth")
        main("self_taught_model/weights/best_model_weights.pth")
      
