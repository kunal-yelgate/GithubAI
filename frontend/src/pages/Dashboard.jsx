import { useEffect, useState } from "react";
import {
  getCurrentUser,
  getRepositories
} from "../services/api";


function Dashboard() {

  const [user, setUser] = useState(null);
  const [repositories, setRepositories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    async function loadData() {

      try {

        const userData = await getCurrentUser();
        const repoData = await getRepositories();

        setUser(userData);
        setRepositories(repoData);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);

      }
    }

    loadData();

  }, []);


  if (loading) {
    return <h2>Loading GitHub data...</h2>;
  }


  return (
    <div>

      <h1>GitHub AI Repo Analyzer</h1>

      {user && (
        <div>
          <img
            src={user.avatar_url}
            alt="GitHub avatar"
            width="80"
          />

          <h2>{user.name || user.login}</h2>

          <p>@{user.login}</p>
        </div>
      )}

      <hr />

      <h2>
        Your Repositories ({repositories.length})
      </h2>

      {repositories.map((repo) => (

        <div key={repo.id}>

          <h3>{repo.name}</h3>

          <p>
            Language: {repo.language || "Unknown"}
          </p>

          <p>
            ⭐ {repo.stargazers_count}
          </p>

        </div>

      ))}

    </div>
  );
}


export default Dashboard;