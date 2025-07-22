import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests

# --- Setup Root Window ---
root = tk.Tk()
root.title("📄 PDF Chatbot")
root.geometry("700x500")
root.configure(bg="#e8f0ff")
# root.resizable(False, False)

# --- Card Container (White Box with Shadow) ---
card = tk.Frame(root, bg="white", bd=0, relief="ridge")
card.place(relx=0.5, rely=0.5, anchor="center", width=640, height=420)

# --- Style Setup ---
style = ttk.Style()
style.theme_use("clam")

style.configure("TNotebook", background="white", borderwidth=0)
style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[20, 10])
style.map("TNotebook.Tab",
          background=[("selected", "#2563eb")],
          foreground=[("selected", "white"), ("!selected", "#333")])

style.configure("TLabel", background="white", foreground="#111", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))
style.configure("TButton",
                font=("Segoe UI", 10, "bold"),
                foreground="white",
                background="#2563eb",
                padding=10)
style.map("TButton",
          background=[("active", "#1d4ed8")])

# --- Notebook Tabs ---
tabs = ttk.Notebook(card)
tabs.pack(fill="both", expand=True)

# ========== Upload Tab ==========
upload_tab = tk.Frame(tabs, bg="white")
tabs.add(upload_tab, text="📤 Upload PDF")

# Name
ttk.Label(upload_tab, text="👤 Enter Name:").grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
name_entry = ttk.Entry(upload_tab, width=50)
name_entry.grid(row=0, column=1, padx=20, pady=(20, 5))

# User ID
ttk.Label(upload_tab, text="🆔 Enter User ID:").grid(row=1, column=0, padx=20, pady=5, sticky="w")
id_entry = ttk.Entry(upload_tab, width=50)
id_entry.grid(row=1, column=1, padx=20, pady=5)

# File Label
selected_file_label = ttk.Label(upload_tab, text="No file selected", foreground="gray")
selected_file_label.grid(row=2, column=1, padx=20, pady=5, sticky="w")

# Browse File
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        selected_file_label.config(text=file_path)
    else:
        selected_file_label.config(text="No file selected")

browse_btn = ttk.Button(upload_tab, text="📁 Choose PDF", command=browse_file)
browse_btn.grid(row=2, column=0, padx=20, pady=10)

# Upload Logic
def upload_pdf():
    name = name_entry.get().strip()
    user_id = id_entry.get().strip()
    file_path = selected_file_label.cget("text")

    if not name or not user_id or "No file" in file_path:
        messagebox.showerror("Missing Info", "Please fill all fields and select a PDF.")
        return

    try:
        with open(file_path, "rb") as f:
            files = {"pdf": f}
            response = requests.post(
                "http://127.0.0.1:8000/upload_file",
                data={"user_name": name, "user_id": user_id},
                files=files
            )
        if response.status_code == 200:
            messagebox.showinfo("✅ Success", "PDF uploaded successfully.")
        else:
            messagebox.showerror("❌ Error", f"{response.json()['detail']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

upload_btn = ttk.Button(upload_tab, text="⬆️ Upload PDF", command=upload_pdf)
upload_btn.grid(row=3, column=1, padx=20, pady=20, sticky="e")

# ========== Ask Tab ==========
ask_tab = tk.Frame(tabs, bg="white")
tabs.add(ask_tab, text="💬 Ask PDF")

# User ID
ttk.Label(ask_tab, text="👤 Enter User ID:").grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
user_id_entry = ttk.Entry(ask_tab, width=50)
user_id_entry.grid(row=0, column=1, padx=20, pady=(20, 5))

# Question
# # Question
# ttk.Label(ask_tab, text="💬 Write your query:").grid(row=1, column=0, padx=20, pady=5, sticky="nw")
# question_entry = tk.Text(ask_tab, width=50, height=4, font=("Segoe UI", 10))
# question_entry.grid(row=1, column=1, padx=20, pady=5)

# # Response # answer
# ttk.Label(ask_tab, text="Response:").grid(row=3, column=0, padx=20, pady=5, sticky="nw")
# response_box = tk.Text(ask_tab, width=60, height=12, bg="#f4f4f4", fg="black", font=("Segoe UI", 11))
# response_box.insert("1.0", "Your answer will appear here...")
# response_box.grid(row=3, column=1, padx=10, pady=10)
# Question
ttk.Label(ask_tab, text="💬 Write your query:").grid(row=1, column=0, padx=20, pady=5, sticky="nw")
question_entry = tk.Text(ask_tab, width=50, height=4, font=("Segoe UI", 10))
question_entry.grid(row=1, column=1, padx=20, pady=5)

# Response
ttk.Label(ask_tab, text="Response:").grid(row=3, column=0, padx=20, pady=5, sticky="nw")
response_box = tk.Text(ask_tab, width=50, height=6, bg="#f4f4f4", fg="black", font=("Segoe UI", 10))
response_box.insert("1.0", "Your answer will appear here...")
response_box.grid(row=3, column=1, padx=20, pady=5)


# Send Query Logic
def send_query():
    user_id = user_id_entry.get().strip()
    question = question_entry.get("1.0", "end").strip()

    if not user_id or not question:
        messagebox.showerror("Missing Info", "Please enter both User ID and a question.")
        return

    try:
        response = requests.post("http://127.0.0.1:8000/query", data={
            "user_id": user_id,
            "question": question
        })
        if response.status_code == 200:
            answer = response.json().get("Answer", "No answer found.")
            response_box.delete("1.0", tk.END)
            response_box.insert(tk.END, answer)
        else:
            messagebox.showerror("Error", f"Failed to get answer:\n{response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

send_btn = ttk.Button(ask_tab, text="📤 Send Query", command=send_query)
send_btn.grid(row=2, column=1, padx=20, pady=10, sticky="e")

root.mainloop()



# import tkinter as tk
# from tkinter import ttk , filedialog


# root=tk.Tk()
# root.title("PDF Chatbot") 
# root.geometry("600x400")
# root.resizable(False,False)

# # Tabs Setup

# tabs=ttk.Notebook(root)
# tabs.pack(fill="both" , expand=True)

# # 1st Tab 
# upload_tab=ttk.Frame(tabs)
# tabs.add(upload_tab, text="Upload PFD")
# #     Name
# ttk.Label(upload_tab, text="Enter Name : ").grid(row=0 , column=0 ,padx=10 ,pady=10, sticky="w")
# name_entery=ttk.Entry(upload_tab ,width=40)
# name_entery.grid(row=0 , column=1, padx=10, pady=10)
# #     ID
# ttk.Label(upload_tab, text="User ID :").grid(row=1,column=0,padx=10,pady=10, sticky="w")
# id_entry=ttk.Entry(upload_tab , width=40)
# id_entry.grid(row=1,column=1,padx=10 , pady=10)

# # File Picker label 
# selected_file_label=ttk.Label(upload_tab, text="No file selected " , foreground="gray")
# selected_file_label.grid(row=2,column=1, padx=10 ,pady=10 , sticky="w")

# # browse file  func
# def browse_file():
#     file_path=filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
#     if file_path:
#         selected_file_label.config(text=file_path)
#     else:
#         selected_file_label.config(text="no file Selected")    

# browse_button=ttk.Button(upload_tab, text="Choose PDF" , command=browse_file )
# browse_button.grid(row=2 , column=0, padx=10, pady=5)

# # upload fun 
# import requests
# from tkinter import messagebox

# def upload_pdf():
#     name=name_entery.get().strip()
#     user_id=id_entry.get().strip()
#     file_path=selected_file_label.cget("text")
#     if not name or not user_id or "No file" in file_path:
#         messagebox.showerror("Missing Info", "Please fill all fields and select a PDF.")
#         return
#     try:
#         with open(file_path, "rb") as f:
#             files={"pdf":f}
#             # data={
#             #     "name":name,
#             #     "user_id":user_id
#             # }
#             response=requests.post(
#                  "http://127.0.0.1:8000/upload_file",
#                  data={"user_name": name, "user_id": user_id},
#                  files=files

#             )
#         if response.status_code==200:
#             messagebox.showinfo("Success", "PDF uploaded successfully.")    
#         else:
#             messagebox.showerror("Error", f"Upload failed: {response.json()['detail']}")    
            
#     except Exception as e:
#         messagebox.showerror("Error", f"Something went wrong:\n{e}")        

# # upload button

# upload_button=ttk.Button(upload_tab, text="Upload PDF" ,command=upload_pdf)
# upload_button.grid(row=3 ,column=1,padx=10,pady=20) 

# # --------------------
# # 2nd Tab
# # --------------------

# chat_tab=ttk.Frame(root)
# tabs.add(chat_tab , text="ASK PDF")

# # userid
# ttk.Label(chat_tab, text="Entry UserId : ").grid(row=0,column=0 , sticky="w", padx=10)
# user_id_entry=ttk.Entry(chat_tab , width=20 )
# user_id_entry.grid(row=0,column=1, padx=10 )

# # Query
# ttk.Label(chat_tab, text="write query : " ).grid(row=1,column=0,padx=10,pady=10, sticky="w")
# question_entry=ttk.Entry(chat_tab, width=40)
# question_entry.grid(row=1, column=1,padx=10)

# # response box:
# response_box=tk.Text(chat_tab, width=40, height=10,wrap="word")
# response_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
# # send logic 
# def send_query():
#     user_id=user_id_entry.get().strip()
#     query=question_entry.get().strip()
#     data={"user_id": user_id,
#             "question":query }
    
#     if not user_id or not query:
#         messagebox.showerror("message","plz entry both id and question")
#         return
    
#     try:
#         response=requests.post(
#         "http://127.0.0.1:8000/query",
#         data=data
        
#     )
#         if response.status_code==200:
#         #    answer=response.json().get("answer", "No answer found.")
#            answer = response.json().get("Answer", "No answer found.")
#            response_box.delete("1.0", tk.END)
#            response_box.insert(tk.END, answer)
#         else:
#             messagebox.showerror("Error", f"Failed to get answer:\n{response.status_code}")     


#     except Exception as e:
#         messagebox.showerror("Error", f"Something went wrong:\n{e}")        

# #send button
# send_btn=ttk.Button(chat_tab, text="Send" , command=send_query)
# send_btn.grid(row=2,column=1,padx=10,pady=10)






# root.mainloop()

