import asyncio
import aiosqlite

# Function to set up the database and add sample data
async def setup_database():
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        await db.executemany("""
            INSERT INTO users (name, age) VALUES (?, ?)
        """, [
            ("Alice", 30),
            ("Bob", 50),
            ("Charlie", 20),
            ("Diana", 45)
        ])
        await db.commit()

# Asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All Users:")
            for user in users:
                print(user)
            return users

# Asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("Users Older than 40:")
            for user in older_users:
                print(user)
            return older_users

# Function to run both fetches concurrently
async def fetch_concurrently():
    await setup_database()  # Ensure the database is set up
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Entry point to run the program
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

