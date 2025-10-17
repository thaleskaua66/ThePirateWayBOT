import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import os
import re
from bs4 import BeautifulSoup

with open("config.json") as f:
    config = json.load(f)


class Search(commands.Cog):  # For online (& offline) search commands...
    def __init__(self, bot):
        self.bot = bot

    # Search for games online/offline
    @app_commands.command(name="search-games", description="Online or offline search for games")
    @app_commands.describe(
        query="Which game are you looking for?",
        style="Do you want to do an online or offline search?"
    )
    @app_commands.choices( # Dropdown to select the type of search :D
        style=[
            app_commands.Choice(name="Online", value="online"),
            app_commands.Choice(name="Offline", value="offline")
        ]
    )
    async def search_games(self, interaction: discord.Interaction, query: str, style: app_commands.Choice[str]):
        await interaction.response.defer()  # For lower hosts or computers :p
        if style.value == "online":
            results = self.google_search(query, config["CSE_GAMES_ID"])

            if not results:
                await interaction.followup.send(f"No results found for `{query}`.")
                return

            embed = discord.Embed(title=f"Results for: {query} (CSE ONLINE)", color=discord.Color.blue())
            for item in results[:5]:  # Change "5" for the number of items u wanna show
                embed.add_field(name=item["title"],
                                value=item["link"], inline=False)

            await interaction.followup.send(embed=embed)

        elif style.value == "offline": # Again, this code is a mess, i WILL change it later...
            # FORMATTING QUERY
            if re.search(r"[@#$%^*]", query):
                await interaction.followup.send("Special characters are not allowed.")
                return

            # Getting links...
            links_elamigos, links_steamrip, links_steamgg, links_dodi = self.load_links()
            query = query.lower()
            elamigos_results = [link for link in links_elamigos if query in link.lower()]
            steamrip_results = [link for link in links_steamrip if query in link.lower()]
            steamgg_results = [link for link in links_steamgg if query in link.lower()]
            dodi_results = [link for link in links_dodi if query in link.lower()]

            if (
                not elamigos_results
                and not steamrip_results
                and not dodi_results
                and not steamgg_results
            ):
                await interaction.followup.send(
                    f"Oops! I couldnt find any results for '{query}', may try an online search?"
                )
                return

            embed = discord.Embed(
                title=f"🔎 Results for '{query}'", color=discord.Color.dark_gray()
            )
            if elamigos_results:
                embed.add_field(
                    name=f"ELAMIGOS",
                    value="\n".join(f"- {game}" for game in elamigos_results[:3]),
                    inline=False,
                )
            if steamrip_results:
                embed.add_field(
                    name=f"STEAMRIP",
                    value="\n".join(f"- {game}" for game in steamrip_results[:3]),
                    inline=False,
                )
            if steamgg_results:
                embed.add_field(
                    name=f"STEAMGG",
                    value="\n".join(f"- {game}" for game in steamgg_results[:3]),
                    inline=False,
                )
            if dodi_results:
                embed.add_field(
                    name=f"DODI REPACKS",
                    value="\n".join(f"- {game}" for game in dodi_results[:3]),
                    inline=False,
                )

            await interaction.followup.send(embed=embed)

    # SEARCH FOR BOOKS ONLINE
    @app_commands.command(name="search-books", description="Online search for books")
    @app_commands.describe(
        query="Which book are you looking for?"
    )
    async def search_books(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        results = self.google_search(query, config["CSE_BOOKS_ID"])

        if not results:
            await interaction.followup.send(f"No results found for `{query}`.")
            return

        embed = discord.Embed(title=f"Results for: {query} (CSE ONLINE)", color=discord.Color.blue())
        for item in results[:5]:  # Change "5" for the number of items u wanna show
            embed.add_field(name=item["title"],
                            value=item["link"], inline=False)

        await interaction.followup.send(embed=embed)


    # ----- FUNCTIONS -----
    # FOR ONLINE SEARCH (GAMES), change the keys in config.json, u can change cx or create another CSE (Recommended)
    def google_search(self, query, cx: str):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": config["API_KEY"],
            "cx": cx,
            # EXCLUDE TERMS YOU DON'T LIKE!!
            "excludeTerms": "page A-Z Upcoming"
        }

        r = requests.get(url, params=params)
        if r.status_code != 200:
            return None

        data = r.json()
        return data.get("items", [])

    # FOR OFFLINE SEARCH (GAMES), this code is a fucking mess, if u are smart enough i recommend rewritting it
    def load_links(self):
        links_elamigos = []
        links_steamrip = []
        links_steamgg = []
        links_dodi = []

        # FOR OTHERS
        HTML_FOLDER = "./games_html"
        if not os.path.exists(HTML_FOLDER):
            os.makedirs(HTML_FOLDER)

        for filename in os.listdir(HTML_FOLDER):
            if filename.endswith(".html"):
                filepath = os.path.join(HTML_FOLDER, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    for link in soup.find_all("a", href=True):
                        link_text = link.get_text(strip=True)
                        link_url = link["href"].strip() # Idk why pyright see it as an error... The code works fine.

                        if not link_url.startswith("https://") and "steamgg" in link_url:
                            link_url = f"https://{link_url}"
                        elif not link_url.startswith("https://"):
                            link_url = f"https://steamrip.com{link_url}"

                        if link_url.startswith("https://elamigos.site"):
                            links_elamigos.append(f"[{link_text}]({link_url})")
                        elif link_url.startswith("https://steamrip.com"):
                            links_steamrip.append(f"[{link_text}]({link_url})")
                        elif link_url.startswith("https://steamgg.net"):
                            links_steamgg.append(f"[{link_text}]({link_url})")
                        elif link_url.startswith("https://dodi-repacks.site"):
                            links_dodi.append(f"[{link_text}]({link_url})")

        return links_elamigos, links_steamrip, links_steamgg, links_dodi


async def setup(bot):
    await bot.add_cog(Search(bot))
