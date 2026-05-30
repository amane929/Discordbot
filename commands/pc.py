import discord
from utils.embed import status_6th, status_7th
from typing import Literal


# PCの能力値を振るコマンド
def pc(tree: discord.app_commands.CommandTree):
    @tree.command(name="pc", description="PCの能力値を振る")
    @discord.app_commands.describe(name="キャラクター名（省略可）",edition="ルールブックの版（6版 or 7版）")
    async def _pc(interaction: discord.Interaction, name: str = "探索者",edition: Literal["6版", "7版"] = "6版"):
        if edition == "6版":
            embed = status_6th(name=name)
            await interaction.response.send_message(embed=embed)
        elif edition == "7版":
            embed = status_7th(name=name)
            await interaction.response.send_message(embed=embed)