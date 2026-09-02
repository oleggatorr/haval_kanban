from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from .models import ZupDepartment
from .schemas import DepartmentRead, DepartmentTree


class DepartmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_departments(self) -> List[ZupDepartment]:
        """Получить плоский список всех отделов"""
        stmt = select(ZupDepartment).order_by(ZupDepartment.name)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_department_by_guid(self, guid: str) -> Optional[ZupDepartment]:
        """Получить конкретный отдел по GUID"""
        stmt = select(ZupDepartment).where(ZupDepartment.guid == guid)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_departments(self) -> List[ZupDepartment]:
        """Получить только активные отделы (где нет даты закрытия)"""
        stmt = (
            select(ZupDepartment)
            .where(ZupDepartment.closure_date.is_(None))
            .order_by(ZupDepartment.name)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def search_by_name(self, search_term: str) -> List[ZupDepartment]:
        """
        Поиск отделов по названию (регистронезависимый, частичное совпадение).
        Ищет как в name, так и в name_en.
        """
        pattern = f"%{search_term}%"
        stmt = (
            select(ZupDepartment)
            .where(
                (ZupDepartment.name.ilike(pattern)) | 
                (ZupDepartment.name_en.ilike(pattern))
            )
            .order_by(ZupDepartment.name)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_parent_guid(self, parent_guid: str) -> List[ZupDepartment]:
        """Получить список дочерних отделов для конкретного родителя"""
        stmt = (
            select(ZupDepartment)
            .where(ZupDepartment.parent_guid == parent_guid)
            .order_by(ZupDepartment.name)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def search_by_short_name(self, short_name: str) -> List[ZupDepartment]:
        """
        Поиск отделов по короткому имени (частичное совпадение).
        """
        pattern = f"%{short_name}%"
        stmt = (
            select(ZupDepartment)
            .where(ZupDepartment.short_name.ilike(pattern))
            .order_by(ZupDepartment.name)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def build_department_tree(self) -> List[DepartmentTree]:
        """
        Построить дерево только из активных отделов (без даты закрытия).
        """
        # 1. Загружаем ТОЛЬКО активные отделы
        all_depts = await self.get_active_departments()
        
        # 2. Создаем словари схем Pydantic напрямую из атрибутов модели
        dept_map = {}
        for d in all_depts:
            dept_schema = DepartmentTree(
                guid=d.guid,
                name=d.name,
                name_en=d.name_en,
                short_name=d.short_name,
                creation_date=d.creation_date,
                closure_date=d.closure_date,
                parent_guid=d.parent_guid,
                created_at=d.created_at,
                updated_at=d.updated_at,
                children=[] 
            )
            dept_map[d.guid] = dept_schema

        root_nodes = []

        # 3. Собираем иерархию в памяти
        for dept in dept_map.values():
            # Проверяем, существует ли родитель в нашем списке активных отделов
            if dept.parent_guid and dept.parent_guid in dept_map:
                parent = dept_map[dept.parent_guid]
                parent.children.append(dept)
            else:
                root_nodes.append(dept)
                
        return root_nodes