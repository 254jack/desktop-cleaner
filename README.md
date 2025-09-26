# 🧹 Desktop Cleaner

A simple Python automation script that cleans up your **Desktop, Downloads, Documents, Pictures, Music, and Videos** folders by moving files to their correct locations.  
It also removes **empty folders** and ensures your files are neatly organized.

---

## 🚀 Features
- Automatically moves files to correct folders (Pictures, Documents, Music, Videos, etc.)
- Works recursively inside subdirectories.
- Deletes empty folders (except system folders).
- Prevents duplicates (skips if file already exists in destination).
- Configurable rules for file extensions.

---

## 📂 Example
Before:
~/Desktop/
├── song.mp3
├── report.pdf
├── image.png
└── random.zip

arduino
Copy code

After running the cleaner:
~/Music/song.mp3
~/Documents/report.pdf
~/Pictures/image.png
~/Archives/random.zip

yaml
Copy code

---

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/254jack/desktop-cleaner.git
   cd desktop-cleaner
Make sure you have Python 3 installed:

bash
Copy code
python3 --version
(Optional) Create a virtual environment:

bash
Copy code
python3 -m venv env
source env/bin/activate   # Linux/Mac
env\Scripts\activate      # Windows
Install dependencies (currently none, but ready for future updates):

bash
Copy code
pip install -r requirements.txt
▶️ Usage
Run the cleaner:

bash
Copy code
python cleaner.py
It will automatically scan your configured folders and organize files.

⚙️ Configuration
You can modify the file extensions and target folders in cleaner.py:

python
Copy code
folders = {
    "Pictures": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".pub"],
    "Music": [".mp3", ".wav", ".rg", ".md", ".m4a"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".xz", ".deb"],
    "Scripts": [".py", ".sh", ".bat"],
    "Others": []
}
🖥️ Supported OS
✅ Linux (tested on Ubuntu)

✅ Windows
(Mac should also work with minor adjustments)

📜 License
This project is licensed under the MIT License.

🤝 Contributing
Pull requests are welcome! If you’d like to improve the script or add more features, please fork the repo and submit a PR.

👨‍💻 Author
Jackson Kimani Njoroge
💼 Software Engineer | Cybersecurity Specialist
🌍 taixonj@gmail.com


---
