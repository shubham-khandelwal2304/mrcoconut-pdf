# Deploy to Render

## Prerequisites

1. **GitHub/GitLab account** – Connect your repo to Render
2. **Static images** – Add these files to the `static/` folder:
   - `logo.png`
   - `gold_coconut.jpg`, `gold_opener.jpg`, `gold_box.jpg`
   - `platinum_coconut.jpg`, `platinum_cocoboys.jpg`, `platinum_cart.jpg`
   - `diamond_coconut.jpg`, `diamond_cocoboys.jpg`

## Deployment Steps

### Option 1: Dashboard (Recommended)

1. Go to [render.com](https://render.com) → **Dashboard** → **New +** → **Web Service**

2. **Connect repository**
   - Connect GitHub/GitLab
   - Select your `pdf` repo
   - Click **Connect**

3. **Configure**
   - **Name:** `pdf-generator` (or any name)
   - **Region:** Choose closest to your n8n (e.g. Oregon for US)
   - **Runtime:** **Docker**
   - **Dockerfile Path:** `./Dockerfile` (default)
   - **Instance Type:** **Starter** ($7/mo) – required for Playwright
   - **Health Check Path:** `/health` (optional)

4. **Deploy**
   - Click **Create Web Service**
   - Wait 5–10 minutes for the first build

5. **Get your URL**
   - Example: `https://pdf-generator-xxxx.onrender.com`
   - API: `https://pdf-generator-xxxx.onrender.com/generate-pdf`

### Option 2: Blueprint

1. Push `render.yaml` to your repo
2. Render Dashboard → **New +** → **Blueprint**
3. Connect repo and deploy

## n8n Configuration

**HTTP Request node:**
- **Method:** POST
- **URL:** `https://YOUR-APP-NAME.onrender.com/generate-pdf`
- **Body (JSON):**
```json
{
  "plan_type": "{{ $json.package_type }}",
  "customer_name": "{{ $json.customer_name }}",
  "event_type": "{{ $json.event_type }}",
  "event_date": "{{ $json.event_date }}",
  "city": "{{ $json.city }}",
  "coconuts": "{{ $json.coconuts.toString() }}",
  "cartons": "{{ $json.cartons }}",
  "coconut_rate": "{{ $json.coconut_rate }}",
  "transportation_cost": "{{ $json.transportation_cost }}",
  "staff_cost": "{{ $json.staff_cost }}",
  "total_amount": "{{ $json.total_cost }}"
}
```

## Test

```bash
curl -X POST https://YOUR-APP-NAME.onrender.com/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{"plan_type":"diamond","event_date":"23-03-2026","city":"JAIPUR","coconuts":"250","total_amount":"58000"}' \
  --output test.pdf
```

## Troubleshooting

- **Build fails:** Ensure `static/` folder exists and has at least one file
- **502/Timeout:** Use Starter plan or higher (512MB+ RAM)
- **Images missing in PDF:** Add all image files to `static/` and redeploy
