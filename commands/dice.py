import discord
from utils.embed import diceSF
from utils.roller import ndn

# このファイルを呼び出す側（dice_bot.py）からtreeを受け取る
def dice(tree: discord.app_commands.CommandTree):
    @tree.command(name="1d100", description="100面ダイス")
    @discord.app_commands.describe(skill="技能値")
    async def _1d100(interaction: discord.Interaction, skill: int):
        if not isinstance(skill, int) or skill <= 0:
            await interaction.response.send_message("⚠️技能値は自然数で入力してください")
            return
        embed = diceSF(skill)
        await interaction.response.send_message(embed=embed)

# 対抗ロール
def oppose(tree: discord.app_commands.CommandTree):
    @tree.command(name="oppose", description="対抗ロール")
    @discord.app_commands.describe(
        first="例: 13(STR) 一人称",
       second="例: 12(STR) 二人称"
    )
    async def oppose(interaction: discord.Interaction, first: int, second: int):
        if isinstance(first, int)  == False or first <= 0:
           await interaction.response.send_message("⚠️一人称の技能値は自然数で入力してください")
           return
        if isinstance(second, int)  == False or second <= 0:
           await interaction.response.send_message("⚠️二人称の技能値は自然数で入力してください")
           return 
        
        embed = oppose(first, second)
        await interaction.response.send_message(embed=embed)

# ダイスロールのコマンド
def roll(tree: discord.app_commands.CommandTree):
    @tree.command(name="roll", description="ダイスロール")
    @discord.app_commands.describe(formula="例: 2d6")
    async def _roll(interaction: discord.Interaction, formula: str):
       num, sides = formula.split("d")
       rolls = ndn(num, sides)
       total = sum(rolls)
       detail = " + ".join(str(r) for r in rolls)
       await interaction.response.send_message(f"{formula} → {detail} = {total}")