import {useEffect, useState} from "react";
import {GeoJSON, MapContainer, Marker, Popup, TileLayer} from "react-leaflet";


export const RailRoutesMap = () => {
    const position = {lat: 52.08692807718995, lng: 5.167149365332764};
    const [routes, setRoutes] = useState<[]>([])

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/rail_routes`).then(res => {
            res.json().then(data => {
                setRoutes(data)
            })
        })
    }, [])

    return (
        <MapContainer center={position} zoom={8} scrollWheelZoom={true} style={{height: '100%', borderRadius: '0.375rem'}}>
            <TileLayer
                /*Extra map colors https://leaflet-extras.github.io/leaflet-providers/preview/*/
                url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
            />
            {/*<Marker position={position}>*/}
            {/*    <Popup>*/}
            {/*        A pretty CSS3 popup. <br/> Easily customizable.*/}
            {/*    </Popup>*/}
            {/*</Marker>*/}
            {routes.map((route, index) =>
                <GeoJSON key={index} data={route} style={(route) => ({color: route.styles.color})}>
                    <Popup>
                        From: {route['stations'][0]}, To: {route['stations'][1]}
                    </Popup>
                </GeoJSON>
            )}
        </MapContainer>
    )
}