import {ResponsiveLine, Serie} from "@nivo/line";
import {FC, useEffect, useState} from "react";
import {Heading, Spinner} from "@chakra-ui/react";

interface PriceComparisonLineGraphProps {
    fromStation: string;
    toStation: string;
}

export const PriceComparisonLineGraph: FC<PriceComparisonLineGraphProps> = ({fromStation, toStation}) => {
    const [graphData, setGraphData] = useState<Serie[] | null>(null)

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/price_comparison/${fromStation}/${toStation}`).then(res => {
            res.json().then(data => {
                setGraphData(data)
            })
        })

    }, [toStation, fromStation])

    return (
        <>
            <Heading size={'md'}
                     textAlign='center'
                     color={'blue.500'}>Price comparison</Heading>
            {graphData === null ? <Spinner/> :
                <ResponsiveLine
                    data={graphData}
                    margin={{top: 50, right: 110, bottom: 50, left: 60}}
                    xScale={{
                        type: 'linear',
                        min: 2006,
                        max: 'auto'
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
                        legend: 'transportation',
                        legendOffset: 36,
                        legendPosition: 'middle',
                        truncateTickAt: 0
                    }}
                    axisLeft={{
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'count',
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
                    legends={[
                        {
                            anchor: 'bottom-right',
                            direction: 'column',
                            justify: false,
                            translateX: 100,
                            translateY: 0,
                            itemsSpacing: 0,
                            itemDirection: 'left-to-right',
                            itemWidth: 80,
                            itemHeight: 20,
                            itemOpacity: 0.75,
                            symbolSize: 12,
                            symbolShape: 'circle',
                            symbolBorderColor: 'rgba(0, 0, 0, .5)',
                            effects: [
                                {
                                    on: 'hover',
                                    style: {
                                        itemBackground: 'rgba(0, 0, 0, .03)',
                                        itemOpacity: 1
                                    }
                                }
                            ]
                        }
                    ]}
                />}
        </>
    )
}