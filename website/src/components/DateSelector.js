import React from "react";

function DateSelector({
  dates,
  selectedDate,
  onDateChange
}) {
  const formatDate = (dateStr) => {
    try {
      const date = new Date(dateStr + "T00:00:00");
      return date.toLocaleDateString("en-US", {
        weekday: "short",
        month: "short",
        day: "numeric",
        year: "numeric"
      });
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="date-selector">
      <label htmlFor="date-select">
        Edition
      </label>

      <select
        id="date-select"
        value={selectedDate}
        onChange={(event) =>
          onDateChange(event.target.value)
        }
      >
        {dates.map((date) => (
          <option key={date} value={date}>
            {formatDate(date)}
          </option>
        ))}
      </select>
    </div>
  );
}

export default DateSelector;