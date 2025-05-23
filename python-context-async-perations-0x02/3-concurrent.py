

import asyncio
import aiosqlite

DB_NAME = "example.db"


async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        print("All Users:")
        for row in rows:
            print(row)
        return rows


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        await cursor.close()
        print("Users older than 40:")
        for row in rows:
            print(row)
        return rows


async def fetch_concurrently():
    """Run both queries concurrently."""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


# === Setup for demonstration ===
async def setup_demo_data():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        """)
        await db.execute("DELETE FROM users")
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 30),
            ("Bob", 22),
            ("Charlie", 45),
            ("Diana", 50)
        ])
        await db.commit()


if __name__ == "__main__":
    asyncio.run(setup_demo_data())
    asyncio.run(fetch_concurrently())
