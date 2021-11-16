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
        "main" : "#000000",
        "main-1": "#646464",
        "sub" : "#ffffff",
        "sub-1": "#d6d6d6",
    },
    "dark" : {
        "main" : "#ffffff",
        "main-1": "#d6d6d6",
        "sub" : "#000000",
        "sub-1": "#646464",
    },
    "theme-1" : {
        "main" : "#006664",
        "main-dark": "#004746",
        "sub-1" : "#3B9693",
        "sub-2": "#c0ca35",
        "sub-2-dark": "#aeb825",
    },
    "theme-2" : {
        "main" : "#262626",
        "main-dark": "#004746",
        "sub-1" : "#181717",
        "sub-2": "#c0ca35",
        "sub-2-dark": "#aeb825",
    },
    "theme-3" : {
        "main" : "#4D3D9E",
        "main-dark": "#49359B",
        "sub-1" : "#565AC5",
        "sub-2": "#5EA6CB",
        "sub-2-dark": "#467EB8",
    },
}
export const TAG_COLORS = {
    "red": "#C00000",
    "yellow": "#FFC000",
    "blue": "#0070C0",
}