import { use, useState } from 'react'
import { BrowserRouter as Router, Routes, Route, useNavigate, useNavigation } from 'react-router-dom'
import logo from './assets/quickcourselogo.png'
import './App.css'

const base_url = "http://localhost:5000";

function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleLogin = async () => {
    try {
      const response = await fetch(base_url + '/login', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: 'include'
      });
  
      const data = await response.json();
  
      if (response.ok) {
        console.log("Logged in:", data);
        navigate('/dashboard')
      } else {
        console.log("Error:", data);
      }
    } catch (err) {
      console.error("Request failed:", err);
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
      <button onClick={() => navigate('/studentdashboard')}>
        Goes to Dashboard. You will access this via sign in when thats functional
      </button>

      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  )
}

function StudentDashboard() {
  const navigate = useNavigate()
  return (
    <section id="header">
      <div style={{display: 'flex', justifyContent: 'flex-end', padding: '40px'}}>
        <button onClick={() => navigate('/')}>
           Sign Out. Takes you back to Login
        </button>
      </div>
      <div style={{textAlign: "center" }}>
        <h1>Your Courses</h1>
        <table>
            <tr>
              <th>Course Name</th>
              <th>Teacher</th>
              <th>Time</th>
              <th>Course Capacity</th>
            </tr>
            <tr></tr>
        </table>
      </div>
      <section id='footer'>
        <div style={{display: 'flex', justifyContent: 'flex-end', padding: '40px'}}>
         <button onClick={() => navigate('/studentaddcourses')}>
            Add Courses
          </button>
        </div>
      </section>
    </section>  
  )
}

function StudentAddCourses() {
  const navigate = useNavigate()
  return (
    <section id="header">
      <div style={{display: 'flex', justifyContent: 'flex-end', padding: '40px'}}>
        <button onClick={() => navigate('/')}>
           Sign Out. Takes you back to Login
        </button>
      </div>
      <div style={{textAlign: "center" }}>
        <h1>Add Courses</h1>
      </div>
      <section id='footer'>
        <div style={{display: 'flex', justifyContent: 'flex-end', padding: '40px'}}>
         <button onClick={() => navigate('/studentdashboard')}>
            View Courses
          </button>
        </div>
      </section>
    </section>  
  )
}

function TeacherDashboard() {
  const navigate = useNavigate()
  return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      <h1>Your Courses</h1>
      <p></p>
      <button onClick={() => navigate('/')}>
        Sign Out. Takes you back to Login
      </button>
    </div>
  )
}

function AdminDashboard() {
  const navigate = useNavigate()
  return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      <h1>View All Courses</h1>
      <p></p>
      <button onClick={() => navigate('/')}>
        Sign Out. Takes you back to Login
      </button>
    </div>
  )
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/studentdashboard" element={<StudentDashboard />} />
        <Route path="/studentaddcourses" element={<StudentAddCourses />} />
        <Route path="/teacherdashboard" element={<TeacherDashboard />} />
        <Route path="/admindashboard" element={<AdminDashboard />} />
      </Routes>
    </Router>
  )
}

export default App
