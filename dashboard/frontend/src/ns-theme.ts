import {extendTheme, Theme} from "@chakra-ui/react";

export const nsTheme = extendTheme({
    styles: {
        global: {
            '@font-face': [
                {
                    fontFamily: 'nssans-regular',
                    src: `url('/nssans-regular.woff2') format('woff2')`,
                    fontWeight: 'normal',
                    fontStyle: 'normal',
                },
                {
                    fontFamily: 'nssans-bold',
                    src: `url('/nssans-bold.woff2') format('woff2')`,
                    fontWeight: 'bold',
                    fontStyle: 'bold',
                }
            ]
        }
    },
    fonts: {
      heading: `'nssans-regular', sans-serif`,
      body: `'nssans-regular', sans-serif`,
      bold: `'nssans-regular', sans-serif`,
    },
    colors: {
        grayTable: {
            100: '#F0F0F2',
        },
        yellow: {500: '#FFC917'},
        blue: {500: '#003082'},
        lightBlue: {500: '#0063D3'},
        white: '#FFFFFF',
        red: {500: '#DB0029'},
        green: {500: '#009A42'},
        orange: {500: '#FF7700'},
        gray: {
            50: '#070721',  // Body Text (Darkest)
            100: '#202037', // Grey 10
            200: '#39394D', // Grey 20
            300: '#515164', // Grey 30
            400: '#6A6A7A', // Grey 40
            500: '#838390', // Grey 50
            600: '#9C9CA6', // Grey 60
            700: '#B5B5BC', // Grey 70
            800: '#CDCDD3', // Grey 80
            900: '#E6E6E9', // Grey 90
            950: '#F0F0F2', // Grey 94 (Lightest)
        },
    }
})