from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
import logging

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Web Server", description="Simple HTML Server")

# Trust proxy headers
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["wtandrews.nova.org", "localhost", "*"]
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"=== Incoming Request ===")
    logger.info(f"Method: {request.method}")
    logger.info(f"URL: {request.url}")
    logger.info(f"Client: {request.client}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    try:
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    """Serve the index.html file"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>index.html not found</h1>", 
            status_code=404
        )

@app.get("/resume")
async def serve_resume():
    """Serve resume PDF to open in browser (not download)"""
    pdf_path = "assets/William_Andrews_Resume.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path, 
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=William_Andrews_Resume.pdf"}
        )
    return HTMLResponse(content="<h1>PDF not found</h1>", status_code=404)

@app.get("/matroid-theory")
async def serve_matroid():
    """Serve Matroid Theory PDF to open in browser (not download)"""
    pdf_path = "assets/Matroid_Theory_Project.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path, 
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=Matroid_Theory_Project.pdf"}
        )
    return HTMLResponse(content="<h1>PDF not found</h1>", status_code=404)

@app.get("/transcript")
async def serve_transcript():
    """Serve transcript PDF to open in browser (not download)"""
    pdf_path = "assets/transcript.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path, 
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=transcript.pdf"}
        )
    return HTMLResponse(content="<h1>PDF not found</h1>", status_code=404)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/{file_path:path}")
async def serve_files(file_path: str):
    """Serve static files from css/, js/, assets/ directories"""
    if file_path in ["health", "docs", "openapi.json", "redoc"]:
        return {"error": "Not found"}, 404
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    return HTMLResponse(content="<h1>404 - File not found</h1>", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)