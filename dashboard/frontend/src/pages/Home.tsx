import "leaflet/dist/leaflet.css";
import {GeoJSON, MapContainer, Marker, Popup, TileLayer} from "react-leaflet";
import {useEffect, useState} from "react";

export const HomePage = () => {
    const position = [52.522501, 6.047887];
    const [routes, setRoutes] = useState<[]>([])

    useEffect(() => {
        fetch('http://127.0.0.1:5000/rail_routes').then(res => {
            res.json().then(data => {
                setRoutes(data)
            })
        })
    }, [])

    return (
        <MapContainer center={position} zoom={13} scrollWheelZoom={true} style={{height: '100vh'}}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <Marker position={position}>
                <Popup>
                    A pretty CSS3 popup. <br/> Easily customizable.
                </Popup>
            </Marker>
            {routes.map((route) =>
                <GeoJSON data={route} style={(route) => ({color: route.style.color})}>
                    <Popup>
                        From: {route['properties']['from']}, To: {route['properties']['to']}
                    </Popup>
                </GeoJSON>
            )}
        </MapContainer>
    )
}