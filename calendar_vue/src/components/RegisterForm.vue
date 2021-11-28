<template>
  <div>
    <h1 class="register-header">Skdue</h1>
    <div class="container" :class="{'sign-up-active' : signUp}">
      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-left">
            <h1>Welcome To Skdue!</h1>
            <p>Please enter your personal detail to start using your calendar.</p>
              <div style="display: flex;">Have an Account Already?
                <button style="color: #c0ca35; font-size: 18px;" class="app-button-tp"
                  id="signIn" @click="signUp = !signUp"> LOG IN</button>
              </div>
          </div>
          <div class="overlay-right">
            <h1>Welcome Back!</h1>
            <p>Please login to see what's going to happen next on your calendar.</p>
            <button title="Google" class="google-button"  @click.prevent="googleLogin">
              <img class="google-icon" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"/>
                Login with google
            </button>
            <div style="display: flex;">New to Skdue?
              <button style="color: #c0ca35; font-size: 18px;" class="app-button-tp"
                id="signUp" @click="signUp = !signUp">SIGN UP</button>
            </div>
          </div>
        </div>
      </div>
      <form @submit.prevent="getData" class="sign-up" action="#">
        <h2>Sign up</h2>
        <div>Use your email for registration</div>
        <input class="register-input" type="text" v-model="dataRegisterForm.username" placeholder="Name" required />
        <input class="register-input" type="email" v-model="dataRegisterForm.email" placeholder="Email" required />
        <input class="register-input" type="password" v-model="dataRegisterForm.password" placeholder="Password" required />
        <button class="register-button">Sign Up</button>
      </form>
      <form @submit.prevent="checkData" class="sign-in" action="#">
        <h2>Login</h2>
        <input class="register-input" type="username" v-model="dataLogIn.username" placeholder="Username" required />
        <input class="register-input" type="password" v-model="dataLogIn.password" placeholder="Password" required />

        <a class="app-button-tp" style="text-decoration: none; color: black;" 
          href="#">Forgot your password?</a>
        <button class="register-button">Continue</button>
      </form>
    </div>

    <!-- router-link for mockup -->
    <!-- <div style="text-align: center;">
      <h1 style="font-size: 50px; color: red;" class="register-header">*This is just a login mockup*</h1>
      <h2 style="color: gray;">Anyway, if you want to create your own calendar check
      <router-link class="app-button-tp" style="text-decoration: none; color: #c0ca35;"
        to=/create_calendar>this</router-link>

      out to see how our Skdue works, or if you want to take a look at the existing Skdue try 
      <router-link class="app-button-tp" style="text-decoration: none; color: #c0ca35;"

        to=/calendar/holidays>this</router-link>.</h2>
    </div> -->

  </div>
</template>


<script>
import axios from 'axios'

  export default {
    data(){
      return {
        slug : '',
        signUp: false,
        dataRegisterForm:{
          username: null,
          email: null,
          password: null,
            },
        dataLogIn:{
          username: null,
          password: null
        },
      }
    },
    methods:{
      googleLoginData(data){
        // for login
        // console.log(data);

        // auth setting
        let token = data.token
        this.$store.commit('setToken', token)
        axios.defaults.headers.common["Authorization"] = "Token " + token
        localStorage.setItem("token", token)

        this.slug = data.user_info.given_name
        this.$router.push({ path: `/me/${this.slug}`});

      },
      setData(data){
        // for register
        // console.log(data);

        // auth setting
        let token = data.token
        this.$store.commit('setToken', token)
        axios.defaults.headers.common["Authorization"] = "Token " + token
        localStorage.setItem("token", token)

        this.slug = data.calendar.slug
        this.$router.push({ path: `/me/${this.slug}`});
      },
      loginData(data){
        // for login
        // console.log(data);

        // auth setting
        let token = data.token
        this.$store.commit('setToken', token)
        axios.defaults.headers.common["Authorization"] = "Token " + token
        localStorage.setItem("token", token)

        this.slug = data.calendar.slug
        this.$router.push({ path: `/me/${this.slug}`});
      },
      async googleLogin(e){
        e.preventDefault();
        let auth_url = ""

        await axios.get(`/oauth/login/`)
                .then(response => {
                // this.googleLoginData(response.data);
                // console.log(response.data);
                // console.log(response.data.slug);
                auth_url = response.data.auth_url
                console.log(auth_url)
                })
                .catch(error => {
                console.log(error)
            })

        window.location.replace(auth_url)
      },
      getData(e){
        e.preventDefault();
        // console.log(this.dataRegisterForm);

        axios.post(`/api/v2/register`, this.dataRegisterForm)
                .then(response => {
                this.setData(response.data);
                // console.log(response.data);
                // console.log(response.data.slug);
                })
                .catch(error => {
                console.log(error)
            })
      },
      checkData(e){
        // for loging
        e.preventDefault();
        // console.log(this.dataLogIn);

        // get API token
        axios.post(`/api/v2/get-auth-token`, this.dataLogIn)
                .then(response => {
                this.loginData(response.data);
                // console.log(response.data);
                // console.log(response.data.slug);
                })
                .catch(error => {
                console.log(error)
            })
      }
    }
  }
</script>

<style lang='scss' scoped>

@import './../assets/style.css';

.google-button{
  width: 70%;
  border-radius: 20px;
  border: none;
  background-color: #c0ca35;
  color: white;
  font-size: 18px;
  font-weight: bold;
  padding: 10px 40px;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  transition: transform .1s ease-in;
  &:active {
    transform: scale(.98);
    background-color: var(--green-dark)
  }
}

.register-header {
  color: #006664;
  font-size: 80px;
  font-weight: 500px;
  text-align: center;

}
.container {
    position: relative;
    margin-left: auto;
    margin-right: auto;
    width: 768px;
    height: 480px;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0px 0px 1px 0px rgba(0, 0, 0, 0.5), 0px 0px 40px 0px rgba(0, 0, 0, 0.2);
    // background: linear-gradient(to bottom, #efefef, #ccc);
  .overlay-container {
    position: absolute;
    top: 0;
    left: 50%;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: transform .5s ease-in-out;
    z-index: 100;
  }
  .overlay {
    position: relative;
    left: -100%;
    height: 100%;
    width: 200%;
    background: linear-gradient(to bottom right, #006664, #3B9693);
    color: #fff;
    transform: translateX(0);
    transition: transform .5s ease-in-out;
  }
  @mixin overlays($property) {
    position: absolute;
    top: 0;
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-direction: column;
    padding: 70px 40px;
    width: calc(50% - 80px);
    height: calc(100% - 140px);
    text-align: center;
    transform: translateX($property);
    transition: transform .5s ease-in-out;
  }
  .overlay-left {
    font-size: 20px;
    @include overlays(-20%);
  }
  .overlay-right {
    font-size: 20px;
    @include overlays(0);
    right: 0;
  }
}
// h2 {
//   margin: 0;
// }
// p {
//   margin: 20px 0 30px;
// }
// a {
//   color: black;
//   text-decoration: none;
//   margin: 15px 0;
//   font-size: 20px;
// }
.register-button {
  width: 100%;
  border-radius: 20px;
  border: none;
  background-color: #c0ca35;
  color: white;
  font-size: 18px;
  font-weight: bold;
  padding: 10px 40px;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  transition: transform .1s ease-in;
  &:active {
    transform: scale(.98);
    background-color: #aeb825
  }
}
// button.invert {
//   background-color: transparent;
//   border-color: white;
// }
form {
  position: absolute;
  top: 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
  flex-direction: column;
  padding: 90px 60px;
  width: calc(50% - 120px);
  height: calc(100% - 180px);
  text-align: center;
  background: linear-gradient(to bottom, #f5f5f5, #999999);
  transition: all .5s ease-in-out;
}
.register-input {
  //   background-color: white;
  //   border: none;
  //   padding: 8px 15px;
  //   margin: 6px 0;
  //   width: calc(100% - 30px);
  //   border-radius: 8px;
  //   border-bottom: 1px solid #ddd;
  //   // box-shadow: inset 0 1px 2px rgba(0, 0, 0, .4),
  //   //                   0 -1px 1px #fff,
  //   //                   0 1px 0 #fff;
  //   overflow: hidden;
  //   &:focus {
  //     outline: none;
  //     background-color: #f5f5f5;
  //   }
  background: #f5f5f5;
	font-size: 18px;
	padding: 8px;
	width: 300px;
	border: none;
	border-radius: 8px;
}
.sign-in {
  left: 0;
  z-index: 2;
}
.sign-up {
  left: 0;
  z-index: 1;
  opacity: 0;
}
.sign-up-active {
  .sign-in {
    transform: translateX(100%);
  }
  .sign-up {
    transform: translateX(100%);
    opacity: 1;
    z-index: 5;
    animation: show .5s;
  }
  .overlay-container {
    transform: translateX(-100%);
  }
  .overlay {
    transform: translateX(50%);
  }
  .overlay-left {
    transform: translateX(0);
  }
  .overlay-right {
    transform: translateX(20%);
  }
}
@keyframes show {
  0% {
    opacity: 0;
    z-index: 1;
  }
  49% {
    opacity: 0;
    z-index: 1;
  }
  50% {
    opacity: 1;
    z-index: 10;
  }
}
</style>
