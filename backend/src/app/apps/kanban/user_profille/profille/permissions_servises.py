# src\app\apps\kanban\user_profille\profille\permissions_servises.py

from typing import List, Dict, Any, Optional

class PermissionService:
    
    @staticmethod
    def get_system_role(permissions: Dict) -> str:
        """Получить глобальную системную роль"""
        return permissions.get("system", {}).get("role", "user")

    @staticmethod
    def has_global_permission(permissions: Dict, flag: str) -> bool:
        """Проверить наличие глобального флага"""
        global_flags = permissions.get("system", {}).get("global_flags", [])
        role = PermissionService.get_system_role(permissions)
        
        # Админ имеет все права
        if role == "admin":
            return True
            
        return flag in global_flags

    @staticmethod
    def get_project_access(permissions: Dict, project_id: int) -> Optional[Dict]:
        """
        Получить данные доступа к конкретному проекту.
        Возвращает словарь вида {"role": "...", "permissions": [...]} или None.
        """
        projects = permissions.get("projects", [])
        for proj in projects:
            if proj.get("project_id") == project_id:
                return proj
        return None

    @staticmethod
    def can_access_project(permissions: Dict, project_id: int) -> bool:
        """Проверить, есть ли у пользователя доступ к проекту (любое право)"""
        return PermissionService.get_project_access(permissions, project_id) is not None

    @staticmethod
    def check_project_permission(permissions: Dict, project_id: int, required_permission: str) -> bool:
        """
        Проверяет наличие конкретного разрешения в проекте.
        
        Логика:
        1. Если роль admin -> True (безоговорочно).
        2. Если проекта нет в списке доступа -> False.
        3. Если у роли есть право 'all' -> True.
        4. Иначе проверяем наличие required_permission в списке прав проекта.
        
        Args:
            permissions: Словарь прав пользователя из БД.
            project_id: ID проекта.
            required_permission: Строка названия права (например, 'edit', 'view', 'delete').
            
        Returns:
            bool: True если доступ разрешен, иначе False.
        """
        # 1. Проверка на админа
        role = PermissionService.get_system_role(permissions)
        if role == "admin":
            return True

        # 2. Получаем данные по проекту
        project_data = PermissionService.get_project_access(permissions, project_id)
        
        # Если проекта нет в списке -> нет доступа
        if not project_data:
            return False

        # 3. Получаем список прав для этого проекта
        project_perms = project_data.get("permissions", [])

        # 4. Если есть универсальное право 'all' -> доступ разрешен
        if "all" in project_perms:
            return True

        # 5. Проверяем наличие конкретного права
        return required_permission in project_perms

    @staticmethod
    def add_project_access(permissions: Dict, project_id: int, role: str = "viewer", perms: List[str] = None) -> Dict:
        """
        Добавить доступ к проекту. Если проект уже есть - обновляет.
        """
        if perms is None:
            # Дефолтные права для роли
            perms_map = {
                "owner": ["all"],
                "editor": ["view", "edit", "create_task"],
                "viewer": ["view"]
            }
            perms = perms_map.get(role, ["view"])

        new_entry = {
            "project_id": project_id,
            "role": role,
            "permissions": perms
        }

        projects = permissions.get("projects", [])
        
        # Удаляем старую запись, если была
        projects = [p for p in projects if p.get("project_id") != project_id]
        
        # Добавляем новую
        projects.append(new_entry)
        
        permissions["projects"] = projects
        return permissions

    @staticmethod
    def remove_project_access(permissions: Dict, project_id: int) -> Dict:
        """Удалить доступ к проекту"""
        projects = permissions.get("projects", [])
        permissions["projects"] = [p for p in projects if p.get("project_id") != project_id]
        return permissions