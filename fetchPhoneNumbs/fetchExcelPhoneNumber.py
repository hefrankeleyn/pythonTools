#! python3
# -*- coding: UTF-8 -*-
###########################
#
# 从excel中提取电话号码
#
#  pip3 install openpyxl
###########################

import logging,openpyxl,os,re,datetime
from configparser import ConfigParser
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# 读取配置文件获取参数
def initParameters(conf_path):
    parameters={}
    cfg = ConfigParser()
    cfg.read(conf_path,'utf-8')
    # 获取文件路径
    dataExcelPath = cfg.get('DATASOURCE','dataExcelPath')
    parameters['dataExcelPath'] = dataExcelPath
    return parameters

# 读取excel并提取电话号码
def readyExcelContentFetchPhoneNumbers(excel_file_path):
    phoneNumbers=[]
    phoneRegx = re.compile(r'''1\d{10}''',re.VERBOSE)
    if os.path.exists(excel_file_path) and os.path.isfile(excel_file_path):
        wb = openpyxl.load_workbook(excel_file_path)
        # 遍历sheet页
        for sheet in wb:
            for row in sheet.values:
                for cell in row:
                    if cell:
                        for phone in phoneRegx.findall(str(cell)):
                            phoneNumbers = insertSort(phoneNumbers,phone)
    else:
        logging.info('%s不存在' % (excel_file_path))
    return phoneNumbers

# 插入排序
def insertSort(phoneNumbers,phone):
    if not phoneNumbers and phone:
        phoneNumbers.append(phone)
        return phoneNumbers
    elif not phone:
        return phoneNumbers
    phoneNumbersLen =  len(phoneNumbers)
    insertIndex = 0
    for i in range(phoneNumbersLen-1,-1,-1):
        if phoneNumbers[i]>phone:
            continue
        elif phoneNumbers[i]==phone:
            return phoneNumbers
        else:
            insertIndex=i+1
    phoneNumbers.insert(insertIndex,phone)
    return phoneNumbers


# 将数据写入到excel中
def writeExcel(excelFilePath,phoneNumbers):
    wb = openpyxl.Workbook()
    defaultSheet = wb.active
    for phoneIndex in range(len(phoneNumbers)):
        defaultSheet.cell(row=phoneIndex+1,column=1).value=phoneNumbers[phoneIndex]
    wb.save(excelFilePath)

# 如果目录不存在，就创建目录
def createDirIfNotExist(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
            
try:
    conf_path='paramConfig.ini'
    # 读取配置文件获取参数
    parameters = initParameters(conf_path)
    toDayObj = datetime.datetime.now()
    if parameters.__contains__("dataExcelPath"):
        # 提取出所有的电话号码，去重排序并放到列表中
        dataSourceExcelPath=parameters['dataExcelPath']
        fileName = os.path.split(dataSourceExcelPath)[1]
        phoneNumbers = readyExcelContentFetchPhoneNumbers(dataSourceExcelPath)
        # 获取当前目录
        newFileName = toDayObj.strftime('%Y%m%d%S') +"_提取_"+fileName;
        # 路径分隔符： os.sep
        excelPath = os.getcwd() + os.sep + toDayObj.strftime('%Y%m')
        createDirIfNotExist(excelPath)
        excelFilePath = os.path.join(excelPath,newFileName)
        # 生成excel
        writeExcel(excelFilePath,phoneNumbers)
        logging.info('提取的数据文件已经生成：%s' % (excelFilePath))
except Exception as e:
    logging.error(e)