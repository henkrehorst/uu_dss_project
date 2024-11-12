import {ResponsiveBar} from '@nivo/bar'
import {FC, useEffect, useState} from "react";
import {Heading, Spinner} from "@chakra-ui/react";


interface TravelTimeComparisonLineChartProps {
    fromStation: string;
    toStation: string;
}

export const TravelTimeComparisonBarChart: FC<TravelTimeComparisonLineChartProps> = ({toStation, fromStation}) => {
    const [data, setData] = useState<any | undefined>(undefined)

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/rail_routes/lines/${fromStation}/${toStation}/duration_comparison`).then(res => {
            res.json().then(data => {
                setData(data)
            })
        })

    }, [toStation, fromStation])


    return (
        <>
            <Heading size={'md'}
                     textAlign='center'
                     color={'blue.500'}>Travel time comparison by vehicle</Heading>
            {data == undefined ? <Spinner/> :
                <ResponsiveBar
                    data={data}
                    indexBy="vehicle"
                    keys={[
                        "travel time car",
                        "travel time train",
                        "travel time differences"
                    ]}
                    colors={['#0063D3', '#FFC917', '#DB0029']}
                    margin={{top: 20, right: 20, bottom: 60, left: 80}}
                    height={400}
                    padding={0.3}
                    valueScale={{type: 'linear'}}
                    indexScale={{type: 'band', round: true}}
                    borderColor={{
                        from: 'color'
                    }}
                    tooltip={({
                                       id,
                                       value
                                   }) => (<div style={{
                        padding: 12,
                        color: "#ffffff",
                        background: '#222222'
                    }}>
                        <strong>
                            {id}: {value} min
                        </strong>
                    </div>)
                    }
                    axisBottom={{
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'Vehicle',
                        legendPosition: 'middle',
                        legendOffset: 32,
                        truncateTickAt: 0
                    }}
                    axisLeft={{
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'Minutes',
                        legendPosition: 'middle',
                        legendOffset: -40,
                        truncateTickAt: 0
                    }}
                    labelSkipWidth={12}
                    labelSkipHeight={12}
                    labelTextColor={{
                        from: 'color'
                    }}
                />
            }
        </>
    )
}