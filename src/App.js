import React, { useState, useEffect } from 'react';
import './App.css'

function TrainBoard() {
  const [departures, setDepartures] = useState([]);
  const [dayOfWeek, setDayOfWeek] = useState("Monday")
  const [date, setDate] = useState("01-01-2000")
  const [time, setTime] = useState("12:00 AM")
  
  useEffect(() => {
    fetch('/train_board').then(res => res.json()).then(data => {
      setDepartures(data.departures);
      setDayOfWeek(data.day_of_week);
      setDate(data.date)
      setTime(data.time)
      document.title = "North Station Departures"
    });
  }, []);

  return (
    <div className="TrainBoard">

            <div class="date">
            <p>{dayOfWeek}</p>
            </div>

            <div class="date">
            <p>{date}</p>
            </div>

            <div class="station">
           <h1>North Station</h1>
            </div>

            <div class="time">
            <p>{time}</p>
            </div>

            <div class="destination-header">
              <p> Destination </p>
            </div>

            <div class = "dep-time-header">
              <p> Time </p>
            </div>

            <div class = "status-header">
              <p> Status </p>
            </div>

            <div class = "train-number-header">
              <p> Train # </p>
            </div>

            {departures.map((departure) => (
            <>
            <div class="destination">
              <p> {departure.destination} </p>
            </div>
            <div class="dep-time">
              <p> {departure.departure_time} </p>
            </div>
            <div class = "status">
              <p> {departure.status} </p>
            </div>
            <div class = "train-number">
              <p> {departure.train_number} </p>
            </div>
            </>
            ))}

           
    </div>

  );
}

export default TrainBoard;
