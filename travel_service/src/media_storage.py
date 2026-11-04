from pathlib import Path
import json
from uuid import uuid4

from fastapi import HTTPException, Request, UploadFile
from pydantic import BaseModel, ValidationError
from fastapi.exceptions import RequestValidationError
from starlette.datastructures import UploadFile as StarletteUploadFile
from typing import get_args, get_origin
from typing import TypeVar


MEDIA_ROOT = Path(__file__).resolve().parents[1] / "media"
MAX_IMAGE_SIZE = 10 * 1024 * 1024
MAX_IMAGES_PER_UPLOAD = 10

_IMAGE_SIGNATURES = (
    (b"\xff\xd8\xff", ".jpg"),
    (b"\x89PNG\r\n\x1a\n", ".png"),
)

MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
ModelT = TypeVar("ModelT", bound=BaseModel)


class InvalidImageError(ValueError):
    pass


class ImageTooLargeError(ValueError):
    pass


def _image_extension(content: bytes) -> str:
    for signature, extension in _IMAGE_SIGNATURES:
        if content.startswith(signature):
            return extension
    if content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return ".webp"
    raise InvalidImageError("Only JPEG, PNG, and WebP images are supported")


async def save_images(files: list[UploadFile], category: str) -> list[str]:
    if not files:
        raise InvalidImageError("At least one image is required")
    if len(files) > MAX_IMAGES_PER_UPLOAD:
        raise InvalidImageError(
            f"No more than {MAX_IMAGES_PER_UPLOAD} images can be uploaded at once"
        )

    pending = []
    for file in files:
        content = await file.read(MAX_IMAGE_SIZE + 1)
        if len(content) > MAX_IMAGE_SIZE:
            raise ImageTooLargeError("Each image must be 10 MB or smaller")
        pending.append((content, _image_extension(content)))

    destination = MEDIA_ROOT / category
    destination.mkdir(parents=True, exist_ok=True)
    saved_paths = []
    urls = []
    try:
        for content, extension in pending:
            filename = f"{uuid4().hex}{extension}"
            path = destination / filename
            path.write_bytes(content)
            saved_paths.append(path)
            urls.append(f"/media/{category}/{filename}")
    except OSError:
        for path in saved_paths:
            path.unlink(missing_ok=True)
        raise

    return urls


async def parse_upload_request(
    request: Request,
    schema: type[ModelT],
    file_field: str,
    category: str,
) -> ModelT:
    content_type = request.headers.get("content-type", "")
    data = {}

    if content_type.startswith("multipart/form-data"):
        form = await request.form()
        data = {}
        values = {}
        files = []
        cover_image_index = None

        for key, value in form.multi_items():
            if key == "data":
                try:
                    legacy_data = json.loads(value)
                except (TypeError, json.JSONDecodeError) as exc:
                    raise HTTPException(
                        status_code=400,
                        detail="'data' must contain a valid JSON object",
                    ) from exc
                if not isinstance(legacy_data, dict):
                    raise HTTPException(
                        status_code=400,
                        detail="'data' must be a JSON object",
                    )
                data.update(legacy_data)
                continue
            if key == "cover_image_index":
                cover_image_index = value or None
                continue
            if isinstance(value, StarletteUploadFile):
                if key == file_field and value.filename:
                    files.append(value)
                continue
            if value == "":
                continue
            values.setdefault(key, []).append(value)

        for key, field_values in values.items():
            annotation = schema.model_fields.get(key)
            annotation = annotation.annotation if annotation else None
            is_array = (
                get_origin(annotation) is list
                or any(get_origin(arg) is list for arg in get_args(annotation))
            )
            value = field_values if len(field_values) > 1 or is_array else field_values[0]
            if key == file_field and key == "images":
                existing_images = data.get(key, [])
                if not isinstance(existing_images, list):
                    raise HTTPException(
                        status_code=400,
                        detail="'images' must be an array of image paths",
                    )
                data[key] = existing_images + (
                    value if isinstance(value, list) else [value]
                )
            else:
                data[key] = value

        if files:
            try:
                urls = await save_images(files, category)
            except ImageTooLargeError as exc:
                raise HTTPException(status_code=413, detail=str(exc)) from exc
            except InvalidImageError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc
            if file_field == "images":
                existing_images = data.get("images", [])
                if not isinstance(existing_images, list):
                    raise HTTPException(
                        status_code=400,
                        detail="'images' must be an array of image paths",
                    )
                data["images"] = existing_images + urls
                if cover_image_index is not None:
                    try:
                        index = int(cover_image_index)
                    except (TypeError, ValueError) as exc:
                        raise HTTPException(
                            status_code=400,
                            detail="cover_image_index must be an integer",
                        ) from exc
                    if index < 0 or index >= len(urls):
                        raise HTTPException(
                            status_code=400,
                            detail="cover_image_index must identify an uploaded image",
                        )
                    data["cover_image"] = urls[index]
            else:
                data[file_field] = urls[0]
    elif content_type.startswith("application/json"):
        try:
            data = await request.json()
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail="Invalid JSON request body") from exc
    else:
        raise HTTPException(
            status_code=415,
            detail="Use application/json or multipart/form-data",
        )

    try:
        return schema.model_validate(data)
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc
