
# 🧰 code\_easier

A simple and extensible open-source **Dart model/entity generator** GUI tool. Built with Python and Tkinter, this app lets you instantly convert raw JSON into clean Dart model classes — optionally with `Entity` inheritance support — ready for use in Flutter apps (Clean Architecture friendly).

## ✨ Features

* ✅ Parse raw JSON into Dart model classes
* ✅ Optional `Entity` class generation and model inheritance
* ✅ Handles nested objects and arrays
* ✅ Smart null-safe default values (`?? ''`, `?? 0`, etc.)
* ✅ Auto-generates:

  * `fromJson`, `toJson`
  * `fromJsonList`
* ✅ Supports PascalCase class names and camelCase fields
* ✅ Clean, simple GUI — no CLI needed
* ✅ Written in pure Python — no extra frameworks

---

## 🚀 Getting Started

### 🔧 Prerequisites

* Python 3.8+
* Tkinter (usually included by default with Python)

### 📦 Installation

```bash
git clone https://github.com/mehedisoftdev/code_easier.git
cd code_easier
python main.py
```

That's it! The GUI will open up and you can paste your JSON and generate Dart code instantly.

---

## 🖼️ Screenshot

![code\_easier screenshot](screenshot.png) <!-- Add screenshot in repo -->

---

## 🧪 Example Usage

### ✅ Input JSON

```json
{
  "employeeCode": "EMP001",
  "employeeId": 101,
  "employeeName": "John Doe"
}
```

### ✅ Output (with Entity checked)

```dart
import 'package:your_project_path/employee.dart';

class EmployeeModel extends Employee {
  EmployeeModel({
    required super.employeeCode,
    required super.employeeId,
    required super.employeeName,
  });

  factory EmployeeModel.fromJson(Map<String, dynamic> json) {
    return EmployeeModel(
      employeeCode: json['employeeCode'] ?? '',
      employeeId: json['employeeId'] ?? 0,
      employeeName: json['employeeName'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'employeeCode': employeeCode,
      'employeeId': employeeId,
      'employeeName': employeeName,
    };
  }

  static List<EmployeeModel> fromJsonList(List<dynamic> jsonList) {
    return jsonList.map((json) => EmployeeModel.fromJson(json)).toList();
  }
}

class Employee {
  final String employeeCode;
  final int employeeId;
  final String employeeName;

  Employee({
    required this.employeeCode,
    required this.employeeId,
    required this.employeeName,
  });
}
```

---

## ⚙️ Future Plans

* 🛠 Build `.exe` or `.msi` installer for Windows
* 🌍 Add localization (Bengali, English)
* 🧩 Add code generators for:

  * Clean Architecture layers (UseCases, Repository)
  * Flutter UI boilerplate

---

## 💡 Tips

* If your input JSON is a **list**, name your entity/model accordingly (e.g., `Employee` not `EmployeeList`).
* For large JSON, make sure objects are not too deeply nested.

---

## 📝 License

MIT License
© 2025 Mehedi Hasan

---

## 🙌 Contributing

Pull requests are welcome!
Feel free to fork the repo, suggest features, or raise issues.

