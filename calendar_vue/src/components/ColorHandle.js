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
        "main": "#000000",
        "main-0": "#292929",
        "main-1": "#acacac",
        "sub": "#ffffff",
        "sub-0": "#f8f8f8",
        "sub-1": "#b3b3b3",
    },
    "dark" : {
        "main": "#ffffff",
        "main-0": "#f8f8f8",
        "main-1": "#b3b3b3",
        "sub": "#000000",
        "sub-0": "#292929",
        "sub-1": "#acacac",
    },
    "theme-1" : {
        "main" : "#006664",
        "sub-1" : "#3B9693",
        "sub-2": "#c0ca35",
    },
    "theme-2" : {
        "main" : "#262626",
        "sub-1" : "#181717",
        "sub-2": "#2069e0",
    },
    "theme-3" : {
        "main" : "#4D3D9E",
        "sub-1" : "#565AC5",
        "sub-2": "#5EA6CB",
    },
}
export const TAG_COLORS = {
    "white": "#f2f2f2",
    "red": "#C51104",
    "yellow": "#FBBC05",
    "blue": "#0096EF",
    "green": "#34A853",
    "pink": "#F4ABBA",
    "purple": "#A73FB9",
}