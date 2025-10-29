import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

# --- CONNECT TO SERVER ---
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# --- ASK FOR NICKNAME ---
nickname = simpledialog.askstring("Nickname", "Enter your nickname:")

# --- SEND AND RECEIVE ---
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, message + '\n')
                chat_area.config(state=tk.DISABLED)
                chat_area.yview(tk.END)
        except:
            print("Error! Closing connection.")
            client.close()
            break

def send_message():
    message = f'{nickname}: {msg_entry.get()}'
    client.send(message.encode('utf-8'))
    msg_entry.delete(0, tk.END)

# --- GUI WINDOW ---
root = tk.Tk()
root.title("Chat Room")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
chat_area.pack(padx=10, pady=10)

msg_entry = tk.Entry(root, width=40)
msg_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT, padx=10, pady=(0, 10))

# --- START THREAD ---
receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.mainloop()
