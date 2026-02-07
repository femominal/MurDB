from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import Response
from pydantic import BaseModel
from app.services.export_service import secure_export
from app.config import API_KEY
from app.logger import logger

app = FastAPI(title="MurDB")


class ExportRequest(BaseModel):
    db_type: str
    db_name: str


@app.post("/export")
async def export_database(
    request: Request,
    body: ExportRequest,
    x_api_key: str = Header(...)
):
    client_ip = request.client.host

    if x_api_key != API_KEY:
        logger.warning(f"UNAUTHORIZED attempt from {client_ip}")
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        container = secure_export(body.db_type, body.db_name)

        logger.info(
            f"EXPORT SUCCESS | IP={client_ip} | TYPE={body.db_type} | DB={body.db_name}"
        )

        return Response(
            content=container,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": "attachment; filename=backup.sq"
            }
        )

    except Exception as e:
        logger.error(
            f"EXPORT FAILED | IP={client_ip} | TYPE={body.db_type} | DB={body.db_name} | ERROR={str(e)}"
        )
        raise HTTPException(status_code=500, detail="Export failed")
