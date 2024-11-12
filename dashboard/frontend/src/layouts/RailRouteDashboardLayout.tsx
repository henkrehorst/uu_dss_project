import {FC, ReactNode} from "react";
import {
    Box, Breadcrumb, BreadcrumbItem, BreadcrumbLink,
    Container,
    Flex,
    Grid,
    GridItem,
    Heading,
    SimpleGrid,
    VStack
} from "@chakra-ui/react";
import {NSLogoIcon} from "@/icons/NSLogoIcon.tsx";
import {Link} from "react-router-dom";

interface DashboardLayoutProps {
    title: string
    mapComponent: ReactNode,
    railLinesComponent: ReactNode,
    railRouteName: string,
    chartSlot1: ReactNode,
    chartSlot2: ReactNode,
    chartSlot3: ReactNode,
    chartSlot4: ReactNode,

}

export const RailRouteDashboardLayout: FC<DashboardLayoutProps> = ({
                                                                       title,
                                                                       mapComponent,
                                                                       chartSlot1,
                                                                       chartSlot2,
                                                                       railLinesComponent,
                                                                       chartSlot4,
                                                                       chartSlot3,
    railRouteName
                                                                   }) => {
    return (
        <>
            <Box w={'100%'} h={'60px'} backgroundColor={'yellow.500'}>
                <Container my={'auto'} maxW={"container.xl"}>
                    <Flex h={'60px'} gap={2} alignItems={'center'}>
                        <NSLogoIcon/>
                        <Heading fontWeight={'bold'} fontSize={'18px'} color={"blue.500"}>{title}</Heading>
                    </Flex>
                </Container>
            </Box>
            <Container border={1} borderColor={"black"} gap={2} maxW={"container.xl"} mt={5} mb={10}>
                <Breadcrumb fontWeight='medium' color={'blue.500'}  fontSize='md' fontWeight={'bold'}>
                    <BreadcrumbItem>
                        <BreadcrumbLink as={Link} to='/'>Overview</BreadcrumbLink>
                    </BreadcrumbItem>
                    <BreadcrumbItem isCurrentPage>
                        <BreadcrumbLink as={Link} to='#'>{railRouteName}</BreadcrumbLink>
                    </BreadcrumbItem>
                </Breadcrumb>
                <VStack>
                    <Grid templateColumns={"repeat(3, 1fr)"} w={'100%'} gap={2}>
                        <GridItem colSpan={[3, 3, 2]} height={"60vh"} backgroundColor={"gray.900"} borderRadius={'md'}>
                            {mapComponent}
                        </GridItem>
                        <GridItem
                            overflow={'auto'}
                            maxH={'60vh'}
                            colSpan={[3, 3, 1]}
                            borderColor={"gray.700"}
                            p={2}
                            borderWidth="1px"
                            borderRadius="md">
                            {railLinesComponent}
                        </GridItem>
                    </Grid>
                    <SimpleGrid columns={[1, 1, 2]} gap={2} w={'100%'}>
                        <Box borderColor={"gray.700"} p={2} borderWidth="1px" borderRadius="md">
                            {chartSlot1}
                        </Box>
                        <Box borderColor={"gray.700"} p={2} borderWidth="1px" borderRadius="md">
                            {chartSlot2}
                        </Box>
                    </SimpleGrid>
                    <SimpleGrid columns={[1, 1, 2]} w={'100%'} gap={2}>
                        <Box borderColor={"gray.700"} p={2} borderWidth="1px" borderRadius="md">
                            {chartSlot3}
                        </Box>
                        <Box borderColor={"gray.700"} p={2} borderWidth="1px" borderRadius="md">
                            {chartSlot4}
                        </Box>
                    </SimpleGrid>
                </VStack>
            </Container>
        </>
    )
}