from typing import Any
from sqlmodel import select, or_
from backend.storage.database import get_session
from backend.storage.models import Employee


class EmployeeCRUD:
    """CRUD operations and business logic for Employee management"""

    @staticmethod
    def create_employee(data: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new employee

        Args:
            data: dict with employee information
        """
        try:
            with get_session() as session:
                # Check if employee with same name already exists
                existing = session.exec(
                    select(Employee).where(Employee.name == data["name"])
                ).first()

                if existing:
                    return {"success": False, "error": "Employee with this name already exists"}

                employee = Employee(**data)
                session.add(employee)
                session.commit()
                session.refresh(employee)

                return {
                    "success": True,
                    "data": {
                        "id": employee.id,
                        "name": employee.name,
                        "position": employee.position,
                        "salary": employee.salary,
                        "date_hired": employee.date_hired
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_employee_by_id(employee_id: int) -> dict[str, Any]:
        """Get employee by ID"""
        try:
            with get_session() as session:
                employee = session.get(Employee, employee_id)
                if not employee:
                    return {"success": False, "error": "Employee not found"}

                return {
                    "success": True,
                    "data": {
                        "id": employee.id,
                        "name": employee.name,
                        "position": employee.position,
                        "salary": employee.salary,
                        "date_hired": employee.date_hired
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_employees() -> dict[str, Any]:
        """Get all employees with optional filtering"""
        try:
            with get_session() as session:
                employees = session.exec(select(Employee)).all()
                return {
                    "success": True,
                    "data": [
                        {
                            "id": emp.id,
                            "name": emp.name,
                            "position": emp.position,
                            "salary": emp.salary,
                            "date_hired": emp.date_hired
                        } for emp in employees
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def search_employees(search_term: str) -> dict[str, Any]:
        """Search employees by name or position"""
        try:
            with get_session() as session:
                employees = session.exec(
                    select(Employee).where(
                        or_(
                            Employee.name.contains(search_term),
                            Employee.position.contains(search_term)
                        )
                    )
                ).all()

                return {
                    "success": True,
                    "data": [
                        {
                            "id": emp.id,
                            "name": emp.name,
                            "position": emp.position,
                            "salary": emp.salary,
                            "date_hired": emp.date_hired
                        } for emp in employees
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_employee(employee_id: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update employee information"""
        try:
            with get_session() as session:
                employee = session.get(Employee, employee_id)
                if not employee:
                    return {"success": False, "error": "Employee not found"}

                # Update fields if provided
                for field, value in data.items():
                    if hasattr(employee, field) and value is not None:
                        setattr(employee, field, value)

                session.add(employee)
                session.commit()
                session.refresh(employee)

                return {
                    "success": True,
                    "data": {
                        "id": employee.id,
                        "name": employee.name,
                        "position": employee.position,
                        "salary": employee.salary,
                        "date_hired": employee.date_hired
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_employee(employee_id: int) -> dict[str, Any]:
        """Delete employee"""
        try:
            with get_session() as session:
                employee = session.get(Employee, employee_id)
                if not employee:
                    return {"success": False, "error": "Employee not found"}

                session.delete(employee)
                session.commit()

                return {"success": True, "message": "Employee deleted successfully"}

        except Exception as e:
            return {"success": False, "error": str(e)}
