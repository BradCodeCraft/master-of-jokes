import React from "react";

export default function UserCard({ user }) {
  if (user !== undefined) {
    return (
      <div className="flex justify-between w-1/2">
        <h3>{user[2]}</h3>
        <div>
          <p>{user[1]}</p>
          <p></p>
        </div>
      </div>
    );
  }
}
