import React, { useEffect, useState } from "react";
import JokeCard from "../components/JokeCard";
import { fetchJokesData, fetchNumberOfJokes } from "../utils/utils";

export default function Jokes() {
  const [numberOfJokes, setNumberOfJokes] = useState(0);
  const [jokesArray, setJokesArray] = useState([]);

  useEffect(() => {
    fetchJokesData().then((data) => setJokesArray(data));
    fetchNumberOfJokes().then((data) => setNumberOfJokes(data));
  }, []);

  return (
    <div className="px-4 pt-2 bg-[#edebeb] text-[#990000] min-h-dvh font-atma">
      <h1 className="text-3xl font-bold">Status Report of Jokes</h1>

      <p className="text-lg mt-2.5">
        This page shows information about jokes that users have created in our
        application.
      </p>

      <h2 className="text-2xl font-bold mt-5">Number of Jokes</h2>

      <p className="text-lg mt-2.5">
        There are {numberOfJokes} {numberOfJokes === 1 ? "joke" : "jokes"}{" "}
        registered to Master of Jokes.
      </p>

      <h2 className="text-2xl font-bold mt-5">Jokes</h2>

      <section>
        {jokesArray.map(function (joke) {
          return <JokeCard joke={joke} key={joke[0]} />;
        })}
      </section>
    </div>
  );
}
