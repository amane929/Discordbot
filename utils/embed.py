import discord
import random
from bisect import bisect_left
from utils.roller import roll_dice_expr, ndn
from utils.roller import diceSan

# 1d100の成功判定
def diceSF(skill: int):
    parsent = random.randint(1, 100)
    if parsent <= skill:
        result  = "成功!"
        if parsent <= 5:
            extreme = "クリティカル"
        else:
            extreme = " "
    else:
        result = "失敗"
        if parsent >= 96:
            extreme = "ファンブル"
        else:
            extreme = " "
    embed = discord.Embed(title="1d100 成功判定ロール", color=0xe0ffff)
    embed.add_field(name="技能値",   value=str(skill),   inline=True)
    embed.add_field(name="ダイス目", value=str(parsent), inline=True)
    embed.add_field(name="判定結果", value=f"**{extreme.strip()} {result}**", inline=False)
    return embed


# #region pc能力値
#dbの計算関数
def db(db):
    if not (2 <= db <= 184):
        return "error"

    thresholds = [12, 16, 20, 24, 32, 46, 72, 88, 114, 120, 136, 152, 168, 184]
    labels = ["-1d6", "-1d4", "±0", "+1d4", "+1d6", "+2d6", "+3d6", "+4d6", "+5d6", "+6d6", "+7d6", "+8d6", "+9d6", "+10d6"]
    
    return labels[bisect_left(thresholds, db)]

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

    stats = {
        "STR": STR, "CON": CON, "POW": POW, "DEX": DEX,
        "APP": APP, "SIZ": SIZ, "INT": INT, "EDU": EDU,
        "SAN": SAN, "幸運": luck, "アイデア": idea, "知識": know,
        "耐久力": hp, "MP": mp, "職業技能P": job_p, "趣味技能P": hob_p,
        "ダメージボーナス": db(dbp)
    }

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
    return embed, stats

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
    dbp   = (STR + SIZ) // 5
    build = STR + SIZ

    stats = {
        "STR": STR, "CON": CON, "POW": POW, "DEX": DEX,
        "APP": APP, "SIZ": SIZ, "INT": INT, "EDU": EDU,
        "SAN": SAN, "幸運": luck, "アイデア": idea, "知識": know,
        "耐久力": hp, "MP": mp, "趣味技能P": hob_p,
        "ダメージボーナス": db(dbp), "ビルド": build
    }

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
# #endregion

# SANチェック
def san_check_embed(current_san: int, success_loss: str, fail_loss: str) -> discord.Embed:
    success_val, success_detail = roll_dice_expr(success_loss)
    fail_val, fail_detail = roll_dice_expr(fail_loss)
    # 1d100を振って判定（_judge()を再利用）
    result, extreme, is_success= diceSan(current_san)
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
 
    return embed, stats

def oppose_embed(first: int, second: int) -> discord.Embed:
    STRopp = (first - second) + 50
    parsent = random.randint(1, 100)
    if parsent <= STRopp:
        result  = "成功!"
        if parsent <= 5:
            extreme = "クリティカル"
        else:
            extreme = " "
    else:
        result = "失敗"
        if parsent >= 96:
            extreme = "ファンブル"
        else:
            extreme = " "
    embed = discord.Embed(title = "対抗ロール", color=0x5865F2)
    embed.add_field(name="一人称", value=str(first), inline=False)
    embed.add_field(name="二人称", value=str(second), inline=False)
    embed.add_field(name="成功率", value=f"{STRopp}%", inline=False)
    embed.add_field(name="判定結果", value=f"{result} ({extreme})", inline=False)
    return embed