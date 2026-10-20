# Caesar and Substitution Cipher: Attack and Prevention Demo

A comprehensive Python-based desktop application demonstrating fundamental cryptographic techniques, their vulnerabilities to common attacks, and modern prevention strategies.

## 🚀 Features

- **Caesar Cipher**: Standard shift encryption and decryption.
- **Substitution Cipher**: Randomized character mapping for enhanced security.
- **Attack Demonstrations**:
  - **Brute Force (Caesar)**: Automatically tries all 26 shifts and ranks results by English frequency scoring.
  - **Frequency Analysis (Substitution)**: Performs statistical analysis on ciphertext to identify common character patterns.
- **Prevention Measures**:
  - **Multi-shift Encryption**: A Vigenere-like approach using multiple keys to thwart simple brute force.
  - **Hybrid Encryption**: Combines Caesar and Substitution ciphers for layered security.

## 🛠 Prerequisites

- Python 3.x
- Tkinter (standard with Python on most OS)
- `pyperclip` (optional, for "Copy to Clipboard" functionality)

## 📥 Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-link>
    cd <repo-name>
    ```

2.  **Install dependencies (Optional)**:
    ```bash
    pip install pyperclip
    ```

## 🖥 How to Run

Run the main application using Python:
```bash
python main.py
```

## 🧪 Running Tests

Ensure all logic is working correctly by running the built-in tests:
```bash
python test_logic.py
```

## 📚 Scenarios and PPT

Find the project presentation content and screenshots in the `docs/` and `screenshots/` folders respectively, detailing the various scenarios from basic encryption to advanced hybrid prevention.
