import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp, subprocess
import glob
import json
import os

# JSON CONFIGS
with open("config.json") as f:
	config = json.load(f)
ffmpeg = config["FFMPEG_LOCATION"]

# OPTS
ydl_mp3_opts = {
	"format": "bestaudio/best",
	"ffmpeg_location": ffmpeg,
	"postprocessors": [{
		"key": "FFmpegExtractAudio",
		"preferredcodec": "mp3",
		"preferredquality": "192",
	}],
	"outtmpl": "file/%(title)s.%(ext)s",
	"cookiefile": "cookies.txt",
	"extractor_args": {"youtube": {"player_client": ["android", "tv"]}},
}

ydl_mp4_opts = {
	"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
	"ffmpeg_location": ffmpeg,
	"merge_output_format": "mp4",
	"outtmpl": "file/%(title)s.%(ext)s",
	"cookiefile": "cookies.txt",
}

class Downloaders(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Downloading mp3
	@app_commands.command(name="rip-mp3", description="Download mp3 from a youtube video or spotify.")
	@app_commands.describe(
		video_url="Audio url"
	)
	async def rip_mp3(self, interaction: discord.Interaction, video_url: str):
		await interaction.response.defer()

		if "youtu" in video_url: # For youtube audios
			try:
				with yt_dlp.YoutubeDL(ydl_mp3_opts) as ydl:
					info = ydl.extract_info(video_url, download=True)
					filename = ydl.prepare_filename(info)
					filename = filename.rsplit(".", 1)[0] + ".mp3"
			except: # In case it can't download the file
				await interaction.followup.send(f"Check the youtube url and try again. {e}")
				return

			# Mounting embed and sending audio
			audio = discord.File(filename)
			title = info.get("title")
			channel = info.get("uploader")
			thumbnail = info.get("thumbnail")
			views = info.get("view_count")
			duration = info.get("duration")
			embed = discord.Embed(
				title=title,
				description=f"**Channel:** {channel}\n**Views:** {views}\n**Duration:** {duration}"
			)
			embed.set_thumbnail(url=thumbnail)
			embed.set_footer(text="Click + hold to download in mobile.")

			file_path = filename
		elif "spotify" in video_url: # For spotify audios
			cmd = [
				"spotdl", video_url,
				"--output", "file"
			]

			# Running download command
			try:
				subprocess.run(cmd, check=True)
			except subprocess.CalledProcessError:
				await interaction.followup.send("Failed to download from spotify, check url.")
				return

			# Searching for mp3
			files = glob.glob(os.path.join("file", "*.mp3"))
			if not files:
				await interaction.followup.send("No music found.")
				return

			file_path = files[0]
			audio = discord.File(file_path)

			# Embed
			title = os.path.basename(file_path).rsplit(".", 1)[0]

			embed = discord.Embed(title=title, description="Extracted via spotify, use youtube next time to get statistics.")
			embed.set_footer(text="Click + hold to download in mobile.")
		else:
			await interaction.followup.send("We don't currently support this plataform, consider making a suggestion.")
			return

		# Send embed previously mounted
		await interaction.followup.send(embed=embed, file=audio)
		os.remove(file_path)

	# Downloading mp4
	@app_commands.command(name="rip-mp4", description="Download mp4 from a youtube video.")
	@app_commands.describe(
		video_url="Youtube url"
	)
	async def rip_mp4(self, interaction: discord.Interaction, video_url: str):
		await interaction.response.defer()

		try:
			with yt_dlp.YoutubeDL(ydl_mp4_opts) as ydl:
				info = ydl.extract_info(video_url, download=True)
				filename = ydl.prepare_filename(info)
				filename = filename.rsplit(".", 1)[0] + ".mp4"
		except: # IK it's not how you use try/except btw, just lemme be happy bruh :D
			await interaction.followup.send("Pls insert a valid url.")
			return

		# Mounting embed and sending video
		video = discord.File(filename)
		title = info.get("title")
		channel = info.get("uploader")
		thumbnail = info.get("thumbnail")
		views = info.get("view_count")
		duration = info.get("duration")
		embed = discord.Embed(
			title=title,
			description=f"**Channel:** {channel}\n**Views:** {views}\n**Duration:** {duration}s"
		)
		embed.set_thumbnail(url=thumbnail)
		embed.set_footer(text="Click + hold to download in mobile.")

		await interaction.followup.send(embed=embed, file=video)
		os.remove(filename)

async def setup(bot):
	await bot.add_cog(Downloaders(bot))