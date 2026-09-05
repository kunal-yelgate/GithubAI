# GitHub AI Repo Analyzer

A full-stack application that authenticates with GitHub, displays a user's repositories, and analyzes repository metadata, languages, structure, commits, and technologies.

## Stack

- **Frontend:** React 19, Vite, JavaScript
- **Backend:** FastAPI, Uvicorn, HTTPX
- **Authentication:** GitHub OAuth with a signed session cookie
- **GitHub API:** User profile, repositories, repository languages, commits, tree, and file contents

## Project Structure

```text
backend/
  app/
    analyzers/       Repository language, structure, and technology analyzers
    routes/          Authentication and GitHub API routes
    services/        GitHub OAuth, API, and repository analysis services
    config.py        Environment configuration
    main.py          FastAPI application
    session.py       Signed session cookie helpers
  requirements.txt

frontend/
  src/
    pages/           Login and dashboard screens
    services/        Backend API client
    App.jsx          Session bootstrap and page selection
  package.json

implementation/     Step-by-step implementation notes
```

## Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer
- A GitHub OAuth App

## GitHub OAuth Setup

Create an OAuth App in GitHub under **Settings > Developer settings > OAuth Apps**.

Use these local development values:

- **Homepage URL:** `http://localhost:5173`
- **Authorization callback URL:** `http://localhost:8000/auth/github/callback`

Create `backend/.env` with the following values:

```env
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback
FRONTEND_URL=http://localhost:5173
```

Do not commit `backend/.env` or expose the client secret.

## Backend Setup

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API is available at `http://localhost:8000`.

FastAPI's interactive documentation is available at:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Frontend Setup

Open a second terminal from the repository root:

```powershell
cd frontend
npm install
npm run dev
```

The frontend is available at `http://localhost:5173`.

Useful frontend commands:

```powershell
npm run build
npm run lint
npm run preview
```

## Authentication Flow

1. Open `http://localhost:5173`.
2. Select **Login with GitHub**.
3. GitHub redirects to the backend callback.
4. The backend exchanges the OAuth code for an access token.
5. The backend creates a signed `session` cookie and redirects to the dashboard.
6. The dashboard requests the authenticated GitHub user and repository list.

## API Endpoints

| Method | Endpoint                                       | Description                                   |
| ------ | ---------------------------------------------- | --------------------------------------------- |
| `GET`  | `/`                                            | API health response                           |
| `GET`  | `/auth/github`                                 | Starts GitHub OAuth                           |
| `GET`  | `/auth/github/callback`                        | Handles the OAuth callback                    |
| `GET`  | `/github/me`                                   | Returns the authenticated GitHub user         |
| `GET`  | `/github/repositories`                         | Returns the authenticated user's repositories |
| `GET`  | `/github/repositories/{owner}/{repo}/analysis` | Analyzes a repository                         |

The GitHub data endpoints require the signed `session` cookie created during login.

## Repository Analysis

The repository analysis endpoint currently returns:

- Repository metadata such as name, description, stars, forks, issues, and default branch
- Language statistics
- Repository structure, including files, directories, and extensions
- Number of fetched commits

The analyzer uses the repository's actual default branch when requesting the Git tree.

## Troubleshooting

### The dashboard shows no data

- Confirm both the backend and frontend are running.
- Confirm the browser is using `http://localhost:5173`.
- Confirm the GitHub OAuth callback URL exactly matches `GITHUB_REDIRECT_URI`.
- Clear stale localhost cookies and log in again.
- Check the browser network panel for failed requests to `/github/me` or `/github/repositories`.

### GitHub OAuth fails

- Verify `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in `backend/.env`.
- Verify the callback URL in GitHub matches the backend environment variable exactly.
- Restart Uvicorn after changing `.env` values.

## License

No license has been specified for this project yet.
