import {createBrowserRouter} from "react-router-dom";
import {RailRoutePage} from "@/pages/RailRoute.tsx";
import {HomePage} from "@/pages/Home.tsx";

export const routes = createBrowserRouter([
    {
        path: "/",
        element: <HomePage/>
    },
    {
        path: "/route/:fromStation/:toStation",
        element: <RailRoutePage/>
    }
])