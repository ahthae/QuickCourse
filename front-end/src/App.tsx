import { useState } from 'react'
import logo from './assets/quickcourselogo.png'
import './App.css'

const base_url = "http://localhost:5000";

function App() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = async () => {
    console.log("Username:", username)
    console.log("Password:", password)

    const response = await fetch(base_url+'/login', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({"username": username, "password": password})
    });

    if (response.ok) {
      console.log("logged in as " + username);
    }
  }

  return (
    <>
      <section id="center">
        <div className="logo">
          <img src={logo} alt="QuickCourse logo" />
        </div>

        <div>
          <h1>User Login</h1>
        </div>

        <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleLogin}>
          Sign in
        </button>
      </section>

      <div className="ticks"></div>


      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  )
}

export default App
