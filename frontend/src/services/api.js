const API_URL = "http://localhost:8000";

export async function signOut() {
  const response = await fetch(`${API_URL}/auth/logout`, {
    method: "POST",
    credentials: "include",
    redirect: "manual"
  });

  if (!response.ok && response.type !== "opaqueredirect") {
    throw new Error("Unable to sign out");
  }
}


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

export async function getActivitySummary() {
  const response = await fetch(`${API_URL}/github/activity-summary`, {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Unable to fetch activity summary");
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

export async function askAI(question, scope = {}) {
  const response = await fetch(`${API_URL}/ai/chat`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, ...scope })
  });

  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "AI request failed");
  return data;
}