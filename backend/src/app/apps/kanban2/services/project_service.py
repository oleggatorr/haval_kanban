from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.projects.Project import Project
from ..models.projects.ProjectData import ProjectData
from ..schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """Сервис для работы с проектами."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Получить проект по ID."""
        query = (
            select(Project)
            .options(
                selectinload(Project.data),
                selectinload(Project.cards)
            )
            .where(Project.id == project_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_projects(
        self, 
        page: int = 1, 
        page_size: int = 10,
        is_active: Optional[bool] = None
    ) -> tuple[list[Project], int]:
        """Получить список проектов с пагинацией."""
        
        # Базовый запрос
        query = select(Project).options(selectinload(Project.data))
        
        # Фильтрация по активности
        if is_active is not None:
            query = query.where(Project.is_active == is_active)
        
        # Получаем общее количество
        count_query = select(func.count()).select_from(Project)
        if is_active is not None:
            count_query = count_query.where(Project.is_active == is_active)
        
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Пагинация
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(Project.create_at.desc())
        
        result = await self.db.execute(query)
        projects = result.scalars().all()
        
        return list(projects), total
    
    async def create_project(self, project_data: ProjectCreate) -> Project:
        """Создать новый проект."""
        
        # Создаем основной объект проекта
        project = Project(
            name=project_data.name,
            is_active=True
        )
        
        self.db.add(project)
        await self.db.flush()  # Получаем ID проекта
        
        # Если есть дополнительные данные, создаем их
        if project_data.data:
            project_data_obj = ProjectData(
                project_id=project.id,
                big_description=project_data.data.big_description
            )
            self.db.add(project_data_obj)
        
        await self.db.commit()
        await self.db.refresh(project)
        
        # Загружаем связанные данные
        await self.db.refresh(project, ['data'])
        
        return project
    
    async def update_project(
        self, 
        project_id: int, 
        project_data: ProjectUpdate
    ) -> Optional[Project]:
        """Обновить проект."""
        
        project = await self.get_project_by_id(project_id)
        if not project:
            return None
        
        # Обновляем основные поля
        if project_data.name is not None:
            project.name = project_data.name
        
        if project_data.is_active is not None:
            project.is_active = project_data.is_active
        
        # Обновляем дополнительные данные
        if project_data.data:
            if project.data:
                # Обновляем существующие данные
                if project_data.data.big_description is not None:
                    project.data.big_description = project_data.data.big_description
            else:
                # Создаем новые данные
                new_data = ProjectData(
                    project_id=project.id,
                    big_description=project_data.data.big_description
                )
                self.db.add(new_data)
        
        await self.db.commit()
        await self.db.refresh(project)
        await self.db.refresh(project, ['data'])
        
        return project
    
    async def delete_project(self, project_id: int) -> bool:
        """Мягко удалить проект (установить флаг удаления)."""
        
        project = await self.get_project_by_id(project_id)
        if not project:
            return False
        
        project.is_active = False
        project.remove_at = datetime.now(timezone.utc)
        
        await self.db.commit()
        return True
    
    async def hard_delete_project(self, project_id: int) -> bool:
        """Полностью удалить проект из базы данных."""
        
        project = await self.get_project_by_id(project_id)
        if not project:
            return False
        
        await self.db.delete(project)
        await self.db.commit()
        return True