import json
import re

def snake_to_pascal(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

def snake_to_camel(name):
    # Handles snake_case, PascalCase, and UPPER_SNAKE_CASE → lowerCamelCase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)  # Convert PascalCase to snake_case
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    components = s2.lower().split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def generate_dart_code(json_str, root_class_name, with_entity):
    try:
        parsed = json.loads(json_str)
    except Exception as e:
        return f"❌ Invalid JSON: {e}"

    is_list_input = False
    if isinstance(parsed, list):
            # Build a dict of all keys and their types across the array
        key_type_map = {}
        for item in json.loads(json_str):
            if isinstance(item, dict):
                for k, v in item.items():
                    if v is not None:
                        current_type = type(v).__name__
                        if k not in key_type_map:
                            key_type_map[k] = current_type

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
        entity_fields = []

        for key, value in obj.items():
            field_name = snake_to_camel(key)

            # Default
            dart_type = "String"
            fallback = "''"

            key_type = key_type_map.get(key, None)

            if value is None:
                if key_type == "int":
                    dart_type = "int?"
                elif key_type == "float":
                    dart_type = "double?"
                elif key_type == "bool":
                    dart_type = "bool?"
                else:
                    dart_type = "String?"  # fallback
                fallback = "null"

            elif isinstance(value, bool):
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
                fields.append(f"  final {dart_type} {field_name};")
                entity_fields.append(f"  final {dart_type} {field_name};")
                continue

            # Handle nullable fallback
            if value is None:
                from_json.append(f"      {field_name}: json['{key}'],")
            else:
                from_json.append(f"      {field_name}: json['{key}'] ?? {fallback},")

            to_json.append(f"      '{key}': {field_name},")
            fields.append(f"  final {dart_type} {field_name};")
            entity_fields.append(f"  final {dart_type} {field_name};")

        
        if with_entity:
            constructor_params = '\n'.join([f"    required super.{f.split()[-1][:-1]}," for f in fields])
        else:
            constructor_params = '\n'.join([f"    required this.{f.split()[-1][:-1]}," for f in fields])

        class_body = ""

        if with_entity:
            class_body += f"""
import 'package:your_project_path/{entity_class_name.lower()}.dart';

class {class_name} extends {entity_class_name} {{
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
