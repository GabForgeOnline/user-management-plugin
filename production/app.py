"""
app.py - Standalone FastAPI Application for User Management Plugin
Purpose: Run the user management plugin as an independent service
Author: User Management Plugin Team
Version: 1.0.0

This file demonstrates how to run the plugin as a standalone FastAPI application.
It can also be imported and integrated into other FastAPI applications.
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from user_management.config import settings, init_db, test_db_connection
from user_management.api.routes import auth

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="User Management Plugin - Independent RBAC System",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION
        }
    
    # API status endpoint
    @app.get("/api/status")
    async def api_status():
        """API status endpoint"""
        db_healthy = test_db_connection()
        return {
            "status": "ok" if db_healthy else "degraded",
            "database": "connected" if db_healthy else "disconnected",
            "version": settings.APP_VERSION
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "docs": "/api/docs",
            "redoc": "/api/redoc"
        }
    
    # Exception handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        """Handle HTTP exceptions"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "status_code": exc.status_code,
                "detail": exc.detail
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """Handle general exceptions"""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "status_code": 500,
                "detail": "Internal server error"
            }
        )
    
    # Include auth routes
    app.include_router(auth.router)
    
    # Startup event
    @app.on_event("startup")
    async def startup():
        """Initialize application on startup"""
        logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        
        if test_db_connection():
            logger.info("📊 Initializing database...")
            init_db()
            logger.info("✅ Database initialized successfully")
        else:
            logger.error("❌ Database connection failed - API may not work correctly")
    
    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown():
        """Cleanup on shutdown"""
        logger.info(f"🛑 Shutting down {settings.APP_NAME}")
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server at http://0.0.0.0:8000")
    logger.info(f"API Docs: http://0.0.0.0:8000/api/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
