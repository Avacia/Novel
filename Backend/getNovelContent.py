import os
import requests
import json
import re
import sys
from bs4 import BeautifulSoup


def fetchDataFromWebMenu(link):
    response = requests.get(link)
    replacedResponse = re.sub(r'&#x[a-f0-9]{4};', "", response.text)
    return replacedResponse


def beautifulSoupFunction(data, itemCSS, needLink):
    soup = BeautifulSoup(data, 'html.parser')
    items = soup.select(itemCSS)
    
    if needLink is None:
        return [item.get_text(strip=True) for item in items]
    else:
        pageLinks = []
        for link in items:
            pageLinks.append(f"{needLink}{link['href']}")
        return pageLinks


def getTitle(data, titleCSS):
    title = beautifulSoupFunction(data, titleCSS, None)
    return title


def getBody(data, bodyCSS):
    body = beautifulSoupFunction(data, bodyCSS, None)
    return body


def unwantedItem(soup, removeItem):
    return soup


def createBookFolder(bookName, folderPath):
    if os.path.exists(folderPath) and os.path.isdir(folderPath):   
        bookPath = os.path.join(folderPath, bookName)     
        os.makedirs(bookPath, exist_ok=True)
        print(f"Folder {bookName} created inside Books.")
        return folderPath
        
    else:
        print(f"The folder 'Books' does not exist in the current directory.")
        

def createBookInfo(bookName, menuUrl, pageCSS, pageLink, titleCSS, bodyCSS, unwantedSelector, folderName):
    data = {
        "Name" : bookName,
        "Menu URL": menuUrl,
        "Page CSS": pageCSS,
        "Page Link": pageLink,
        "Title CSS": titleCSS,
        "Body CSS": bodyCSS,
        "Unwanted selector": unwantedSelector
    }
    
    fileName = f"{bookName}.json"
    
    folderPath = findFolderPath(folderName)
    filePath = os.path.join(folderPath, fileName)
    with open(filePath, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON file {fileName} created successfully.")
    

def createFileForChapter(i, title, paragraph, folderPath):
    filePath = os.path.join(folderPath, f"Chapter {i}.json")
    data = {
        "Title" : title,
        "Paragraph" : paragraph
    }
    with open(filePath, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        

def checkFolderExist(filePath):
    return True if os.path.isdir(filePath) else False


def checkFileExist(filePath):
    return True if os.path.isfile(filePath) else False


def collectUserInput():
    menuUrl = input("Please input the menu url: ")
    pageCSS = input("Please input page css: ")
    pageLink = input("Please input page link: ")
    titleCSS = input("Please input chapter title css: ")
    bodyCSS = input("Please input chapter body css: ")
    unwantedSelector = input("Please input the unwanted selector: ")
    return menuUrl, pageCSS, pageLink, titleCSS, bodyCSS, unwantedSelector


def loadDataFromFile(dataPath):
    with open(f'{dataPath}', "r", encoding="utf-8") as file:
           data = json.load(file)
    return data


def findFolderPath(folderName):
    currentPath = os.getcwd()
    targetPath = os.path.join(currentPath, folderName)
    return targetPath


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s | Iteration: %d/%d' % (prefix, bar, percent, suffix, iteration, total), end='\r')
    if iteration == total: 
        print()


def main():
    bookFolder = "Books"
    jsonFolder = "JSON"
    bookName = input("Please input book name: ")
    
    bookFolderPath = findFolderPath(bookFolder)
    bookPath = os.path.join(bookFolderPath, bookName)
    jsonFolderPath = findFolderPath(jsonFolder)
    jsonPath = os.path.join(jsonFolderPath, f"{bookName}.json")
    pathInJson = checkFileExist(jsonPath)
    pathInBooks = checkFolderExist(bookPath)
    
    if (pathInJson is True) or (pathInBooks is True):
        data = loadDataFromFile(jsonPath)
           
        menuUrl = data["Menu URL"]
        pageCSS = data["Page CSS"]
        pageLink = data["Page Link"]
        titleCSS = data["Title CSS"]
        bodyCSS = data["Body CSS"]
        unwantedSelector = data["Unwanted selector"]
        
        print("Loaded data from existing book folder.")  
    else:
        createBookFolder(bookName, bookFolderPath)
        menuUrl, pageCSS, pageLink, titleCSS, bodyCSS, unwantedSelector = collectUserInput()
        createBookInfo(bookName, menuUrl, pageCSS, pageLink, titleCSS, bodyCSS, unwantedSelector, jsonFolder)
    
    data = fetchDataFromWebMenu(menuUrl)
    page = beautifulSoupFunction(data, pageCSS, pageLink)
    
    for i in range(len(page)):
        printProgressBar(i, len(page), prefix = 'Progress:', suffix = "Complete", length = 50)
        data = fetchDataFromWebMenu(page[i])
        title = getTitle(data, titleCSS)
        paragraph = getBody(data, bodyCSS)
        createFileForChapter(i + 1, title, paragraph, bookPath)

main()
