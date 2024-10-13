import {useEffect, useState} from "react";
import {GeoJSON, MapContainer, Marker, Popup, TileLayer} from "react-leaflet";

export const RailRoutesMap = () => {
    const position = {lat: 51.505, lng: -0.09};
    const [routes, setRoutes] = useState<[]>([])

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/rail_routes`).then(res => {
            res.json().then(data => {
                setRoutes(data)
            })
        })
    }, [])

    return (
        <MapContainer center={position} zoom={13} scrollWheelZoom={true} style={{height: '100%', borderRadius: '0.375rem'}}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <Marker position={position}>
                <Popup>
                    A pretty CSS3 popup. <br/> Easily customizable.
                </Popup>
            </Marker>
            {routes.map((route, index) =>
                <GeoJSON key={index} data={route} style={(route) => ({color: route.style.color})}>
                    <Popup>
                        From: {route['properties']['from']}, To: {route['properties']['to']}
                    </Popup>
                </GeoJSON>
            )}
        </MapContainer>
    )
}