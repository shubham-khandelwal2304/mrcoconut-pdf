# Mr. Coconut PDF Generator

A FastAPI service that generates PDF quotation flyers for Mr. Coconut package plans (Gold, Platinum, Diamond). Uses Playwright and Chromium to render HTML templates to high-quality PDFs.

## Features

- **Multiple package types**: Gold, Platinum, and Diamond plan templates
- **Customizable quotations**: Customer name, event details, pricing, and contact info
- **HTML-to-PDF**: Renders Jinja2 templates with Playwright for pixel-perfect output
- **Docker-ready**: Optimized for deployment on Render or any container platform

## Requirements

- Python 3.11+
- Playwright with Chromium

## Quick Start

### Local development

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # source venv/bin/activate   # macOS/Linux
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Run the server**:

   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`.

## API

### Health check

```
GET /health
```

Returns `{"status": "ok"}` when the service is running.

### Generate PDF

```
POST /generate-pdf
Content-Type: application/json
```

**Request body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `package_type` | string | Yes | One of: `gold`, `platinum`, `diamond` |
| `customer_name` | string | No | Customer name |
| `event_type` | string | No | Type of event |
| `event_date` | string | No | Event date |
| `city` | string | No | Event city |
| `coconuts` | string/int | No | Number of coconuts |
| `cartons` | string/int | No | Number of cartons |
| `coconut_rate` | string/int | No | Rate per coconut |
| `transportation_cost` | string/int | No | Transportation cost |
| `staff_cost` | string/int | No | Staff cost |
| `total_cost` | string/int | No | Total amount |
| `phone` | string | No | Contact number (default: +91-9799999069) |

**Example:**

```bash
curl -X POST http://localhost:8000/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{"package_type": "gold", "customer_name": "John", "event_date": "2025-04-15", "city": "Chennai", "coconuts": "100", "total_cost": "15000"}' \
  --output quotation.pdf
```

**Response:** PDF file (`gold-quotation.pdf`, `platinum-quotation.pdf`, or `diamond-quotation.pdf`)

## Project structure

```
mrcoconut-pdf/
├── main.py           # FastAPI app and PDF generation logic
├── templates/        # Jinja2 HTML templates
│   ├── gold.html
│   ├── platinum.html
│   └── diamond.html
├── static/           # Images and assets (logos, backgrounds)
├── requirements.txt
├── Dockerfile
└── render.yaml       # Render Blueprint for deployment
```

## Deployment

### Docker

```bash
docker build -t mrcoconut-pdf .
docker run -p 8000:8000 mrcoconut-pdf
```

### Render

1. Connect your repository to Render
2. Create a new **Blueprint** from the dashboard
3. Select `render.yaml` — it will create a web service using the Dockerfile
4. The service will be available at the provided URL with `/health` and `/generate-pdf` endpoints

## License

Private / Internal use.
