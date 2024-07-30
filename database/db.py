import aiosqlite

db_name = 'database/user.db'


class users():
    async def add_table(self):
        async with aiosqlite.connect(db_name) as db:
            cursor = await db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
            )
            table_exists = await cursor.fetchone()

            # Создаём таблицу, если её нет
            if not table_exists:
                await db.execute(
                    """
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        name TEXT,
                        age INTEGER
                    )
                    """
                )

            else:
                print('adding')
            await db.commit()
    async def add_user(self, user_id, name, age):
        async with aiosqlite.connect(db_name) as con:
            await con.execute("INSERT INTO users "
                              "(user_id, name, age) "
                              "VALUES (?, ?, ?)", [user_id, name, age])
            await con.commit()

    ############################### ПРОВЕРКА ЮЗЕРА #####################################

    async def get_users(self):
        async with aiosqlite.connect(db_name) as con:
            async with con.cursor() as cur:
                conn = await cur.execute("SELECT `name` FROM `users`")
                get_u = await conn.fetchall()
                await con.commit()
            return get_u

    async def get_users_id(self):
        async with aiosqlite.connect(db_name) as con:
            async with con.cursor() as cur:
                conn = await cur.execute("SELECT `user_id` FROM `users`")
                get_u = await conn.fetchall()
                await con.commit()
            return get_u



