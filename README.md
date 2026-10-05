# GitHub AI Repo Intelligence

A full-stack GitHub repository intelligence platform that authenticates with GitHub, analyzes repository metadata, and surfaces AI-assisted insights about code structure, technologies, languages, and commit history.

<p align="center">
  <img alt="GitHub AI Repo Intelligence" src="https://img.shields.io/badge/Stack-FastAPI%20%2B%20React-blue" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB" />
  <img alt="Node" src="https://img.shields.io/badge/Node.js-18%2B-339933" />
  <img alt="License" src="https://img.shields.io/badge/License-Unspecified-lightgrey" />
</p>

## Overview

This project combines a React frontend with a FastAPI backend to:

- authenticate users through GitHub OAuth
- load the user’s repositories and GitHub profile
- analyze language usage, repository structure, and technology stacks
- inspect commit and repository metadata
- provide a clean dashboard for exploring project health and repository context

It is designed to be a strong foundation for AI-powered repository analysis, developer tooling, and GitHub intelligence workflows.

## Features

- GitHub OAuth authentication
- Repository listing and user profile retrieval
- Repository structure and language analysis
- Technology and architecture detection
- Commit and repository metadata inspection
- FastAPI backend with interactive API docs
- React-based frontend with dashboard experience

## Tech Stack

- Frontend: React 19, Vite, JavaScript
- Backend: FastAPI, Uvicorn, HTTPX
- Authentication: GitHub OAuth + signed session cookies
- Data sources: GitHub REST API and repository metadata endpoints
- AI integrations: configurable provider support for Groq and Mistral

## Repository Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── chunker.py
│   │   │   ├── context.py
│   │   │   ├── embeddings.py
│   │   │   ├── llm.py
│   │   │   ├── retrieval.py
│   │   │   └── service.py
│   │   ├── analyzers/
│   │   │   ├── activity_analyzer.py
│   │   │   ├── architecture_analyzer.py
│   │   │   ├── commit_analyzer.py
│   │   │   ├── file_detector.py
│   │   │   ├── language_analyzer.py
│   │   │   ├── readme_analyzer.py
│   │   │   ├── source_analyzer.py
│   │   │   ├── structure_analyzer.py
│   │   │   └── technology_analyzer.py
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── repositories.py
│   │   ├── routes/
│   │   │   ├── ai.py
│   │   │   ├── auth.py
│   │   │   └── github.py
│   │   ├── services/
│   │   │   ├── analysis_service.py
│   │   │   ├── github_api.py
│   │   │   ├── github_oauth.py
│   │   │   └── repo_analyzer.py
│   │   ├── config.py
│   │   ├── main.py
│   │   └── session.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   └── ChatBox.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Repository.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── api.test.js
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── chat.css
│   │   ├── cursor-theme.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── DESIGN.md
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
├── data/
├── tests/
│   ├── test_ai_response.py
│   ├── test_auth_callback.py
│   └── test_llm_provider_fallback.py
├── render.yaml
├── README.md
├── skills-lock.json
└── LICENSE
```

## Prerequisites

Before running the app, make sure you have:

- Python 3.10+
- Node.js 18+
- npm
- A GitHub OAuth App

## Quick Start

### 1) Configure GitHub OAuth

Create a GitHub OAuth App in:

- GitHub → Settings → Developer settings → OAuth Apps

Use the following local development values:

- Homepage URL: `http://localhost:5173`
- Authorization callback URL: `http://localhost:8000/auth/github/callback`

Then add your credentials in `backend/.env`:

```env
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback
FRONTEND_URL=http://localhost:5173
```

> Do not commit your `.env` file or expose the client secret in public repositories.

### 2) Start the backend

From the repository root:

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The backend will be available at:

- `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3) Start the frontend

Open a second terminal and run:

```bash
cd frontend
npm install
npm run dev
```

Then open:

- `http://localhost:5173`

## Deployment

This repository includes a Render deployment configuration via `render.yaml`.
The frontend is deployed to Vercel from the `frontend` directory, and the
backend is deployed to Render at `https://githubai-backend.onrender.com`.
Production browser requests use the Vercel `/api` rewrite to reach Render. This
keeps the session cookie first-party; do not set `VITE_API_URL` to the Render
origin in Vercel.

For Render, use these settings:

- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/`

Set these Render environment variables (the non-secret URLs are also configured
in `render.yaml`):

```env
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=https://githubai-anly.vercel.app/api/auth/github/callback
FRONTEND_URL=https://githubai-anly.vercel.app
DATABASE_URL=your_postgres_connection_string
GROQ_API_KEY=your_groq_api_key
MISTRAL_API_KEY=your_mistral_api_key
AI_PROVIDER=groq
```

In the GitHub OAuth App settings, set the Homepage URL to
`https://githubai-anly.vercel.app` and the Authorization callback URL to
`https://githubai-anly.vercel.app/api/auth/github/callback` exactly. Set
`GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `GITHUB_REDIRECT_URI`, and
`FRONTEND_URL` in Render. In Vercel, set the project's Root Directory to
`frontend` and remove any `VITE_API_URL` value that points directly to Render.
The frontend defaults to the same-origin `/api` route; if you set
`VITE_API_URL`, use `/api`. Redeploy both services after changing settings.

## Authentication Flow

1. User opens the frontend at `http://localhost:5173`
2. User clicks the GitHub login button
3. GitHub redirects to the Vercel `/api/auth/github/callback` route, which
   forwards the callback to Render
4. The backend exchanges the OAuth code for an access token
5. A signed, secure, HTTP-only, same-site session cookie is created on the
   frontend origin
6. The dashboard loads the authenticated user and repository data

## API Endpoints

| Method | Endpoint                                       | Description                                   |
| ------ | ---------------------------------------------- | --------------------------------------------- |
| `GET`  | `/`                                            | API health response                           |
| `GET`  | `/auth/github`                                 | Starts GitHub OAuth flow                      |
| `GET`  | `/auth/github/callback`                        | Handles the OAuth callback                    |
| `GET`  | `/github/me`                                   | Returns the authenticated GitHub user         |
| `GET`  | `/github/repositories`                         | Returns the authenticated user’s repositories |
| `GET`  | `/github/repositories/{owner}/{repo}/analysis` | Analyzes a specific repository                |

The GitHub data routes require the signed session cookie created during login.

## Repository Analysis Capabilities

The analysis endpoint currently returns:

- repository metadata such as name, description, stars, forks, issues, and default branch
- language statistics
- repository structure including files, folders, and extensions
- commit counts and repository insights

This data is gathered using the repository’s actual default branch when fetching the Git tree.

## Troubleshooting

### Dashboard shows no data

- confirm both the backend and frontend are running
- verify you are using `http://localhost:5173`
- confirm the GitHub callback URL matches `GITHUB_REDIRECT_URI`
- clear stale localhost cookies and log in again
- inspect browser network requests to `/github/me` and `/github/repositories`

### GitHub OAuth fails

- verify `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in `backend/.env`
- confirm GitHub's callback URL and Render's `GITHUB_REDIRECT_URI` both equal
  `https://githubai-anly.vercel.app/api/auth/github/callback`
- remove a Vercel `VITE_API_URL` value that points directly to Render;
  production browser requests must use `/api` so the session cookie is sent
- restart Uvicorn after changing environment values

## Contributing

Contributions are welcome.

If you want to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the relevant checks
5. Submit a pull request with a clear description

## License

This project does not currently include a license file. If you intend to make it open source, add an appropriate license such as MIT or Apache 2.0 before publishing.

## Support

For questions, issues, or feature requests, open a GitHub issue in this repository.
