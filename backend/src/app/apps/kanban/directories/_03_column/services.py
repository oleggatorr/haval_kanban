from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from sqlalchemy.sql import func

from .models import Column
from .._02_tab.models import Tab  # Импортируем модель Tab
from .._02_tab.services import TabService
from .schemas import ColumnCreate, ColumnUpdate, ColumnResponse, Column_deep_Response


class ColumnService:
    """Сервис для работы с колонками"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_tab_exists(self, tab_id: int) -> bool:
        """
        Проверка существования таба
        
        Args:
            tab_id: ID таба
            
        Returns:
            True если таб существует, иначе False
        """
        result = await self.db.execute(
            select(Tab).where(Tab.id == tab_id)
        )
        return result.scalar_one_or_none() is not None
    
    async def _touch_tab(self, tab_id: int) -> None:
        """
        Обновление временной метки таба
        
        Args:
            tab_id: ID таба
        """
        tab_service = TabService(self.db)
        await tab_service.touch_tab(tab_id)

    async def create_column(self, column_data: ColumnCreate) -> ColumnResponse:
        """
        Создание новой колонки
        
        Args:
            column_data: Данные для создания колонки
            
        Returns:
            Созданная колонка
            
        Raises:
            ValueError: Если таб не существует
        """
        # Проверяем существование таба
        if not await self._check_tab_exists(column_data.tab_id):
            raise ValueError(f"Таб с ID {column_data.tab_id} не существует")
        
        db_column = Column(
            tab_id=column_data.tab_id,
            name=column_data.name,
            order_id=column_data.order_id,
            is_start=column_data.is_start,
            is_final=column_data.is_final,
            is_active=column_data.is_active
        )
        
        self.db.add(db_column)
        await self.db.commit()
        await self.db.refresh(db_column)
        
        # Используем tab_id, а не column.tab
        await self._touch_tab(db_column.tab_id)
        
        return ColumnResponse.model_validate(db_column)

    async def get_column_by_id(self, column_id: int) -> Optional[ColumnResponse]:
        """
        Получение колонки по ID
        
        Args:
            column_id: ID колонки
            
        Returns:
            Колонка или None если не найдена
        """
        result = await self.db.execute(
            select(Column).where(Column.id == column_id)
        )
        column = result.scalar_one_or_none()
        
        if column:
            return ColumnResponse.model_validate(column)
        return None

    async def get_column_by_id_deep(self, column_id: int) -> Optional[Column_deep_Response]:
        """
        Получение колонки по ID с глубокими данными (задачи, подзадачи, исполнители)
        """
        try:
            # 1. Получаем базовую колонку
            column = await self.get_column_by_id(column_id)
            
            if not column:
                return None
            
            # 2. Получаем все задачи колонки с глубокими данными
            from .._04_task.services import TaskService
            task_service = TaskService(self.db)
            tasks_deep = await task_service.get_task_by_column_deep(column_id)
            
            # 3. Преобразуем колонку в словарь и добавляем задачи
            column_dict = column.model_dump()
            column_dict['tasks'] = tasks_deep  # tasks_deep уже содержит подзадачи и исполнителей
            
            # 4. Создаем Column_deep_Response
            column_deep = Column_deep_Response.model_validate(column_dict)
            
            return column_deep
            
        except ValueError as e:
            print(f"ValueError in get_column_by_id_deep: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in get_column_by_id_deep: {e}")
            return None

    async def get_column_by_tab_id_deep(self, tab_id: int) -> List[Column_deep_Response]:
        """
        Получение всех колонок вкладки с глубокими данными (задачи, подзадачи, исполнители)
        """
        try:
            # 1. Получаем все колонки вкладки
            columns = await self.get_columns_by_tab_id(tab_id)
            
            if not columns:
                return []
            
            # 2. Для каждой колонки получаем глубокие данные
            deep_columns = []
            for column in columns:
                column_deep = await self.get_column_by_id_deep(column.id)
                if column_deep:
                    deep_columns.append(column_deep)
            
            return deep_columns
            
        except ValueError as e:
            print(f"ValueError in get_column_by_tab_id_deep: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in get_column_by_tab_id_deep: {e}")
            return []

    async def get_columns_by_tab_id(self, tab_id: int) -> List[ColumnResponse]:
        """
        Получение всех колонок таба
        
        Args:
            tab_id: ID таба
            
        Returns:
            Список колонок таба, отсортированных по order_id
            
        Raises:
            ValueError: Если таб не существует
        """
        # Проверяем существование таба
        if not await self._check_tab_exists(tab_id):
            raise ValueError(f"Таб с ID {tab_id} не существует")
        
        result = await self.db.execute(
            select(Column)
            .where(Column.tab_id == tab_id)
            .order_by(Column.order_id)
        )
        columns = result.scalars().all()
        
        return [ColumnResponse.model_validate(c) for c in columns]

    async def get_all_columns(self) -> List[ColumnResponse]:
        """
        Получение всех колонок
        
        Returns:
            Список всех колонок
        """
        result = await self.db.execute(select(Column))
        columns = result.scalars().all()
        
        return [ColumnResponse.model_validate(c) for c in columns]

    async def update_column(
        self, 
        column_id: int, 
        column_data: ColumnUpdate
    ) -> Optional[ColumnResponse]:
        """
        Обновление колонки
        
        Args:
            column_id: ID колонки
            column_data: Данные для обновления
            
        Returns:
            Обновленная колонка или None если не найдена
        """
        result = await self.db.execute(
            select(Column).where(Column.id == column_id)
        )
        column = result.scalar_one_or_none()
        
        if not column:
            return None
        
        # Сохраняем tab_id до обновления
        tab_id = column.tab_id
        
        # Обновляем только переданные поля
        if column_data.name is not None:
            column.name = column_data.name
        if column_data.order_id is not None:
            column.order_id = column_data.order_id
        if column_data.is_start is not None:
            column.is_start = column_data.is_start
        if column_data.is_final is not None:
            column.is_final = column_data.is_final
        if column_data.is_active is not None:
            column.is_active = column_data.is_active
        
        await self.db.commit()
        await self.db.refresh(column)
        
        # Используем сохраненный tab_id
        await self._touch_tab(tab_id)
        
        return ColumnResponse.model_validate(column)

    async def delete_column(self, column_id: int) -> bool:
        """
        Удаление колонки
        
        Args:
            column_id: ID колонки
            
        Returns:
            True если удалена, False если не найдена
        """
        result = await self.db.execute(
            select(Column).where(Column.id == column_id)
        )
        column = result.scalar_one_or_none()
        
        if not column:
            return False
        
        # Сохраняем tab_id до удаления
        tab_id = column.tab_id
        
        await self.db.delete(column)
        await self.db.commit()
        
        # Используем сохраненный tab_id
        await self._touch_tab(tab_id)
        
        return True

    async def normalize_column_orders(self, tab_id: int) -> List[ColumnResponse]:
        """
        Нормализация порядков колонок в табе
        
        Переназначает order_id всем колонкам таба последовательно от 1 до N
        
        Args:
            tab_id: ID таба
            
        Returns:
            Список колонок с обновленными порядками
            
        Raises:
            ValueError: Если таб не существует
        """
        # Проверяем существование таба
        if not await self._check_tab_exists(tab_id):
            raise ValueError(f"Таб с ID {tab_id} не существует")
        
        # Получаем все колонки таба, отсортированные по текущему order_id
        result = await self.db.execute(
            select(Column)
            .where(Column.tab_id == tab_id)
            .order_by(Column.order_id, Column.id)  # Сортируем по order_id, затем по id для стабильности
        )
        columns = result.scalars().all()
        
        # Присваиваем новые порядковые номера от 1 до N
        for index, column in enumerate(columns, start=1):
            column.order_id = index
        
        await self.db.commit()
        
        # Обновляем таб
        await self._touch_tab(tab_id)
        
        # Возвращаем обновленные колонки
        return [ColumnResponse.model_validate(column) for column in columns]

    async def reorder_columns(
        self, 
        tab_id: int, 
        new_order: List[int]
    ) -> List[ColumnResponse]:
        """
        Изменение порядка колонок в табе
        
        Args:
            tab_id: ID таба
            new_order: Список ID колонок в новом порядке
            
        Returns:
            Список колонок с обновленными порядками
            
        Raises:
            ValueError: Если таб не существует или список ID некорректен
        """
        # Проверяем существование таба
        if not await self._check_tab_exists(tab_id):
            raise ValueError(f"Таб с ID {tab_id} не существует")
        
        # Проверяем что список не пустой
        if not new_order:
            raise ValueError("Список ID колонок не может быть пустым")
        
        # Получаем все колонки таба
        result = await self.db.execute(
            select(Column).where(Column.tab_id == tab_id)
        )
        existing_columns = result.scalars().all()
        existing_column_ids = {col.id for col in existing_columns}
        
        # Проверяем что все ID из new_order существуют в табе
        new_order_set = set(new_order)
        if not new_order_set.issubset(existing_column_ids):
            invalid_ids = new_order_set - existing_column_ids
            raise ValueError(f"Колонки с ID {invalid_ids} не принадлежат табу {tab_id}")
        
        # Проверяем что количество ID совпадает
        if len(new_order) != len(existing_columns):
            raise ValueError(
                f"Количество ID в списке ({len(new_order)}) не совпадает "
                f"с количеством колонок в табе ({len(existing_columns)})"
            )
        
        # Обновляем order_id согласно новому порядку
        for index, column_id in enumerate(new_order, start=1):
            # Находим колонку по ID
            column = next((c for c in existing_columns if c.id == column_id), None)
            if column:
                column.order_id = index
        
        await self.db.commit()
        
        # Обновляем таб
        await self._touch_tab(tab_id)
        
        # Возвращаем колонки в новом порядке
        result = await self.db.execute(
            select(Column)
            .where(Column.tab_id == tab_id)
            .order_by(Column.order_id)
        )
        reordered_columns = result.scalars().all()
        
        return [ColumnResponse.model_validate(col) for col in reordered_columns]

    async def touch_column(self, column_id: int) -> Optional[ColumnResponse]:
        """
        Обновление только поля updated_at колонки и связанного таба
        
        Используется для обновления временной метки без изменения данных.
        
        Args:
            column_id: ID колонки
            
        Returns:
            Обновленная колонка или None если не найдена
        """
        result = await self.db.execute(
            select(Column).where(Column.id == column_id)
        )
        column = result.scalar_one_or_none()
        
        if not column:
            return None
        
        tab_id = column.tab_id
        
        # Принудительно обновляем updated_at колонки
        column.updated_at = func.now()
        
        await self.db.commit()
        await self.db.refresh(column)
        
        # Обновляем таб
        await self._touch_tab(tab_id)
        
        return ColumnResponse.model_validate(column)

    async def touch_columns_by_tab(self, tab_id: int) -> List[ColumnResponse]:
        """
        Обновление поля updated_at для всех колонок таба
        
        Args:
            tab_id: ID таба
            
        Returns:
            Список обновленных колонок
            
        Raises:
            ValueError: Если таб не существует
        """
        # Проверяем существование таба
        if not await self._check_tab_exists(tab_id):
            raise ValueError(f"Таб с ID {tab_id} не существует")
        
        # Получаем все колонки таба
        result = await self.db.execute(
            select(Column).where(Column.tab_id == tab_id)
        )
        columns = result.scalars().all()
        
        if not columns:
            return []
        
        # Обновляем updated_at для всех колонок
        now = func.now()
        for column in columns:
            column.updated_at = now
        
        await self.db.commit()
        
        # Обновляем объекты из БД
        for column in columns:
            await self.db.refresh(column)
        
        # Обновляем таб
        await self._touch_tab(tab_id)
        
        return [ColumnResponse.model_validate(column) for column in columns]

    async def bulk_touch_columns(self, column_ids: List[int]) -> List[ColumnResponse]:
        """
        Массовое обновление поля updated_at для нескольких колонок
        
        Args:
            column_ids: Список ID колонок
            
        Returns:
            Список обновленных колонок
        """
        if not column_ids:
            return []
        
        # Получаем все колонки по списку ID
        result = await self.db.execute(
            select(Column).where(Column.id.in_(column_ids))
        )
        columns = result.scalars().all()
        
        if not columns:
            return []
        
        # Сохраняем уникальные tab_id для обновления
        tab_ids = {column.tab_id for column in columns}
        
        # Обновляем updated_at для всех найденных колонок
        now = func.now()
        for column in columns:
            column.updated_at = now
        
        await self.db.commit()
        
        # Обновляем объекты из БД
        for column in columns:
            await self.db.refresh(column)
        
        # Обновляем все затронутые табы
        for tab_id in tab_ids:
            await self._touch_tab(tab_id)
        
        return [ColumnResponse.model_validate(column) for column in columns]