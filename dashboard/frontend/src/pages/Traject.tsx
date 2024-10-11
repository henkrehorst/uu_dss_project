 // This page is supposed to show the railroute-specific data when a railroute IS selected

import {useParams} from "react-router-dom";

export const TrajectPage = () => {
    let {traject} = useParams<{traject: string}>()

  return (
      <h1>Traject: {traject}</h1>
  )
}