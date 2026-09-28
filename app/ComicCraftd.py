from fastapi import FastAPI

from fastapi.staticfiles import (
    StaticFiles
)

from app.config import get_settings

from app.routes import router


settings = get_settings()


app = FastAPI(

    title="ComicCraft - AI Comic Story Creator",

    description=(
        "Generate five-panel comics "
        "using generative AI."
    ),

    version="1.0.0"
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(

    "/static",

    StaticFiles(
        directory=str(
            settings.static_dir
        )
    ),

    name="static"
)


# =========================================================
# ROUTES
# =========================================================

app.include_router(
    router
)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {

        "status": "ok",

        "demo_mode": settings.demo_mode,

        "gemini_configured": bool(
            settings.gemini_api_key
        ),

        "huggingface_configured": bool(
            settings.hf_api_key
        )
    }