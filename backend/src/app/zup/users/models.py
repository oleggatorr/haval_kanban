from sqlalchemy import Column, String, Date, DateTime
from ..database.zup_connection import get_db, Base


class Employee(Base):
    """Модель сотрудника"""
    __tablename__ = 'zup_employees'  # замените на реальное имя таблицы
    
    guid = Column(String(36), primary_key=True)
    guid_person = Column(String(36), nullable=True)
    employee_id = Column(String(20), nullable=False, index=True)
    last_name = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    middle_name = Column(String(100), nullable=True)
    last_name_en = Column(String(100), nullable=True)
    first_name_en = Column(String(100), nullable=True)
    middle_name_en = Column(String(100), nullable=True)
    birth_date = Column(Date, nullable=True)
    employment_date = Column(Date, nullable=True)
    dismissal_date = Column(Date, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    position_guid = Column(String(36), nullable=True)
    department_guid = Column(String(36), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        """Конвертация в словарь"""
        return {
            'guid': self.guid,
            'guid_person': self.guid_person,
            'employee_id': self.employee_id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name_en': self.last_name_en,
            'first_name_en': self.first_name_en,
            'middle_name_en': self.middle_name_en,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'employment_date': self.employment_date.isoformat() if self.employment_date else None,
            'dismissal_date': self.dismissal_date.isoformat() if self.dismissal_date else None,
            'phone': self.phone,
            'email': self.email,
            'position_guid': self.position_guid,
            'department_guid': self.department_guid,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }