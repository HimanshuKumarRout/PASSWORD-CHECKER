## Password Strength Checker

A small Python command‑line tool to **estimate password strength** and provide **clear, actionable feedback**.  
It uses lightweight heuristics (no heavy dependencies) to score passwords from 0–100 and classify them as **Weak**, **Medium**, **Strong**, or **Very Strong**.

---

### Features

- **Secure input**: Prompts for your password without echoing it to the screen.
- **Numeric score**: Strength score from 0–100.
- **Human‑readable label**: Weak / Medium / Strong / Very Strong.
- **Actionable feedback**: Suggestions to improve your password.
- **CLI friendly**: Optional `--min-score` flag for scripts or CI checks.
- **No external services**: Fully local; no password data is sent anywhere.

---

### Project Structure

- `main.py` – Entrypoint for the CLI application.
- `password/cli.py` – Command‑line parsing, input handling, and output.
- `password/scorer.py` – Password strength heuristic and scoring logic.
- `password/__init__.py` – Public helpers and exports.

---

### Requirements

- **Python 3.x** (3.8+ recommended)
- No third‑party dependencies required.

---

### Installation

Clone or download this repository, then navigate into the project folder:

```bash
cd "PASSWORD CHECHER"
```

(Use quotes because the directory name contains a space.)

You can run the script directly with your system Python; no extra install step is strictly required.  
Optionally, create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate  # on Windows PowerShell
```

---

### Usage

You can either **pass a password as an argument** or **enter it interactively**.

#### 1. Pass password as an argument

```bash
python main.py "YourPasswordHere"
```

#### 2. Interactive (hidden input)

```bash
python main.py
```

You’ll be prompted:

```text
Enter password (input hidden):
```

Type your password (it will not be shown) and press Enter.

---

### Example Output

```text
Score: 72/100
Strength: Strong
Feedback:
- Increase length to 16+ characters for better protection.
- Avoid common words or obvious patterns.
```

---

### Using `--min-score` (for scripts/CI)

You can enforce a **minimum required strength** and use the exit code to fail a script or pipeline:

```bash
python main.py "MyPassword123" --min-score 80
```

Exit codes:

- `0` – Password meets or exceeds the `--min-score` (or no `--min-score` provided).
- `2` – Password score is below the requested `--min-score`.

This is useful for:

- Enforcing password strength rules in internal tooling.
- Quick checks in automated scripts.

---

### How It Works (Overview)

The core logic in `password/scorer.py`:

- Checks **length** and **character variety** (lowercase, uppercase, digits, symbols).
- Estimates **entropy‑like strength** based on the effective character pool.
- Applies **penalties** for:
  - Very common passwords.
  - Simple sequences like `abcd` or `1234`.
  - Repeated characters (e.g. `aaaaaa`).
- Produces a `PasswordStrength` object with:
  - `score` (0–100),
  - `label` (Weak / Medium / Strong / Very Strong),
  - `feedback` (list of tips),
  - `details` (extra diagnostic info).

---

### Security Notes & Limitations

- **Do not** treat this as a replacement for a professional password auditing tool.
- The scoring is **heuristic**, not a formal cryptographic analysis.
- For real‑world authentication systems:
  - Always use a **slow, salted password hash** such as `bcrypt`, `scrypt`, or `argon2`.
  - Consider integrating a well‑maintained password strength library or service.
- Never store or log real passwords used with this tool.

---

### License

Add your chosen license here (e.g. MIT, Apache‑2.0, etc.).