import { Outlet } from "react-router-dom";

export default function NavigationBar() {
  return (
    <>
      <nav className="bg-[#ffffff] text-[#990000] font-atma px-4 py-1 grid grid-cols-5 gap-x-2">
        <h1 className="text-4xl col-span-4 font-semibold">
          <a href="/">Master of Jokes</a>
        </h1>
        <ul className="flex justify-evenly">
          <li className="flex justify-center items-center text-xl">
            <a href="/users">Users</a>
          </li>
          <li className="flex justify-center items-center text-xl">
            <a href="/jokes">Jokes</a>
          </li>
        </ul>
      </nav>

      <Outlet />
    </>
  );
}
