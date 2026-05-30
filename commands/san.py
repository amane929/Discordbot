import random
import discord
from utils.embed import san_check_embed

# ダイスを振る関数
def ndn(a, b):
    return [random.randint(1, int(b)) for _ in range(int(a))]


def san(tree: discord.app_commands.CommandTree):
    # SANチェック
    @tree.command(name="san", description="SANチェック（正気度判定）")
    @discord.app_commands.describe(
        current_san="現在のSAN値（1〜99）",
        success_loss="成功時のSAN減少量（例: 0 または 1）",
        fail_loss="失敗時のSAN減少量（例: 1d6 または 2）"
    )
    async def _san(interaction: discord.Interaction, current_san: int, success_loss: str, fail_loss: str):
        if not (1 <= current_san <= 99):
            await interaction.response.send_message("⚠️ SAN値は1〜99の範囲で入力してください。")
            return

        # ダイス式のパース
        try:
            sanembed = san_check_embed(current_san, success_loss, fail_loss)
            await interaction.response.send_message(embed=sanembed)
        except (ValueError, IndexError):
            await interaction.response.send_message(
                "⚠️ SAN減少量の形式が正しくありません。\n"
                "例: `0`、`1`、`1d4`、`1d6` など"
            )