import { useEffect, useState } from "react";
import LoginPage from "./components/LoginPage";

function App() {
  const [data, setData] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((res) => res.json())
      .then((data) => setData(data.message));
  }, []);

  
  return (
    <>
      <LoginPage />
      <h1>{data}</h1>
    </>
  );;
}

export default App;