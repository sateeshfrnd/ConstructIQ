# Deploying ConstructIQ Frontend on Streamlit Community Cloud

## Prerequisites

- GitHub account with the ConstructIQ repo pushed
- Backend API deployed and publicly accessible (Render, Railway, or any host)
- Streamlit Community Cloud account at [share.streamlit.io](https://share.streamlit.io)

---

## Step 1: Prepare Your Repository

Ensure your repo has this structure (already set up):

```
ConstructIQ/
├── frontend/
│   ├── .streamlit/
│   │   └── config.toml        # Theme and server settings
│   ├── app.py                  # Main entry point
│   ├── requirements.txt        # Python dependencies
│   ├── components/
│   ├── page_layouts/
│   ├── services/
│   ├── assets/
│   └── utils/
```

Key files Streamlit Cloud looks for:
- `frontend/requirements.txt` — installs dependencies
- `frontend/app.py` — the app entry point

---

## Step 2: Deploy Backend First

Your backend must be publicly accessible before deploying the frontend.
The frontend makes API calls to the backend, so it needs a live URL.

Recommended free options:
- **Render** (https://render.com) — connect GitHub, deploy as Web Service
- **Railway** (https://railway.app) — one-click deploy from GitHub
- **Fly.io** (https://fly.io) — deploy using Docker

Once deployed, note your backend URL (e.g., `https://constructiq-api.onrender.com`).

---

## Step 3: Deploy on Streamlit Community Cloud

### 3.1 Sign In

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub** account
3. Authorize Streamlit to access your repositories

### 3.2 Create New App

1. Click **"New app"**
2. Fill in the details:

| Field | Value |
|-------|-------|
| Repository | `your-username/ConstructIQ` |
| Branch | `main` |
| Main file path | `frontend/app.py` |

3. Click **"Advanced settings"** before deploying

### 3.3 Configure Secrets

In **Advanced settings → Secrets**, paste:

```toml
API_BASE_URL = "https://your-backend-url.com"
```

Replace with your actual deployed backend URL. No trailing slash.

Example:
```toml
API_BASE_URL = "https://constructiq-api.onrender.com"
```

### 3.4 Deploy

Click **"Deploy!"** — Streamlit will:
1. Clone your repo
2. Install packages from `frontend/requirements.txt`
3. Run `frontend/app.py`

Deployment takes 2-5 minutes on first build.

---

## Step 4: Verify

1. Open the app URL provided by Streamlit (e.g., `https://constructiq.streamlit.app`)
2. Login with `admin@example.com` / `admin710`
3. Check that data loads correctly from your backend

---

## Updating the App

Any push to the `main` branch automatically redeploys the app.

```bash
git add .
git commit -m "update frontend"
git push origin main
```

Streamlit Cloud detects the change and rebuilds within 1-2 minutes.

---

## Managing Secrets After Deployment

If you need to update the backend URL or add new secrets:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Find your app → click **"⋮"** menu → **"Settings"**
3. Go to **"Secrets"** tab
4. Edit and save

The app restarts automatically with new secrets.

---

## Custom Domain (Optional)

Streamlit Community Cloud gives you a URL like `your-app.streamlit.app`.

To use a custom domain:
1. Go to app Settings → General
2. Add your custom domain
3. Update your DNS (CNAME record pointing to Streamlit)

---

## Troubleshooting

### App won't start — "ModuleNotFoundError"

Check `frontend/requirements.txt` has all packages listed.

### API calls failing — "Connection refused"

- Verify your backend is running and publicly accessible
- Check the `API_BASE_URL` secret is correct (no trailing slash)
- Make sure backend has CORS enabled if needed

### CSS not loading

The sidebar CSS loads from `assets/styles.css` using a path relative to
the app root. This is handled automatically — no changes needed.

### App is slow to wake up

Free-tier apps on Streamlit Community Cloud go to sleep after inactivity.
First load after sleep takes 30-60 seconds. This is normal.

### Python version issues

If you need a specific Python version, create:

```
frontend/runtime.txt
```

With content:
```
python-3.12
```

---

## Resource Limits (Free Tier)

| Resource | Limit |
|----------|-------|
| Apps | Unlimited public apps |
| RAM | 1 GB |
| Storage | Limited |
| Sleep | After ~7 days of inactivity |
| Viewers | Unlimited |

---

## File Reference

| File | Purpose |
|------|---------|
| `frontend/app.py` | App entry point (Streamlit reads this) |
| `frontend/requirements.txt` | Python package dependencies |
| `frontend/.streamlit/config.toml` | Theme colors and server config |
| `frontend/.streamlit/secrets.toml.example` | Template for secrets (not deployed — for reference only) |

---

## Quick Checklist

- [ ] Backend deployed and accessible via public URL
- [ ] Repo pushed to GitHub
- [ ] `frontend/requirements.txt` has all dependencies
- [ ] Connected GitHub to Streamlit Community Cloud
- [ ] Set `API_BASE_URL` in Streamlit secrets
- [ ] Main file path set to `frontend/app.py`
- [ ] App deployed and login works
