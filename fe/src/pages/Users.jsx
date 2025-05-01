import React, { useEffect, useState } from "react";
import UserCard from "../components/UserCard";
import { fetchNumberOfUsers, fetchUserData } from "../utils/utils";

export default function Users() {
  const [numberOfUsers, setNumberOfUsers] = useState(0);
  const [usersArray, setUsersArray] = useState([]);

  useEffect(() => {
    fetchUserData().then((data) => setUsersArray(data));
    fetchNumberOfUsers().then((data) => setNumberOfUsers(data));
  }, []);

  return (
    <div className="px-4 pt-2 bg-[#edebeb] text-[#990000] min-h-dvh font-atma">
      <h1 className="text-3xl font-bold">Status Report of Users</h1>

      <p className="text-lg mt-2.5">
        This page shows information about users that have signed up to our
        application.
      </p>

      <h2 className="text-2xl font-bold mt-5">Number of Users</h2>

      <p className="text-lg mt-2.5">
        There are {numberOfUsers} {numberOfUsers === 1 ? "person" : "people"}{" "}
        registered to Master of Jokes.
      </p>

      <h2 className="text-2xl font-bold mt-5">Users</h2>

      <section>
        {usersArray.map(function (user) {
          return <UserCard user={user} key={user[0]} />;
        })}
      </section>
    </div>
  );
}
