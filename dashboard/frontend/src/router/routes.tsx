import {createBrowserRouter} from "react-router-dom";
import {TrajectPage} from "@/pages/Traject.tsx";
import {HomePage} from "@/pages/Home.tsx";

export const routes = createBrowserRouter([
    {
        path: "/",
        element: <HomePage/>
    },
    {
        path: "/traject/:traject",
        element: <TrajectPage/>
    }
])