// This page is supposed to show the railroute-specific data when a railroute IS selected

import {useParams} from "react-router-dom";
import {RailRoutesMap} from "@/components/RailRoutesMap.tsx";
import {TBSPerformanceGauge} from "@/components/TBSPerformanceGauge.tsx";
import {InfrastructurePerformanceGauge} from "@/components/InfrastructurePerformanceGauge.tsx";
import {EquipmentPerformanceGauge} from "@/components/EquipmentPerformanceGauge.tsx";
import {RailRoutesLines} from "@/components/RailRoutesLines.tsx";
import {RailRouteDashboardLayout} from "@/layouts/RailRouteDashboardLayout.tsx";
import {useEffect, useState} from "react";
import {RailRouteType} from "@/types/RailRouteType.ts";
import {TravelTimeComparisonBarChart} from "@/components/charts/TravelTimeComparisonBarChart.tsx";
import {EmissionComparisonBarChart} from "@/components/charts/EmissionComparisonBarChart.tsx";

export const RailRoutePage = () => {
    let {toStation, fromStation} = useParams<{ toStation: string, fromStation: string }>()

    const [railRoute, setRailRoute] = useState<RailRouteType | undefined>(undefined)

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/rail_routes/lines/${fromStation}/${toStation}`).then(res => {
            res.json().then(data => {
                setRailRoute(data)
            })
        })

    }, [toStation, fromStation])

    return (
        <>
            {railRoute != undefined && <RailRouteDashboardLayout
                mapComponent={<RailRoutesMap railRoute={railRoute}/>}
                railRouteName={railRoute.name}
                title={'Tough Autumn Dashboard'}
                railLinesComponent={<RailRoutesLines/>}
                gaugeSlot1={<TBSPerformanceGauge/>}
                gaugeSlot2={<EquipmentPerformanceGauge/>}
                gaugeSlot3={<InfrastructurePerformanceGauge/>}
                lineGraphSlot1={<EmissionComparisonBarChart fromStation={railRoute.from_station}
                                                            toStation={railRoute.to_station}/>}
                lineGraphSlot2={<TravelTimeComparisonBarChart fromStation={railRoute.from_station}
                                                              toStation={railRoute.to_station}/>}
            />}
        </>
    )
}