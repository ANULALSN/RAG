import { useEffect, useState } from "react";
import Subject from "./pages/Subject";
import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import AppShell from "./components/layout/AppShell";
import Home from "./pages/Home";
import Chat from "./pages/Chat";

type Theme = "light" | "dark";

function App() {
  const [theme, setTheme] = useState<Theme>(() => {
    const saved =
      localStorage.getItem("subzero-theme");

    return saved === "light" || saved === "dark"
      ? saved
      : "dark";
  });

  useEffect(() => {
    document.documentElement.setAttribute(
      "data-theme",
      theme
    );

    localStorage.setItem(
      "subzero-theme",
      theme
    );
  }, [theme]);

  const toggleTheme = () => {
    setTheme((current) =>
      current === "dark" ? "light" : "dark"
    );
  };

  return (
    <BrowserRouter>
      <AppShell
        theme={theme}
        onToggleTheme={toggleTheme}
      >
        <Routes>
  <Route path="/" element={<Home />} />
  <Route
  path="/subjects/:subjectId/chat"
  element={<Chat />}
/>

  <Route
    path="/subjects/:subjectId"
    element={<Subject />}
  />
</Routes>
      </AppShell>
    </BrowserRouter>
  );
}

export default App;