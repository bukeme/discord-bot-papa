import os
import discord
from google import genai
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
genai.Client(api_key=GEMINI_API_KEY)

client = discord.Client(intents=discord.Intents.default(), intents__message_content=True)

# Load your FAQ as context
FAQ_CONTEXT = """
Forex Funds Flow FAQ:
1. What is Forex Funds Flow? -> Forex Funds Flow is a proprietary trading firm...
2. How do payouts work? -> Payouts are processed within X days...
3. What are the account sizes? -> We offer $10k, $25k, $50k accounts...
...
"""

async def ask_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    resp = model.generate_content(FAQ_CONTEXT + "\nUser: " + prompt)
    return resp.text

@client.event
async def on_ready():
    print(f"Discord bot ready as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!faq"):
        user_q = message.content[len("!faq "):]
        answer = await ask_gemini(user_q)
        await message.channel.send(answer)

client.run(DISCORD_TOKEN)
