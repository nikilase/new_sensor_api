from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from app.dependencies import favicon_path, templates

router = APIRouter()


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    print("\n")
    return FileResponse(favicon_path)


@router.get("/")
async def home(request: Request):
    print("\n")
    return templates.TemplateResponse("root.html", context={"request": request})
