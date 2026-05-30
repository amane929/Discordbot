import sqlite3
import json
import os
 
DB_PATH = os.path.join(os.path.dirname(__file__), "characters.db")
 
def get_conn():
    return sqlite3.connect(DB_PATH)
 
def init_db():
    """DBとテーブルを初期化する"""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                guild_id    TEXT NOT NULL,
                user_id     TEXT NOT NULL,
                char_name   TEXT NOT NULL,
                edition     TEXT NOT NULL,
                stats       TEXT NOT NULL,
                updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (guild_id, user_id, char_name)
            )
        """)
        conn.commit()
 
def save_character(guild_id: int, user_id: int, char_name: str, edition: str, stats: dict):
    """キャラクターを保存（既存なら上書き）"""
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO characters (guild_id, user_id, char_name, edition, stats, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(guild_id, user_id, char_name)
            DO UPDATE SET edition=excluded.edition, stats=excluded.stats, updated_at=CURRENT_TIMESTAMP
        """, (str(guild_id), str(user_id), char_name, edition, json.dumps(stats, ensure_ascii=False)))
        conn.commit()
 
def load_character(guild_id: int, user_id: int, char_name: str) -> dict | None:
    """キャラクターを取得。存在しない場合はNone"""
    with get_conn() as conn:
        row = conn.execute("""
            SELECT char_name, edition, stats FROM characters
            WHERE guild_id=? AND user_id=? AND char_name=?
        """, (str(guild_id), str(user_id), char_name)).fetchone()
    if row is None:
        return None
    return {"char_name": row[0], "edition": row[1], "stats": json.loads(row[2])}
 
def list_characters(guild_id: int, user_id: int) -> list[dict]:
    """ユーザーのキャラクター一覧を取得"""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT char_name, edition, updated_at FROM characters
            WHERE guild_id=? AND user_id=?
            ORDER BY updated_at DESC
        """, (str(guild_id), str(user_id))).fetchall()
    return [{"char_name": r[0], "edition": r[1], "updated_at": r[2]} for r in rows]
 
def delete_character(guild_id: int, user_id: int, char_name: str) -> bool:
    """キャラクターを削除。削除できた場合はTrueを返す"""
    with get_conn() as conn:
        cur = conn.execute("""
            DELETE FROM characters
            WHERE guild_id=? AND user_id=? AND char_name=?
        """, (str(guild_id), str(user_id), char_name))
        conn.commit()
    return cur.rowcount > 0