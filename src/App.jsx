import { useState, useEffect } from 'react'

import './App.css'

function App() {
  const [sessions, setSessions] = useState([]);
  const [day, setDay] = useState('2025-07-30');

  // others are '2025-07-31', '2025-08-01', and '2025-08-02'
  useEffect(() => {
    // on load, get shcedule.json from public folder
    fetch('/schedule.json')
      .then(response => response.json())
      .then(data => {
        // find the day in the start_time field

        //start time is in ISO 8601 format, We want it in PST
        data.sessions.forEach(session => {
          const startTime = new Date(session.start_time);
          session.start_time = startTime.toLocaleString('en-US', { timeZone: 'America/Los_Angeles' });
        }); 
        setSessions(data.sessions);

        console.log(data.sessions)
      })
      .catch(error => {
        console.error('Error fetching schedule:', error)
      })
  }, [])

  return (
    <>
      <h1>#AAJA25</h1>
      <ul className="card">
       {sessions.map((session, index) => (
          <li key={index} className="session">
            <p>{session.name}</p>
          </li>
      ))}
      </ul>

    </>
  )
}

export default App
