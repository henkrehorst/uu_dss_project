import GaugeComponent from "react-gauge-component";
import {FC} from "react";

interface PerformanceGaugeComponentProps {
    value: number
}

export const PerformanceGaugeComponent: FC<PerformanceGaugeComponentProps> = ({value}) => {
    return (
        <GaugeComponent
            type={'semicircle'}
            style={{color: '#070721'}}
            labels={{
                valueLabel: {
                    style: {
                        fill: '#070721'
                    }
                },
                tickLabels: {
                    defaultTickValueConfig: {
                        style: {
                            fill: '#070721'
                        }
                    }
                }
            }}
            arc={{
                subArcs: [
                    {
                        limit: 40,
                        color: '#009A42',
                        showTick: true
                    },
                    {
                        limit: 60,
                        color: '#FF7700',
                        showTick: true
                    },
                    {
                        limit: 90,
                        color: '#DB0029',
                        showTick: true
                    },
                    {
                        limit: 100,
                        color: '#800017',
                        showTick: true
                    },
                ]
            }}
            value={value}
        />
    )
}