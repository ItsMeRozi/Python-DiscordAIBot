"""
Discord bot powered by AI that provides the same answers as Chat-GPT.
Latest update: 12.11.2023
A Discord-based program for delivering Chat-GPT answers on a Discord channel.
"""

# Import necessary modules
import importlib
import subprocess
import time
import sys

#Install necessary modules
required_modules = ['discord', 'openai']

missing_modules = []

for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    for module in missing_modules:
        try:
            subprocess.check_call([f"pip install {module}"])
        except subprocess.CalledProcessError as e:
            print(f'Start failed. Program will break in 5s')
            time.sleep(5)
            sys.exit()

# Import necessary modules
import openai
import discord
from discord.ext import commands

# Set your OpenAI API key and Discord bot token
openai.api_key = ''
TOKEN = ''

# Initialize Discord bot with command prefix '.' and all intents enabled
client = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Dictionary to store user chat history
user_history = {}

# Main asynchronous function to handle user messages and interact with Chat-GPT
async def main(ctx, message):
    user_id = str(ctx.author.id)
    
    # If user ID not in history, initialize an empty list
    if user_id not in user_history:
        user_history[user_id] = []

    # Append user's message to their chat history
    user_history[user_id].append({'role': 'user', 'content': message})

    # Get the user's message history
    user_messages = user_history[user_id]

    # Get response from Chat-GPT and send it to the Discord channel
    response = await chat_with_gpt(user_messages)
    await ctx.send(response)

# Asynchronous function to interact with Chat-GPT using OpenAI API
async def chat_with_gpt(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    return response.choices[0].message.content.strip()

# Event handler when the bot is ready
@client.event
async def on_ready():
    print("Bot on")

# Discord command to use the AI chat function
@client.command()
async def ai(ctx, *, message):
    await main(ctx, message)

# Discord command to clear user's chat history
@client.command()
async def clear(ctx):
    user_id = str(ctx.author.id)
    
    # If user ID in history, clear their chat history
    if user_id in user_history:
        user_history[user_id] = []
        await ctx.send("Cleared chat history.")
    else:
        await ctx.send("No chat history to clear.")

# Run the Discord bot with the specified token
client.run(TOKEN)