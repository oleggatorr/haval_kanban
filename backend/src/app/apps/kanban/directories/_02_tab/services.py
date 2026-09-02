from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional
from sqlalchemy.sql import func

from .models import Tab
from .._01_project.models import Project
from .._01_project.services import ProjectService
from .schemas import TabCreate, TabUpdate, TabResponse, Tab_deep_Response


class TabService:
    """Сервис для работы с табами"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_project_exists(self, project_id: int) -> bool:
        """
        Проверка существования проекта
        
        Args:
            project_id: ID проекта
            
        Returns:
            True если проект существует, иначе False
        """
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none() is not None

    async def _touch_project(self, project_id: int) -> None:
        """
        Обновление временной метки проекта
        
        Args:
            project_id: ID проекта
        """
        project_service = ProjectService(self.db)
        await project_service.touch_project(project_id)

    async def create_tab(self, tab_data: TabCreate) -> TabResponse:
        """
        Создание нового таба
        
        Args:
            tab_data: Данные для создания таба
            
        Returns:
            Созданный таб
            
        Raises:
            ValueError: Если проект не существует
        """
        # Проверяем существование проекта
        if not await self._check_project_exists(tab_data.project_id):
            raise ValueError(f"Проект с ID {tab_data.project_id} не существует")
        
        db_tab = Tab(
            project_id=tab_data.project_id,
            name=tab_data.name,
            order_id=tab_data.order_id
        )
        
        self.db.add(db_tab)
        await self.db.commit()
        await self.db.refresh(db_tab)
        
        # Нормализуем порядки и обновляем проект
        await self.normalize_tab_orders(project_id=tab_data.project_id)
        await self._touch_project(tab_data.project_id)
        
        return TabResponse.model_validate(db_tab)

    async def get_tabs_by_project_id(self, project_id: int) -> List[TabResponse]:
        """
        Получение всех табов проекта
        
        Args:
            project_id: ID проекта
            
        Returns:
            Список табов проекта, отсортированных по order_id
            
        Raises:
            ValueError: Если проект не существует
        """
        # Проверяем существование проекта
        if not await self._check_project_exists(project_id):
            raise ValueError(f"Проект с ID {project_id} не существует")
        
        result = await self.db.execute(
            select(Tab)
            .where(Tab.project_id == project_id)
            .order_by(Tab.order_id)
        )
        tabs = result.scalars().all()
        
        return [TabResponse.model_validate(t) for t in tabs]

    async def get_tab_by_id(self, tab_id: int) -> Optional[TabResponse]:
        """
        Получение таба по ID
        
        Args:
            tab_id: ID таба
            
        Returns:
            Таб или None если не найден
        """
        result = await self.db.execute(
            select(Tab).where(Tab.id == tab_id)
        )
        tab = result.scalar_one_or_none()
        
        if tab:
            return TabResponse.model_validate(tab)
        return None

    async def get_tab_by_id_deep(self, tab_id: int) -> Optional[Tab_deep_Response]:
        """
            Получение вкладки по ID с глубокими данными (колонки, задачи, подзадачи, исполнители)
        """
        
        try:
            # 1. Получаем базовую вкладку
            tab = await self.get_tab_by_id(tab_id)
            
            if not tab:
                return None
            
            # 2. Получаем все колонки вкладки с глубокими данными
            from .._03_column.services import ColumnService
            column_service = ColumnService(self.db)
            columns_deep = await column_service.get_column_by_tab_id_deep(tab_id)
            
            # 3. Преобразуем вкладку в словарь и добавляем колонки
            tab_dict = tab.model_dump()
            tab_dict['columns'] = columns_deep
            
            # 4. Создаем Tab_deep_Response
            tab_deep = Tab_deep_Response.model_validate(tab_dict)
            
            return tab_deep
            
        except ValueError as e:
            print(f"ValueError in get_tab_by_id_deep: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in get_tab_by_id_deep: {e}")
            return None

    async def get_tabs_by_project_id_deep(self, project_id: int) -> List[Tab_deep_Response]:
        """
        Получение всех табов проекта с глубокими данными (колонки, задачи, подзадачи, исполнители)
        
        Args:
            project_id: ID проекта
            
        Returns:
            Список табов проекта с глубокими данными
            
        Raises:
            ValueError: Если проект не существует
        """
        try:
            # 1. Проверяем существование проекта
            if not await self._check_project_exists(project_id):
                raise ValueError(f"Проект с ID {project_id} не существует")
            
            # 2. Получаем все табы проекта
            tabs = await self.get_tabs_by_project_id(project_id)
            
            if not tabs:
                return []
            
            # 3. Для каждого таба получаем глубокие данные
            deep_tabs = []
            for tab in tabs:
                tab_deep = await self.get_tab_by_id_deep(tab.id)
                if tab_deep:
                    deep_tabs.append(tab_deep)
            
            return deep_tabs
            
        except ValueError as e:
            print(f"ValueError in get_tabs_by_project_id_deep: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in get_tabs_by_project_id_deep: {e}")
            return []

    async def get_all_tabs(self) -> List[TabResponse]:
        """
        Получение всех табов
        
        Returns:
            Список всех табов
        """
        result = await self.db.execute(select(Tab).order_by(Tab.order_id).order_by(Tab.project_id))
        tabs = result.scalars().all()
        
        return [TabResponse.model_validate(t) for t in tabs]

    async def update_tab(
        self, 
        tab_id: int, 
        tab_data: TabUpdate
    ) -> Optional[TabResponse]:
        """
        Обновление таба
        
        Args:
            tab_id: ID таба
            tab_data: Данные для обновления
            
        Returns:
            Обновленный таб или None если не найден
        """
        result = await self.db.execute(
            select(Tab).where(Tab.id == tab_id)
        )
        tab = result.scalar_one_or_none()
        
        if not tab:
            return None
        
        project_id = tab.project_id
        
        # Обновляем только переданные поля
        if tab_data.name is not None:
            tab.name = tab_data.name
        if tab_data.order_id is not None:
            tab.order_id = tab_data.order_id
        
        await self.db.commit()
        await self.db.refresh(tab)
        
        # Обновляем проект
        await self._touch_project(project_id)
        
        return TabResponse.model_validate(tab)

    async def delete_tab(self, tab_id: int) -> bool:
        """
        Удаление таба
        
        Args:
            tab_id: ID таба
            
        Returns:
            True если удален, False если не найден
        """
        result = await self.db.execute(
            select(Tab).where(Tab.id == tab_id)
        )
        tab = result.scalar_one_or_none()
        
        if not tab:
            return False
        
        project_id = tab.project_id
        
        await self.db.delete(tab)
        await self.db.commit()
        
        # Нормализуем порядки и обновляем проект
        await self.normalize_tab_orders(project_id=project_id)
        await self._touch_project(project_id)
        
        return True

    async def normalize_tab_orders(self, project_id: int) -> List[TabResponse]:
        """
        Нормализация порядков табов в проекте
        
        Переназначает order_id всем табам проекта последовательно от 1 до N
        
        Args:
            project_id: ID проекта
            
        Returns:
            Список табов с обновленными порядками
            
        Raises:
            ValueError: Если проект не существует
        """
        # Проверяем существование проекта
        if not await self._check_project_exists(project_id):
            raise ValueError(f"Проект с ID {project_id} не существует")
        
        # Получаем все табы проекта, отсортированные по текущему order_id
        result = await self.db.execute(
            select(Tab)
            .where(Tab.project_id == project_id)
            .order_by(Tab.order_id, Tab.id)  # Сортируем по order_id, затем по id для стабильности
        )
        tabs = result.scalars().all()
        
        # Присваиваем новые порядковые номера от 1 до N
        for index, tab in enumerate(tabs, start=1):
            tab.order_id = index
        
        await self.db.commit()
        
        # Возвращаем обновленные табы
        return [TabResponse.model_validate(tab) for tab in tabs]

    async def reorder_tabs(
        self, 
        project_id: int, 
        new_order: List[int]
    ) -> List[TabResponse]:
        """
        Изменение порядка табов в проекте
        
        Args:
            project_id: ID проекта
            new_order: Список ID табов в новом порядке
            
        Returns:
            Список табов с обновленными порядками
            
        Raises:
            ValueError: Если проект не существует или список ID некорректен
        """
        # Проверяем существование проекта
        if not await self._check_project_exists(project_id):
            raise ValueError(f"Проект с ID {project_id} не существует")
        
        # Проверяем что список не пустой
        if not new_order:
            raise ValueError("Список ID табов не может быть пустым")
        
        # Получаем все табы проекта
        result = await self.db.execute(
            select(Tab).where(Tab.project_id == project_id)
        )
        existing_tabs = result.scalars().all()
        existing_tab_ids = {tab.id for tab in existing_tabs}
        
        # Проверяем что все ID из new_order существуют в проекте
        new_order_set = set(new_order)
        if not new_order_set.issubset(existing_tab_ids):
            invalid_ids = new_order_set - existing_tab_ids
            raise ValueError(f"Табы с ID {invalid_ids} не принадлежат проекту {project_id}")
        
        # Проверяем что количество ID совпадает
        if len(new_order) != len(existing_tabs):
            raise ValueError(
                f"Количество ID в списке ({len(new_order)}) не совпадает "
                f"с количеством табов в проекте ({len(existing_tabs)})"
            )
        
        # Обновляем order_id согласно новому порядку
        for index, tab_id in enumerate(new_order, start=1):
            # Находим таб по ID
            tab = next((t for t in existing_tabs if t.id == tab_id), None)
            if tab:
                tab.order_id = index
        
        await self.db.commit()
        
        # Обновляем проект
        await self._touch_project(project_id)
        
        # Возвращаем табы в новом порядке
        result = await self.db.execute(
            select(Tab)
            .where(Tab.project_id == project_id)
            .order_by(Tab.order_id)
        )
        reordered_tabs = result.scalars().all()
        
        return [TabResponse.model_validate(tab) for tab in reordered_tabs]

    async def touch_tab(self, tab_id: int) -> Optional[TabResponse]:
        """
        Обновление только поля updated_at (касание таба)
        
        Используется для обновления временной метки без изменения данных.
        Полезно, например, когда нужно отметить таб как "активный" или 
        обновить кэш связанных данных.
        
        Args:
            tab_id: ID таба
            
        Returns:
            Обновленный таб или None если не найден
        """
        result = await self.db.execute(
            select(Tab).where(Tab.id == tab_id)
        )
        tab = result.scalar_one_or_none()
        
        if not tab:
            return None
        
        project_id = tab.project_id
        
        # Принудительно обновляем updated_at
        tab.updated_at = func.now()
        
        await self.db.commit()
        await self.db.refresh(tab)
        
        # Обновляем проект
        await self._touch_project(project_id)
        
        return TabResponse.model_validate(tab)

    async def touch_tabs_by_project(self, project_id: int) -> List[TabResponse]:
        """
        Обновление поля updated_at для всех табов проекта
        
        Args:
            project_id: ID проекта
            
        Returns:
            Список обновленных табов
            
        Raises:
            ValueError: Если проект не существует
        """
        # Проверяем существование проекта
        if not await self._check_project_exists(project_id):
            raise ValueError(f"Проект с ID {project_id} не существует")
        
        # Получаем все табы проекта
        result = await self.db.execute(
            select(Tab).where(Tab.project_id == project_id)
        )
        tabs = result.scalars().all()
        
        if not tabs:
            return []
        
        # Обновляем updated_at для всех табов
        now = func.now()
        for tab in tabs:
            tab.updated_at = now
        
        await self.db.commit()
        
        # Обновляем объекты из БД
        for tab in tabs:
            await self.db.refresh(tab)
        
        # Обновляем проект
        await self._touch_project(project_id)
        
        return [TabResponse.model_validate(tab) for tab in tabs]

    async def bulk_touch_tabs(self, tab_ids: List[int]) -> List[TabResponse]:
        """
        Массовое обновление поля updated_at для нескольких табов
        
        Args:
            tab_ids: Список ID табов
            
        Returns:
            Список обновленных табов
        """
        if not tab_ids:
            return []
        
        # Получаем все табы по списку ID
        result = await self.db.execute(
            select(Tab).where(Tab.id.in_(tab_ids))
        )
        tabs = result.scalars().all()
        
        if not tabs:
            return []
        
        # Сохраняем уникальные project_id для обновления
        project_ids = {tab.project_id for tab in tabs}
        
        # Обновляем updated_at для всех найденных табов
        now = func.now()
        for tab in tabs:
            tab.updated_at = now
        
        await self.db.commit()
        
        # Обновляем объекты из БД
        for tab in tabs:
            await self.db.refresh(tab)
        
        # Обновляем все затронутые проекты
        for project_id in project_ids:
            await self._touch_project(project_id)
        
        return [TabResponse.model_validate(tab) for tab in tabs]