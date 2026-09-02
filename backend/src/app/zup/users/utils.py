


def normalise_employee_id(employee_id: str):
    """Нормализация employee_id к ЗУП состоянию"""
    employee_id.lower()
    if employee_id[:5] == "gw070":
        employee_id = '0' * 5 + employee_id[5:]
    return employee_id