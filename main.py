import discord
import asyncio
import requests
from discord.ext import commands
import json, os

os.system("clear") # Clean view :)

with open("config.json") as f: # Loading configs.json
	config = json.load(f)

if config["TOKEN"] == "None": # Remembering user to update json
	print("Update config.json!!!")
	quit()


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	print(f"🤖 Logged in as {bot.user} (ID: {bot.user.id})")
	try:
		synced = await bot.tree.sync()
		print(f"🚀 Synced {len(synced)} slash command(s).")
	except Exception as e:
		print("Error with commands sync!")
		print(e)
	print("-----")


async def main():
	for filename in os.listdir("./cogs"): # LOADING COGS
		if filename.endswith(".py"):
			await bot.load_extension(f"cogs.{filename[:-3]}")
	await bot.start(config["TOKEN"])

asyncio.run(main())