import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
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
root.geometry("1000x700")
root.minsize(800, 600)
root.state('zoomed')


style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"))
style.configure("TCheckbutton", font=("Segoe UI", 10))

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# Input JSON
ttk.Label(main_frame, text="Paste JSON:").grid(row=0, column=0, sticky="w", pady=(0, 5))
json_text = scrolledtext.ScrolledText(main_frame, height=12, wrap="word", font=("Consolas", 10),  undo=True)
json_text.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, 10))

# Entity input
ttk.Label(main_frame, text="Entity Class Name:").grid(row=2, column=0, sticky="w")
entity_entry = ttk.Entry(main_frame)
entity_entry.grid(row=2, column=1, sticky="ew", padx=(5, 0))

entity_var = tk.BooleanVar()
ttk.Checkbutton(main_frame, text="With Entity", variable=entity_var).grid(row=2, column=2, sticky="w", padx=(10, 0))

# Generate button
ttk.Button(main_frame, text="Generate", command=on_generate).grid(row=3, column=0, columnspan=3, pady=10)

# Output
ttk.Label(main_frame, text="Generated Dart Code:").grid(row=4, column=0, sticky="w", pady=(10, 5))
output_text = scrolledtext.ScrolledText(main_frame, height=15, wrap="word", font=("Consolas", 10),  undo=True)
output_text.grid(row=5, column=0, columnspan=3, sticky="nsew")

# Grid configuration
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=2)
main_frame.columnconfigure(2, weight=1)
main_frame.rowconfigure(1, weight=1)
main_frame.rowconfigure(5, weight=2)

root.mainloop()
