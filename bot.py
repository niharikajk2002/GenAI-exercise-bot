import discord
from discord import app_commands
import os
import requests
import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_URL = os.getenv("SERVER_URL")  # Should be your LLM server URL
SERVER_API_KEY = os.getenv("SERVER_API_KEY")  # Optional

# Global headers
HEADERS = {
    "Content-Type": "application/json"
}

if SERVER_API_KEY:
    HEADERS["Authorization"] = f"Bearer {SERVER_API_KEY}"

def build_payload(user_message: str):
    now = datetime.datetime.now()

    payload = {
        "stream": True,
        "model": "gemini-2.0-flash",
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "params": {},
        "background_tasks": {
            "title_generation": True,
            "tags_generation": True
        },
        "features": {
            "image_generation": False,
            "code_interpreter": False,
            "web_search": False
        },
        "chat_id": "d130f879-142a-466b-80cb-230a6a6d9a59",
        "session_id": "bAzQAXXG_04e5ljPAAS2",
        "variables": {
            "{{USER_NAME}}": "niharika janardhan konduru",
            "{{USER_LOCATION}}": "Unknown",
            "{{USER_LANGUAGE}}": "en-US",
            "{{CURRENT_DATE}}": now.strftime("%Y-%m-%d"),
            "{{CURRENT_TIME}}": now.strftime("%H:%M:%S"),
            "{{CURRENT_DATETIME}}": now.strftime("%Y-%m-%d %H:%M:%S"),
            "{{CURRENT_TIMEZONE}}": "America/New_York",
            "{{CURRENT_WEEKDAY}}": now.strftime("%A")
        },
        "tags": [],
        "actions": [],
        "tool_servers": []
    }
    return payload

class WorkoutClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        try:
            await self.tree.sync()
            print('Slash Commands Synced')
        except Exception as e:
            print(f'Failed to sync slash commands: {e}')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        user_message = message.content.strip()

        async with message.channel.typing():
            bot_reply = await self.ask_llm(user_message)

        await message.channel.send(bot_reply)

    async def ask_llm(self, user_message):
        payload = build_payload(user_message)

        try:
            response = requests.post(
                f"{SERVER_URL}/api/chat/completions",
                headers=HEADERS,
                json=payload,
                stream=True
            )
            response.raise_for_status()

            full_reply = ""

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        data_part = decoded_line[6:]
                        if data_part.strip() == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_part)
                            delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
                            if delta:
                                full_reply += delta
                        except Exception as e:
                            print(f"Error parsing chunk: {e}")
                            continue

            if full_reply.strip() == "":
                full_reply = "No response received."

            bot_reply = full_reply

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error contacting workout server: {e} - Response: {e.response.text}")
            bot_reply = f"Server error: {e.response.status_code}"
        except Exception as e:
            print(f"Error contacting workout server: {e}")
            bot_reply = "Sorry, I couldn't get a response from the workout server."

        return bot_reply

# Create client instance
client = WorkoutClient()

# Slash Command: /workout
@client.tree.command(name="workout", description="Get workout plans and fitness advice")
async def workout(interaction: discord.Interaction, question: str):
    await interaction.response.defer()

    bot_reply = await client.ask_llm(question)

    await interaction.followup.send(bot_reply)

# Run the bot
client.run(DISCORD_TOKEN)
