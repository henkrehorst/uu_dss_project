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
                     color={'blue.500'}>Price comparison between car and train</Heading>
            {graphData === null ? <Spinner/> :
                <ResponsiveLine
                    colors={['#FFC917', '#0063D3', '#FFC917', '#0063D3']}
                    data={graphData}
                    margin={{top: 50, right: 110, bottom: 50, left: 60}}
                    xScale={{
                        type: 'linear',
                        min: 2016,
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
                        legend: 'Year',
                        legendOffset: 36,
                        legendPosition: 'middle',
                        truncateTickAt: 0
                    }}
                    axisLeft={{
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'Price in €',
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
                    layers={[
                        "grid",
                        "markers",
                        "axes",
                        "areas",
                        "crosshair",
                        "line",
                        "slices",
                        "points",
                        "mesh",
                        "legends",
                        DashedSolidLine
                    ]}
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
                            ],
                            data: graphData.filter(item => !String(item.id).includes("future")).map(item => ({
                                id: item.id,
                                label: item.id,
                                color: item.id.toString().includes('train') ? '#FFC917' : '#0063D3'
                            }))
                        }
                    ]}
                />}
        </>
    )
}

const DashedSolidLine = ({series, lineGenerator, xScale, yScale}) => {
    return series.map(({id, data, color}, index) => (
        <path
            key={id}
            d={lineGenerator(
                data.map((d) => ({
                    x: xScale(d.data.x),
                    y: yScale(d.data.y)
                }))
            )}
            fill="none"
            stroke={color}
            style={
                index < 2
                    ? {
                        // simulate line will dash stroke when index is even
                        strokeDasharray: "2, 2",
                        strokeWidth: 2
                    }
                    : {
                        // simulate line with solid stroke
                        strokeWidth: 2
                    }
            }
        />
    ));
};