"""GraphQL type definitions using Strawberry."""
import strawberry
import strawberry_django
from typing import Optional, List
from datetime import date, datetime
from django.contrib.auth import get_user_model

User = get_user_model()


@strawberry_django.type(User)
class UserType:
    """User GraphQL type."""
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    date_joined: datetime
    created_at: datetime
    updated_at: datetime
    phone_number: Optional[str]
    bio: Optional[str]
    date_of_birth: Optional[date]
    
    @strawberry.field
    def is_complete_profile(self) -> bool:
        """Check if user has completed their profile."""
        return all([
            self.first_name,
            self.last_name,
            self.phone_number,
            self.date_of_birth,
        ])
    
    @strawberry.field
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username


@strawberry.input
class UserInput:
    """Input type for user creation/update."""
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None


@strawberry.input
class UserProfileInput:
    """Input type for user profile update."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None


@strawberry.input
class LoginInput:
    """Input for login mutation."""
    email: str
    password: str


@strawberry.input
class RegisterInput:
    """Input for registration mutation."""
    email: str
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@strawberry.type
class AuthPayload:
    """Authentication response payload."""
    user: UserType
    token: str
    refresh_token: str


@strawberry.type
class MutationResult:
    """Generic mutation result."""
    success: bool
    message: Optional[str] = None
    errors: Optional[List[str]] = None