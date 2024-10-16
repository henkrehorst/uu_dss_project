import {RouterProvider} from "react-router-dom";
import {routes} from "@/router/routes.tsx";


function App() {
  return (
    <RouterProvider router={routes}/>
  )
}

export default App
