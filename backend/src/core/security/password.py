from passlib.context import CryptContext

# Настройка алгоритма хеширования
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(
    password: str
) -> str:
    """
    Хеширует пароль перед сохранением в БД
    """

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Проверяет соответствие пароля хешу
    """

    return pwd_context.verify(
        plain_password,
        hashed_password
    )