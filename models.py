import compressai

def get_model(ch = None):
    if(ch == None):
           ch = input("Choices \n1 : bmshj2018_factorized\n2 : bmshj2018_factorized_relu\n3 : bmshj2018_hyperprior\n4 : mbt2018_mean\n5 : mbt2018\n6 : cheng2020_anchor\nEnter choice : ")
    match(ch):
        case '1':
                return  {'name': 'bmshj2018_factorized','model':compressai.zoo.bmshj2018_factorized(quality = 4 , metric = "mse" , pretrained = True , progress=True)}
        case '2':
                return  {'name': 'bmshj2018_factorized_relu','model':compressai.zoo.bmshj2018_factorized_relu(quality = 4 , metric = "mse" , pretrained = True , progress=True)}
        case '3':
                return  {'name': 'bmshj2018_hyperprior','model':compressai.zoo.bmshj2018_hyperprior(quality = 4 , metric = "mse" , pretrained = True , progress=True)}
        case '4':
                return  {'name': 'mbt2018_mean','model':compressai.zoo.mbt2018_mean(quality = 4 , metric = "mse" , pretrained = True , progress=True)}
        case '5':
                return  {'name': 'mbt2018','model':compressai.zoo.mbt2018(quality = 4 , metric = "mse" , pretrained = True , progress=True)}
        case '6':
                return  {'name': 'cheng2020_anchor','model':compressai.zoo.cheng2020_anchor(quality = 4 , metric = "mse" , pretrained = True , progress=True)}