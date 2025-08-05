# main.py

import tkinter as tk
from tkinter import messagebox, scrolledtext
from logic.generator import generate_dart_code

def on_generate():
    json_input = json_text.get("1.0", tk.END).strip()
    entity_name = entity_entry.get().strip()
    with_entity = entity_var.get()

    if not entity_name:
        messagebox.showwarning("Input Missing", "Please enter Entity Class Name")
        return

    output = generate_dart_code(json_input, entity_name, with_entity)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)

# === UI SETUP ===
root = tk.Tk()
root.title("code_easier - Dart Model/Entity Generator")
root.state('zoomed')

tk.Label(root, text="Paste JSON:").pack()
json_text = scrolledtext.ScrolledText(root, height=10)
json_text.pack(fill="both", padx=10, pady=5)

tk.Label(root, text="Entity Class Name:").pack()
entity_entry = tk.Entry(root)
entity_entry.pack(fill="x", padx=10)

entity_var = tk.BooleanVar()
tk.Checkbutton(root, text="With Entity", variable=entity_var).pack(anchor="w", padx=10)

tk.Button(root, text="Generate", command=on_generate).pack(pady=10)

tk.Label(root, text="Generated Dart Code:").pack()
output_text = scrolledtext.ScrolledText(root, height=20)
output_text.pack(fill="both", padx=10, pady=5)

root.mainloop()
