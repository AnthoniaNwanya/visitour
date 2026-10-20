from fastapi import HTTPException
from schemas.dtos.traveler_signup_response import TravelerSignupResponse
from schemas.dtos.traveler_login_response import TravelerLoginResponse
from models.enums.traveler_status import TravelerStatus
from repository import traveler_repository
from services.exception.exceptions import ( 
    TravelerNotFoundError,
    ValueRequiredError, 
    TravelerAlreadyExistsError, 
    VerifyMismatchError,
    ForbiddenError)
from argon2 import PasswordHasher
from services.authentications.authentication import create_access_token

async def create_traveler(request):

    existing_email = traveler_repository.get_traveler_by_email(request.email)
    if existing_email:
        raise TravelerAlreadyExistsError("A traveler with this email already exists")
    

    if request.password != request.confirm_password:
        raise VerifyMismatchError("Password and Confirm Password do not match")

    password_hasher = PasswordHasher()
    password_hash = password_hasher.hash(request.password)
   
    traveler = traveler_repository.create(
        request, 
        password_hash
    )

    return TravelerSignupResponse(
        id=traveler["id"],
        first_name=traveler["first_name"],
        last_name=traveler["last_name"],
        email=traveler["email"],
        phone_number=traveler["phone_number"],
        date_of_birth=traveler["date_of_birth"],
        address=traveler["address"],
        city=traveler["city"],
        country=traveler["country"],
        nationality=traveler["nationality"],
        status=traveler["status"],
        created_at=traveler["created_at"]
    )
 
def login_traveler(request):
    traveler = traveler_repository.get_traveler_by_email(request.email)

    if not traveler:
        raise TravelerNotFoundError("traveler not found")
    
    password_hasher = PasswordHasher()
    try:
        password_hasher.verify(
            traveler["password_hash"], 
            request.password
        )

    except VerifyMismatchError:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        user_id=traveler["id"],
        role="traveler"
    )
    
    return TravelerLoginResponse(
        id=traveler["id"],
        first_name=traveler["first_name"],
        last_name=traveler["last_name"],
        email=traveler["email"],
        phone_number=traveler["phone_number"],
        date_of_birth=traveler["date_of_birth"],
        address=traveler["address"],
        city=traveler["city"],
        country=traveler["country"],
        nationality=traveler["nationality"],
        status=traveler["status"],
        created_at=traveler["created_at"],
        access_token= access_token,
        token_type="bearer"
    )