import {FC, useEffect, useState} from "react";
import {GeoJSON, MapContainer, Marker, Popup, TileLayer, useMap} from "react-leaflet";
import {RailRouteType} from "@/types/RailRouteType.ts";
import {RailRoutesLines} from "@/components/RailRoutesLines.tsx";


interface RailRoutesMapProps {
    railRoute?: RailRouteType | undefined
}

export const RailRoutesMap: FC<RailRoutesMapProps> = ({railRoute = undefined}) => {
    const position = {lat: 52.08692807718995, lng: 5.167149365332764};

    return (
        <MapContainer center={position} zoom={8} scrollWheelZoom={true}
                      style={{height: '100%', borderRadius: '0.375rem'}}>
            <TileLayer
                /*Extra map colors https://leaflet-extras.github.io/leaflet-providers/preview/*/
                url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
            />
            <RailRoutesGeoJson railRoute={railRoute}/>
        </MapContainer>
    )
}

const RailRoutesGeoJson: FC<RailRoutesMapProps> = ({railRoute}) => {
    const map = useMap();
    const [routes, setRoutes] = useState<[]>([])
    const [geoJsonKey, setGeoJsonKey] = useState(0);

    useEffect(() => {
        if (railRoute == undefined) {
            fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/rail_routes`).then(res => {
                res.json().then(data => {
                    setRoutes(data)
                })
            })
        } else {
            setRoutes(railRoute.geojson)
            map.setView({
                lat: Number(railRoute.from_coordinates.split(',')[0]),
                lng: Number(railRoute.from_coordinates.split(',')[1])
            }, 9.2)
            // geo json force rerender geo json on map
            setGeoJsonKey(prevKey => prevKey + 1)
        }

    }, [railRoute])

    return (
        <>  {railRoute != undefined &&
            <GeoJSON key={geoJsonKey} data={railRoute?.car_geo_json} style={{color: '#0063D3'}}>
                <Popup>
                    Car route
                </Popup>
            </GeoJSON>}
            {routes.map((route, index) =>
                <GeoJSON key={index + geoJsonKey} data={route} style={(route) => ({color: railRoute != undefined ? '#FFC917' : route.styles.color})}>
                    <Popup>
                        From: {route['stations'][0]}, To: {route['stations'][1]}
                    </Popup>
                </GeoJSON>
            )}
        </>
    )
}