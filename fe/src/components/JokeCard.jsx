import React from "react";

export default function JokeCard({ joke }) {
  console.log(joke);

  if (joke !== undefined) {
    return (
      <div className="flex justify-between w-1/2">
        <h3>{joke[3]}</h3>
        <div>
          <p>{joke[4]}</p>
        </div>
      </div>
    );
  }
}
