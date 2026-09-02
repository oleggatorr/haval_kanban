from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import String, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

# Предполагается, что у вас есть базовый класс Base
from ..database.zup_connection import get_db, Base

class ZupDepartment(Base):
    __tablename__ = "zup_departments"

    # Основные поля
    guid: Mapped[str] = mapped_column(String(36), primary_key=True, comment="GUID отдела")
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="Название отдела")
    name_en: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="Название отдела (EN)")
    short_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Краткое название")
    
    # Даты
    creation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="Дата создания")
    closure_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="Дата закрытия")
    
    # Иерархия
    parent_guid: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("zup_departments.guid"), 
        nullable=True, 
        comment="GUID родительского отдела"
    )
    
    # Системные метки времени
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="Дата создания записи")
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Дата обновления записи")

    # Отношения (Relationships)
    # Родительский отдел
    parent: Mapped[Optional["ZupDepartment"]] = relationship(
        "ZupDepartment", 
        back_populates="children", 
        remote_side=[guid],
        lazy="selectin"  # Рекомендуется selectin для асинхронного режима
    )
    
    # Дочерние отделы
    children: Mapped[List["ZupDepartment"]] = relationship(
        "ZupDepartment", 
        back_populates="parent",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<ZupDepartment(guid={self.guid}, name='{self.name}')>"