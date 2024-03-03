import Home from "./pages/Home";
import { Routes, Route } from "react-router-dom";
import { Register } from "./pages/Register";
import { Interface } from "./pages/Interface";
import { Login } from "./pages/Login";
import { useState } from "react";
import { Navigate } from "react-router-dom";

function App() {
  const [token,setToken] = useState();
  return (
      <>
        <Routes>
            <Route path = "/" element ={<Home/>}></Route>
            <Route path = "/register" element ={<Register/>}></Route>
            <Route
              path="/login"
              element={token ? <Navigate to="/interface" /> : <Login setToken={setToken} />}
            />
            <Route path="/interface" element={token ? <Interface /> : <Navigate to="/login" />} />
        </Routes> 
      </>
  )
}

export default App;