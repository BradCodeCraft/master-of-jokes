import { BrowserRouter, Route, Routes } from "react-router-dom";
import NavigationBar from "./components/NavigationBar";
import Home from "./pages/Home";
import Jokes from "./pages/Jokes";
import Users from "./pages/Users";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<NavigationBar />}>
          <Route index element={<Home />} />
          <Route path="users" element={<Users />} />
          <Route path="jokes" element={<Jokes />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
