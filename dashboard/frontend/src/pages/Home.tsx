import "leaflet/dist/leaflet.css";
import {RailRoutesMap} from "@/components/RailRoutesMap.tsx";
import {RailRoutesLines} from "@/components/RailRoutesLines.tsx";
import {HomeDashboardLayout} from "@/layouts/HomeDashboardLayout.tsx";

export const HomePage = () => {

    return (
        <HomeDashboardLayout
          mapComponent={<RailRoutesMap/>}
          title={'Tough Autumn Dashboard'}
          railLinesComponent={<RailRoutesLines/>}
      />
    )
}