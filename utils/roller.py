import random

# ダイスを振る関数
def ndn(a, b):
    return [random.randint(1, int(b)) for _ in range(int(a))]

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
    
