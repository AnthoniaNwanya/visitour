from fastapi import APIRouter
from api.controllers import tour_controller
from api.controllers import visa_application_controller
from schemas.dtos.delete_tour_response import DeleteTourResponse
from schemas.dtos.delete_visa_response import DeleteVisaResponse
from api.controllers import visa_type_controller

travelrouter = APIRouter(
    prefix="/travel",
    tags=["Travels"],
)

tour_upload_schema = {
    "type": "object",
    "properties": {
        "tour_name": {"type": "string"},
        "description": {"type": "string"},
        "country": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Repeat the country form field for additional countries.",
        },
        "start_date": {"type": "string", "format": "date"},
        "end_date": {"type": "string", "format": "date"},
        "price": {"type": "number"},
        "available_slots": {"type": "integer"},
        "images": {
            "type": "array",
            "items": {
                "oneOf": [
                    {"type": "string", "format": "binary"},
                    {"type": "string"},
                ]
            },
        },
        "cover_image": {"type": "string"},
        "cover_image_index": {
            "type": "integer",
            "description": "Zero-based index of the selected cover among the uploaded images",
        },
    },
}

visa_upload_schema = {
    "type": "object",
    "properties": {
        "visa_name": {"type": "string"},
        "country": {"type": "string"},
        "visa_type_id": {"type": "integer"},
        "processing_time_value": {"type": "integer"},
        "processing_time_unit": {"type": "string"},
        "processing_fee": {"type": "number"},
        "images": {
            "type": "array",
            "items": {
                "oneOf": [
                    {"type": "string", "format": "binary"},
                    {"type": "string"},
                ]
            },
        },
        "cover_image": {"type": "string"},
        "cover_image_index": {
            "type": "integer",
            "description": "Zero-based index of the selected cover among the uploaded images",
        },
    },
}

def travel_upload_openapi(schema):
    return {
        "requestBody": {
            "required": True,
            "content": {
                "multipart/form-data": {"schema": schema},
                "application/json": {"schema": {"type": "object"}},
            },
        }
    }

travelrouter.post(
    "/tours/create",
    openapi_extra=travel_upload_openapi(tour_upload_schema),
)(tour_controller.create_tour)
travelrouter.post(
    "/visa-applications/create",
    openapi_extra=travel_upload_openapi(visa_upload_schema),
)(visa_application_controller.create_visa_application)

travelrouter.get("/tours")(tour_controller.get_tours)
travelrouter.get("/tours/agency-tours")(tour_controller.get_my_agency_tours)
travelrouter.get("/visa-applications")(visa_application_controller.get_visa_applications)
travelrouter.get("/visa-applications/agency-visas")(visa_application_controller.get_my_agency_visa_applications)
travelrouter.get("/visa-types")(visa_type_controller.get_visa_types)

travelrouter.put(
    "/tours/edit/{tour_id}",
    openapi_extra=travel_upload_openapi(tour_upload_schema),
)(tour_controller.update_tour)
travelrouter.put(
    "/visa-applications/edit/{visa_id}",
    openapi_extra=travel_upload_openapi(visa_upload_schema),
)(visa_application_controller.update_visa_application)

travelrouter.delete("/tours/delete/{tour_id}", response_model=DeleteTourResponse)(tour_controller.delete_tour)
travelrouter.delete("/visa-applications/delete/{visa_id}", response_model=DeleteVisaResponse)(visa_application_controller.delete_visa_application)
