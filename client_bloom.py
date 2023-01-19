import tkinter as tk
import json
import websockets
from tkinter import filedialog

# Define global variables
max_length = 4096
stop_sequence = None
websocket = None

# Define functions for GUI buttons and WebSocket communication
def open_and_connect_inference_session():
    global websocket, max_length, stop_sequence
    max_length = int(max_length_entry.get())
    uri = "ws://chat.petals.ml/api/v2/generate"
    websocket = websockets.connect(uri)
    request = {"type": "open_inference_session", "max_length": max_length, "stop_sequence": stop_sequence}
    websocket.send(json.dumps(request))
    response = json.loads(websocket.recv())
    print(response)

def generate_text():
    global websocket
    input_text = input_text_entry.get(1.0, tk.END)
    request = {"type":"generate", "input_text": input_text, "max_length": max_length, "stop_sequence": stop_sequence}
    websocket.send(json.dumps(request))
    response = json.loads(websocket.recv())
    output_text.insert(tk.END, response['output'])

def save_conversation():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt")
    with open(filepath, 'w') as file:
        file.write(output_text.get(1.0, tk.END))

root = tk.Tk()
root.configure(bg='black')

max_length_label = tk.Label(root, text="Max Length:", bg='black', fg='white')
max_length_label.grid(row=0, column=0)
max_length_entry = tk.Entry(root, bg='black', fg='white')
max_length_entry.insert(0, max_length)
max_length_entry.grid(row=0, column=1)
input_text_label = tk.Label(root, text="Input:", bg='black', fg='white')
input_text_label.grid(row=2, column=0)
input_text_entry = tk.Text(root, height=5, width=50, bg='black', fg='white')
input_text_entry.grid(row=3, column=0, columnspan=2)

output_text_label = tk.Label(root, text="Output:", bg='black', fg='white')
output_text_label.grid(row=4, column=0)
output_text = tk.Text(root, height=5, width=50, bg='black', fg='white')
output_text.grid(row=5, column=0, columnspan=2)
output_text = tk.Text(root, height=5, width=50, bg='black', fg='white')
output_text.grid(row=5, column=0, columnspan=2)

open_inference_session_button = tk.Button(root, text="Open Inference Session", command=open_and_connect_inference_session, bg='black', fg='white')
open_inference_session_button.grid(row=6, column=0)

generate_text_button = tk.Button(root, text="Generate Text", command=generate_text, bg='black', fg='white')
generate_text_button.grid(row=6, column=1)

save_conversation_button = tk.Button(root, text="Save Conversation", command=save_conversation, bg='black', fg='white')
save_conversation_button.grid(row=7, column=0, columnspan=2)

root.mainloop()