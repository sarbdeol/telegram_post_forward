# 📤 Telegram Auto-Forwarder Bot (Telethon)

This Python bot uses **Telethon** to **monitor multiple source Telegram groups/channels** and **automatically forward all new messages** (text, media, and albums) to a **destination channel or group**.

---

## 🚀 Features

- 📥 Monitors multiple source chats (groups/channels)
- 📤 Forwards text, media (photos/videos), and albums
- 🧠 Handles Telegram albums (media groups) correctly
- 🧹 Automatically cleans up temporary files
- 🔐 Secure local session storage

---

## 🧰 Requirements

- Python 3.7+
- [Telethon](https://docs.telethon.dev)

Install dependencies:

```bash
pip install telethon




⚙️ Configuration
Go to my.telegram.org and create:

API ID

API Hash

Replace the placeholders in the script:

python
Copy
Edit
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
Set your source and destination chat IDs:

python
Copy
Edit
source_chats = [
    -1001543796382,
    -1001870005959,
    # ...add more chat IDs here
]

destination_chat = -1002646228196  # Channel or group where messages will be forwarded



📄 License
This project is for educational and personal automation use. Use responsibly.
