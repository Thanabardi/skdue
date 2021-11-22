<template>
    <center class="center"><div class="error">
        <div class="box">
            <div class="box-code"><h2 style="font-size: 100px;"> ERROR 401 </h2></div>
            <p style="font-size: 25px;">Unauthorized: The page that you looking for require login.</p>
            <router-link to='/'><button class="button" style="font-size: 25px;">Login page</button></router-link>
        </div>
    </div></center>
</template>

<script>

export default ({
})
</script>

<style scoped>
.center {
    position: absolute;
    top: 50%;
    width: 100%;
    text-align: center;
}

.box {
    border: 2px solid #c0ca35;
    background-color: #c0ca35;
    padding: 10px;
    border-radius: 15px 85px;
    font-size: 100px;
    width: 70%;
    margin: auto;
}

.router-link {
    text-decoration: none;
    appearance: button;
}

.button {
    border-radius: 20px;
    border: none;
    font-weight: bold;
    padding: 10px 40px;
    text-transform: uppercase;
    cursor: pointer;
}
</style>