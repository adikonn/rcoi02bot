from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, update
from typing import Optional, List
from .models import Base, User
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self):
        self.engine = create_async_engine(settings.database_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def init_db(self) -> None:
        """Инициализация базы данных"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_user(
            self,
            user_id: int,
            family: str,
            name: str,
            father: str,
            number: str,
            class_: str
    ) -> User:
        """Создание нового пользователя"""
        async with self.async_session() as session:
            # Проверяем, существует ли пользователь
            existing_user = await self.get_user_by_id(user_id)
            if existing_user:
                # Обновляем данные существующего пользователя
                stmt = update(User).where(User.user_id == user_id).values(
                    family=family,
                    name=name,
                    father=father,
                    number=number,
                    class_=class_
                )
                await session.execute(stmt)
                await session.commit()
                return await self.get_user_by_id(user_id)
            else:
                # Создаем нового пользователя
                user = User(
                    user_id=user_id,
                    family=family,
                    name=name,
                    father=father,
                    number=number,
                    class_=class_
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        async with self.async_session() as session:
            stmt = select(User).where(User.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all_users(self) -> List[User]:
        """Получение всех пользователей"""
        async with self.async_session() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def update_user_result(self, user_id: int, result: str) -> None:
        """Обновление результата пользователя"""
        async with self.async_session() as session:
            stmt = update(User).where(User.user_id == user_id).values(last_result=result)
            await session.execute(stmt)
            await session.commit()


# Глобальный экземпляр репозитория
user_repository = UserRepository()
