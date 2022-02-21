import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Pool = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.IP,
            database=config.db
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connect:
            connect: Connection
            async with connect.transaction():
                if fetch:
                    result = await connect.fetch(command, *args)
                elif fetchval:
                    result = await connect.fetchval(command, *args)
                elif fetchrow:
                    result = await connect.fetchrow(command, *args)
                elif execute:
                    result = await connect.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = '''
               CREATE TABLE IF NOT EXISTS users (
                   id SERIAL PRIMARY KEY,
                   fullname VARCHAR(255) NOT NULL,
                   username varchar(255) NULL,
                   tg_id BIGINT NOT NULL UNIQUE,
                   balance REAL NOT NULL DEFAULT 0,
                   referral BIGINT NOT NULL DEFAULT 0,
                   is_sell BOOLEAN NOT NULL DEFAULT true
                   
               );
           '''
        return await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, tg_id, fullname, username, referral):
        sql = """
            INSERT INTO users (
                fullname, username, tg_id, referral
            ) VALUES ($1, $2, $3, $4) returning *;
        """
        return await self.execute(sql, fullname, username, tg_id, referral, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = 'SELECT * FROM users WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_all_users(self):
        sql = 'SELECT * FROM users;'
        return await self.execute(sql, fetch=True)

    async def get_balance(self, tg_id):
        sql = "SELECT balance FROM users WHERE tg_id=$1;"
        return await self.execute(sql, tg_id, fetchrow=True)

    async def update_is_sell(self, is_sell, tg_id):
        sql = 'UPDATE users SET is_sell=$1 WHERE tg_id=$2;'
        return await self.execute(sql, is_sell, tg_id, execute=True)

    async def add_balance(self, balance, tg_id):
        sql = "UPDATE users SET balance=$1 + balance WHERE tg_id=$2"
        return await self.execute(sql, balance, tg_id, execute=True)

    async def take_balance(self, balance, tg_id):
        sql = "UPDATE users SET balance=balance-$1 WHERE tg_id=$2"
        return await self.execute(sql, balance, tg_id, execute=True)


if __name__ == "__main__":
    pass
