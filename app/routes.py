from fastapi import (
    APIRouter,
    Form,
    Request
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from app.config import get_settings

from app.schemas import (
    PromptRequest
)

from app.services.comic_service import (
    generate_comic
)

from app.services.image_generator import (
    generate_image
)


router = APIRouter()

settings = get_settings()

templates = Jinja2Templates(
    directory=str(
        settings.templates_dir
    )
)


# =========================================================
# HOME
# =========================================================

@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# =========================================================
# HTML COMIC GENERATION
# =========================================================

@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate(

    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)

):

    try:

        data = PromptRequest(

            story_prompt=story_prompt,

            character_name=character_name,

            setting=setting,

            tone=tone,

            art_style=art_style
        )

        comic = generate_comic(
            data
        )

        return templates.TemplateResponse(
            "comic_preview.html",
            {
                "request": request,
                **comic
            }
        )

    except Exception as exc:

        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": str(exc)
            },
            status_code=500
        )


# =========================================================
# JSON API
# =========================================================

@router.post(
    "/generate-comic/json"
)
async def generate_json(
    payload: PromptRequest
):

    try:

        result = generate_comic(
            payload
        )

        return JSONResponse(
            content=result
        )

    except Exception as exc:

        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc)
            }
        )


# =========================================================
# IMAGE TEST
# =========================================================

@router.post(
    "/test-image"
)
async def test_image(
    prompt: str = Form(...)
):

    try:

        request = PromptRequest(

            story_prompt=prompt,

            character_name="Test Character",

            setting="Fantasy World",

            tone="dramatic",

            art_style="comic book"
        )

        image_url = generate_image(

            prompt,

            1,

            request
        )

        return {
            "image_url": image_url
        }

    except Exception as exc:

        return JSONResponse(

            status_code=500,

            content={
                "detail": str(exc)
            }
        )


# =========================================================
# EXPORT SUCCESS
# =========================================================

@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(

    request: Request,

    pdf_url: str = ""

):

    return templates.TemplateResponse(

        "export_success.html",

        {
            "request": request,
            "pdf_url": pdf_url
        }
    )