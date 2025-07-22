import os
import json

DATA_FILE = "data.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE ,"r",encoding="utf-8") as f:
        data=json.load(f)
else:
    data= {}  

def save_data():
    with open(DATA_FILE,"w" ,encoding="utf-8")as f:
        json.dump(data,f,ensure_ascii=False, indent=4)         