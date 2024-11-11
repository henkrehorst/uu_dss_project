// This page is supposed to show the railroute-specific data when a railroute IS selected

import {useParams} from "react-router-dom";
import {RailRoutesMap} from "@/components/RailRoutesMap.tsx";
import {TravelersCompensationsLineGraph} from "@/components/TravelersCompensationsLineGraph.tsx";
import {TBSPerformanceGauge} from "@/components/TBSPerformanceGauge.tsx";
import {InfrastructurePerformanceGauge} from "@/components/InfrastructurePerformanceGauge.tsx";
import {EquipmentPerformanceGauge} from "@/components/EquipmentPerformanceGauge.tsx";
import {RailRoutesLines} from "@/components/RailRoutesLines.tsx";
import {RailRouteDashboardLayout} from "@/layouts/RailRouteDashboardLayout.tsx";
import {useEffect, useState} from "react";
import {RailRouteType} from "@/types/RailRouteType.ts";

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
                lineGraphSlot1={<TravelersCompensationsLineGraph/>}
                lineGraphSlot2={<TravelersCompensationsLineGraph/>}
            />}
        </>
    )
}