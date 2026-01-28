from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path
import sys
import uuid
import threading

sys.path.append(str(Path(__file__).parent.parent))
from new_scripts.ascii import process

app = FastAPI(title="Learning")

UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(exist_ok=True)

BASE_URL = "http://localhost:8000"
task_status = {}

app.mount('/static', StaticFiles(directory='./static'), 'HtmlPages')
templates = Jinja2Templates(directory='./templates')


def process_images_thread(task_id: str, saved_files: list, filename: str):
    """Thread function to process images"""
    try:
        task_status[task_id] = {"status": "processing"}
        output = process(saved_files[0], 'static/processed', filename, saved_files)
        
        if isinstance(output, str):
            output_url = f"{BASE_URL}/{output}"
        elif isinstance(output, list):
            output_url = [f"{BASE_URL}/static/{path}" for path in output]
        else:
            output_url = output
            
        task_status[task_id] = {"status": "completed", "result": output_url}
    except Exception as e:
        task_status[task_id] = {"status": "failed", "error": str(e)}


@app.get('/', tags=['Home'])
def home(req: Request):
    return templates.TemplateResponse(request=req, name='home.html')


@app.post('/upload')
def upload(images: list[UploadFile] = File(..., max_length=10)):
    saved_files = []
    for img in images:
        file_path = UPLOAD_DIR / img.filename
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(img.file, buffer)
        saved_files.append(str(file_path))
    
    task_id = str(uuid.uuid4())
    task_status[task_id] = {"status": "pending"}
    
    # Start processing in a separate thread
    thread = threading.Thread(
        target=process_images_thread,
        args=(task_id, saved_files, images[0].filename)
    )
    thread.start()
    
    return {"message": "Processing started", "task_id": task_id}


@app.get('/status/{task_id}')
def get_status(task_id: str):
    if task_id not in task_status:
        return {"status": "not_found"}
    return task_status[task_id]