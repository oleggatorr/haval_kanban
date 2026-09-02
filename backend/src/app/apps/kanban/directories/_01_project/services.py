from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from sqlalchemy.sql import func

from .models import Project
from .schemas import ProjectCreate, ProjectUpdate, ProjectResponse, Project_deep_Response


class ProjectService:
    """Сервис для работы с проектами"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def touch_project(self, project_id: int) -> Optional[ProjectResponse]:
        """
        Обновление только поля updated_at (касание проекта)
        
        Args:
            project_id: ID проекта
            
        Returns:
            Обновленный проект или None если не найден
        """
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()
        
        if not project:
            return None
        
        # Принудительно обновляем updated_at
        project.updated_at = func.now()
        
        await self.db.commit()
        await self.db.refresh(project)
        
        return ProjectResponse.model_validate(project)

    async def create_project(self, project_data: ProjectCreate) -> ProjectResponse:
        """
        Создание нового проекта
        
        Args:
            project_data: Данные для создания проекта
            
        Returns:
            Созданный проект
        """
        db_project = Project(
            name=project_data.name,
            description=project_data.description
        )
        
        self.db.add(db_project)
        await self.db.commit()
        await self.db.refresh(db_project)
        
        return ProjectResponse.model_validate(db_project)

    async def get_project_by_id(self, project_id: int) -> Optional[ProjectResponse]:
        """
        Получение проекта по ID
        
        Args:
            project_id: ID проекта
            
        Returns:
            Проект или None если не найден
        """
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()
        
        if project:
            return ProjectResponse.model_validate(project)
        return None

    async def get_project_updated_at(self, project_id: int) -> Optional[dict]:
        """
        Получение временной метки обновления проекта с проверкой существования
        
        Args:
            project_id: ID проекта
            
        Returns:
            Словарь с id и updated_at или None если проект не найден
        """
        result = await self.db.execute(
            select(Project.id, Project.updated_at).where(Project.id == project_id)
        )
        row = result.first()
        
        if not row:
            return None
        
        return {
            "id": row.id,
            "updated_at": row.updated_at
        }
    
    async def get_all_projects(self) -> List[ProjectResponse]:
        """
        Получение всех проектов
        
        Returns:
            Список всех проектов
        """
        result = await self.db.execute(select(Project))
        projects = result.scalars().all()
        
        return [ProjectResponse.model_validate(p) for p in projects]

    async def update_project(
        self, 
        project_id: int, 
        project_data: ProjectUpdate
    ) -> Optional[ProjectResponse]:
        """
        Обновление проекта
        
        Args:
            project_id: ID проекта
            project_data: Данные для обновления
            
        Returns:
            Обновленный проект или None если не найден
        """
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()
        
        if not project:
            return None
        
        # Обновляем только переданные поля
        if project_data.name is not None:
            project.name = project_data.name
        if project_data.description is not None:
            project.description = project_data.description
        
        await self.db.commit()
        await self.db.refresh(project)
        
        return ProjectResponse.model_validate(project)

    async def delete_project(self, project_id: int) -> bool:
        """
        Удаление проекта
        
        Args:
            project_id: ID проекта
            
        Returns:
            True если удален, False если не найден
        """
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()
        
        if not project:
            return False
        
        await self.db.delete(project)
        await self.db.commit()
        
        return True


    async def get_project_by_id_deep(self, project_id: int) -> Optional[Project_deep_Response]:
        """"""
        try:
            # 1. Получаем базовый проект
            project = await self.get_project_by_id(project_id)
            
            if not project:
                return None
            
            # 2. Получаем все табы проекта с глубокими данными
            from .._02_tab.services import TabService
            tab_service = TabService(self.db)
            tabs_deep = await tab_service.get_tabs_by_project_id_deep(project_id)
            
            # 3. Преобразуем проект в словарь и добавляем табы
            project_dict = project.model_dump()
            project_dict['tabs'] = tabs_deep
            
            # 4. Создаем Project_deep_Response
            project_deep = Project_deep_Response.model_validate(project_dict)
            
            return project_deep
            
        except ValueError as e:
            print(f"ValueError in get_project_by_id_deep: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in get_project_by_id_deep: {e}")
            return None