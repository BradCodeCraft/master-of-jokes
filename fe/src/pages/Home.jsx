import React from "react";

export default function Home() {
  return (
    <div className="px-4 pt-2 bg-[#edebeb] text-[#990000] min-h-dvh font-atma">
      <h1 className="text-3xl font-bold">
        Welcome to Status Report of Master of Jokes
      </h1>

      <p className="text-lg mt-2.5">
        The purpose of this page is to showcase the use case of{" "}
        <strong>React as a Front end</strong> that can make asynchronous call to
        the <strong>Flask application in the Back end</strong> for data about
        the users and jokes in the database.
      </p>

      <h2 className="text-2xl font-bold mt-5">Instructions</h2>

      <p className="text-lg mt-2.5">
        Just navigate to either the users or the jokes page using the navigation
        link in the navigation bar.
      </p>
    </div>
  );
}
