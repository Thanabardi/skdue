import axios from 'axios'

export const colorData = async () => {
    axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
    axios.get(`/api/v2/me/user_setting`)
        .then(response => {
            // console.log('color',response.data.color)
            return response.data.color
        })
        .catch(error => {
            console.log(error)
        })
}

export const APP_COLORS = {
    "light" : {
        "main": "#000000", // black
        "main-0": "#292929", // lighther black
        "main-1": "#acacac", // more lighter black
        "sub": "#ffffff", // white
        "sub-0": "#f8f8f8", // lighther white
        "sub-1": "#b3b3b3", // more lighther white
    },
    "dark" : {
        "main": "#ffffff", // white
        "main-0": "#f8f8f8", // lighther white
        "main-1": "#b3b3b3", // more lighther white
        "sub": "#000000", // black
        "sub-0": "#292929", // lighther black
        "sub-1": "#acacac", // more lighter black
    },
    "theme-1" : {
        "main" : "#006664", // main green
        "sub-1" : "#3B9693", // ligther main green
        "sub-2": "#c0ca35", //  green
    },
    "theme-2" : {
        "main" : "#262626", // main black
        "sub-1" : "#181717", // ligther main black
        "sub-2": "#2069e0", // blue
    },
    "theme-3" : {
        "main" : "#4D3D9E", // main purple
        "sub-1" : "#565AC5", // ligther main purple
        "sub-2": "#5EA6CB", // blue
    },
}
export const TAG_COLORS = {
    "default": "#3788d8",
    "follow": "rgba(220, 220, 220, 0.5)",
    "white": "#f2f2f2",
    "red": "#C51104",
    "yellow": "#FBBC05",
    "blue": "#3788d8",
    "green": "#34A853",
    "pink": "#F4ABBA",
    "purple": "#A73FB9",
    "orange" : "#E36005",
}