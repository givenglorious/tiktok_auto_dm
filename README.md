# TikTok Auto DM 🤖

> **Delete TikTok. Keep your streaks.**

Are you stuck in a doomscrolling loop on TikTok but too afraid to delete the app because your streaks with friends will break? This tool is the solution. Just run this program once a day — it automatically sends a message to all your friends so your streaks stay alive, without you ever opening TikTok.

---

## Features

- Auto login using TikTok email & password
- Gmail format validation on email input
- Send the same message to multiple usernames at once
- Activity log saved to `tiktok_dm.log`
- Auto screenshot on error for easy debugging

---

## Project Structure

```
tiktok_auto_streak/
├── main.py
├── tiktok_dm.py
├── requirements.txt
└── README.md
```

---

## Installation

1. Clone this repository:
```bash
git clone https://github.com/username/tiktok-auto-dm.git
cd tiktok-auto-dm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure **Google Chrome** is installed on your computer.

---

## Usage

Run the program:
```bash
python main.py
```

Follow the prompts in the terminal:
```
Enter your TikTok email  : emailkamu@gmail.com
Enter your password      : ********
Enter your message       : Streak!
Enter target username    : friend1
Add another account? (y/n): y
Enter target username    : friend2
Add another account? (y/n): n
```

The program will automatically open Chrome, log in to TikTok, and send the message to all listed usernames.

---

## Requirements

- Python 3.9+
- Google Chrome
- See `requirements.txt` for Python packages

---

## Disclaimer

This tool is intended for personal use only. Use responsibly and in accordance with TikTok's Terms of Service.
