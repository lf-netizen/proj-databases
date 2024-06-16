import os
import io
from bson import ObjectId
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from clients.mongodb import mongofs


ROUTE_NAME = os.path.basename(__file__).replace(".py", "")

router = APIRouter(prefix=f"/{ROUTE_NAME}", tags=[ROUTE_NAME])


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    file_id = mongofs.put(contents, filename=file.filename)
    return {"file_id": str(file_id)}


@router.get("/download/{file_id}")
async def download_file(file_id: str):
    try:
        grid_out = mongofs.get(ObjectId(file_id))
        filename = grid_out.filename  # Get the filename from the GridOut object
        return StreamingResponse(
            io.BytesIO(grid_out.read()),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception:
        raise HTTPException(status_code=404, detail="File not found")
