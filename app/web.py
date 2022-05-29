from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api import base_router
from app.api import router as global_router
from app.api.handlers.business_error_handler import business_exception_handler
from app.api.handlers.validation_error_handler import \
	validation_exception_handler
from app.core.logging import app_logger
from app.core.settings import DEBUG, SERVICE_NAME, TAGS_METADATA, VERSION
from app.domain.exceptions.base_exception import BaseDomainException
from app.utils.init_cache import init_cache_redis


def create_app() -> FastAPI:
	"""Create FastAPI application."""
	# Init FastAPI application
	_app = FastAPI(
		title=f"{SERVICE_NAME} backend service",
		debug=DEBUG,
		# Swagger available only in DEBUG-mode
		docs_url="/docs" if DEBUG else None,
		# Redoc available only in DEBUG-mode
		redoc_url="/redoc" if DEBUG else None,
		version=VERSION,
		openapi_tags=TAGS_METADATA,
		on_startup=(init_cache_redis,),
	)

	# Init app logger
	_app.logger = app_logger  # type: ignore

	# Init middlewares
	_app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	_app.add_exception_handler(RequestValidationError, validation_exception_handler)
	_app.add_exception_handler(BaseDomainException, business_exception_handler)

	# Init routes
	_app.include_router(global_router)
	_app.include_router(base_router)

	return _app


app = create_app()
