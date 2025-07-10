import { useState, useEffect } from 'react'

import './App.css'

function App() {

  const [day, setDay] = useState('2025-07-30');

  // others are '2025-07-31', '2025-08-01', and '2025-08-02'
  useEffect(() => {
    // on load, get shcedule.json from public folder
    fetch('/schedule.json')
      .then(response => response.json())
      .then(data => {
        // find the day in the start_time field

        console.log(data)
      })
      .catch(error => {
        console.error('Error fetching schedule:', error)
      })
  }, [])

  return (
    <>
      <h1>#AAJA25</h1>
      <div className="card">
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
