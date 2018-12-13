from StockDataAnalysis.VolumeDataProcessing import VolumeDataProcessor
from StockDataAnalysis.ClusteringFunctionStorage import movingAverageClustering

from SharedGeneralUtils.SharedGeneralUtils import config_handling

from StockDataPrediction.TrainingFunctionStorage.TrainingFunctionStorage import modelStoragePathBase, combineDataSets
from StockDataPrediction.MachineLearningModels.SingleDataCateogryRNN import RNNNormal
from StockDataPrediction.MachineLearningModels.TrainingDataStorages import RNNTrainingDataStorage
from StockDataPrediction.NormalizationFunctionStorage import movementDirectionDenormalization, movementDirectionNormalization

from EmailUtils.EMessage import EMessage
from EmailUtils.EClient import EClient, EClientFilter
from EmailUtils.EMessageSender import EMessageSender

from os import listdir, path
from typing import List
from datetime import datetime, timedelta


messageBody = '''Hello {customer},
Here is your prediction results for today:
{ticker}
Have a nice day'''



def parseModelString(passedStr : str):
    unScorePos = passedStr.find("_")
    periodPos = passedStr.find(".")
    modelTypeName = passedStr[:unScorePos]
    ticker = passedStr[unScorePos+1:periodPos]
    extension = passedStr[periodPos+1:]
    return [modelTypeName, ticker, extension]

def getModelFiles() -> List[str]:
    fileList = listdir(modelStoragePathBase.format('.'))
    return [modelStoragePathBase.format(x) for x in fileList if not path.isdir(x)]

def loadModel(fileExtension, modelFilePath):
    if fileExtension == 'scml':
        rnn = RNNNormal(1, 1, 1, 1, .5, .5)
        rnn.load(modelFilePath)
        return rnn

def genPredictionData(modelTypeName : str, ticker : str, loginCredentials, examplesPerSet):
    trainingTickers = None
    if modelTypeName == "VolMovDir":
        startDate = datetime.now() - timedelta(365)
        trainingTickers = movingAverageClustering(ticker, loginCredentials, 0, [.60, 5, 15, startDate])
        trainingTickers = [trainingTickers[0]] + trainingTickers[1]
        
        dataProc = VolumeDataProcessor(loginCredentials)
        sourceStorages = dataProc.calculateMovementDirections(startDate)
        dataStorage = [x.data for x in sourceStorages.tickers if x.ticker in trainingTickers]
        dataStorage = combineDataSets(dataStorage)
        predictionDataStorage = RNNTrainingDataStorage(movementDirectionNormalization, movementDirectionDenormalization)
        predictionDataStorage.addPredictionData(dataStorage[-examplesPerSet:])
        return predictionDataStorage


def genClients():
    jimClient = EClient("Jim Carey", "careyjw@plu.edu", EClientFilter())
    jimClient.clientFilter.addWhitelistEntry("tick", [])
    coltonClient = EClient("Colton Freitas", "freitacr@plu.edu", EClientFilter())
    coltonClient.clientFilter.addWhitelistEntry("tick", [])
    return [jimClient, coltonClient]



if __name__ == "__main__":

    emailSys = EMessageSender("smtp.gmail.com", 465, "mlstockpredictions@gmail.com", "PrayersAndFaith")

    msg = EMessage(messageBody, "tick", "Prediction Results", [], defaultMessageStatus= True)
    clients = genClients()

    loginCredentials = config_handling()
    modelFiles = getModelFiles()
    
    msg = msg.multiplyKey("{ticker}", len(modelFiles))

    for x in modelFiles:
        modelTypeName, ticker, fileExtension = parseModelString(path.split(x)[1])
        model = loadModel(fileExtension, x)
        predData = genPredictionData(modelTypeName, ticker, loginCredentials, 10)
        res = model.predict(predData)
        msg = msg.replaceKey("{ticker}", "Volume Movement Direction Result for {0}: {1}".format(ticker, res), 1)

    for cli in clients:
        sendMsg = msg.replaceKey("{customer}", cli.clientName)
        emailSys.sendMessage(sendMsg, cli)
    emailSys.close()