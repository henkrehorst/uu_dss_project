export interface RailRouteType {
  color: string
  from_coordinates: string
  from_station: string
  geojson: any,
  car_geo_json: any
  id: number
  name: string
  tariff_units: number
  to_coordinates: string
  to_station: string
  trip_duration: number
}