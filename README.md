# 🏋️‍♀️ Workout Discord Bot

A Discord bot that interacts with an external LLM (Large Language Model) server to generate **workout plans**, **fitness advice**, and more using both message-based and slash command interactions.

---

## 📜 Features
- Responds to normal text messages with intelligent fitness advice.
- Supports `/workout` slash command for structured queries.
- Streams replies in real-time from your custom LLM server.
- Environment-based configuration for easy setup.
- Handles server errors gracefully.

---

## 📂 Project Structure
```
├── bot.py                # Main bot source code
├── config/.env            # Environment variables file (add your tokens and server URLs here)
├── README.md              # Documentation (this file)
├── requirements.txt       # Python dependencies (you need to create this)
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/discord-workout-bot.git
cd discord-workout-bot
```

### 2. Install Dependencies
You need Python 3.8 or higher.

Install the required packages:
```bash
pip install -r requirements.txt
```

**Sample `requirements.txt`** you should create:
```
discord.py
python-dotenv
requests
```

---

### 3. Create a `.env` File
Inside the `config/` folder, create a file named `.env` with the following contents:
```env
DISCORD_TOKEN=your-discord-bot-token-here
SERVER_URL=https://your-llm-server.com
SERVER_API_KEY=your-server-api-key (optional)
```

> **Tip:** Keep your `.env` file private and never share it publicly.

---

### 4. Run the Bot
```bash
python bot.py
```

If successful, you should see:
```
Logged in as <YourBotName>
Slash Commands Synced
```

---

## 🛠 How It Works

- When a **user sends a message**, the bot:
  1. Builds a request payload with user details.
  2. Sends it to the LLM server's `/api/chat/completions` endpoint.
  3. Streams and parses the response back in real time.
  4. Replies in the same channel.

- The **slash command** `/workout` works similarly but is triggered by a formal Discord interaction.

---

## 🧪 Example Usage

**In Chat:**
> User: *"Suggest me a full body workout for beginners."*  
> Bot: *"Here's a beginner-friendly full body workout plan: 1. Squats (3x15), 2. Pushups (3x10)... "*

**Slash Command:**
```bash
/workout question:"Give me a 5-day gym workout split."
```
> Bot: *"Sure! Here's a 5-day split: Day 1 - Chest & Triceps, Day 2 - Back & Biceps, ..."*

---

## ⚠️ Important Notes

- Make sure your LLM server supports **streaming responses**.
- Slash commands can sometimes take a few minutes to sync after you first deploy your bot.
- This bot is set to only process messages **not authored by itself** (`if message.author == self.user: return`).

---

## 🚀 Future Improvements
- Add buttons and embeds for better message formatting.
- Implement a `/dietplan` command.
- Add session management for continuous conversations.
- Caching common responses for faster retrieval.

---

## 🧑‍💻 Author
**Niharika Janardhan Konduru**  



