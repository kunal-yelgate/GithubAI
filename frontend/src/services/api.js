const API_URL = "http://localhost:8000";


export async function getCurrentUser() {

  const response = await fetch(
    `${API_URL}/github/me`,
    {
      credentials: "include"
    }
  );

  if (!response.ok) {
    throw new Error("Not authenticated");
  }

  return response.json();
}


export async function getRepositories() {

  const response = await fetch(
    `${API_URL}/github/repositories`,
    {
      credentials: "include"
    }
  );

  if (!response.ok) {
    throw new Error("Unable to fetch repositories");
  }

  return response.json();
}

export async function analyzeRepository(owner, repo) {
  const response = await fetch(
    `${API_URL}/github/repositories/${owner}/${repo}/analysis`,
    { credentials: "include" }
  );

  if (!response.ok) throw new Error("Unable to analyze repository");
  return response.json();
}

export async function analyzeAllRepositories() {
  const response = await fetch(`${API_URL}/github/analyze-all`, {
    method: "POST",
    credentials: "include"
  });

  if (!response.ok) throw new Error("Unable to analyze repositories");
  return response.json();
}