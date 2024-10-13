import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import {ChakraProvider} from "@chakra-ui/react";
import {nsTheme} from "@/ns-theme.ts";



createRoot(document.getElementById('root')!).render(
    <ChakraProvider theme={nsTheme}>
        <App />
    </ChakraProvider>
)
