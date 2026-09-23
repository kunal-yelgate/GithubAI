const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

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
  let response;
  try {
    response = await fetch(
      `${API_URL}/github/repositories/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/analysis`,
      { credentials: "include" }
    );
  } catch {
    throw new Error(
      "Could not reach the backend. Make sure the API is running on port 8000."
    );
  }

  if (!response.ok) {
    let message = "Unable to analyze repository";
    try {
      const errorData = await response.json();
      if (errorData?.detail) message = errorData.detail;
    } catch {
      // Keep the fallback when the server does not return JSON.
    }
    throw new Error(message);
  }

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
  let response;

  try {
    response = await fetch(`${API_URL}/ai/chat`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, ...scope })
    });
  } catch (error) {
    throw new Error(
      "Unable to reach the backend AI API. Make sure the API server is running on http://localhost:8000."
    );
  }

  let data = {};
  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Your session has expired. Please log in again to use the AI assistant.");
    }

    if (response.status === 403) {
      throw new Error("AI access is not allowed for this session.");
    }

    throw new Error(data?.detail || "AI request failed");
  }

  return data;
}