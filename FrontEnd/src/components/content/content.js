import React from "react";

import DaysOfWeek from "./daysOfWeek"
import CalendarSquares from "./calendarSquares"

export default function content(props) {
    return (
        <div className="content">
            <DaysOfWeek />
            <CalendarSquares 
                daysInMonth={props.daysInMonth} 
                daysInPreviousMonth={props.daysInPreviousMonth}
                startDay={props.startDay}
                month={props.month}
                year={props.year}
            />


        </div>
    )
}