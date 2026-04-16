import { useState } from 'react'
import logo from './assets/quickcourselogo.png'
import './App.css'

function App() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = () => {
    console.log("Username:", username)
    console.log("Password:", password)

    // connect to back-end later
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
