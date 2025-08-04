import tkinter as tk
from tkinter import messagebox, scrolledtext
import json


def snake_to_camel(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

def generate_dart_code(json_str, entity_name, with_entity):
    try:
        data = json.loads(json_str)
    except Exception as e:
        return f"Invalid JSON: {e}"

    if isinstance(data, list):
        if len(data) == 0:
            return "JSON array is empty."
        if not isinstance(data[0], dict):
            return "JSON array must contain objects."
        data = data[0]  # use first object as structure

    if not isinstance(data, dict):
        return "Please provide a JSON object or array of objects."

    fields = []
    from_json_lines = []
    to_json_lines = []

    for key, value in data.items():
        dart_type = "String"
        fallback = "''"
        if isinstance(value, int):
            dart_type = "int"
            fallback = "0"
        elif isinstance(value, float):
            dart_type = "double"
            fallback = "0.0"
        elif isinstance(value, bool):
            dart_type = "bool"
            fallback = "false"

        fields.append(f"  final {dart_type} {key};")
        from_json_lines.append(f"      {key}: json['{key}'] ?? {fallback},")
        to_json_lines.append(f"      '{key}': {key},")

    entity_code = f"""
class {entity_name} {{
{chr(10).join(fields)}

  {entity_name}({{
{chr(10).join(['    required this.' + line.split()[-1][:-1] + ',' for line in fields])}
  }});
}}
""" if with_entity else ""

    model_name = f"{entity_name}Model"

    model_code = f"""
import 'package:your_project_path/{entity_name.lower()}.dart';

class {model_name} extends {entity_name} {{
  {model_name}({{
{chr(10).join(['    required super.' + line.split()[-1][:-1] + ',' for line in fields])}
  }});

  factory {model_name}.fromJson(Map<String, dynamic> json) {{
    return {model_name}(
{chr(10).join(from_json_lines)}
    );
  }}

  Map<String, dynamic> toJson() {{
    return {{
{chr(10).join(to_json_lines)}
    }};
  }}
{f"""
  {entity_name} toEntity() => {entity_name}(
{chr(10).join(['      ' + line.split()[-1][:-1] + ': ' + line.split()[-1][:-1] + ',' for line in fields])}
  );""" if with_entity else ""}
  
  static List<{model_name}> fromJsonList(List<dynamic> jsonList) {{
    return jsonList.map((json) => {model_name}.fromJson(json)).toList();
  }}
}}
"""

    return entity_code + "\n" + model_code



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


# === UI Setup ===
root = tk.Tk()
root.title("Dart Model & Entity Generator")

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
