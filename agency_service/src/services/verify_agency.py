from repository import agency_repository


async def approve_agency(agency_id: int, cac_number: str):
    return agency_repository.accept_cac(
        agency_id,
        cac_number
    )

async def reject_agency(agency_id: int, cac_number: str):
    return agency_repository.reject_cac(
        agency_id,
        cac_number
    )