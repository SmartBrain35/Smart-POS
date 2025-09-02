import bcrypt

from typing import Any
from sqlmodel import select, and_, func
from backend.storage.database import get_session
from backend.storage.models import User


class UserCRUD:
    """CRUD operations and business logic for User management"""

    @staticmethod
    def create_user(data: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new user with password hashing and validation

        Args:
            data: dict with keys: username, password, email (optional), role (optional)

        Returns:
            dict with user data or error information
        """
        try:
            with get_session() as session:
                # Check if username already exists
                existing_user = session.exec(
                    select(User).where(User.username == data["username"])
                ).first()

                if existing_user:
                    return {"success": False, "error": "Username already exists"}

                # Check if email already exists (if provided)
                if data.get("email"):
                    existing_email = session.exec(
                        select(User).where(User.email == data["email"])
                    ).first()
                    if existing_email:
                        return {"success": False, "error": "Email already exists"}

                # Hash password
                hashed_password = bcrypt.hashpw(
                    data["password"].encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8')

                # Create user
                user = User(
                    username=data["username"],
                    password=hashed_password,
                    email=data.get("email"),
                    role=data.get("role", "staff")
                )

                session.add(user)
                session.flush()
                session.refresh(user)

                return {
                    "success": True,
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                        "created_at": user.created_at
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def authenticate_user(username: str, password: str) -> dict[str, Any]:
        """
        Authenticate user login

        Args:
            username: User's username
            password: Plain text password

        Returns:
            dict with authentication result and user data
        """
        try:
            with get_session() as session:
                user = session.exec(
                    select(User).where(User.username == username)
                ).first()

                if not user:
                    return {"success": False, "error": "Invalid credentials"}

                # Verify password
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    return {
                        "success": True,
                        "data": {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "role": user.role
                        }
                    }
                else:
                    return {"success": False, "error": "Invalid credentials"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_user_by_id(user_id: int) -> dict[str, Any]:
        """Get user by ID"""
        try:
            with get_session() as session:
                user = session.get(User, user_id)
                if not user:
                    return {"success": False, "error": "User not found"}

                return {
                    "success": True,
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                        "created_at": user.created_at
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_users() -> dict[str, Any]:
        """Get all users"""
        try:
            with get_session() as session:
                users = session.exec(select(User)).all()
                return {
                    "success": True,
                    "data": [
                        {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "role": user.role,
                            "created_at": user.created_at
                        } for user in users
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_user(user_id: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update user information"""
        try:
            with get_session() as session:
                user = session.get(User, user_id)
                if not user:
                    return {"success": False, "error": "User not found"}

                # Update fields if provided
                if "username" in data and data["username"]:
                    # Check if new username already exists
                    existing = session.exec(
                        select(User).where(
                            and_(User.username == data["username"], User.id != user_id)
                        )
                    ).first()
                    if existing:
                        return {"success": False, "error": "Username already exists"}
                    user.username = data["username"]

                if "email" in data:
                    if data["email"]:
                        # Check if new email already exists
                        existing = session.exec(
                            select(User).where(
                                and_(User.email == data["email"], User.id != user_id)
                            )
                        ).first()
                        if existing:
                            return {"success": False, "error": "Email already exists"}
                    user.email = data["email"]

                if "role" in data and data["role"]:
                    user.role = data["role"]

                if "password" in data and data["password"]:
                    user.password = bcrypt.hashpw(
                        data["password"].encode('utf-8'),
                        bcrypt.gensalt()
                    ).decode('utf-8')

                session.add(user)
                session.commit()
                session.refresh(user)

                return {
                    "success": True,
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_user(user_id: int) -> dict[str, Any]:
        """Delete user (soft delete or hard delete based on business rules)"""
        try:
            with get_session() as session:
                user = session.get(User, user_id)
                if not user:
                    return {"success": False, "error": "User not found"}

                # Business rule: Cannot delete admin users if they're the last admin
                if user.role == "admin":
                    admin_count = session.exec(
                        select(func.count(User.id)).where(User.role == "admin")
                    ).one()
                    if admin_count <= 1:
                        return {"success": False, "error": "Cannot delete the last admin user"}

                session.delete(user)
                session.commit()

                return {"success": True, "message": "User deleted successfully"}

        except Exception as e:
            return {"success": False, "error": str(e)}
