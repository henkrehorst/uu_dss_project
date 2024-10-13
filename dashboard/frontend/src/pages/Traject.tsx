 // This page is supposed to show the railroute-specific data when a railroute IS selected

import {useParams} from "react-router-dom";
import {DashboardLayout} from "@/layouts/DashboardLayout.tsx";
import {RailRoutesMap} from "@/components/RailRoutesMap.tsx";
import {TravelersCompensationsLineGraph} from "@/components/TravelersCompensationsLineGraph.tsx";
import {TBSPerformanceGauge} from "@/components/TBSPerformanceGauge.tsx";
import {InfrastructurePerformanceGauge} from "@/components/InfrastructurePerformanceGauge.tsx";
import {EquipmentPerformanceGauge} from "@/components/EquipmentPerformanceGauge.tsx";

export const TrajectPage = () => {
    let {traject} = useParams<{traject: string}>()

  return (
      <DashboardLayout
          mapComponent={<RailRoutesMap/>}
          title={'Tough Autumn Dashboard'}
          gaugeSlot1={<TBSPerformanceGauge/>}
          gaugeSlot2={<EquipmentPerformanceGauge/>}
          gaugeSlot3={<InfrastructurePerformanceGauge/>}
          lineGraphSlot1={<TravelersCompensationsLineGraph/>}
          lineGraphSlot2={<TravelersCompensationsLineGraph/>}
      />
  )
}