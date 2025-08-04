import tkinter as tk
from tkinter import messagebox, scrolledtext
import json

def snake_to_pascal(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

def snake_to_camel(word):
    components = word.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def generate_dart_code(json_str, root_class_name, with_entity):
    try:
        parsed = json.loads(json_str)
    except Exception as e:
        return f"❌ Invalid JSON: {e}"

    is_list_input = False
    if isinstance(parsed, list):
        if len(parsed) == 0 or not isinstance(parsed[0], dict):
            return "⚠️ JSON array must contain objects."
        parsed = parsed[0]
        is_list_input = True

    generated_classes = {}

    def parse_object(obj, class_name, entity_class_name=None):
        is_model = entity_class_name is not None

        if class_name in generated_classes:
            return

        fields = []
        from_json = []
        to_json = []
        to_entity = []
        entity_fields = []

        for key, value in obj.items():
            field_name = snake_to_camel(key)
            dart_type = "String"
            fallback = "''"

            if isinstance(value, bool):
                dart_type = "bool"
                fallback = "false"
            elif isinstance(value, int):
                dart_type = "int"
                fallback = "0"
            elif isinstance(value, float):
                dart_type = "double"
                fallback = "0.0"
            elif isinstance(value, list):
                if len(value) > 0 and isinstance(value[0], dict):
                    sub_class = snake_to_pascal(key)
                    parse_object(value[0], sub_class)
                    dart_type = f"List<{sub_class}>"
                    fallback = "[]"
                    from_json.append(f"      {field_name}: (json['{key}'] as List).map((e) => {sub_class}.fromJson(e)).toList(),")
                    to_json.append(f"      '{key}': {field_name}.map((e) => e.toJson()).toList(),")
                    if with_entity:
                        to_entity.append(f"      {field_name}: {field_name},")
                    fields.append(f"  final {dart_type} {field_name};")
                    entity_fields.append(f"  final {dart_type} {field_name};")
                    continue
                else:
                    dart_type = "List<dynamic>"
                    fallback = "[]"
            elif isinstance(value, dict):
                sub_class = snake_to_pascal(key)
                parse_object(value, sub_class)
                dart_type = sub_class
                fallback = f"{sub_class}.fromJson({{}})"
                from_json.append(f"      {field_name}: {sub_class}.fromJson(json['{key}']),")
                to_json.append(f"      '{key}': {field_name}.toJson(),")
                if with_entity:
                    to_entity.append(f"      {field_name}: {field_name},")
                fields.append(f"  final {dart_type} {field_name};")
                entity_fields.append(f"  final {dart_type} {field_name};")
                continue

            fields.append(f"  final {dart_type} {field_name};")
            from_json.append(f"      {field_name}: json['{key}'] ?? {fallback},")
            to_json.append(f"      '{key}': {field_name},")
            if with_entity:
                to_entity.append(f"      {field_name}: {field_name},")
                entity_fields.append(f"  final {dart_type} {field_name};")

        constructor_params = '\n'.join([f"    required this.{f.split()[-1][:-1]}," for f in fields])
        class_body = ""

        if with_entity:
            class_body += f"""
import 'package:your_project_path/{entity_class_name.lower()}.dart';

class {class_name} extends {entity_class_name} {{
  {class_name}({{
{constructor_params}
  }}) : super(
{chr(10).join([f"    {line.split()[-1][:-1]}: {line.split()[-1][:-1]}," for line in fields])}
  );

  factory {class_name}.fromJson(Map<String, dynamic> json) {{
    return {class_name}(
{chr(10).join(from_json)}
    );
  }}

  Map<String, dynamic> toJson() {{
    return {{
{chr(10).join(to_json)}
    }};
  }}

  static List<{class_name}> fromJsonList(List<dynamic> jsonList) {{
    return jsonList.map((json) => {class_name}.fromJson(json)).toList();
  }}
}}"""
            entity_constructor = '\n'.join([f"    required this.{f.split()[-1][:-1]}," for f in entity_fields])
            entity_class = f"""
class {entity_class_name} {{
{chr(10).join(entity_fields)}

  {entity_class_name}({{
{entity_constructor}
  }});
}}"""
            generated_classes[class_name] = class_body.strip()
            generated_classes[entity_class_name] = entity_class.strip()
        else:
            class_body += f"""
class {class_name} {{
{chr(10).join(fields)}

  {class_name}({{
{constructor_params}
  }});

  factory {class_name}.fromJson(Map<String, dynamic> json) {{
    return {class_name}(
{chr(10).join(from_json)}
    );
  }}

  Map<String, dynamic> toJson() {{
    return {{
{chr(10).join(to_json)}
    }};
  }}

  static List<{class_name}> fromJsonList(List<dynamic> jsonList) {{
    return jsonList.map((json) => {class_name}.fromJson(json)).toList();
  }}
}}"""
            generated_classes[class_name] = class_body.strip()

    if with_entity:
        entity_class_name = root_class_name
        model_class_name = root_class_name + "Model"
        parse_object(parsed, model_class_name, entity_class_name=entity_class_name)
    else:
        parse_object(parsed, root_class_name)

    note = ""
    if is_list_input and root_class_name.lower().endswith("list"):
        suggested = root_class_name[:-4]
        note = f"// ⚠️ Tip: Your input is a list. You probably want to use entity name like '{suggested}'.\n\n"

    return note + "\n\n" + "\n\n".join(generated_classes.values())


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
root.title("code_easier - Dart Model/Entity Generator")

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
