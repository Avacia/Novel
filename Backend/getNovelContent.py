import os
import requests
import json
from bs4 import BeautifulSoup


def fetchDataFromWebMenu(link):
    """response = link.request"""
    return ""


def beautifulSoupFunction(data):
    """ soup = BeautifulSoup(data, 'html.parser') """
    return ""


def getPageLink(data, pageCSS):
    return [1,2,3,4,5]


def getTitle(content, titleCSS):
    """ title = content.title.string """
    return "Title"


def getBody(content, bodyCSS):
    """body = content.body.string"""
    return "Hi I am Yen"


def unwantedItem(soup, removeItem):
    return ""


def createBookFolder(bookName, bookFolder):
    current_directory = os.getcwd()
    targetFolderPath = os.path.join(current_directory, bookFolder)
    
    if os.path.exists(targetFolderPath) and os.path.isdir(targetFolderPath):
        new_folder_path = os.path.join(targetFolderPath, bookName)
        os.makedirs(new_folder_path, exist_ok=True)
        print(f"Folder {bookName} created inside {bookFolder}.")
        return new_folder_path
        
    else:
        print(f"The folder {bookFolder} does not exist in the current directory.")
        

def createBookInfo(bookName, menuUrl, pageCSS, titleCSS, bodyCSS, unwantedSelector, folderPath):
    data = {
        "Name" : bookName,
        "Menu URL": menuUrl,
        "Page CSS": pageCSS,
        "Title CSS": titleCSS,
        "Body CSS": bodyCSS,
        "Unwanted selector": unwantedSelector
    }
    
    fileName = "data.json"
    
    filePath = os.path.join(folderPath, fileName)
    with open(filePath, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON file {fileName} created successfully.")
    

def createFileForChapter(i, title, paragraph, folderPath):
    filePath = os.path.join(folderPath, f"Chapter {i}.txt")
    with open(filePath, "w") as file:
        file.write(f"Title: {title} \nBody: {paragraph}")


def main():
    bookFolder = "Books"
    bookName = input("Please input book name: ")
    menuUrl = input("Please input the menu url: ")
        
    pageCSS = input("Please input page css: ")
    titleCSS = input("Please input chapter title css: ")
    bodyCSS = input("Please input chapter body css: ")
    unwantedSelector = input("Please input the unwanted selector: ")
    
    data = fetchDataFromWebMenu(menuUrl)
    soup = beautifulSoupFunction(data)
    page = getPageLink(soup, pageCSS)
    
        
    folderPath = createBookFolder(bookName, bookFolder)
    createBookInfo(bookName, menuUrl, pageCSS, titleCSS, bodyCSS, unwantedSelector, folderPath)
    
    for i in range(len(page)):
        filteredFile = unwantedItem(page[i], unwantedSelector)
        title = getTitle(filteredFile, titleCSS)
        paragraph = getBody(filteredFile, bodyCSS)
        createFileForChapter(i, title, paragraph, folderPath)


main()
