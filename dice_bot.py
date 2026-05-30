import random
import discord
import os
from typing import Literal
from bisect import bisect_left
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

#discord.pyのクライアントとコマンドツリーの設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# ダイスを振る関数
def ndn(a, b):
    return [random.randint(1, int(b)) for _ in range(int(a))]

#dbの計算関数
def db(db):
    if not (2 <= db <= 184):
        return "error"

    thresholds = [12, 16, 20, 24, 32, 46, 72, 88, 114, 120, 136, 152, 168, 184]
    labels = ["-1d6", "-1d4", "±0", "+1d4", "+1d6", "+2d6", "+3d6", "+4d6", "+5d6", "+6d6", "+7d6", "+8d6", "+9d6", "+10d6"]
    
    return labels[bisect_left(thresholds, db)]

# ダイス判定の関数
def diceSF(skill):
    if skill <= 0:
        return "技能値は自然数で入力してください"

    parsent = random.randint(1, 100)
    if parsent <= 5:
        extreme = "クリティカル"
    elif parsent >= 96:
        extreme = "ファンブル"
    else:
        extreme = " "

    if parsent <= skill:
        result = "成功!"
    else:
        result = "失敗"

    embed = discord.Embed(title=f"1d100 成功判定ロール", color=0xe0ffff)
    embed.add_field(name="技能値", value=str(skill), inline=True)
    embed.add_field(name="ダイス目", value=str(parsent), inline=True)
    embed.add_field(name="判定結果", value=f"**{extreme.strip()} {result}**", inline=False)
    return embed

# ダイス式（"1d6" や "2" など）を評価してロール結果を返す関数
def roll_dice_expr(expr: str) -> tuple[int, str]:
    expr = expr.strip().lower()
    if "d" in expr:
        parts = expr.split("d")
        if len(parts) != 2:
            raise ValueError(f"無効なダイス式: {expr}")
        num, sides = int(parts[0]), int(parts[1])
        rolls = ndn(num, sides)
        total = sum(rolls)
        detail = f"{expr}[{', '.join(str(r) for r in rolls)}]"
        return total, detail
    else:
        val = int(expr)
        return val, str(val)

# 6版の能力値を振る関数
def status_6th(name="探索者"):
    STR = sum(ndn(3, 6))
    CON = sum(ndn(3, 6))
    POW = sum(ndn(3, 6))
    DEX = sum(ndn(3, 6))
    APP = sum(ndn(3, 6))
    SIZ = (sum(ndn(2, 6)) + 6)
    INT = (sum(ndn(2, 6)) + 6)
    EDU = (sum(ndn(3, 6)) + 3)

    SAN   = POW * 5
    luck  = POW * 5
    idea  = INT * 5
    know  = EDU * 5
    hp    = (CON + SIZ) // 2
    mp    = POW
    job_p = EDU * 20
    hob_p = INT * 10
    dbp   = STR + SIZ

    embed = discord.Embed(title=f"{name} のキャラクターシート（6版）", color=0x5865F2)
    embed.add_field(name="⚔️ 能力値", value="───────────", inline=False)
    embed.add_field(name="STR（筋力）",   value=str(STR), inline=True)
    embed.add_field(name="CON（体力）",   value=str(CON), inline=True)
    embed.add_field(name="POW（精神力）", value=str(POW), inline=True)
    embed.add_field(name="DEX（敏捷性）", value=str(DEX), inline=True)
    embed.add_field(name="APP（外見）",   value=str(APP), inline=True)
    embed.add_field(name="SIZ（体格）",   value=str(SIZ), inline=True)
    embed.add_field(name="INT（知性）",   value=str(INT), inline=True)
    embed.add_field(name="EDU（教育）",   value=str(EDU), inline=True)
    embed.add_field(name="\u200b",        value="\u200b",  inline=True)

    embed.add_field(name="✨ SAN値・ポイント", value="───────────", inline=False)
    embed.add_field(name="SAN（正気度）",   value=f"{SAN}/99", inline=True)
    embed.add_field(name="幸運",            value=str(luck),   inline=True)
    embed.add_field(name="アイデア",        value=str(idea),   inline=True)
    embed.add_field(name="知識",            value=str(know),   inline=True)
    embed.add_field(name="耐久力",          value=str(hp),     inline=True)
    embed.add_field(name="マジックポイント", value=str(mp),     inline=True)
    embed.add_field(name="職業技能P",       value=str(job_p),  inline=True)
    embed.add_field(name="趣味技能P",       value=str(hob_p),  inline=True)
    embed.add_field(name="ダメージボーナス", value=db(dbp),          inline=True)
    return embed

# 7版の能力値を振る関数
def status_7th(name="探索者"):
    STR = sum(ndn(3, 6)) * 5
    CON = sum(ndn(3, 6)) * 5
    POW = sum(ndn(3, 6)) * 5
    DEX = sum(ndn(3, 6)) * 5
    APP = sum(ndn(3, 6)) * 5
    SIZ = (sum(ndn(2, 6)) + 6) * 5
    INT = (sum(ndn(2, 6)) + 6) * 5
    EDU = (sum(ndn(2, 6)) + 3) * 5
    luck= sum(ndn(3, 6)) * 5

    SAN   = POW
    idea  = INT
    know  = EDU
    hp    = (CON + SIZ) // 10
    mp    = POW // 5
    hob_p = INT * 2
    dbp   = STR + SIZ // 5
    build = STR + SIZ

    embed = discord.Embed(title=f"{name} のキャラクターシート（7版）", color=0x5865F2)
    embed.add_field(name="⚔️ 能力値", value="───────────", inline=False)
    embed.add_field(name="STR（筋力）",   value=str(STR), inline=True)
    embed.add_field(name="CON（体力）",   value=str(CON), inline=True)
    embed.add_field(name="POW（精神力）", value=str(POW), inline=True)
    embed.add_field(name="DEX（敏捷性）", value=str(DEX), inline=True)
    embed.add_field(name="APP（外見）",   value=str(APP), inline=True)
    embed.add_field(name="SIZ（体格）",   value=str(SIZ), inline=True)
    embed.add_field(name="INT（知性）",   value=str(INT), inline=True)
    embed.add_field(name="EDU（教育）",   value=str(EDU), inline=True)
    embed.add_field(name="\u200b",        value="\u200b",  inline=True)

    embed.add_field(name="✨ SAN値・ポイント", value="───────────", inline=False)
    embed.add_field(name="SAN（正気度）",   value=f"{SAN}/99", inline=True)
    embed.add_field(name="幸運",            value=str(luck),   inline=True)
    embed.add_field(name="アイデア",        value=str(idea),   inline=True)
    embed.add_field(name="知識",            value=str(know),   inline=True)
    embed.add_field(name="耐久力",          value=str(hp),     inline=True)
    embed.add_field(name="マジックポイント", value=str(mp),     inline=True)
    embed.add_field(name="趣味技能P",       value=str(hob_p),  inline=True)
    embed.add_field(name="ダメージボーナス", value=db(dbp),      inline=True)
    embed.add_field(name="ビルド",            value=str(build),  inline=True)
    return embed

# PCの能力値を振るコマンド
@tree.command(name="pc", description="PCの能力値を振る")
@discord.app_commands.describe(name="キャラクター名（省略可）",edition="ルールブックの版（6版 or 7版）")
async def _pc(interaction: discord.Interaction, name: str = "探索者",edition: Literal["6版", "7版"] = "6版"):
    if edition == "6版":
        embed = status_6th(name=name)
        await interaction.response.send_message(embed=embed)

    elif edition == "7版":
        embed = status_7th(name=name)
        await interaction.response.send_message(embed=embed)

# 1d100のコマンド
@tree.command(name="1d100", description="100面ダイス ")
@discord.app_commands.describe(skill="技能値")
async def _1d100(interaction: discord.Interaction, skill: int):
    if isinstance(skill, int) == False or skill <= 0:
        await interaction.response.send_message("⚠️技能値は自然数で入力してください")
        return
    
    embed = diceSF(skill)
    await interaction.response.send_message(embed=embed)


# ダイスロールのコマンド
@tree.command(name="roll", description="ダイスロール")
@discord.app_commands.describe(formula="例: 2d6")
async def _roll(interaction: discord.Interaction, formula: str):
    num, sides = formula.split("d")
    rolls = ndn(num, sides)
    total = sum(rolls)
    detail = " + ".join(str(r) for r in rolls)
    await interaction.response.send_message(f"{formula} → {detail} = {total}")

# 対抗ロール
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
    
    STRopp = (first - second) + 50
    diceSF_result = diceSF(STRopp)
    embed = discord.Embed(title = "対抗ロール", color=0x5865F2)
    embed.add_field(name="一人称", value=str(first), inline=False)
    embed.add_field(name="二人称", value=str(second), inline=False)
    embed.add_field(name="成功率", value=f"{STRopp}%", inline=False)
    embed.add_field(name="判定結果", value=diceSF_result, inline=False)
    await interaction.response.send_message(embed=embed)

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
        success_val, success_detail = roll_dice_expr(success_loss)
        fail_val,    fail_detail    = roll_dice_expr(fail_loss)
    except (ValueError, IndexError):
        await interaction.response.send_message(
            "⚠️ SAN減少量の形式が正しくありません。\n"
            "例: `0`、`1`、`1d4`、`1d6` など"
        )
        return
 
    # 1d100を振って判定（_judge()を再利用）
    result, extreme, is_success = diceSF(current_san)
 
    judge_label = extreme.strip() if extreme.strip() else result.rstrip("!")
    color = 0x57F287 if is_success else 0xED4245
 
    # SAN減少量の決定
    if is_success:
        san_loss      = success_val
        loss_detail   = success_detail
        loss_label    = f"成功時ロス（{success_loss}）"
    else:
        san_loss      = fail_val
        loss_detail   = fail_detail
        loss_label    = f"失敗時ロス（{fail_loss}）"
 
    new_san = max(current_san - san_loss, 0)
 
    # 狂気判定
    insanity_warning = ""
    if san_loss >= 5:
        insanity_warning = "\n🌀 **一時的狂気の可能性あり！**（5以上のSAN喪失）"
    if new_san == 0:
        insanity_warning += "\n💀 **SAN値が0になりました。永久狂気!**"
 
    # Embedの作成
    embed = discord.Embed(title="🧠 SANチェック", color=color)
    embed.add_field(name="判定",        value=f"**{judge_label}**（{result} / SAN {current_san}）", inline=False)
    embed.add_field(name=loss_label,    value=loss_detail,                                        inline=True)
    embed.add_field(name="SAN減少",     value=f"**-{san_loss}**",                                 inline=True)
    embed.add_field(name="SAN値の変化", value=f"{current_san}  →  **{new_san}**",                 inline=False)
 
    if insanity_warning:
        embed.add_field(name="⚠️ 警告", value=insanity_warning, inline=False)
 
    await interaction.response.send_message(embed=embed)

# 最初に実行されるもの
@client.event
async def on_ready():
    await tree.sync()
 
client.run(TOKEN)