from fastapi import HTTPException
from schemas.dtos.agency_signup_response import AgencySignupResponse
from schemas.dtos.agency_login_response import AgencyLoginResponse
from models.enums.agency_status import AgencyStatus
from repository import agency_repository
from services.exceptions import ( 
    AgencyNotFoundError, 
    ValueRequiredError, 
    AgencyAlreadyExistsError, 
    VerifyMismatchError,
    ForbiddenError)
from argon2 import PasswordHasher
from services.authentication import create_access_token

async def create_new_agency(request):
    if not request.agency_name or not request.email:
        raise ValueRequiredError("AgencyName and Email are required")
    
    existing_email = agency_repository.get_agency_email(request.email)
    if existing_email:
        raise AgencyAlreadyExistsError("An agency with this email already exists")
    
    existing_name = agency_repository.get_agency_name(request.agency_name)
    if existing_name:
        raise AgencyAlreadyExistsError("An agency with this name already exists")
    
    if not request.password or not request.confirm_password:
        raise ValueRequiredError("Password and Confirm Password are required")
    
    if request.password != request.confirm_password:
        raise VerifyMismatchError("Password and Confirm Password do not match")

    if not request.cac_number or not request.cac_number.strip():
        raise ValueRequiredError("CAC Number is required")
    
    existing_cac = agency_repository.get_cac(request.cac_number)

# make cac optional and only save cac field if it is an active/approved cac
    if existing_cac:
        raise AgencyAlreadyExistsError(
            "An agency with this CAC number already exists."
    )

    if not request.first_name or not request.last_name:
        raise ValueRequiredError("First and Last Names are required")
    
    password_hasher = PasswordHasher()
    status = AgencyStatus.PENDING_VERIFICATION
    password_hash = password_hasher.hash(request.password)

    agency = agency_repository.create(
        request, 
        status,
        password_hash
    )

    return AgencySignupResponse(
        id=agency["id"],
        agency_name=agency["agency_name"],
        description=agency["description"],
        first_name=agency["first_name"],
        last_name=agency["last_name"],
        email=agency["email"],
        phone_number=agency["phone_number"],
        address=agency["address"],
        country=agency["country"],
        city=agency["city"],
        cac_number=agency["cac_number"],
        status=agency["status"],
        created_at=agency["created_at"]
    )
 
def login_agency(request):
    if not request.email or not request.password:
        raise ValueRequiredError("Email and Password are required")
    
    agency = agency_repository.get_agency_email(request.email)

    if not agency:
        raise AgencyNotFoundError("Agency not found")
    
    if agency["status"] not in (AgencyStatus.ACTIVE.value, AgencyStatus.INACTIVE.value):
        raise ForbiddenError(
            "Agency is not verified to make this request"
        )
    
    password_hasher = PasswordHasher()
    try:
        password_hasher.verify(
            agency["password_hash"], 
            request.password
        )

    except VerifyMismatchError:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        agency["id"]
    )
    
    return AgencyLoginResponse(
        id=agency["id"],
        agency_name=agency["agency_name"],
        description=agency["description"],
        first_name=agency["first_name"],
        last_name=agency["last_name"],
        email=agency["email"],
        phone_number=agency["phone_number"],
        address=agency["address"],
        country=agency["country"],
        city=agency["city"],
        status=agency["status"],
        cac_number=agency["cac_number"],
        created_at=agency["created_at"],
        access_token= access_token,
        token_type="bearer"
    )