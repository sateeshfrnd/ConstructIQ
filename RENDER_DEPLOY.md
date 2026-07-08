# Deploying ConstructIQ Backend on Render

## Prerequisites

- GitHub account with the ConstructIQ repo pushed
- Render account at [render.com](https://render.com) (free tier available)
- PostgreSQL database (Neon, Render Postgres, or any cloud Postgres)

---

## Option A: Deploy with Render Blueprint (Recommended)

Render can auto-detect your Dockerfile. This is the simplest approach.

### Step 1: Sign In to Render

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Sign in with GitHub
3. Authorize Render to access your repositories

### Step 2: Create a New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repo (`ConstructIQ`)
3. Configure:

| Setting | Value |
|---------|-------|
| Name | `constructiq-api` |
| Region | Choose nearest to you |
| Branch | `main` |
| Root Directory | `backend` |
| Runtime | `Docker` |
| Instance Type | `Free` |

### Step 3: Set Environment Variables

In the **"Environment"** section, add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/construct_iq` |
| `SECRET_KEY` | `your-strong-random-secret-key` |
| `SQL_ECHO` | `false` |

For `DATABASE_URL`, use your Neon connection string or any cloud PostgreSQL URL.

### Step 4: Deploy

Click **"Create Web Service"** — Render will:
1. Pull your repo
2. Build the Docker image from `backend/Dockerfile`
3. Start the FastAPI server on port 8000

First deploy takes 3-5 minutes.

---

## Option B: Deploy Without Docker (Native Python)

If you prefer not to use Docker:

### Step 1: Create Web Service

Same as Option A, but set:

| Setting | Value |
|---------|-------|
| Runtime | `Python` |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

### Step 2: Set Environment Variables

Same as Option A — add `DATABASE_URL`, `SECRET_KEY`, `SQL_ECHO`.

### Step 3: Deploy

Click **"Create Web Service"**.

---

## Step 5: Seed Admin User (First Time Only)

After deployment, you need to create the admin user.

### Option 1: Render Shell

1. Go to your service in Render dashboard
2. Click **"Shell"** tab
3. Run:

```bash
python create_user.py
```

### Option 2: Use the API directly

```bash
# Replace with your Render URL
curl -X POST https://constructiq-api.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin710"}'
```

If this returns 401, the user doesn't exist yet — use the Shell method.

---

## Step 6: Verify Deployment

1. Open your Render URL: `https://constructiq-api.onrender.com`
2. Check API docs: `https://constructiq-api.onrender.com/docs`
3. Test login endpoint:

```bash
curl -X POST https://constructiq-api.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin710"}'
```

Expected response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

## Step 7: Connect Frontend

Once backend is live, update your Streamlit frontend secrets:

```toml
API_BASE_URL = "https://constructiq-api.onrender.com"
```

---

## Setting Up Render PostgreSQL (Optional)

If you want Render to host your database too:

1. Click **"New +"** → **"PostgreSQL"**
2. Configure:

| Setting | Value |
|---------|-------|
| Name | `constructiq-db` |
| Database | `construct_iq` |
| User | `constructiq` |
| Region | Same as your Web Service |
| Instance Type | `Free` |

3. After creation, copy the **Internal Database URL**
4. Set it as `DATABASE_URL` in your Web Service environment variables

The internal URL looks like:
```
postgresql://constructiq:password@dpg-xxxxx-a.region.render.com/construct_iq
```

---

## Auto-Deploy on Git Push

By default, Render auto-deploys when you push to `main`:

```bash
git add .
git commit -m "update backend"
git push origin main
```

Render detects the push and redeploys within 2-3 minutes.

To disable: Service Settings → Build & Deploy → Auto-Deploy → Off.

---

## Custom Domain (Optional)

1. Go to service **Settings** → **Custom Domains**
2. Add your domain (e.g., `api.constructiq.com`)
3. Update DNS:
   - Add a CNAME record pointing to `constructiq-api.onrender.com`
4. Render provisions SSL automatically

---

## Free Tier Limitations

| Resource | Limit |
|----------|-------|
| Instances | 1 |
| RAM | 512 MB |
| CPU | Shared |
| Sleep | After 15 min of inactivity |
| Wake time | ~30 seconds on first request |
| Bandwidth | 100 GB / month |
| Build time | 400 min / month |

**Important**: Free tier services spin down after inactivity. First request after sleep takes ~30 seconds. For production use, upgrade to the paid tier ($7/month) to keep it always on.

---

## Troubleshooting

### Deploy fails — "No module named 'core'"

Make sure `Root Directory` is set to `backend` in Render settings.

### "Connection refused" from frontend

- Check your Render service is running (green status)
- Verify the URL in Streamlit secrets matches exactly
- Wait 30 seconds if the service was sleeping

### Database connection errors

- Verify `DATABASE_URL` is correct in environment variables
- If using Neon, ensure `sslmode=require` is in the URL
- If using Render Postgres, use the **Internal URL** (not External)

### Health check failing

Render pings your app to check if it's alive. Add a health endpoint if needed:

The FastAPI app responds to any GET request at root. You can also add:

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

### Slow cold starts

Free tier sleeps after 15 min. Solutions:
- Upgrade to paid ($7/month)
- Use a cron service to ping your app every 14 minutes
- Accept the 30-second wake time for personal projects

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `SECRET_KEY` | Yes | JWT token signing key (use a random 32+ char string) |
| `SQL_ECHO` | No | Set `true` to log SQL queries (debugging only) |
| `PORT` | No | Render sets this automatically |

---

## Quick Checklist

- [ ] GitHub repo pushed with `backend/` directory
- [ ] Render account created and GitHub connected
- [ ] Web Service created with Root Directory = `backend`
- [ ] `DATABASE_URL` set in environment variables
- [ ] `SECRET_KEY` set in environment variables
- [ ] Deploy successful (green status)
- [ ] Admin user seeded via Shell
- [ ] API docs accessible at `/docs`
- [ ] Frontend `API_BASE_URL` updated with Render URL
