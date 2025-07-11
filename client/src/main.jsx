import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { router } from "@/routes";
import "./index.css";
import { RouterProvider } from "react-router-dom";
import AuthProvider from "@/context/auth-context";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  </StrictMode>
);
