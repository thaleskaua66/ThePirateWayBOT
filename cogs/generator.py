import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import json

with open("config.json") as f:
	config = json.load(f)

class Generator(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Manifest generator
	@app_commands.command(name="manifest-gen", description="Generate a steam manifest")
	@app_commands.describe(
		app_id="Your game's ID. you can get it from SteamDB."
	)
	async def gen_manifest(self, interaction: discord.Interaction, app_id: str):
		await interaction.response.defer()
		
		# Common servers
		download_mirrors = [
			f"[The Pirate Way](https://pmpvwcnnplthvtdeypin.supabase.co/storage/v1/object/public/manifests/zip/{app_id}.zip)",
			f"[Fares](https://steamdatabase.s3.eu-north-1.amazonaws.com/{app_id}.zip)",
			f"[Cysaw](https://cysaw.org/)"
		]
		steam_key = config["STEAM_WEB_API_KEY"] # Useless for now lol :)

		# Getting info about the game
		url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=us&l=en"

		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				if response.status != 200:
					await interaction.followup.send("Unable to connect to steam servers, did you insert letters?")
					return
				data = await response.json()

		app_data = data.get(str(app_id), {})
		if not app_data.get("success"):
			await interaction.followup.send("Game not found.")
			return

		game = app_data["data"]
		title = game["name"]
		description = game.get("short_description", "No description available.")
		image = game.get("header_image", "")

		# Mounting embed :)
		embed = discord.Embed(title=f"{title} ({app_id})", description=f"{description}\n\nTutorial by <@566778920272265246>", color=discord.Color.green())
		embed.set_image(url=image)
		embed.add_field(name="🎮 Download Mirrors", value="\n".join(download_mirrors))
		embed.add_field(name="📦 Resources", value="[Steamtools](https://steamtools.net/)\n[Tutorial](https://www.youtube.com/watch?v=_xSjI86JM2Q)")
		embed.set_footer(text="If none of the mirrors are working, make a request.")

		await interaction.followup.send(embed=embed)

	# App id searcher and more info
	@app_commands.command(name="steam", description="Search for a game and his APP_ID.")
	@app_commands.describe(
		game="Game you are searching for."
	)
	async def steam(self, interaction: discord.Interaction, game: str):
		await interaction.response.defer()

		# Search for app id
		async with aiohttp.ClientSession() as session:
			search_url = f"https://store.steampowered.com/api/storesearch/?term={game}&cc=us&l=en"
			async with session.get(search_url) as resp:
				data = await resp.json()

			if not data.get("items"):
				await interaction.followup.send("No games found with this name.")
				return

			game = data["items"][0]
			appid = data["items"][0]["id"]

			# Get game info with app id
			details_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
			async with session.get(details_url) as resp:
				details = await resp.json()

		info = details.get(str(appid), {}).get("data")
		if not info:
			await interaction.followup.send("It wasn't possible to fetch game data.")
			return

		price = info.get("price_overview", {}).get("final_formatted", "Free or unavailable.")
		genres = ", ".join([g["description"] for g in info.get("genres", [])])
		reviews = info.get("recommendations", {}).get("total", "No data.")
		link = f"https://store.steampowered.com/app/{appid}"
		title = info["name"]
		description = info.get("short_description", "No description available.")
		image = info.get("header_image", "")

		# Mounting embed with all the info
		embed = discord.Embed(title=title, description=description, color=discord.Color.blue(), url=link)
		embed.add_field(name="🆔 App ID", value=str(appid), inline=True)
		embed.add_field(name="💵 Price", value=price, inline=True)
		embed.add_field(name="🏷️ Genres", value=genres, inline=False)
		embed.add_field(name="📊 Reviews", value=str(reviews), inline=True)
		embed.set_image(url=image)

		await interaction.followup.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Generator(bot))