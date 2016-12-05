from utilities import *
from scipy.stats import spearmanr


def findSpearmanRank(userMap, valueList):
	spearmanDict = dict()

	for idx, item in enumerate(valueList):
		for gdx, item1 in enumerate(valueList):
			if ((idx+1, gdx+1) not in spearmanDict.keys() and (gdx+1, idx+1) not in spearmanDict.keys()) and idx != gdx:
				if not userMap.get(idx+1)[0] in spearmanDict:
					spearmanDict[userMap.get(idx + 1)[0]] = []
				else:
					spearmanDict[userMap.get(idx+1)[0]].append((userMap.get(gdx)[0], abs(spearmanr(item, item1)[0])))

	iterator = 0
	for key, val in spearmanDict.items():
		val.sort(key=lambda tup: tup[1])
		possibleCombination = [x[0] for x in val[-25:]]
		iterator += 1
		a = set(userMap[iterator][1])
		b = set(possibleCombination)
		friends = b.intersection(a)
		for eachPossibleFan in val[-25:]:
			if eachPossibleFan[0] in friends:
				del eachPossibleFan #Since they are already friends.

	return spearmanDict


def printPossibleFollowers(dictionary):
	for key, val in dictionary[0].items():
		print 'Recommended Friends for user ' + dictionary[1].get(key) + ' with ID ' + key + ' are'
		for eachItem in val[-25:]:
			print dictionary[1].get(eachItem[0]) + ', ',
		print '\n'


if __name__ == '__main__':
	content = readFile('Data/yelp_academic_dataset_user.csv')
	userDict, userIndexMap, valList, userIDName = createUserDict(content)
	spearManDict = findSpearmanRank(userIndexMap, valList)
	makeModelFile('correlatedModelFile', (spearManDict, userIDName))
	userAndFollowers = getModelFile('correlatedModelFile')
	printPossibleFollowers(userAndFollowers)

