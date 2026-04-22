
<div align="center">
  <h1>🔐 Password Strength Checker</h1>
  <p>
    <strong>A lightweight Python CLI tool to evaluate password strength with actionable feedback.</strong>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/CLI-Tool-black?style=for-the-badge" alt="CLI Tool" />
    <img src="https://img.shields.io/badge/No%20Dependencies-brightgreen?style=for-the-badge" alt="No Dependencies" />
    <img src="https://img.shields.io/badge/Security-Focused-red?style=for-the-badge" alt="Security Focused" />
  </p>
</div>

<br />

## 🌟 Overview

**Password Strength Checker** is a simple yet powerful command-line tool built in Python to analyze password strength and provide clear, actionable suggestions.

It runs completely **offline**, ensuring your passwords are never exposed or sent over the internet.

---

## 🚀 Key Features

- 🔒 **Secure Input** – Hidden password entry (no echo)
- 📊 **Strength Score** – Numeric score (0–100)
- 🏷️ **Labels** – Weak / Medium / Strong / Very Strong
- 💡 **Actionable Feedback** – Suggestions to improve passwords
- ⚙️ **CLI Friendly** – Supports `--min-score` for automation
- 🚫 **No Dependencies** – Lightweight and fast

---

## 📁 Project Structure

```text
PASSWORD-CHECKER/
├── main.py                # CLI entry point
├── password/
│   ├── __init__.py       # Package exports
│   ├── cli.py            # CLI handling
│   └── scorer.py         # Strength logic
└── README.md
---

## ⚙️ Requirements

* **Python 3.8+**
* No additional libraries required

---

## 🛠️ Installation

Clone or download the repository:

```bash
git clone https://github.com/HimanshuKumarRout/password-checker.git
cd "PASSWORD CHECKER"
```

(Optional) Create a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
```

---

## ▶️ Usage

### 1. Pass password as argument

```bash
python main.py "YourPasswordHere"
```

### 2. Interactive mode (recommended)

```bash
python main.py
```

Prompt:

```text
Enter password (input hidden):
```

---

## 📌 Example Output

```text
Score: 72/100
Strength: Strong
Feedback:
- Increase length to 16+ characters for better protection.
- Avoid common words or obvious patterns.
```

---

## ⚡ Using `--min-score` (Automation / CI)

Enforce minimum password strength:

```bash
python main.py "MyPassword123" --min-score 80
```

### Exit Codes

* `0` → Meets required strength
* `2` → Below minimum score

Perfect for:

* CI/CD pipelines
* Internal validation scripts
* Security checks

---

## 🧠 How It Works

The scoring system in `scorer.py` evaluates:

* 📏 **Length of password**
* 🔤 **Character diversity** (uppercase, lowercase, digits, symbols)
* 🔢 **Entropy-like estimation**
* ⚠️ **Penalties for weak patterns**:

  * Common passwords
  * Sequential patterns (`1234`, `abcd`)
  * Repeated characters (`aaaaaa`)

### Output Includes:

* `score` → Numeric value (0–100)
* `label` → Strength category
* `feedback` → Improvement tips
* `details` → Diagnostic insights

---

## ⚠️ Security Notes

* ❌ Not a replacement for professional security auditing tools
* 🔐 Use proper hashing algorithms in real systems:

  * `bcrypt`
  * `scrypt`
  * `argon2`
* 🚫 Never store or log real passwords

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch (`feature/your-feature`)
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 📝 License

Add your preferred license (MIT recommended).

---

<p align="center">Built with 🔐 for better password security.</p>

---
