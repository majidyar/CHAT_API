import logging.config
from fastapi import FastAPI, UploadFile,File ,HTTPException , Form
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
from pypdf import PdfReader 
import logging

from data_store.data_store import data,save_data
from llm_client.clientllm import ai_response

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"

)




app =FastAPI(
    title="Chat With Your PDF",
    description="This API is for uploading pdf and chating with them with specific uuids",
    version="1.0.0"
)



@app.get("/", response_class=HTMLResponse , tags=["root"])
def read_root():
    return FileResponse("templates/welcome.html")

@app.post("/upload_file" , tags=["upload"])
def upload_pdf(user_name:str=Form(...), user_id:str=Form(...) , pdf:UploadFile=File(...)):
    user_id_str=str(user_id)
    if user_id_str in data:
        logging.warning(f"Duplicate user_id attempted: {user_id_str}")
        raise HTTPException(
            status_code=500, detail="plz try an other already "
        )
    try :
        #  here we will extract text
        reader=PdfReader(pdf.file)
        text=""
        for page in reader.pages:
         
            extracted_text=page.extract_text()
            text+=extracted_text
        if not text.strip():
          raise HTTPException(status_code=400, detail="Uploaded PDF has no readable text.")    
        # save data 
        # data[user_id_str]=text
        data[user_id_str] = {
            "name": user_name,
            "text": text
        }
        save_data()
        logging.info(f"PDF uploaded by user: {user_id_str}")
        return {"message": "PDF uploaded and processed successfully!"}
    except Exception as e:
        raise HTTPException(
        status_code=500 , detail=f" something went wrong during reading : {e}"
        )
    
@app.post("/query", tags=["Chat"])
def query_pdf(user_id:str=Form(...), question:str=Form(...)):
    if user_id not in data:
        logging.warning(f"Query failed: unknown user_id {user_id}")
        raise HTTPException(
            status_code=404, detail="user id not exist  "
        ) 
    try:
        pdf_text = data[user_id]["text"]
        user_name = data[user_id]["name"]
        logging.info(f"Query from user: {user_id}, question: {question}")


        return {"Answer": ai_response(user_name,pdf_text,question)}
    except Exception as e:
        print(f"the is some error :{e}")

    
@app.put("/update" , tags=["Updata Data"])    
def update_data(user_id:str=Form(...),new_pdf:UploadFile=File(...)):
    if user_id not in data:
        logging.warning(f"Query failed: unknown user_id {user_id}")
        raise HTTPException(
            status_code=404, detail="user id not exist  "
        ) 
    try :
        #  here we will extract text
        reader=PdfReader(new_pdf.file)
        text=""
        for page in reader.pages:
            extracted_text=page.extract_text()
            text+=extracted_text
        if not text.strip():
          raise HTTPException(status_code=400, detail="Uploaded PDF has no readable text.")    
        # save data 
        data[user_id]["text"]=text
        save_data()
        logging.info(f"PDF updated by user: {user_id}")
        return {"message": "PDF updated and processed successfully!"}
    except Exception as e:
        raise HTTPException(
        status_code=500 , detail=f" something went wrong during reading : {e}"
        )  
    

@app.delete("/delete", tags=["Delte Data"])
def del_data(user_id:str=Form(...)):
    if user_id not in data:
        logging.warning(f"Query failed: unknown user_id {user_id}")
        raise HTTPException(
            status_code=404, detail="user id not exist  "
        )
    try:
        del data[user_id]
        save_data()
        logging.info(f"the key {user_id}: and its text deleted")
        return{"message":f"the data and in id:{user_id} had been deleted"}
        
        
    except Exception as e:
        raise HTTPException(
        status_code=500 , detail=f" something went wrong during deletion : {e}"
        )            
 



if __name__=="__main__":
    uvicorn.run(
        app , host="127.0.0.1" , port=8000
    )







