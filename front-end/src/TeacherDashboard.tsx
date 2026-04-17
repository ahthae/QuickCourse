import { BrowserRouter as Router, Routes, Route, useNavigate, useNavigation } from 'react-router-dom'

export default function TeacherDashboard({baseUrl}) {
    const navigate = useNavigate()
    const user = JSON.parse(localStorage.getItem('user'))
    
  return (
    <section id="header">
      <div style={{display: 'flex', justifyContent: 'flex-end', padding: '40px'}}>
        <button onClick={() => navigate('/')}>
           Sign Out. Takes you back to Login
        </button>
      </div>
      <div style={{textAlign: "center" }}>
        <h1>Hello, {user.username}. Your Courses</h1>
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