from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select, literal_column, update, delete, and_, or_
from sqlalchemy.orm import joinedload

from db.sql.connect import AsyncSessionMaker
from db.sql.enum.enums import Sex, ChatSettingsSex
from db.sql.model import Users, ChatSettings, Connection


class SqlService(ABC):
    @abstractmethod
    async def run(self):
        raise NotImplementedError


class ReadUser(SqlService):

    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            user = await session.scalar(select(Users).where(Users.tg_id == literal_column(str(self.tg_id)))
                                        .options(joinedload(Users.chat_settings)))
            return user


class CreateUser(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            new_user = Users(tg_id=self.tg_id)
            chat_settings = ChatSettings(user_id=new_user.tg_id)
            session.add(new_user)
            session.add(chat_settings)
            await session.commit()
            await session.refresh(new_user)
            return new_user


class UpdateUser(SqlService):
    def __init__(self, tg_id: int, sex: Optional[Sex] = None, age: Optional[int] = None, is_vip: Optional[bool] = None):
        self.tg_id = tg_id
        self.sex = sex
        self.age = age
        self.is_vip = is_vip

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                update(Users)
                .where(Users.tg_id == literal_column(str(self.tg_id)))
                .values(
                    sex=self.sex if self.sex is not None else Users.sex,
                    age=self.age if self.age is not None else Users.age,
                    is_vip=self.is_vip if self.is_vip is not None else Users.is_vip,
                )
            )
            await session.execute(stmt)
            await session.commit()


class DeleteUser(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = delete(Users).where(Users.tg_id == literal_column(str(self.tg_id)))
            await session.execute(stmt)
            await session.commit()


class AllUsers(SqlService):
    async def run(self):
        async with AsyncSessionMaker() as session:
            users_scalar = await session.scalars(select(Users))
            return users_scalar.all()


class UpdateChatSettings(SqlService):
    def __init__(self, tg_id: int, sex: Optional[ChatSettingsSex] = None, age_min: Optional[int] = None,
                 age_max: Optional[int] = None):
        self.tg_id = tg_id
        self.sex = sex
        self.age_min = age_min
        self.age_max = age_max

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                update(ChatSettings)
                .where(ChatSettings.user_id == literal_column(str(self.tg_id)))
                .values(
                    sex=self.sex if self.sex is not None else ChatSettings.sex,
                    min_age=self.age_min if self.age_min is not None else ChatSettings.min_age,
                    max_age=self.age_max if self.age_max is not None else ChatSettings.max_age,
                )
            )
            await session.execute(stmt)
            await session.commit()


class ReadConnection(SqlService):

    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            connection = await session.scalar(
                select(Connection).where(or_(Connection.first_user_id == literal_column(
                    str(self.tg_id)), Connection.second_user_id == literal_column(str(self.tg_id))))
            )
            if connection is None:
                return None, -1, -1
            return connection, connection.first_user_id or -1, connection.second_user_id or -1


class ConnectConnection(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            connection = await session.scalar(
                select(Connection).where(or_(Connection.first_user_id != -1,
                                             Connection.second_user_id != 1)))
            print('Conn, ', connection)
            if connection.first_user_id == -1:
                connection.first_user_id = self.tg_id
            elif connection.second_user_id == -1:
                connection.second_user_id = self.tg_id
            await session.commit()


class DeleteConnection(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            search = or_(Connection.first_user_id == literal_column(str(self.tg_id)),
                         Connection.second_user_id == literal_column(str(self.tg_id)))
            connect = await session.scalar(select(Connection).where(search))
            stmt = delete(Connection).where(search)
            await session.execute(stmt)
            await session.commit()
            return connect


class DeleteConnectionById(SqlService):
    def __init__(self, conn_id: int):
        self.conn_id = conn_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            search = Connection.id == literal_column(str(self.conn_id))
            connect = await session.scalar(select(Connection).where(search))
            stmt = delete(Connection).where(search)
            await session.execute(stmt)
            await session.commit()
            return connect


class FindHalfConnectionOrCreate(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            query = select(Connection).where(
                or_(
                    and_(Connection.first_user_id != -1, Connection.second_user_id == -1),
                    and_(Connection.second_user_id != -1, Connection.first_user_id == -1)
                )
            )
        result = await session.execute(query)
        sc = result.scalars().all()
        print(f"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ::: {sc}")
        print(f"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ::: {sc}")
        if len(sc) != 0:
            return sc[0], True
        connection = Connection(first_user_id=self.tg_id)
        session.add(connection)
        await session.commit()
        await session.refresh(connection)
        return connection, False


async def run_sql(runnable: SqlService):
    return await runnable.run()
