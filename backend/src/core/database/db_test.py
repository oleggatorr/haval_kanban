#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестового подключения к PostgreSQL
SQLAlchemy 2.0 compatible
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import time
from datetime import datetime

from sqlalchemy import text

from config.settings import settings
from src.core.database.connection import (
    engine,
    SessionLocal,
    get_db_connection
)


def print_header(title: str):
    print(f"\n{'=' * 60}")
    print(f"🔍 {title}")
    print(f"{'=' * 60}")


def print_result(
    test_name: str,
    success: bool,
    message: str,
    details: dict = None
):
    status = "✅ PASS" if success else "❌ FAIL"

    print(f"\n[{status}] {test_name}")
    print(f"   └─ {message}")

    if details:
        for key, value in details.items():
            print(f"      • {key}: {value}")

    return success


def _fetch_row_dict(result):
    """
    SQLAlchemy 2.0 safe fetch
    Возвращает первую строку результата как dict
    """
    row = result.mappings().first()

    if row is None:
        return {}

    return dict(row)


def test_sqlalchemy_pool():
    """
    Тест подключения через SQLAlchemy Engine + Pool
    """
    test_name = "SQLAlchemy Engine + Pool"

    try:
        start = time.time()

        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT
                        1 as test,
                        version() as version,
                        current_user as user,
                        current_database() as database
                """)
            )

            data = _fetch_row_dict(result)

        elapsed = (time.time() - start) * 1000

        return print_result(
            test_name,
            True,
            f"Подключение успешно, время: {elapsed:.1f} мс",
            {
                "test": data.get("test"),
                "version": data.get("version"),
                "user": data.get("user"),
                "database": data.get("database"),
                "pool_size": engine.pool.size(),
                "checked_out": engine.pool.checkedout()
            }
        )

    except Exception as e:
        return print_result(
            test_name,
            False,
            f"Ошибка: {type(e).__name__}",
            {
                "details": str(e)
            }
        )


def test_sqlalchemy_session():
    """
    Тест работы ORM Session
    """
    test_name = "SQLAlchemy Session (ORM)"

    try:
        start = time.time()

        with SessionLocal() as session:
            db_name = session.execute(
                text("SELECT current_database()")
            ).scalar_one()

        elapsed = (time.time() - start) * 1000

        return print_result(
            test_name,
            True,
            f"Сессия создана, БД: {db_name}, время: {elapsed:.1f} мс"
        )

    except Exception as e:
        return print_result(
            test_name,
            False,
            f"Ошибка: {type(e).__name__}",
            {
                "details": str(e)
            }
        )


def test_direct_connection():
    """
    Тест прямого подключения через psycopg2
    """
    test_name = "Direct Connection (psycopg2)"

    try:
        start = time.time()

        conn = get_db_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        1 + 1 as result,
                        NOW() as now
                """)

                row = cursor.fetchone()

        finally:
            conn.close()

        elapsed = (time.time() - start) * 1000

        return print_result(
            test_name,
            True,
            f"Прямое подключение успешно, время: {elapsed:.1f} мс",
            {
                "result": row[0],
                "now": row[1]
            }
        )

    except Exception as e:
        return print_result(
            test_name,
            False,
            f"Ошибка: {type(e).__name__}",
            {
                "details": str(e)
            }
        )


def test_permissions():
    """
    Проверка прав пользователя
    """
    test_name = "Проверка прав (read-only)"

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT COUNT(*) as tables_count
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
            )

            data = _fetch_row_dict(result)
            tables_count = data.get("tables_count", 0)

        return print_result(
            test_name,
            True,
            f"Таблиц в схеме public: {tables_count}, чтение: ✅ подтверждено",
            {
                "tables_count": tables_count
            }
        )

    except Exception as e:
        return print_result(
            test_name,
            False,
            f"Ошибка: {type(e).__name__}",
            {
                "details": str(e)
            }
        )


def test_ssl_connection():
    """
    Проверка SSL-соединения
    """
    test_name = "Проверка SSL-соединения"

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT ssl_is_used()")
            )

            ssl_used = result.scalar_one()

        return print_result(
            test_name,
            True,
            f"Шифрование: {'✅ активно' if ssl_used else '⚠️ не используется'}",
            {
                "ssl_used": ssl_used
            }
        )

    except Exception as e:
        return print_result(
            test_name,
            False,
            f"Не удалось проверить: {type(e).__name__}",
            {
                "details": str(e)
            }
        )


def main():
    """
    Главная функция
    """
    print_header(
        f"Тест подключения к PostgreSQL "
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
    )

    print("\n📋 Конфигурация:")

    print(
        f"   • Хост: "
        f"{settings.DB_HOST}:{settings.DB_PORT}"
    )

    print(
        f"   • БД: "
        f"{settings.DB_NAME}"
    )

    print(
        f"   • Пользователь: "
        f"{settings.DB_USER}"
    )

    print(
        f"   • SSL: "
        f"{'✅' if getattr(settings, 'PG_SSL_MODE', '') == 'require' else '⚠️ отключён'}"
    )

    print(
        f"   • Pool size: "
        f"{settings.DB_POOL_SIZE} (+{settings.DB_MAX_OVERFLOW})"
    )

    results = [
        test_sqlalchemy_pool(),
        test_sqlalchemy_session(),
        test_direct_connection(),
        test_permissions(),
        test_ssl_connection()
    ]

    print_header("ИТОГИ")

    passed = sum(results)
    total = len(results)

    print(f"\n📊 Пройдено тестов: {passed}/{total}")

    if passed == total:
        print(
            "\n🎉 Все проверки пройдены! "
            "Подключение работает корректно."
        )
        return 0
    else:
        print(f"\n⚠️ Не пройдено тестов: {total - passed}")
        print("   Проверьте настройки и права доступа.")
        return 1


if __name__ == "__main__":
    sys.exit(main())