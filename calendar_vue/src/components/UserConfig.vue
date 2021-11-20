<template>
	<div class="user-detail">
		
		<div v-if="(this.token == '')" class="user-detail-not-login">
			<h2><router-link class="user-detail-app-button"
            	to=/>Skdue</router-link></h2>
			<!-- <router-link class="user-detail-button" style=" background: none; border: 2px solid white;" 
            	to=/>Login</router-link> -->
			<router-link class="user-detail-button" :style="'background-color:'+app_colors[this.color_theme['name']]['sub-2']" 
            	to=/>Login</router-link>
		</div>

		<div v-else>
			<h2><div class="user-detail-app-button" @click="redirectUserHome()">Skdue</div></h2>
			<div class="user-detail-login" @click="() => TogglePopup('buttonTrigger')">
				<div><img :src="img" class="avatar"> {{ this.display_name }}</div>
				<div v-if="popupTriggers.buttonTrigger">
					<div class="user-detail-tab">
						<button class="user-detail-button-tp" @click="settingRoute">Setting</button>
						<button class="user-detail-button-tp" @click="() => logoutData()">Logout</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import Calendar from '../components/Calendar.vue'
import { TAG_COLORS, APP_COLORS } from './ColorHandle'

export default {
	setup () {
		const popupTriggers = ref({
			buttonTrigger: false,
		});

		const TogglePopup = (trigger) => {
			popupTriggers.value[trigger] = !popupTriggers.value[trigger]
		}
		return {
			popupTriggers,
			TogglePopup
		}
	},
	data() {
		return {
			user_name: '',
			dataLogout:{
				"status":"logout"
			},
			display_name: '',
			img: '',
			tag_colors: TAG_COLORS,
            app_colors: APP_COLORS,
		}
	},
	props: {
		color_theme: {},
    },
    mounted () {
        this.getUserName()
		this.getUserDetail()
    },
	methods: {
        getUserName() {
            // const calendar_slug = this.$route.params.calendar_slug
			this.token = localStorage.token
			// console.log("slug =", calendar_slug)
			axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
            axios.get(`/api/v2/me`)
			.then( response => {
				// console.log(response.data)
                this.user_name = response.data["user"]["username"]
				console.log(response.data)
            })
        },
		async redirectUserHome() {
			await this.$router.push({ path: `/me/` })
			await this.$router.replace({ path: `/me/${this.user_name}` })
			// this.$router.go()
			Calendar.components.FullCalendar.calendar.currentData.calendarApi.refetchEvents()
        },
		clearlogout(data) {
			localStorage.setItem("token", "")
			this.$router.push({ path: `/`});

		},
		logoutData(){
			// e.preventDefault();
			axios.delete(`/api/v2/logout`, this.dataLogout)
				.then(response => {
				this.clearlogout(response.data);
				// console.log(response.data);
				// console.log(response.data.slug);
			})
				.catch(error => {
				console.log(error)
			})
		},
		settingRoute(){
			this.$router.push({path: '/setting'})
		},
		getUserDetail(){
			axios
				.get(`/api/v2/me/user_setting`)
				.then(response => {
					this.user_data = response.data
					console.log(this.user_data)
					this.display_name = this.user_data.setting.display_name
					this.description = this.user_data.setting.about
					this.img = "http://127.0.0.1:8000"+this.user_data.setting.image
					console.log(this.img)
				})
		},		
	}
}

</script>

<style lang='scss' scoped>

@import './../assets/style.css';

.user-detail {
    position: absolute;
    right: 2%;
	top: 12px;
}
.user-detail-not-login {
	display: flex;
	justify-content: space-evenly;
	top: 6px;
	width: 320px;
}
.user-detail-login {
	color: white;
	width: 200px;
    border: 1px solid transparent;
    padding: 5px;
	font-size: 22px;
	transform: translate(0, -20px);
	cursor: pointer;
}
.user-detail-login:hover {
	border: 1px solid rgba(255, 255, 255, 0.5);
}
.user-detail-tab {
    background-color: rgb(240, 240, 240);
  	box-shadow: 0px 0px 1px 0px rgba(0, 0, 0, 0.5), 0px 0px 40px 0px rgba(0, 0, 0, 0.2);
    position: absolute;
    width: 212px;
    margin-top: 10px;
    overflow-x: hidden;
    right: 0;
    border-radius: 2px;
    text-align: left;
}
.user-detail-app-button {
    line-height: 0px;
    font-size: 40px;
    font-weight: 500px;
    position: fixed;
    left: 2%;
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    text-decoration: none;
}
.user-detail-app-button:hover {
	opacity: 0.8;
}
.user-detail-button-tp {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 18px;
    width: 100%;
    padding: 8px 15px 8px 15px;
    text-align: left;
}
.user-detail-button-tp:hover {
    background-color: rgb(220, 220, 220);
}
.user-detail-button {
    color: white;
    cursor: pointer;
    font-size: 22px;
    width: 100px;
    padding: 4px 15px 4px 15px;
    text-align: center;
	border-radius: 40px;
	text-decoration: none;
}
.avatar {
  vertical-align: middle;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  object-fit: cover;
}
// .avatar img {
//     padding: -10px 0px 0px -180px;
// }
</style>