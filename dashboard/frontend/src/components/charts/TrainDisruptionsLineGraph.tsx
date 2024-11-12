import {ResponsiveLine, Serie} from "@nivo/line";
import {FC, useEffect, useState} from "react";
import {Heading, Spinner} from "@chakra-ui/react";

interface TrainDisruptionsLineGraphProps {
    fromStation: string;
    toStation: string;
}

export const TrainDisruptionsLineGraph: FC<TrainDisruptionsLineGraphProps> = ({fromStation, toStation}) => {
    const [graphData, setGraphData] = useState<Serie[] | null>(null)

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/rail_routes/lines/${fromStation}/${toStation}/disruptions`).then(res => {
            res.json().then(data => {
                setGraphData(data)
            })
        })

    }, [toStation, fromStation])

    return (
        <>
            <Heading size={'md'}
                     textAlign='center'
                     color={'blue.500'}>Average train disruption by min(s) over years</Heading>
            {graphData === null ? <Spinner/> :
                <ResponsiveLine
                    colors={['#FFC917', '#003082', '#FFC917', '#003082']}
                    data={graphData}
                    margin={{top: 50, right: 60, bottom: 50, left: 60}}
                    xScale={{
                        type: 'point',
                        min: 2017
                    }}
                    yScale={{
                        type: 'linear',
                        min: 'auto',
                        max: 'auto'
                    }}
                    yFormat=" >-.2f"
                    height={400}
                    axisTop={null}
                    axisRight={null}
                    axisBottom={{
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'Year',
                        legendOffset: 36,
                        legendPosition: 'middle',
                        truncateTickAt: 0
                    }}
                    tooltip={({point}) => (<div style={{
                        padding: 12,
                        color: "#ffffff",
                        background: '#222222'
                    }}>
                        <strong>
                            {console.log(point)}
                            {Number(point.data.y).toFixed(1)} minutes in {point.data.x}
                        </strong>
                    </div>)}
                    axisLeft={{
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'Minutes',
                        legendOffset: -40,
                        legendPosition: 'middle',
                        truncateTickAt: 0
                    }}
                    pointSize={10}
                    pointColor={{theme: 'background'}}
                    pointBorderWidth={2}
                    pointBorderColor={{from: 'serieColor'}}
                    pointLabel="data.yFormatted"
                    pointLabelYOffset={-12}
                    enableTouchCrosshair={true}
                    useMesh={true}
                />}
        </>
    )
}