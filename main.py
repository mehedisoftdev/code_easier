import tkinter as tk
from tkinter import messagebox, scrolledtext
import json


def snake_to_camel(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def generate_dart_code(json_str, entity_name, with_entity):
    try:
        data = json.loads(json_str)
    except Exception as e:
        return f"❌ Invalid JSON: {e}"

    is_list_input = False
    if isinstance(data, list):
        if len(data) == 0:
            return "⚠️ JSON array is empty."
        if not isinstance(data[0], dict):
            return "⚠️ JSON array must contain objects."
        data = data[0]
        is_list_input = True

    if not isinstance(data, dict):
        return "⚠️ Please provide a JSON object or array of objects."

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

        camel_key = snake_to_camel(key[0].lower() + key[1:]) if "_" in key else key
        fields.append(f"  final {dart_type} {camel_key};")
        from_json_lines.append(f"      {camel_key}: json['{key}'] ?? {fallback},")
        to_json_lines.append(f"      '{key}': {camel_key},")

    note = ""
    if is_list_input and entity_name.lower().endswith("list"):
        suggested_name = entity_name[:-4]
        note = f"\n// ⚠️ Tip: Your input is a list. You probably want to use entity name like '{suggested_name}'."

    # === Entity class ===
    entity_code = f"""
class {entity_name} {{
{chr(10).join(fields)}

  {entity_name}({{
{chr(10).join(['    required this.' + line.split()[-1][:-1] + ',' for line in fields])}
  }});
}}""" if with_entity else ""

    # === Model class ===
    model_name = f"{entity_name}Model"

    if with_entity:
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

  {entity_name} toEntity() => {entity_name}(
{chr(10).join(['      ' + line.split()[-1][:-1] + ': ' + line.split()[-1][:-1] + ',' for line in fields])}
  );

  static List<{model_name}> fromJsonList(List<dynamic> jsonList) {{
    return jsonList.map((json) => {model_name}.fromJson(json)).toList();
  }}
}}"""
    else:
        model_code = f"""
class {model_name} {{
{chr(10).join(fields)}

  {model_name}({{
{chr(10).join(['    required this.' + line.split()[-1][:-1] + ',' for line in fields])}
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

  static List<{model_name}> fromJsonList(List<dynamic> jsonList) {{
    return jsonList.map((json) => {model_name}.fromJson(json)).toList();
  }}
}}"""

    return note + "\n\n" + entity_code + "\n\n" + model_code


# === GUI HANDLERS ===
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

