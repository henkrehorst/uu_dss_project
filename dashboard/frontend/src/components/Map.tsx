import {Marker, Popup, TileLayer} from "react-leaflet"
import {MapContainer} from "react-leaflet"
import 'leaflet/dist/leaflet.css';
import {GeoJSON} from 'react-leaflet/GeoJSON'
import '/dashboard/ns_get_railroads.py'

export const MapComponent = () => {
    const position = [52.0869292262318, 5.167003617262731]
    return (
        <MapContainer center={position} zoom={8.4} style={{height: '100vh'}} scrollWheelZoom={true}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {/*<Marker position={position}>*/}
            {/*    <Popup>*/}
            {/*        A pretty CSS3 popup. <br/> Easily customizable.*/}
            {/*    </Popup>*/}
            {/*</Marker>*/}
            <GeoJSON attribution="&copy; credits due..." data={...}/>
        </MapContainer>
    )
}

// https://react-leaflet.js.org/docs/example-vector-layers/