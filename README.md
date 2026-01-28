# Mosaic Generator

A web application that transforms images into photo mosaics using a library of tile images.

## Features

- Upload images via drag & drop or file picker
- Asynchronous image processing
- Real-time status updates
- Downloadable mosaic output

## Tech Stack

- **Backend:** FastAPI, Python 3.13+
- **Image Processing:** Pillow
- **Frontend:** HTML, CSS, JavaScript

## Getting Started

### Prerequisites

- Python 3.13 or higher
- pip

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/mosaic-generator.git
   cd mosaic-generator
   ```

2. Create a virtual environment
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r backend/requirements.txt
   ```

### Running Locally

```bash
cd backend
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| POST | `/upload` | Upload images for processing |
| GET | `/status/{task_id}` | Check processing status |

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── templates/           # HTML templates
│   ├── static/processed/    # Output images
│   └── uploaded_images/     # Uploaded files
├── new_scripts/
│   └── ascii.py             # Image processing logic
|
└── render.yaml              # Render deployment config
```

## Deployment

This app is configured for deployment on [Render](https://render.com). Push to your connected repository and Render will automatically deploy.


