<p align="center">
  <img src="https://raw.githubusercontent.com/givenglorious/tiktok_auto_dm/master/assets/banner.png" alt="streak-bot" width="100%" />
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ea44f" alt="License: MIT"></a>
  <a href="https://github.com/givenglorious/tiktok_auto_dm/releases"><img src="https://img.shields.io/github/v/release/givenglorious/tiktok_auto_dm?label=version&color=1f6feb" alt="Version"></a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/selenium-4.18-green" alt="Selenium">
</p>

# streak-bot

> **Delete TikTok. Keep your streaks.**
>
> Tired of doomscrolling on TikTok but scared to delete it because your streaks with friends will break? This tool automatically sends a DM to all your friends every time you run it — so you can finally delete the app without losing your streaks.

---

## What it does

- **Cookie-based login** — no email/password stored, no bot detection
- **Sends DMs automatically** to a list of TikTok usernames
- **Skips unavailable accounts** — accounts that can't be DM'd are logged and skipped
- **Activity log** saved to `tiktok_dm.log` after every run
- **Screenshot on error** — saves a `.png` when something goes wrong for easy debugging

---

## How it works

```
Load cookies.json → Open TikTok → Click Message → Type & send → Next account
```

No email. No password. No bot detection. Just cookies.

---

## Requirements

- Python 3.9+
- Google Chrome (latest)
- ChromeDriver matching your Chrome version

---

## Installation

**1. Clone the repository:**
```bash
git clone https://github.com/givenglorious/tiktok_auto_dm.git
cd tiktok_auto_dm
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Export your TikTok cookies:**

Install the [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) extension in Chrome, log in to TikTok, then:
- Open `tiktok.com`
- Click the Cookie-Editor icon
- Click **Export → Export as JSON**
- Save the file as `cookies.json` in the project folder

---

## Configuration

Open `tiktok_dm.py` and edit the `CONFIG` block:

```python
CONFIG = {
    "cookies_file":           "cookies.json",  # Cookies file from Cookie-Editor
    "message":                "STREAK!!!",     # Message to send
    "target_usernames":       ["friend1", "friend2"],  # TikTok usernames (without @)
    "headless":               False,           # False = visible | True = background
    "delay_between_messages": 10,              # Seconds between each message
}
```

---

## Usage

```bash
python tiktok_dm.py
```

The bot will open Chrome, load your TikTok session via cookies, and send the message to every username in the list one by one.

---

## Project Structure

```
tiktok_auto_dm/
├── tiktok_dm.py        ← Main script
├── cookies.json        ← Your TikTok session (export from Cookie-Editor)
├── requirements.txt    ← Python dependencies
├── tiktok_dm.log       ← Activity log (auto-generated)
└── README.md
```

---

## FAQ

**Do I need to export cookies every time?**
No. Cookies are valid for several weeks. Re-export only when the bot says "Cookies expired."

**What if an account can't be DM'd?**
It gets logged as `SKIP` and the bot moves on to the next one. Usually means you're not following each other.

**Can I run this on a server?**
Set `"headless": True` in CONFIG. Note: TikTok may block headless Chrome — cookie login helps bypass this.

**Is this against TikTok's ToS?**
Automation may violate TikTok's Terms of Service. Use at your own risk and keep usage reasonable.

---

## License

MIT: [LICENSE](LICENSE)

---

<p align="center"><em>"You don't need TikTok open to keep your streaks alive."</em></p>
