import { useState, useEffect } from 'react'
import parse from 'html-react-parser'
import { Sidechain } from '@nprapps/sidechain';

import './App.css'

function App() {
  const [sessions, setSessions] = useState([]);
  const [day, setDay] = useState('Wed 7/30');
  const [selectedSession, setSelectedSession] = useState(null);
  const [dialogPosition, setDialogPosition] = useState({ top: '50%' });

  // // choices for days:  "Wed 7/30","Thu 7/31", "Fri 8/1","Sat 8/2"
  const conferenceDays = ["Wed 7/30","Thu 7/31", "Fri 8/1","Sat 8/2"];

  // others are '2025-07-31', '2025-08-01', and '2025-08-02'
  useEffect(() => {
    // on load, get shcedule.json from public folder
    fetch('./schedule.json')
      .then(response => response.json())
      .then(data => {
        // find the day in the start_time field

        //start time is in ISO 8601 format, We want it in PST

        setSessions(data.sessions);

        // console.log(data.sessions)
      })
      .catch(error => {
        console.error('Error fetching schedule:', error)
      })
  }, [])

  // register sidechain
  useEffect(() => {
    Sidechain.registerGuest();
  }, []);

  const buttons = conferenceDays.map((dayName) => (
    <button
      key={dayName}
      className={day === dayName ? 'active' : ''}
      onClick={() => setDay(dayName)}
    >
      {dayName}
    </button>
  ));

  // Update your click handler to capture the mouse position
const handleSessionClick = (session, event) => {
  const clickY = event.clientY;
  const windowHeight = window.innerHeight;
  
  let dialogTop;
  if (clickY > windowHeight / 2) {
    // If click is in bottom half, position dialog above the click
    dialogTop = Math.max(50, clickY - 250); // Adjust 250px to account for dialog height
  } else {
    // If click is in top half, position dialog below the click
    dialogTop = Math.max(50, clickY - 50);
  }
  
  setDialogPosition({ top: `${dialogTop}px` });
  setSelectedSession(session);
};

  return (
    <>
      <div className="day-selector">
        {buttons}
      </div>
      <ul className="sessions">
        {/* filter by session.day === day */}
       {sessions.filter(session => session.day === day).map((session, index) => (
          <li 
            key={index} 
            className={`session ${session.tracks?.includes('Mixers/Receptions') ? 'other' : ''}`}
            onClick={(event) => handleSessionClick(session, event)}
          >
            <span className="meta">
              {session.time} 
            </span>
            {session.name}
          </li>
      ))}
      </ul>
      {/* Modal */}
      {selectedSession && (
        <dialog 
          open 
          style={{ '--dialog-top': dialogPosition.top }}
        >
          <button className="close-top" onClick={() => setSelectedSession(null)}>×</button>
          <h3>{selectedSession.name}</h3>
          <div className="meta">
            {selectedSession.day} - {selectedSession.time}
          </div>
          <div className="description">{parse(selectedSession.description || '')}</div>
          <a className="button" href={`https://builder.guidebook.com/g/#/guides/aaja25/schedule/sessions/${selectedSession.id}`} target="_blank" rel="noopener noreferrer">
            View in AAJA25 App
          </a>
          <button onClick={() => setSelectedSession(null)}>Close</button>
        </dialog>
      )}
    </>
  )
}

export default App
