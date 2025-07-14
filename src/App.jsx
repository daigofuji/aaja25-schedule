import { useState, useEffect } from 'react'
import parse from 'html-react-parser'

import './App.css'

function App() {
  const [sessions, setSessions] = useState([]);
  const [day, setDay] = useState('Wed 7/30');
  const [selectedSession, setSelectedSession] = useState(null);

  // // choices for days:  "Wed 7/30","Thur 7/31", "Fri 8/1","Sat 8/2"
  const conferenceDays = ["Wed 7/30","Thur 7/31", "Fri 8/1","Sat 8/2"];

  // others are '2025-07-31', '2025-08-01', and '2025-08-02'
  useEffect(() => {
    // on load, get shcedule.json from public folder
    fetch('./schedule.json')
      .then(response => response.json())
      .then(data => {
        // find the day in the start_time field

        //start time is in ISO 8601 format, We want it in PST

        setSessions(data.sessions);

        console.log(data.sessions)
      })
      .catch(error => {
        console.error('Error fetching schedule:', error)
      })
  }, [])

  const buttons = conferenceDays.map((dayName) => (
    <button
      key={dayName}
      className={day === dayName ? 'active' : ''}
      onClick={() => setDay(dayName)}
    >
      {dayName}
    </button>
  )); 
  return (
    <>
      <div className="day-selector">
        {buttons}
      </div>
      <ul className="sessions">
        {/* filter by session.day === day */}
       {sessions.filter(session => session.day === day).map((session, index) => (
          <li key={index} className="session" onClick={() => setSelectedSession(session)}>
            <span className="meta">
              {session.time} - {session.locations?.[0] || 'TBD'}
            </span>
            {session.name}
          </li>
      ))}
      </ul>
      {/* Modal */}
      {selectedSession && (
        <dialog open>
          <button className="close-top" onClick={() => setSelectedSession(null)}>×</button>
          <h3>{selectedSession.name}</h3>
          <div className="meta">
            {selectedSession.day} - {selectedSession.time} - {selectedSession.locations?.[0] || 'TBD'}
          </div>
          <div>{parse(selectedSession.description || '')}</div>
          <button onClick={() => setSelectedSession(null)}>Close</button>
        </dialog>
      )}
    </>
  )
}

export default App
