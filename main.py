from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from playwright.sync_api import sync_playwright
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

app = FastAPI()

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"])
)

class PdfRequest(BaseModel):
    package_type: str
    customer_name: str = ""
    event_type: str = ""
    event_date: str = ""
    city: str = ""
    coconuts: str | int = ""
    cartons: str | int = ""
    coconut_rate: str | int = ""
    transportation_cost: str | int = ""
    staff_cost: str | int = ""
    total_cost: str | int = ""
    phone: str = "+91-9799999069"

    model_config = {"extra": "ignore"}

def render_pdf(html: str) -> bytes:
    # Write to temp file in project dir so relative paths (static/...) resolve for local images
    temp_html = BASE_DIR / "_temp_render.html"
    try:
        temp_html.write_text(html, encoding="utf-8")
        file_uri = temp_html.resolve().as_uri()

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-setuid-sandbox"]
            )
            page = browser.new_page(viewport={"width": 794, "height": 1122})
            page.goto(file_uri, wait_until="networkidle")
            pdf_bytes = page.pdf(format="A4", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            browser.close()
            return pdf_bytes
    finally:
        temp_html.unlink(missing_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate-pdf")
def generate_pdf(data: PdfRequest):
    templates = {
        "gold": "gold.html",
        "platinum": "platinum.html",
        "diamond": "diamond.html",
    }

    plan = data.package_type.lower().strip()

    if plan not in templates:
        raise HTTPException(status_code=400, detail="Invalid package_type")

    template = env.get_template(templates[plan])

    html = template.render(
        plan_type=plan,
        customer_name=data.customer_name,
        event_type=data.event_type,
        event_date=data.event_date,
        city=data.city,
        coconuts=str(data.coconuts),
        cartons=str(data.cartons),
        coconut_rate=str(data.coconut_rate),
        transportation_cost=str(data.transportation_cost),
        staff_cost=str(data.staff_cost),
        total_amount=str(data.total_cost),
        phone=data.phone,
    )

    pdf_bytes = render_pdf(html)

    filename = f"{plan}-quotation.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
