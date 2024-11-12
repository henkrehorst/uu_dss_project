import {ResponsiveBar} from '@nivo/bar'
import {FC, useEffect, useState} from "react";
import {Heading, Spinner} from "@chakra-ui/react";


interface EmissionComparisonLineBarProps {
    fromStation: string;
    toStation: string;
}

export const EmissionComparisonBarChart: FC<EmissionComparisonLineBarProps> = ({toStation, fromStation}) => {
    const [data, setData] = useState<any | undefined>(undefined)

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/rail_routes/lines/${fromStation}/${toStation}/emissions`).then(res => {
            res.json().then(data => {
                setData(data)
            })
        })

    }, [toStation, fromStation])


    return (
        <>
            <Heading size={'md'}
                     textAlign='center'
                     color={'blue.500'}>Comparison of average CO2 emissions per trip by vehicle</Heading>
            {data == undefined ? <Spinner/> :
                <ResponsiveBar
                    data={data}
                    indexBy="vehicle"
                    keys={[
                        "co2 emission car diesel",
                        "co2 emission car electric",
                        "co2 emission car gasoline",
                        "co2 emission train",
                    ]}
                    colors={['#FF7700', '#009A42', '#DB0029', '#FFC917']}
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
                            {id}: {value} grams
                        </strong>
                    </div>)
                    }
                    axisBottom={{
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'Vehicle',
                        legendPosition: 'middle',
                        legendOffset: 40,
                        truncateTickAt: 0
                    }}
                    axisLeft={{
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'CO2 Emissions in grams',
                        legendPosition: 'middle',
                        legendOffset:-60,
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