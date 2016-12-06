'''
This file contains all the utility functions that can be used in this project.
'''

import csv
import pickle

categoriesMain = ['Indian', 'Chinese', 'Japanese', 'American', 'Thai', 'Italian', 'Pakistani', 'Mediterranean', 'Delis', 'Ethiopian', 'Mexican', 'Vietnamese', 'Caribbean', 'Greek', 'Coffee & Tea', 'Breakfast & Brunch', 'Korean']

map_cuisine = dict()
map_cuisine['American'] = ['Beer', 'Bars', 'Burgers', 'Pubs', 'Bakeries', 'Sandwiches', 'Smoothies', 'Barbeque', 'Steakhouses', 'Donuts', 'Fast Food']
map_cuisine['Italian'] = ['Pizza']
map_cuisine['Japanese'] = ['Noodles']

def readFile(fileName):
	fileContents = []
	with open(fileName, 'rb') as f:
		reader = csv.reader(f, dialect='excel', delimiter=',')
		for row in reader:
			fileContents.append(row)
	f.close()
	return fileContents[1:1000] #Restricting it to 1000 for testing purpose

'''
Adds all the compliment values
'''
def addComplimentValues(userItem):
	return int(userItem[1]) if userItem[1] != '' else 0 + int(userItem[4]) if userItem[4] != '' else 0 + int(userItem[5]) if userItem[5] != '' else 0 + int(userItem[7]) if userItem[7] != '' else 0 + int(userItem[9]) if userItem[9] != '' else 0 + int(userItem[10]) if userItem[10] != '' else 0 + int(userItem[11]) if userItem[11] != '' else 0 + int(userItem[13]) if userItem[13] != '' else 0 +int(userItem[18]) if userItem[18] != '' else 0 + int(userItem[21]) if userItem[21] != '' else 0
'''
Adds all the vote values
'''
def addVoteValues(userItem):
	return int(userItem[17]) if userItem[17] != '' else 0 + int(userItem[19]) if userItem[19] != '' else 0 + int(userItem[22]) if userItem[22] != '' else 0

def createUserDict(listOfUsers):
	userDict = dict()
	userMap = dict()
	valList = list()
	userIdwithName = dict()
	index = 0
	for eachrow in listOfUsers:
		index += 1
		complimentVals = addComplimentValues(eachrow)
		voteValues = addVoteValues(eachrow)
		friendsList = eachrow[3].translate(None, "'\\").translate(None, '[').translate(None, ']').split(',')
		friendsList = map(str.strip, friendsList)
		userDict[eachrow[16]] = [int(eachrow[0].split('-')[0]), complimentVals, int(eachrow[2]), len(friendsList), int(eachrow[6]), float(eachrow[12]), voteValues]
		userMap[index] = [eachrow[16], friendsList]
		userIdwithName[eachrow[16]] = eachrow[15].strip()
		valList.append(userDict[eachrow[16]])
	return userDict, userMap, valList, userIdwithName


def makeModelFile(filename, content):
	with open(filename, 'wb') as file:
		pickle.dump(content, file)
		file.close()


def getModelFile(fileName):
	with open(fileName, 'rb') as file:
		return pickle.load(file)


def consolidateCusines(fileName, newFileName):
    categoryList = {}
    finalCategory = []
    with open(fileName, 'rb') as file:
        categories = csv.reader(file)
        for row in categories:
            category = row[1].translate(None, "'\\").translate(None, '[').translate(None, ']').split(',')
            category = map(str.strip, category)
            categoryList[row[0].strip()] = category

    with open(newFileName, 'wb') as file2:
        writer = csv.writer(file2)
        for key, val in categoryList.items():
            items = []
            for cuisines in val:
                if cuisines in categoriesMain:
                    val = cuisines
                else:
                    if cuisines in map_cuisine['American']:
                        val = 'American'
                    elif cuisines in map_cuisine['Italian']:
                        val = 'Italian'
                    elif cuisines in map_cuisine['Japanese']:
                        val = 'Japanese'
            items.append(key)
            if type(val) != list:
                items.append(val)
                finalCategory.append(items)
        writer.writerows(finalCategory)
    file2.close()


#consolidateCusines('business_extract.csv', 'newBusiness.csv')

