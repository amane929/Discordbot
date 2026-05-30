import discord
from utils.embed import status_6th, status_7th
from typing import Literal
import db_manager


# PCの能力値を振るコマンド
def pc(tree: discord.app_commands.CommandTree):
    @tree.command(name="pc", description="PCの能力値を振る")
    @discord.app_commands.describe(name="キャラクター名（省略可）",edition="ルールブックの版（6版 or 7版）")
    async def _pc(interaction: discord.Interaction, name: str = "探索者",edition: Literal["6版", "7版"] = "6版"):
        if edition == "6版":
            embed, stats = status_6th(name=name)
            _pending[interaction.user.id] = {"edition": edition, "stats": stats}
            await interaction.response.send_message(embed=embed, view=SaveView())
        elif edition == "7版":
            embed, stats = status_7th(name=name)
            _pending[interaction.user.id] = {"edition": edition, "stats": stats}
            await interaction.response.send_message(embed=embed, view=SaveView())



# 一時保存用（user_id -> {stats, edition}）
_pending: dict[int, dict] = {}

#  モーダル：キャラ名入力 → DB保存
class SaveModal(discord.ui.Modal, title="キャラクターを保存"):
    char_name = discord.ui.TextInput(
        label="キャラクター名",
        placeholder="例: 田中太郎",
        max_length=50
    )
 
    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        pending = _pending.get(user_id)
        if pending is None:
            await interaction.response.send_message("⚠️ 保存データが見つかりません。再度 /pc を実行してください。", ephemeral=True)
            return
 
        name = self.char_name.value
        db_manager.init_db()
        db_manager.save_character(interaction.guild_id, user_id, name, pending["edition"], pending["stats"])
        _pending.pop(user_id, None)
 
        await interaction.response.send_message(f"✅ `{name}`（{pending['edition']}）を保存しました！", ephemeral=True)
 
 
#  ボタン：「保存する」を押したらモーダルを開く
class SaveView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
 
    @discord.ui.button(label="💾 保存する", style=discord.ButtonStyle.primary)
    async def save_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SaveModal())
 
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

#  /pc_load コマンド
def pc_load(tree: discord.app_commands.CommandTree):
    @tree.command(name="pc_load", description="保存したPCを読み込む")
    @discord.app_commands.describe(name="キャラクター名")
    async def _pc_load(interaction: discord.Interaction, name: str):
        db_manager.init_db()
        char = db_manager.load_character(interaction.guild_id, interaction.user.id, name)
        if char is None:
            await interaction.response.send_message(f"⚠️ `{name}` が見つかりませんでした。")
            return
 
        embed = discord.Embed(title=f"📋 {char['char_name']}（{char['edition']}）", color=0x5865F2)
        for k, v in char["stats"].items():
            embed.add_field(name=k, value=str(v), inline=True)
        await interaction.response.send_message(embed=embed)
 
 
#  /pc_delete コマンド
def pc_delete(tree: discord.app_commands.CommandTree):
    @tree.command(name="pc_delete", description="保存したPCを削除する")
    @discord.app_commands.describe(name="キャラクター名")
    async def _pc_delete(interaction: discord.Interaction, name: str):
        db_manager.init_db()
        deleted = db_manager.delete_character(interaction.guild_id, interaction.user.id, name)
        if deleted:
            await interaction.response.send_message(f"🗑️ `{name}` を削除しました。")
        else:
            await interaction.response.send_message(f"⚠️ `{name}` が見つかりませんでした。")
 
 
#  /pc_list コマンド
def pc_list(tree: discord.app_commands.CommandTree):
    @tree.command(name="pc_list", description="保存したPC一覧を表示する")
    async def _pc_list(interaction: discord.Interaction):
        db_manager.init_db()
        chars = db_manager.list_characters(interaction.guild_id, interaction.user.id)
        if not chars:
            await interaction.response.send_message("保存されているキャラクターはいません。")
            return
 
        embed = discord.Embed(title="📚 あなたのキャラクター一覧", color=0x5865F2)
        for c in chars:
            embed.add_field(
                name=c["char_name"],
                value=f"版: {c['edition']}\n更新: {c['updated_at']}",
                inline=False
            )
        await interaction.response.send_message(embed=embed)