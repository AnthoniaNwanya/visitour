from pydantic import BaseModel, ConfigDict, Field, model_validator


class UpdateCartItemRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantity: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_quantity(self):
        if "quantity" not in self.model_fields_set:
            raise ValueError("quantity must be provided")
        return self
