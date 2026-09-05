# Deployment Guide

The Control Center (`apps/admin`) can be deployed on **any platform that runs Docker** — you are not locked to Vercel.

## What gets deployed

| Component | Deploy now? | How |
|---|---|---|
| **Control Center** (Next.js) | Yes | Docker image |
| **Production pipeline** (Python) | No (runs locally / CI / Cursor agents) | Not a web service yet |
| **Consumer PWA** | Not built yet | Future `apps/app` |

## Platform comparison

| Platform | Best for | Cost (starter) | Persistent disk | Difficulty |
|---|---|---|---|---|
| **Railway** | Fastest deploy, GitHub auto-deploy | ~$5/mo | Yes (volumes) | Easy |
| **Fly.io** | Global edge, full Docker control | ~$5/mo | Yes (volumes) | Easy |
| **Render** | Simple PaaS, free tier to start | Free–$7/mo | Limited on free | Easy |
| **DigitalOcean App Platform** | DO ecosystem | ~$5/mo | Yes | Easy |
| **Hetzner / VPS + Docker** | Cheapest long-term | ~$4/mo | Yes | Medium |
| **AWS ECS / GCP Cloud Run** | Enterprise scale | Variable | Yes | Harder |
| **Coolify** (self-hosted) | Own server, Heroku-like UX | VPS cost only | Yes | Medium |
| **Vercel** | Next.js native | Free tier | No filesystem* | Easy |

\*Vercel is a poor fit for this app today because the Control Center **reads/writes YAML files and serves zip downloads from disk**. Serverless has no persistent filesystem unless you refactor to S3 + database first.

**Recommendation:** **Railway** or **Fly.io** for the Control Center — Docker-native, persistent volumes, custom domain, ~5 minutes to deploy.

---

## Prerequisites

1. Domain (optional): `admin.colourpages.app`
2. Strong `ADMIN_PASSWORD` (enables HTTP Basic Auth on all routes except `/api/health`)
3. GitHub repo connected to your host

---

## Option A: Railway (recommended)

1. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
2. Select `colourpages` repo
3. Settings:
   - **Dockerfile path:** `apps/admin/Dockerfile`
   - **Root directory:** `/` (repo root)
4. **Variables:**
   ```
   ADMIN_PASSWORD=your-secure-password-here
   CATALOG_DIR=/catalog/books
   DATA_DIR=/data/books
   ```
5. **(Recommended)** Add a volume mounted at `/data` so book artifacts survive redeploys
6. **Networking** → Generate domain or add custom domain
7. Deploy

---

## Option B: Fly.io

```bash
# Install flyctl: https://fly.io/docs/hands-on/install-flyctl/
fly auth login
fly launch --no-deploy   # uses fly.toml in repo root
fly secrets set ADMIN_PASSWORD=your-secure-password-here
fly deploy
fly certs add admin.colourpages.app   # optional custom domain
```

For persistent book data:
```bash
fly volumes create colourpages_data -r iad -s 1
# Then uncomment [mounts] in fly.toml and redeploy
```

---

## Option C: Render

1. [render.com](https://render.com) → **New** → **Blueprint** or **Web Service**
2. Connect repo — Render reads `render.yaml` automatically if using Blueprint
3. Or manual: **Environment: Docker**, Dockerfile `apps/admin/Dockerfile`, context `.`
4. Set `ADMIN_PASSWORD` in Environment (secret)
5. Deploy

---

## Option D: Any VPS (Hetzner, DigitalOcean Droplet, etc.)

```bash
# On your server
git clone https://github.com/sridushiva-dev/colouringpages.git
cd colouringpages
export ADMIN_PASSWORD=your-secure-password
docker compose up -d --build
```

Put **Caddy** or **nginx** in front for HTTPS:

```caddy
admin.colourpages.app {
  reverse_proxy localhost:3000
}
```

---

## Option E: Local production test

```bash
# From repo root
export ADMIN_PASSWORD=colourpages-dev
docker compose up --build
```

Open http://localhost:3000 — browser will prompt for password (`admin` / `colourpages-dev` or any username with that password).

---

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `ADMIN_PASSWORD` | **Yes (prod)** | — | HTTP Basic Auth password |
| `CATALOG_DIR` | No | `../../catalog/books` | Book registry YAML path |
| `DATA_DIR` | No | `../../data/books` | Artifacts + publish zips |
| `PORT` | No | `3000` | HTTP port |

---

## After deploy

1. Visit your URL — enter password when prompted
2. Confirm pilot book appears in **Approvals**
3. Point `admin.colourpages.app` DNS CNAME to your host
4. Run production builds locally (or via CI) and sync `data/books/` to the server volume

### Syncing new books to production

Until we add S3/API storage, copy artifacts to the server:

```bash
# Example: rsync after local build
rsync -avz data/books/ user@your-server:/path/to/colouringpages/data/books/
rsync -avz catalog/books/ user@your-server:/path/to/colouringpages/catalog/books/
docker compose restart admin
```

---

## What NOT to use Vercel for (yet)

- Control Center file downloads (`publish-ready.zip`)
- Catalog YAML writes from approval actions
- Large binary artifact storage

Refactor to **Postgres + S3** later if you want fully serverless — we can do that in a future phase.

---

## Security checklist

- [ ] Set a strong `ADMIN_PASSWORD` (20+ chars)
- [ ] HTTPS enabled (all platforms above do this automatically)
- [ ] Do not commit `.env.local` or passwords to git
- [ ] Restrict admin URL (no public links; optional IP allowlist on Fly/Cloudflare)
