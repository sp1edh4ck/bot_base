from datetime import datetime as dt

import asyncpg

from config import DB_PASSWORD


class Database:
    def __init__(self):
        # A variable for accessing the database.
        self.pool = None
        # The cache of the user's language,
        # so as not to pull the database once again
        self.lang_cache = {}

    """
    The function of connecting to a database file.
    """
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user='postgres',
            password=DB_PASSWORD,
            database='postgres',
            host='127.0.0.1',
            port='5432',
            min_size=1,
            max_size=5
        )

    """
    The function for cleaning the database is needed,
    for example, for tests.

    Don't forget to remove the call to this function on the bot release.
    """
    async def clear_all_tables(self):
        async with self.pool.acquire() as conn:
            tables = await conn.fetch(
                "SELECT tablename FROM pg_tables WHERE schemaname='public'"
            )
            for t in tables:
                await conn.execute(
                    f'TRUNCATE TABLE "{t["tablename"]}" RESTART IDENTITY CASCADE'
                )

    """
    A function for creating tables in a database,
    creates tables only if they are not in the database.
    """
    async def create_tables(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_id BIGINT UNIQUE NOT NULL,
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS message (
                id SERIAL PRIMARY KEY,
                user_id BIGINT UNIQUE NOT NULL,
                text TEXT NOT NULL
            );
            """
        ]
        async with self.pool.acquire() as conn:
            for q in queries:
                await conn.execute(q)

    """
    Example.
    User search function.
    """
    async def user_exists(self, user_id: int) -> bool:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT 1 FROM users WHERE user_id=$1", user_id)
            return row is not None

    """
    Example.
    User search function.
    """
    async def add_user(self, user_id: int, username: str, lang: str, ref_id=None):
        registration_date = dt.now()
        async with self.pool.acquire() as conn:
            if ref_id:
                await conn.execute(
                    "INSERT INTO users (user_id, username, ref_id, registration_date) VALUES ($1,$2,$3,$4)",
                    user_id, username, ref_id, registration_date
                )
            else:
                await conn.execute(
                    "INSERT INTO users (user_id, username, lang, registration_date) VALUES ($1,$2,$3,$4)",
                    user_id, username, lang, registration_date
                )

    """
    Example.
    A function for getting user information.
    """
    async def get_user(self, user_value, check_value):
        async with self.pool.acquire() as conn:
            if check_value == "int":
                return await conn.fetch("SELECT * FROM users WHERE user_id=$1", user_value)
            else:
                return await conn.fetch("SELECT * FROM users WHERE username=$1", user_value)

    """
    Example.
    A function for getting the user's language.
    There is a scenario where the user has not
    selected a language, then the language is selected automatically.
    """
    async def get_lang(self, user_id: int):
        # First, we try from the cache.
        if user_id in self.lang_cache:
            return self.lang_cache[user_id]
    
        # If the user is not in the database yet, we return the default.
        async with self.pool.acquire() as conn:
            lang = await conn.fetchval(
                "SELECT lang FROM users WHERE user_id=$1", user_id
            )
            if lang is None:
                lang = "ru"  # Default for new users.
            self.lang_cache[user_id] = lang
            return lang

    """
    Example.
    A function for changing the user's language.
    """
    async def set_lang(self, user_id, lang):
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE users SET lang=$1 WHERE user_id=$2", lang, user_id)
        self.lang_cache[user_id] = lang
