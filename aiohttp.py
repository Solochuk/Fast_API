import aiohttp
import aiomysql
import asyncio

async def fetch_users():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://jsonplaceholder.typicode.com/users") as response:
            return await response.json()
        
async def connect_to_db():
    return await aiomysql.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        db="your_database"
    )

async def fetch_users_from_db():
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM users;")
        result = await cursor.fetchall()
    await conn.close()
    return result

async def add_user_to_db(name, email):
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        await cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
        await conn.commit()
    await conn.close()

async def delete_user_from_db(user_id):
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        await cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        await conn.commit()
    await conn.close()

async def main():
    users = await fetch_users()
    print("Fetched users from API:", users)

    db_users = await fetch_users_from_db()
    print("Fetched users from DB:", db_users)

    await add_user_to_db("Jane Doe", "jane.doe@example.com")
    print("Added new user.")

    await delete_user_from_db(1)
    print("Deleted user with ID 1.")

if __name__ == "__main__":
    asyncio.run(main())
