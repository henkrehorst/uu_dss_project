import {Heading, Skeleton, Stack} from "@chakra-ui/react";
import {useEffect, useState} from "react";
import {PerformanceGaugeComponent} from "@/components/PerformanceGaugeComponent.tsx";

export const EquipmentPerformanceGauge = () => {
    const [gaugeValue, setGaugeValue] = useState<number | null>(null);

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/performance/equipment`).then(res => {
            res.json().then((data: { value: number }) => {
                setGaugeValue(data.value)
            })
        })
    }, [])


    return (
        <>
            <Heading size={'md'}
                     textAlign='center'
                     color={'blue.500'}>Equipment</Heading>
            {gaugeValue === null ?
                <Stack>
                    <Skeleton height='20px'/>
                    <Skeleton height='20px'/>
                    <Skeleton height='20px'/>
                </Stack> :
                <PerformanceGaugeComponent value={gaugeValue}/>
            }
        </>
    )
}