from dotenv import load_dotenv

load_dotenv(
    # dotenv_path=os.path.dirname(__file__) + "/.env",
    verbose=True,
    override=True
)

import argparse
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from controllers import (
    test,
    recom_renewal,
    recom_content,
    recom_adv,
)
from connections import PrestoConnection
from utils.loggers import access_handler_hook


app = FastAPI(
    title="testboard-server",
    version="0.1.0",
    description="Backend server for testboard (Jobkorea ML)",
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test.router, prefix="/test")
app.include_router(recom_renewal.router, prefix="/recom_renewal")
app.include_router(recom_content.router, prefix="/recom_content")
app.include_router(recom_adv.router, prefix="/recom_adv")


@app.on_event("startup")
async def on_startup():
    print("on startup...")
    access_handler_hook()


@app.on_event("shutdown")
async def on_shutdown():
    print("on shutdown...")
    PrestoConnection.disconnect()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    print(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--workers", type=int, required=True)
    is_reload = parser.add_mutually_exclusive_group(required=True)
    is_reload.add_argument("--reload", action="store_true")
    is_reload.add_argument("--no-reload", action="store_false")

    args = parser.parse_args()

    uvicorn.run("main:app", host="0.0.0.0", port=args.port, workers=args.workers, reload=args.reload)
