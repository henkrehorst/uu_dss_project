import {useEffect, useState} from "react";
import {Button, Skeleton, Table, Tbody, Td, Th, Thead, Tr} from "@chakra-ui/react";
import {Search2Icon} from "@chakra-ui/icons";
import {Link as ReactRouterLink} from 'react-router-dom'

export const RailRoutesLines = () => {
    const [lines, setLines] = useState<null | {
        id: string,
        name: string,
        from_station: string,
        to_station: string
    }[]>(null);

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/rail_routes/lines`).then(res => {
            res.json().then((data: { id: string, name: string }[]) => {
                setLines(data)
            })
        })
    }, [])

    return (
        <Table size={'sm'} variant='striped' colorScheme='grayTable'>
            <Thead>
                <Tr>
                    <Th fontFamily={"nssans-bold"}>Rail routes</Th>
                </Tr>
            </Thead>
            <Tbody>
                {lines === null ? <Tr><Td><Skeleton/></Td></Tr> :
                    lines.map((line) => (
                        <Tr key={line.id}>
                            <Td>
                                <Button w={'100%'}
                                        as={ReactRouterLink}
                                        to={`/route/${line.from_station}/${line.to_station}`}
                                        leftIcon={<Search2Icon/>}
                                        justifyContent={'left'}
                                        key={line.id}
                                        size={'sm'}
                                        colorScheme='blue'
                                        variant='ghost'>
                                    {line.name}
                                </Button>
                            </Td>
                        </Tr>
                    ))
                }
            </Tbody>
        </Table>
    )
}