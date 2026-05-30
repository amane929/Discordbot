import discord
from dotenv import load_dotenv
import os
from commands import dice, pc, san

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


# ─────────────────────────────────────────────
#  discord.pyのクライアントとコマンドツリーの設定
# ─────────────────────────────────────────────
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# ─────────────────────────────────────────────
#  treeにコマンドを登録
# ─────────────────────────────────────────────
dice.dice(tree)
dice.oppose(tree)
dice.roll(tree)
pc.pc(tree)
san.san(tree)


# ─────────────────────────────────────────────
#  起動
# ─────────────────────────────────────────────
@client.event
async def on_ready():
    await tree.sync()

client.run(TOKEN)