#! python3
# -*- coding: UTF-8 -*-
###########################
#
# description: 从列表中提取子列表
#
###########################



import logging,datetime
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# 提取子集，items 是字符串， 用逗号分隔
def fetchSubFromList(items):
    subList = []
    oneSubSizeMin = 3;
    oneSubSizeMax = 5;
    if items:
        itemList = str(items).split(',')
        if itemList and len(itemList)>=oneSubSizeMin:
            endLen = (oneSubSizeMax + 1) if len(itemList)>=oneSubSizeMax else (len(itemList)+1)
            for subSize in range(oneSubSizeMin, endLen):
                # 提取所有大小为subSize的子集
                oneSubList = fetchSubListBySubSize(subSize,itemList)
                subList += oneSubList
    return subList

# 从itemList中提取，元素个数为subSize的所有子集
def fetchSubListBySubSize(subSize,itemList):
    oneSubList = []
    if (not itemList) or (subSize>len(itemList)):
        logging.error("子集过大，无法提取")
        return oneSubList
    # 递归提取子集
    fetchSubListByRecursive(itemList,oneSubList,[],subSize)
    return oneSubList


# 递归提取元素子集元素，并将元素存放到currentSub中
def fetchSubListByRecursive(subList,totalSubList,currentSub,targetNum):
    lastIndex = len(subList) - targetNum + len(currentSub)
    for one_index in range(lastIndex+1):
        oneValue = subList[one_index]
        if len(currentSub) == targetNum -1:
            tempList = copyList(currentSub)
            tempList.append(oneValue)
            tempList.sort()
            totalSubList.append(tempList)
            return
        elif len(currentSub)<targetNum-1 and len(currentSub)>0:
            tempList = copyList(currentSub)
            tempList.append(oneValue)
            fetchSubListByRecursive(subList[one_index+1:],totalSubList,tempList,targetNum)
        else:
            tempList = [oneValue]
            fetchSubListByRecursive(subList[one_index+1:],totalSubList,tempList,targetNum)

# 复制数组元素 
def copyList(oneSubList):
    oneList = []
    for one_value in oneSubList:
        oneList.append(one_value)
    return oneList


try:
    items = '1,2,3,4,5'
    subList = fetchSubFromList(items)
    logging.info(subList)
except Exception as e:
    logging.error(e)
    raise e