from tkinter import Tk
from tkinter import filedialog
import os
import json
import collections

i18nList = {}
i18realused = {}
i18nMissingInProp ={}
PropMissingIni18n ={}
root = Tk()
root.withdraw()

current_directory = filedialog.askdirectory()

for root, dirs, files in os.walk(current_directory):  
    for filename in files:
        if any(x in filename for x in [".js",".properties",".xml"]):
            if "i18n" not in filename:
                print(root+"\\"+filename)
                with open(root+"\\"+filename,encoding="utf-8") as f:
                    content = f.read().splitlines()
                    oneFileList = []
                    tempvars = []
                    for element in content:
                        element = element.strip()
                        if "i18n" in element:
                            if "xml" in filename:
                                oneFileList.append(element.split(">")[1].split("}")[0])
                            elif "json" in filename:
                                continue
                            elif "js" in filename:
                                if not (filename.startswith("*") or filename.startswith("//")) :
                                    if "getText(" in element:
                                        oneFileList.append(element.split("getText(")[1].split(")")[0].replace("\"",""))
                                    else:
                                        tempvars.append((element.split("=")[0].replace("var","")).strip())
                        if len(tempvars)>0:
                            if any(x in element for x in tempvars):
                                if "getText(" in element:
                                    oneFileList.append(element.split("getText(")[1].split(")")[0].replace("\"",""))        
                    i18realused[filename] = oneFileList
            else:
                print(root+"\\"+filename)
                with open(root+"\\"+filename,encoding="utf-8") as f:
                    content = f.read().splitlines()
                    oneFileList = {}
                    for element in content:
                        onFile = {}
                        if len(element.split("=")) >1:
                            onFile["value"] = element.split("=")[1]
                            oneFileList[element.split("=")[0]] = onFile
                    i18nList[filename] = oneFileList

for k in i18realused:
    for element in i18realused[k]:
        allIm = 0
        if element != "":
            for k2 in i18nList:
                if k2 not in i18nMissingInProp:
                    i18nMissingInProp[k2]={}
                counter = 0
                for k3 in i18nList[k2]:
                    if k3 == element:
                        counter = counter +1
                if counter >0:
                    allIm = allIm +1
                else:
                    if filename not in i18nMissingInProp[k2]:
                        i18nMissingInProp[k2][filename]=[]
                    i18nMissingInProp[k2][filename].append(element)
tempflatList = []
tempflatListValue = []
for k2 in i18nList:
    for k3 in i18nList[k2]:
        if k3 not in tempflatList:
            tempflatList.append(k3)
            tempflatListValue.append(i18nList[k2][k3]["value"].strip())
tempflattealused = []
for k in i18realused:
    for element in i18realused[k]:
        if element not in tempflattealused:
            tempflattealused.append(element)
unnessecaryi18nprop=[]
tempcopyList =collections.defaultdict(dict)
for element in tempflatList:
    if element not in tempflattealused:
        unnessecaryi18nprop.append(element)
for k2 in i18nList:
    for k3 in i18nList[k2]:
        if k3 not in unnessecaryi18nprop:
            tempcopyList[k2][k3] = i18nList[k2][k3]




f = open("Alli18nProperties.txt", "a")
f.write(json.dumps(i18nList, indent=4, sort_keys=True))
f = open("Alli18nFromFiles.txt", "a")
f.write(json.dumps(i18realused, indent=4, sort_keys=True))
f = open("Missing_Values_From_Properties.txt", "a")
f.write(json.dumps(i18nMissingInProp, indent=4, sort_keys=True))
f = open("Missing_Values_From_i18n.txt", "a")
for item in unnessecaryi18nprop:
    f.write("%s\n" % item)
for k2 in tempcopyList:
    f = open(k2, "a")
    for k3 in tempcopyList[k2]:
        f.write(k3 +"=" +tempcopyList[k2][k3]["value"]+"\n")
f = open("duplicates.txt", "a")
for item in [item for item, count in collections.Counter(tempflatListValue).items() if count > 1]:
    f.write("%s\n" % item)