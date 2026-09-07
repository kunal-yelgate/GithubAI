# GitHub AI Repo Intelligence

A full-stack application that authenticates with GitHub, displays a user's repositories, and provides fresh, evidence-based repository and architecture analysis with Groq or Mistral.

## Stack

- **Frontend:** React 19, Vite, JavaScript
- **Backend:** FastAPI, Uvicorn, HTTPX
- **Authentication:** GitHub OAuth with a signed session cookie
- **GitHub API:** User profile, repositories, repository languages, commits, tree, and file contents
- **AI:** Groq and Mistral chat completion providers with retrieval-augmented repository context

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
.github/workflows/  Frontend and backend continuous integration
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

Optional AI configuration can be added to `backend/.env`:

```env
AI_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
MISTRAL_API_KEY=your_mistral_api_key
AI_MODEL=your_provider_model
```

When `AI_MODEL` is not set, the application uses the configured provider's default model. Keep provider keys private and never commit them.

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

| Method | Endpoint                                       | Description                                    |
| ------ | ---------------------------------------------- | ---------------------------------------------- |
| `GET`  | `/`                                            | API health response                            |
| `GET`  | `/auth/github`                                 | Starts GitHub OAuth                            |
| `GET`  | `/auth/github/callback`                        | Handles the OAuth callback                     |
| `GET`  | `/github/me`                                   | Returns the authenticated GitHub user          |
| `GET`  | `/github/repositories`                         | Returns the authenticated user's repositories  |
| `GET`  | `/github/repositories/{owner}/{repo}/analysis` | Analyzes a repository                          |
| `GET`  | `/github/activity-summary`                     | Returns authored pull request and issue counts |
| `POST` | `/github/analyze-all`                          | Analyzes all accessible user repositories      |
| `POST` | `/ai/chat`                                     | Answers a profile or repository question       |
| `POST` | `/ai/index/{owner}/{repo}`                     | Rebuilds the repository code index             |

The GitHub data endpoints require the signed `session` cookie created during login.

## Repository Analysis

The repository analysis endpoint currently returns:

- Repository metadata such as name, description, stars, forks, issues, and default branch
- Language statistics
- Repository structure, including files, directories, and extensions
- Recent commit and activity analysis
- Detected technologies, dependency files, README signals, and important files
- Source-level summaries for functions, classes, components, imports, exports, and routes
- Architecture type, inferred layers, entry points, and import-based module relationships

The analyzer uses the repository's actual default branch when requesting the Git tree. It inspects a bounded set of prioritized files concurrently, then caches the result against GitHub's latest repository update timestamp.

## AI Repository Questions

Repository questions use the latest repository version as the retrieval source. The system combines structured analysis with relevant code chunks and import relationships before calling the selected AI provider. If the repository context is too large for the automatic Groq request, the service can retry with Mistral.

Examples of useful questions:

- `Explain the architecture and request flow.`
- `Where is authentication implemented?`
- `Which modules depend on the GitHub API?`
- `What are the main entry points and service boundaries?`

## Continuous Integration

The GitHub Actions workflow in `.github/workflows/ci.yml` runs on pushes to `main` or `master` and on pull requests. It installs dependencies, runs frontend ESLint and production build checks, and compiles the backend.

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
