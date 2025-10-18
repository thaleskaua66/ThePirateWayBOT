import discord, base64
from discord.ext import commands
from discord import app_commands


class Resources(commands.Cog): # For resources commands, such as /games
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name="games", description="Reputable games websites.")
	async def games(self, interaction: discord.Interaction):
		embed = discord.Embed(title="👾 Games Resources", description="Best sites to download free games!")

		# Setting all the links, u can change anything u want from here
		ddl_links = [
			"⭐ SteamRip - `aHR0cHM6Ly9zdGVhbXJpcC5jb20v`",
			"⭐ GOG Games - `aHR0cHM6Ly9nb2ctZ2FtZXMudG8v`",
			"⭐:penguin: JohnCena141 - `aHR0cHM6Ly8xMzM3eC50by91c2VyL2pvaG5jZW5hMTQxLw==`"
			"AnkerGames - `aHR0cHM6Ly9hbmtlcmdhbWVzLm5ldC8=`",
			"Ovagames - `aHR0cHM6Ly93d3cub3ZhZ2FtZXMuY29tLw==`",
			"GameBounty - `aHR0cHM6Ly9nYW1lYm91bnR5LndvcmxkLw==`",
			"Steam Underground - `aHR0cHM6Ly9zdGVhbXVuZGVyZ3JvdW5kLm5ldC8=`",
			"CS.RIN.RU `aHR0cHM6Ly9jcy5yaW4ucnUvZm9ydW0=`",
			"Games4U - `aHR0cHM6Ly9nYW1lczR1Lm9yZy8=`",
			"SteamGG - `aHR0cHM6Ly9zdGVhbWdnLm5ldC8=`"
		]
		repack_links = [
			"⭐ FitGirl Repacks - `aHR0cHM6Ly9maXRnaXJsLXJlcGFja3Muc2l0ZS8=`",
			"⭐ DODI Repacks - `aHR0cHM6Ly9kb2RpLXJlcGFja3Muc2l0ZS8=`",
			"Kaos Krew - `aHR0cHM6Ly93d3cua2Fvc2tyZXcub3JnLw==`",
			"Tiny Repacks - `aHR0cHM6Ly93d3cudGlueS1yZXBhY2tzLndpbi8=`"
		]
		vr_links = [
			"VR Pirates Wiki - `aHR0cHM6Ly92cnBpcmF0ZXMud2lraS8=`",
			"ARMGDDN Browser - `aHR0cHM6Ly9jcy5yaW4ucnUvZm9ydW0vdmlld3RvcGljLnBocD9mPTE0JnQ9MTQwNTkz`",
			"r/QuestPiracy - `aHR0cHM6Ly93d3cucmVkZGl0LmNvbS9yL1F1ZXN0UGlyYWN5Lw==`"
		]
		tools_links = [
			"⭐ Online-Fix - `aHR0cHM6Ly9vbmxpbmUtZml4Lm1lLw==`",
			"IRC Games - `aHR0cHM6Ly9yZWRkLml0L3g4MDR3Zw==`",
			"ARMGDDN Browser - `aHR0cHM6Ly9naXRodWIuY29tL0thbGFkaW5ETVAvQUdCcm93c2Vy`"
		]

		# Mounting the embed
		embed.add_field(name="🔗 DDL", value="\n".join(ddl_links), inline=False)
		embed.add_field(name="📦 Repacks", value="\n".join(repack_links), inline=False)
		embed.add_field(name="👓 Virtual Reality", value="\n".join(vr_links), inline=False)
		embed.add_field(name="➕ Patches/Fixes/Tools", value="\n".join(tools_links), inline=False)
		embed.set_footer(text="Also try /search-games!")

		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="media", description="Free media websites.")
	async def media(self, interaction: discord.Interaction):
		embed = discord.Embed(title="🎬 Media Resources", description="Free media websites.")

		# Links. Change it as your need.
		streaming_links = [
			"⭐ PStream - `aHR0cHM6Ly9wc3RyZWFtLm9yZy8=`",
			"⭐ FlickyStream - `aHR0cHM6Ly9mbGlja3lzdHJlYW0uY29tLw==`",
			"CineBy - `aHR0cHM6Ly93d3cuY2luZWJ5LmFwcC8=`",
			"Hexa Watch - `aHR0cHM6Ly9oZXhhLndhdGNoLw==`",
			"RiveStream - `aHR0cHM6Ly9yaXZlc3RyZWFtLm9yZy8=`",
			"123MoviesFree - `aHR0cHM6Ly8xMjNtb3ZpZXNmcmVlLmF0Lw==`"
		]
		anime_links = [
			"⭐ AnimeKai - `aHR0cHM6Ly9hbmltZWthaS50by8=`",
			"MiruRo - `aHR0cHM6Ly93d3cubWlydXJvLmNvbS8=`",
			"HiAnimeZ - `aHR0cHM6Ly9oaWFuaW1lei50by8=`",
			"KAA - `aHR0cHM6Ly9rYWEubXgv`"
		]
		cartoon_links = [
			"WCO - `aHR0cHM6Ly93d3cud2NvLnR2Lw==`",
			"KimCartoon - `aHR0cHM6Ly9raW1jYXJ0b29uLnNpLw==`",
			"HiCartoon - `aHR0cHM6Ly9oaWNhcnRvb24udG8v`"
		]
		livetv_links = [
			"TheTVApp - `aHR0cHM6Ly90dnBhc3Mub3JnLw==`",
			"TV Garden - `aHR0cHM6Ly90di5nYXJkZW4v`",
			"DaddyLive - `aHR0cHM6Ly9kYWRkeWxpdmUubXAv`",
			"RGShows LiveTV - `aHR0cHM6Ly93d3cucmdzaG93cy5tZS9saXZldHYv`",
			"FSTV - `aHR0cHM6Ly9mc3R2LnVzLw==`",
			"Streamed.su - `aHR0cHM6Ly9zdHJlYW1lZC5zdS8=`"
		]

		# Mounting embed :p
		embed.add_field(name="📺 Streaming", value="\n".join(streaming_links), inline=False)
		embed.add_field(name="🍜 Anime", value="\n".join(anime_links), inline=False)
		embed.add_field(name="🐦 Cartoon", value="\n".join(cartoon_links), inline=False)
		embed.add_field(name="⚽ Live TV (sports, etc.)", value="\n".join(livetv_links), inline=False)

		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="books", description="Books resources.")
	async def books(self, interaction: discord.Interaction):
		embed = discord.Embed(
			title="📚 Books Resources",
			description="Sites to download and access e-books, audiobooks and educational books.",
		)

		# Links
		e_books = [
			"⭐ Anna's Archive - `aHR0cHM6Ly9hbm5hcy1hcmNoaXZlLm9yZy8=`",
			"⭐ Library Genesis - `aHR0cHM6Ly9saWJnZW4ucnMv`",
			"Z-Library - `aHR0cHM6Ly96LWxpYi5nZC8=`",
			"Bookracy - `aHR0cHM6Ly9ib29rcmFjeS5ydS8=`",
			"Mobilism Forum - `aHR0cHM6Ly9mb3J1bS5tb2JpbGlzbS5vcmcv`",
			"MyAnonamouse - `aHR0cHM6Ly93d3cubXlhbm9uYW1vdXNlLm5ldC8=`",
			"Internet Archive - `aHR0cHM6Ly9hcmNoaXZlLm9yZy9kZXRhaWxzL3RleHRz`"
		]
		audio_books = [
			"Mobilism Audiobooks - `aHR0cHM6Ly9mb3J1bS5tb2JpbGlzbS5vcmcvdmlld2ZvcnVtLnBocD9mPTEyNA==`",
			"AudioBook Bay - `aHR0cHM6Ly9hdWRpb2Jvb2tiYXkubHUv`",
			"MyAnonamouse - `aHR0cHM6Ly93d3cubXlhbm9uYW1vdXNlLm5ldC8=`",
			"Audio Book CSE - `aHR0cHM6Ly9jc2UuZ29vZ2xlLmNvbS9jc2U/Y3g9MDA2NTE2NzUzMDA4MTEwODc0MDQ2OmN3YmJ6YTU2dmhk`"
		]
		educational_books = [
			"OpenStax - `aHR0cHM6Ly9vcGVuc3RheC5vcmcv`",
			"Academic Torrents - `aHR0cHM6Ly9hY2FkZW1pY3RvcnJlbnRzLmNvbS8=`",
			"Wikiversity - `aHR0cHM6Ly93d3cud2lraXZlcnNpdHkub3JnLw==`",
			"IvyPanda 1000+ Open Textbooks - `aHR0cHM6Ly9pdnlwYW5kYS5jb20vYmxvZy8xMDAwLW9wZW4tdGV4dGJvb2tzLWFuZC1sZWFybmluZy1yZXNvdXJjZXMtZm9yLWFsbC1zdWJqZWN0cy8=`"
		]

		# Mounting embed :)
		embed.add_field(name="📖 E-Books", value="\n".join(e_books), inline=False)
		embed.add_field(name="🎧 Audio Books", value="\n".join(audio_books), inline=False)
		embed.add_field(name="🎓 Education Books", value="\n".join(educational_books), inline=False)
		embed.set_footer(text="Also try /search-books!")

		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="music", description="Music resources.")
	async def music(self, interaction: discord.Interaction):
		embed = discord.Embed(
		title="🎵 Music Resources",
		description="Apps, sites and tools for streaming, download and music ripping.",
		)

		# Sites
		streaming_apps_mobile = [
			"⭐ ReVanced Manager - `aHR0cHM6Ly92YW5jZWQudG8v`",
			"⭐ XManager - `aHR0cHM6Ly93d3cueG1hbmFnZXJhcHAuY29tLw==`"

		]
		streaming_apps_desktop = [
			"⭐ Spicetify - `aHR0cHM6Ly9zcGljZXRpZnkuYXBwLw==`",
			"Spotify clients - `aHR0cHM6Ly9mbWh5Lm5ldC9hdWRpb3BpcmFjeWd1aWRlI3Nwb3RpZnktY2xpZW50cw==`",
			"Custom YouTube Music - `aHR0cHM6Ly90aC1jaC5naXRodWIuaW8veW91dHViZS1tdXNpYy8=`",
			"Lofi Rocks - `aHR0cHM6Ly93d3cubG9maS5yb2Nrcy8=`"
		]
		streaming_sites = [
			"YouTube Music - `aHR0cHM6Ly9tdXNpYy55b3V0dWJlLmNvbS8=`",
			"Dab Music Player - `aHR0cHM6Ly9kYWIueWVldC5zdS8=`",
			"Reddit Music Player - `aHR0cHM6Ly9yZWRkaXQubXVzaWNwbGF5ZXIuaW8v`",
			"SoundCloud - `aHR0cHM6Ly9zb3VuZGNsb3VkLmNvbS8=`"
		]
		audio_ripping = [
			"⭐ Cobalt - `aHR0cHM6Ly9jb2JhbHQudG9vbHMv`",
			"DoubleDouble - `aHR0cHM6Ly9kb3VibGVkb3VibGUudG9wLw==`",
			"Squid - `aHR0cHM6Ly9zcXVpZC53dGYv`"
		]
		download = [
			"⭐ Nicotine+ - aHR0cHM6Ly9uaWNvdGluZS1wbHVzLm9yZy8=",
			"Musify - aHR0cHM6Ly9tdXNpZnkuY2x1Yi8=",
			"PunkCata - aHR0cHM6Ly9wdW5rY2F0YS5ibG9nc3BvdC5jb20v",
			"Internet Archive (Audio) - aHR0cHM6Ly9hcmNoaXZlLm9yZy9kZXRhaWxzL2F1ZGlv"
		]

		# Mounting embed
		embed.add_field(name="📱 Streaming Apps (Android)", value="\n".join(streaming_apps_mobile), inline=False)
		embed.add_field(name="💻 Streaming Apps (Desktop)", value="\n".join(streaming_apps_desktop), inline=False)
		embed.add_field(name="🌐 Streaming Sites", value="\n".join(streaming_sites), inline=False)
		embed.add_field(name="🎙️ Audio Ripping", value="\n".join(audio_ripping), inline=False)
		embed.add_field(name="📥 Download", value="\n".join(download), inline=False)


		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="softwares", description="Software Resources")
	async def softwares(self, interaction: discord.Interaction):
		embed = discord.Embed(
			title="🖥️ Software Resources",
			description="Best websites to download softwares for Windows and Macos."
		)

		# Links
		windows = [
			"⭐ AppDoze - `aHR0cHM6Ly9hcHBkb3plLm5ldC8=`",
			"⭐ Monkrus Adobe (:flag_ru:) - `aHR0cHM6Ly93MTYubW9ua3J1cy53cy8=`",
			"⭐ CracksURL - `aHR0cHM6Ly9jcmFja3N1cmwuY29tLw==`",
			"LRepacks (:flag_ir:) - `aHR0cHM6Ly9scmVwYWNrcy5uZXQv`",
			"AudioZ - `aHR0cHM6Ly9hdWRpb3ouZG93bmxvYWQv`",
		]
		mac = [
			"⭐ AppKed - `aHR0cHM6Ly93d3cubWFjYmVkLmNvbS8=`",
			"⭐ AppsTorrent (:flag_ru:) - `aHR0cHM6Ly9hcHBzdG9ycmVudC5ydS8=`",
			"InsMac - `aHR0cHM6Ly9pbnNtYWMub3JnLw==`",
			"Macintosh Garden - `aHR0cHM6Ly9tYWNpbnRvc2hnYXJkZW4ub3JnLw==`",
			"NMac Hub - `aHR0cHM6Ly9ubWFjLnRvL2h1Yi8=`",
			"NMac Download - `aHR0cHM6Ly93d3cubWFjYXBwZG93bmxvYWQuY29tLw==`"
		]

		# Mounting embed
		embed.add_field(name="🚪 Windows", value="\n".join(windows), inline=False)
		embed.add_field(name="🍎 Mac", value="\n".join(mac), inline=False)

		await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Resources(bot))