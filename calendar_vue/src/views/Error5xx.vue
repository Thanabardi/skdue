<template>
<body class="centered-wrapper">
    <center class="center"><div class="error">
        <div class="box">
            <p class="glitch" style="font-size: 100px;">
                            <!-- <span aria-hidden="true">Error 5XX</span> -->
                            Error 5XX
                            <!-- <span aria-hidden="true">Error 5XX</span> -->
                        </p>
            <p style="font-size: 25px;">Internal server error</p>
            <p style="font-size: 25px;">Please come back later</p>
            <!-- <div><router-link style="font-size: 45px" to='/'>Go to login page</router-link></div> -->
        </div>
    </div></center>
</body>
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
.glitch {
  font-size: 5rem;
  font-weight: bold;
  text-transform: uppercase;
  position: relative;
  text-shadow: 0.05em 0 0 #00fffc, -0.03em -0.04em 0 #fc00ff,
    0.025em 0.04em 0 #fffc00;
  animation: glitch 725ms infinite;
}

.glitch span {
  position: absolute;
  top: 0;
  left: 0;
}
.glitch span:first-child {
  animation: glitch 500ms infinite;
  clip-path: polygon(0 0, 150% 0, 100% 35%, 0 35%);
  transform: translate(-0.04em, -0.03em);
  opacity: 0.75;
  left: 303px;
}

.glitch span:last-child {
  animation: glitch 375ms infinite;
  clip-path: polygon(0 65%, 100% 65%, 100% 100%, 0 100%);
  transform: translate(0.04em, 0.03em);
  opacity: 0.75;
  left: 295px;
}
@keyframes glitch {
  0% {
    text-shadow: 0.05em 0 0 #00fffc, -0.03em -0.04em 0 #fc00ff,
      0.025em 0.04em 0 #fffc00;
  }
  15% {
    text-shadow: 0.05em 0 0 #00fffc, -0.03em -0.04em 0 #fc00ff,
      0.025em 0.04em 0 #fffc00;
  }
  16% {
    text-shadow: -0.05em -0.025em 0 #00fffc, 0.025em 0.035em 0 #fc00ff,
      -0.05em -0.05em 0 #fffc00;
  }
  49% {
    text-shadow: -0.05em -0.025em 0 #00fffc, 0.025em 0.035em 0 #fc00ff,
      -0.05em -0.05em 0 #fffc00;
  }
  50% {
    text-shadow: 0.05em 0.035em 0 #00fffc, 0.03em 0 0 #fc00ff,
      0 -0.04em 0 #fffc00;
  }
  99% {
    text-shadow: 0.05em 0.035em 0 #00fffc, 0.03em 0 0 #fc00ff,
      0 -0.04em 0 #fffc00;
  }
  100% {
    text-shadow: -0.05em 0 0 #00fffc, -0.025em -0.04em 0 #fc00ff,
      -0.04em -0.025em 0 #fffc00;
  }
}
.centered-wrapper {
    position: relative;
    text-align: center;
}
.centered-wrapper:before {
    content: "";
    position: relative;
    display: inline-block;
    width: 0; height: 100%;
    vertical-align: middle;
}
.centered-content {
    display: inline-block;
    vertical-align: middle;
}
html, body {
    width: 100%;
    height: 100%;
    padding-top: 10%;
    margin: 0;
}
</style>