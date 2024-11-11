import {FC, ReactNode} from "react";
import {
    Box,
    Container,
    Flex,
    Grid,
    GridItem,
    Heading,
    VStack
} from "@chakra-ui/react";
import {NSLogoIcon} from "@/icons/NSLogoIcon.tsx";

interface DashboardLayoutProps {
    title: string
    mapComponent: ReactNode,
    railLinesComponent: ReactNode
}

export const HomeDashboardLayout: FC<DashboardLayoutProps> = ({
                                                              title,
                                                              mapComponent,
                                                              railLinesComponent
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
                </VStack>
            </Container>
        </>
    )
}