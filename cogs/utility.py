import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
import vt
import json
import asyncio
import hashlib
import validators
import requests
import base64

with open("config.json") as f:
	config = json.load(f)

vt_client = vt.Client(config["VIRUSTOTAL_API_KEY"])


class DecodeButton(discord.ui.View):
	def __init__(self, msg: str):
		super().__init__(timeout=None)
		self.msg = msg
		
	@discord.ui.button(label="Decode", style=discord.ButtonStyle.blurple)
	async def decode_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		bytes = base64.b64decode(self.msg)
		msg = bytes.decode("utf-8")
		
		await interaction.response.send_message(msg, ephemeral=True)

class Utility(commands.Cog):  # For utility commands...
	def __init__(self, bot):
		self.bot = bot

	# ---- PREFIX COMMANDS ----
	@commands.command(name="ping", help="Answer with Pong!")
	async def ping(self, ctx):  # Ping command just for convenience :)
		await ctx.send("PONG!")

	# ---- SLASH COMMANDS ----
	# Guide for new members :p
	@app_commands.command(name="getting-started", description="A guide for The Pirate Way!")
	async def getting_started(self, interaction: discord.Interaction):
		embed = discord.Embed(
			title="🏴‍☠️ The Pirate Way 🏴‍☠️",
			description="The Pirate Way is the ultimate hub for piracy in discord, where you can easily share, request, and even publish, **free content**."
		)

		embed.add_field( # BOT
			name="🤖 The Pirate Way Bot",
			value="Our bot is a **full featured bot** made specifically for piracy, with an entire megathread included in commands like `/games` and `/media`. Be sure to also take a look on our **manifest generator** with `/manifest-gen`!",
			inline=False
		)
		embed.add_field( # Requesting
			name="🔗 Requesting",
			value="While requesting a content, make sure to be clear, fast, and follow [nohello.net](https://nohello.net)!",
			inline=False
		)
		embed.add_field( # Helpers
			name="👷 Helpers",
			value="If your request is taking long, don't be shy to ping <@&1370069224881524797> to get a faster reply. Want to get the role? Reach level 5+ and click [here](https://discord.com/channels/1277379249573068944/1370068528920530955)!",
			inline=False
		)
		embed.add_field(
			name="That's it!",
			value="You are now ready to interact with our community, make sure to follow the rules.",
			inline=False
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1277379249573068944/d706e8069e52db12018425a7b0061868.png?size=2048")
		embed.set_footer(text="Want to contribuate with the community? check /donate!")

		await interaction.response.send_message(embed=embed)

	# Command for checking viruses :D
	@app_commands.command(name="scan-file", description="Verify for viruses in a file.")
	@app_commands.describe(
		file="Send a file to start a virus verification."
	)
	@app_commands.choices( # Idk if i'm gonna add other tools such as virustotal later, but lets put it here
		tool=[
			app_commands.Choice(name="Virus Total (max 650mb)", value="virustotal"),
		]
	)
	async def scan_file(self, interaction: discord.Interaction, file: discord.Attachment, tool: app_commands.Choice[str]):
		await interaction.response.send_message("Checking files...", ephemeral=False)
		if tool.value == "virustotal":
			await interaction.edit_original_response(content=f"Downloading {file.filename}...")

			# Downloading the package for virus verification later :P
			package = file.url
			destiny_folder = "file"
			os.makedirs(destiny_folder, exist_ok=True)

			file_path = os.path.join(destiny_folder, file.filename)
			try:
				async with aiohttp.ClientSession() as session:
					async with session.get(package) as response:
						response.raise_for_status() # Checking errors
						content = await response.read()
						with open(file_path, "wb") as f:
							f.write(content)
				await interaction.edit_original_response(content=f"File: {file.filename} successfully downloaded!\nChecking for viruses...")
			except Exception as e:
				await interaction.followup.send("Error while downloading package, check terminal.")
				print(e)
				return

			# Checking if package is not so big
			if os.path.getsize(file_path) > 649 * 1024 * 1024:
				await interaction.followup.send("Error: package is way too big. Limit is 650mb")
				return

			# Scannning for viruses :D
			upload_url = await asyncio.wait_for(vt_client.get_data_async("/files/upload_url"), timeout=30)

			async with aiohttp.ClientSession() as session:
				with open(file_path, "rb") as f:
					data = aiohttp.FormData()
					data.add_field("file", f, filename=file_path)

					headers = {
						"x-apikey": config["VIRUSTOTAL_API_KEY"]
					}

					async with session.post(upload_url, data=data, headers=headers) as resp:
						analysis = await resp.json()
						analysis_id = analysis["data"]["id"]

			while True:  # Checking if it's completed or not :(
				analysis = await vt_client.get_object_async(f"/analyses/{analysis_id}")
				await interaction.edit_original_response(content=f"Analysis Status: {analysis.status}")
				if analysis.status == "completed":
					break
				await asyncio.sleep(5)

			# -- When scanning is complete :) --
			file_id = self.calculate_sha256(file_path)
			file_link = f"https://www.virustotal.com/gui/file/{file_id}"
			file_report = await vt_client.get_object_async(f"/files/{file_id}")

			stats = file_report.last_analysis_stats # harmless, suspicious or malicious :P
			names = file_report.names # Possible package alt names
			scan_results = file_report.last_analysis_results # Antiviruses and their status about the file

			stats_summary = f"✅ Harmless: {stats.get('undetected', 0)}\n"
			stats_summary += f"⚠️ Suspicious: {stats.get('suspicious', 0)}\n"
			stats_summary += f"❌ Malicious: {stats.get('malicious', 0)}\n"

			# Reducing Scan Results to not excede 1024 char length haha :D
			scan_summary = ""
			count = 0
			for engine, result in scan_results.items():
				if count >= 5:
					break
				category = result.get("category", "unknown")
				scan_summary += f"🔹 {engine}: {category}\n"
				count += 1

			# Creating and sending embed :p
			embed = discord.Embed(title=f"🛡️ Scan complete for **{file.filename}**", description="Check the results above.", url=file_link)
			embed.add_field(name="Stats", value=stats_summary, inline=False) # STATS
			embed.add_field(name="Possible names", value="\n".join(names[:5]), inline=False) # POSSIBLE NAMES
			embed.add_field(name="Scan Results (top 5)", value=scan_summary, inline=False) # SCAN RESULTS
			embed.set_footer(text="Virustotal scan")

			os.remove(file_path)
			await interaction.edit_original_response(content="✅ Scan complete", embed=embed)
		else:
			await interaction.edit_original_response(content="Sorry, we don't have this tool yet.")
		
	# Scan websites
	@app_commands.command(name="scan-url", description="Check for viruses in an url.")
	@app_commands.describe(
		url="URL to be scanned."
	)
	async def scan_url(self, interaction: discord.Interaction, url: str):
		await interaction.response.send_message("Checking url...")

		# Checking if url is valid :D
		if not validators.url(url):
			await interaction.edit_original_response(content="Invalid url!\nMake sure to add `https://` at the beggining.")

		# Preventing silly errors with hash
		if url.count("/") < 3:
			url = f"{url}/"

		# Starting analysis
		analysis = await vt_client.scan_url_async(url) # Analysing
		url_id = hashlib.sha256(url.encode()) # Getting ID
		url_id = url_id.hexdigest() # Turning it readable haha

		while True:  # Checking if it's completed or not :(
				analysis = await vt_client.get_object_async(f"/analyses/{analysis.id}")
				await interaction.edit_original_response(content=f"Analysis Status: {analysis.status}")
				if analysis.status == "completed":
					break
				await asyncio.sleep(3)

		# Getting scan results :p
		url_link = f"https://www.virustotal.com/gui/url/{url_id}"
		url_report = await vt_client.get_object_async(f"/urls/{url_id}")

		stats = url_report.last_analysis_stats # harmless, suspicious or malicious :P
		scan_results = url_report.last_analysis_results # Antiviruses and their status about the url
		whois_data = url_report.get("attributes", {}).get("whois")

		stats_summary = f"✅ Harmless: {stats.get('harmless', 0)}\n"
		stats_summary += f"⚠️ Suspicious: {stats.get('suspicious', 0)}\n"
		stats_summary += f"❌ Malicious: {stats.get('malicious', 0)}\n"

		# Reducing Scan Results to not excede 1024 char length haha :D
		scan_summary = ""
		count = 0
		for engine, result in scan_results.items():
			if count >= 5:
				break
			category = result.get("category", "unknown")
			scan_summary += f"🔹 {engine}: {category}\n"
			count += 1

		# Creating and sending embed :p
		embed = discord.Embed(title=f"🛡️ Scan complete for **{url}**", description="Check the results above.", url=url_link)
		embed.add_field(name="Stats", value=stats_summary, inline=False) # STATS
		embed.add_field(name="Whois", value=whois_data, inline=False)
		embed.add_field(name="Scan Results (top 5)", value=scan_summary, inline=False) # SCAN RESULTS
		embed.set_footer(text="Virustotal scan")

		await interaction.edit_original_response(content="✅ Scan complete", embed=embed)

	# Donation haha
	@app_commands.command(name="donate", description="Donate to our server!")
	async def donate(self, interaction: discord.Interaction):
		crypto_options = [
			"**Bitcoin (mainnet):** `bc1q0ctn0cq49yk8cq3m3cna8dmq4w5a77dac06la4`",
			"**Ethereum (ERC-20):** `0x3Dee33b53f0812A9710edfd365C80d02dBdD16e7`",
			"**BNB (BEP-20):** `0x3Dee33b53f0812A9710edfd365C80d02dBdD16e7`"
		]

		embed = discord.Embed(title="Donate", description="Thanks for your wish to help our community!\nCheck above the payment options available.")
		embed.add_field(name="Crypto", value="\n".join(crypto_options), inline=False)
		embed.add_field(name="Pix", value="In order to make a PIX (Brazil), create a ticket.", inline=False)
		embed.set_footer(text="After donating, create a ticket to claim @Donator role!")

		await interaction.response.send_message(embed=embed)
		
	@app_commands.command(name="encode", description="Encodes texts into base64")
	async def encode(self, interaction: discord.Interaction, input_string: str):
		bytes = input_string.encode("utf-8")
		base64_text = base64.b64encode(bytes).decode("utf-8")
		
		view = DecodeButton(base64_text)
		
		await interaction.response.send_message(f"`{base64_text}`", view=view)
		
	@app_commands.command(name="decode", description="Decodes base64 texts")
	async def decode(self, interaction: discord.Interaction, input_string: str):
		bytes = base64.b64decode(input_string)
		msg = bytes.decode("utf-8")
		
		await interaction.response.send_message(msg, ephemeral=True)

	# ---- FUNCTIONS ----
	def calculate_sha256(self, file_path):
		sha256_hash = hashlib.sha256()
		with open(file_path, "rb") as f:
			for byte_block in iter(lambda: f.read(4096), b""):
				sha256_hash.update(byte_block)
		return sha256_hash.hexdigest()

async def setup(bot):
	await bot.add_cog(Utility(bot)) 
