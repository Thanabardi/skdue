<template>
    <center class="center"><div class="error">
        <div class="box">
            <h3 style="font-size: 100px;"> ERROR 403 </h3>
            <p style="font-size: 25px;">Forbidden: Access to this calendar on the server is denied!</p>
            <!-- <div><router-link style="font-size: 45px" to='/'>Go to login page</router-link></div> -->
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