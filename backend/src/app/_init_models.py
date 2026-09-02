# src/app/models.py

# Импортируем все модели, чтобы они зарегистрировались в Base.metadata
# Порядок важен: сначала те, от которых зависят другие, но обычно SQLAlchemy справляется сама.

# from src.app.users.models import User
# from src.app.knowledge_base.models import Department
# from src.app.messages.models import Chat, Message, MessageAttachment, chat_participants, message_reads

# Kanban models
# from src.app.kanban._01_project.models import Project, UserProject
# from src.app.kanban._02_tab.models import Tab
# from src.app.kanban._03_column.models import Column
# from src.app.kanban._04_task.models import Task
# from src.app.kanban._05_sub_task.models import Sub_Task

from src.app.user_auth.users.models import AuthUser

from .apps.kanban.__init__models import *