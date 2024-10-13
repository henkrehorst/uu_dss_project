import {ResponsiveLine, Serie} from "@nivo/line";
import {useEffect, useState} from "react";
import {Heading, Spinner} from "@chakra-ui/react";

export const TravelersCompensationsLineGraph = () => {
    const [graphData, setGraphData] = useState<Serie[] | null>(null)

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/travelers_compensations`).then(res => {
            res.json().then((data: Serie[]) => {
                setGraphData(data)
            })
        })
    }, [])

    return (
        <>
            <Heading size={'md'}
                     textAlign='center'
                     color={'blue.500'}>Travelers Compensations</Heading>
            {graphData === null ? <Spinner/> :
                <ResponsiveLine
                    data={graphData}
                    margin={{top: 20, right: 20, bottom: 60, left: 80}}
                    height={400}
                    animate
                    enableTouchCrosshair
                    enableSlices={'x'}
                    initialHiddenIds={['cognac']}
                    yScale={{
                        type: 'linear',
                        stacked: true,
                    }}
                    curve={"linear"}
                    legends={[
                        {
                            anchor: 'bottom',
                            direction: 'row',
                            itemHeight: 20,
                            itemWidth: 80,
                            toggleSerie: true,
                            translateY: 50,
                        },
                    ]}
                />}
        </>
    )
}