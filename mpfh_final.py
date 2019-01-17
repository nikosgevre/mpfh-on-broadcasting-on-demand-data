from collections import Counter

# Global variable timeSlot for checking time
timeSlot = 1

#######################################################################################
#                                      FUNCTIONS                                      #
#######################################################################################

# Function popularities finds the most popular data item
def popularities(requests):

    popularList = []
    for request in requests:
        if request["deadline"] > timeSlot:
            popularList.extend(request["dataItems"])


    data = Counter(popularList)
    popularList = []
    popularList.extend(data.most_common())
    
    # initializing the min values
    min_deadline = 999
    min_ID = "Q999"
    min_data_ID = "d999"
    min_val = 0

    for i in range(len(popularList)):
    # if item in popularList has len(requests) occurences, it goes directly to candidateList
        if popularList[i][1] == len(requests):
            for request in requests:
                request["candidate"] = popularList[i][0]
                
            break

        for request in requests:
            if popularList[i][0] in request["dataItems"]:
                if popularList[i][1] > min_val:
                    min_val = popularList[i][1]
                    request["candidate"] = popularList[i][0]
                
                elif popularList[i][1] == min_val:
                    # ***dependsing on python version this may be needed. it is not needed in python 3.6. it is needed in python 2.7***
                    if request["candidate"] != " " and popularList[i][0] <= min_data_ID:

                        #min_data_ID = popularList[i][0]
                        #request["candidate"] = popularList[i][0]
                        #print("not needed if python 3.7")
                        continue
                    
                    elif request["candidate"] == " ":
                        request["candidate"] = popularList[i][0]

                elif request["candidate"] == " ":
                    request["candidate"] = popularList[i][0]
                    
    return

# Aggregation phase of mpfh ccording to the paper
def aggregation(requests):
    
    candidateList = []
    myList = []
    
    # initializing min values
    min_deadline = 999
    min_unservedData = 999
    min_ID = "Q999"
 
    for request in requests:
        if request["candidate"] in candidateList :
            index = candidateList.index(request["candidate"])
            for i in myList:
                if request["candidate"] == i["dataItem"]:
                    thesi=myList.index(i)
                    break
            
            if request["deadline"] < min_deadline:
                del candidateList[index]
                del myList[thesi]
                candidateList.append(request["candidate"])
                min_deadline = request["deadline"]
                temp = {
                    "slackTime" : request["deadline"] - timeSlot - len(request["dataItems"]),
                    "ID" : request["ID"],
                    "dataItem" : request["candidate"],
                    "unservedData" : len(request["dataItems"])
                }
                myList.append(temp)

            elif request["deadline"] == min_deadline:
                if len(request["dataItems"]) < min_unservedData:
                    del candidateList[index]
                    del myList[thesi]
                    candidateList.append(request["candidate"])
                    min_unservedData = len(request["dataItems"])
                    temp = {
                        "slackTime" : request["deadline"] - timeSlot - len(request["dataItems"]),
                        "ID" : request["ID"],
                        "dataItem" : request["candidate"],
                        "unservedData" : len(request["dataItems"])
                    }
                    myList.append(temp)

                elif len(request["dataItems"]) == min_unservedData:
                    if request["ID"] < min_ID:
                        del candidateList[index]
                        del myList[thesi]
                        candidateList.append(request["candidate"])
                        min_ID = request["ID"]
                        temp = {
                            "slackTime" : request["deadline"] - timeSlot - len(request["dataItems"]),
                            "ID" : request["ID"],
                            "dataItem" : request["candidate"],
                            "unservedData" : len(request["dataItems"])
                        }
                        myList.append(temp)

        else:
            candidateList.append(request["candidate"])
            min_deadline = request["deadline"]
            min_ID = request["ID"]
            min_unservedData = len(request["dataItems"])
            temp = {
                "slackTime" : request["deadline"] - 1 - len(request["dataItems"]),
                "ID" : request["ID"],
                "dataItem" : request["candidate"],
                "unservedData" : len(request["dataItems"])
            }
            myList.append(temp)
            
    return(myList)

# Conversion phase accoring to the paper
def conversion(candidateList):

    conversionList = []
    i = 0

    while(i < 2):
        min_slackTime = 999
        min_unservedData = 999
        min_ID = "Q999"

        for candidate in candidateList:
            if candidate["slackTime"] < min_slackTime:
                min_slackTime = candidate["slackTime"]
                min_ID = candidate["dataItem"]
                min_unservedData = candidate["unservedData"]

            elif candidate["slackTime"] == min_slackTime:
                if candidate["unservedData"] < min_unservedData:
                    min_unservedData = candidate["unservedData"]
                    min_ID = candidateList["dataItem"]

                elif candidate["unservedData"] == min_unservedData:
                    if candidate["dataItem"] < min_ID:
                        min_ID = candidate["dataItem"]


        conversionList.append(min_ID)
        
        for candidate in candidateList:
            if candidate["dataItem"] == min_ID:
                    thesi=candidateList.index(candidate)
                    break

        del  candidateList[thesi]
        i += 1

    return(conversionList)    

# Removing phase according to the papaer
def remove_phase(requests, bcast_list):
        
    for item in bcast_list:
        for request in requests:
            if item == request["candidate"]:
                request["dataItems"].remove(request["candidate"])
                request["candidate"] = " "

# Initializing the requests list containing all the requests specified from the user
def init():
    # all requests are written in file "requests.txt"
    # data in requests.txt file should have the following format: ID,deadline,timeArrived,(dataItem1/dataItem2/.../dataItemn),()
    index1=['ID','deadline','timeArrived','dataItems','candidate']
    dict_main={}
    myList=[]
    with open ('requests.txt') as f:
        count=0
        for line in f:
            dict1={}
            lst1=line.strip().split(',')
            dict1[index1[0]]=lst1[0]
            dict1[index1[1]]=int(lst1[1])
            dict1[index1[2]]=int(lst1[2])
            dict1[index1[3]]=lst1[3][1:-1].strip().split('/')
            dict1[index1[4]]=" "
            count+=1
            myList.append(dict1)
    return myList
                
########################################################################################
#                                         MAIN                                         #
########################################################################################

# a list containing all the requests that are read from a file
requests=[]
requests=init()

# number of channels that are broadcsting
numChannels = 2
candidateList = []

# While loop that our algorithm is running until all requests end
while(requests):
    print ("Time slot =  %d" %timeSlot)
    tempList = []
    for request in requests:
        if request["timeArrived"] <= timeSlot:
            tempList.append(request)

    # print the updated requests
    print("Requests:")
    for request in tempList:
        print(request["ID"],request["dataItems"])

    popularities(tempList)
    candidateList = aggregation(tempList)

    bcast_list = []
    if len(candidateList) < numChannels:
        bcast_list.append(candidateList[0]["dataItem"])

    elif len(candidateList) == numChannels:
        bcast_list.append(candidateList[0]["dataItem"])
        bcast_list.append(candidateList[1]["dataItem"])

    else:
        bcast_list = conversion(candidateList)

    print ("bcast_list: ", bcast_list)

    # delete the items which is in bcast_list cause they have already been bcasted
    remove_phase(requests, bcast_list)

    # in this for-loop we delete a request if it does not have any other dataItems
    for request in requests:
        if not request["dataItems"]:
            requests.remove(request)

    # increasing the time slot after every loop
    timeSlot += 1

# print the time slot after the program has ended. if last dataItem was broadcasted in timeSlot=t the program has succesfully ended at timeSlot=t+1
print ("Program has ended in time slot: ", timeSlot)