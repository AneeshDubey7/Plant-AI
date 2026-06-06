"""
Image validation utilities — file type, size, and integrity checks.
"""

import io
from typing import Tuple

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError
from loguru import logger

from app.core.config import settings

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


async def validate_and_load_image(file: UploadFile) -> Image.Image:
    """
    Validate an uploaded file and return a PIL Image.
    Raises HTTPException on any validation failure.
    """
    # 1. Content-type check
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"Unsupported file type: '{file.content_type}'. "
                f"Accepted types: {', '.join(sorted(ALLOWED_CONTENT_TYPES))}"
            ),
        )

    # 2. Read bytes
    raw = await file.read()

    # 3. Size check
    if len(raw) > settings.MAX_IMAGE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=(
                f"File size {len(raw) / 1024 / 1024:.1f} MB exceeds "
                f"the {settings.MAX_IMAGE_SIZE_MB} MB limit."
            ),
        )

    # 4. Decode and validate with Pillow
    try:
        image = Image.open(io.BytesIO(raw))
        image.verify()  # Checks file integrity
        image = Image.open(io.BytesIO(raw))  # Re-open after verify (verify() closes)
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File does not appear to be a valid image.",
        )
    except Exception as e:
        logger.error(f"Image decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not decode the uploaded image.",
        )

    logger.info(
        f"Image validated: {file.filename} | "
        f"size={len(raw) / 1024:.1f}KB | "
        f"dims={image.size} | mode={image.mode}"
    )
    return image
