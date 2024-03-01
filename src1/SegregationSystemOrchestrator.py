from StorageController import *
from PreparedSession import *
from CheckDataBalance import *
from CheckInputCoverage import *
from LearningSetGenerator import *
from random import random
import numpy as np

toleranceValue = 5
serviceFlag = 0

storageController = StorageController()
checkDataBalance = CheckDataBalance(toleranceValue)
checkinputCoverage = CheckInputCoverage()
learningSetGenerator = LearningSetGenerator(70, 15, 15)


def send(data):
    # send data
    return 0


def recive():
    # recive
    label = ["High", "Medium", "Low"]
    test_array = np.array(label)
    random_num = np.random.choice(test_array)
    params = [random(), random(), random(), random(), random(), random(), random_num]
    p = PreparedSession(params)
    return p


preparedSessionRecived = 0
limitPreparedSession = 3

p = []
# storageController.createTablePreparedSession()
# storageController.deletePreparedSession()
while 1:

    while ((storageController.countPreparedSession()[0][0]) != limitPreparedSession):
        p = recive()
        storageController.insertPreparedSession(p)

    outcome = 0
    if (serviceFlag):
        # result obtained stochastically
        outcome = random()
        if outcome <= 0.5:
            outcome = 0
        else:
            outcome = 1
    else:
        # result obtained from human that writes into a json file
        checkDataBalance.plotCheckDataBalance(storageController.retrivePreparedSession())
        #TODO the application ends| the user insert the result in a json| then he reopens the data
        outcome = 1

    if (outcome == 0):
        # the checkDataBalance is not correct
        limitPreparedSession += 50
        continue

    # check data balance is ok
    # let's check input coverage
    if (serviceFlag):
        # result obtained stochastically
        outcome = random()
        if outcome <= 0.5:
            outcome = 0
        else:
            outcome = 1
    else:
        # result obtained from human that writes into a json file
        checkinputCoverage.plotCheckinputCoverage(storageController.retrivePreparedSession())
        outcome = 1

    if (outcome == 0):
        # the checkDataBalance is not correct
        limitPreparedSession += 50
        continue
    # generate learning set
    learninSet = learningSetGenerator.generateLearningSet(storageController.retrivePreparedSession())

    send(learninSet)
    storageController.deletePreparedSession()

