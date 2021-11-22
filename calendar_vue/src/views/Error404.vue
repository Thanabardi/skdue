<template>
    <center class="center"><div class="error">
        <div class="box">
            <h3 style="font-size: 150px;"> ERROR 404 </h3>
            <p style="font-size: 100px; border-top: double;">Page is not found</p>
            <div><router-link style="font-size: 45px" to='/'>Go to login page</router-link></div>
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
  font-size: 18px;
}
</style>