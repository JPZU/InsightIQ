import React, { useEffect, useState } from "react";
import { getUsers } from "./services/api";

function App() {
  const [users, setUsers] = useState<{ message: string } | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const data = await getUsers();
        setUsers(data);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="App">
      <h1>Welcome to SoftServeAnalytics Frontend</h1>
      {users ? (
        <p>{users.message}</p>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;