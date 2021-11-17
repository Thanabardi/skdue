<template>
	<div class="user-detail">
		
		<div v-if="this.user_name == ''" class="user-detail-not-login">
			<h2><router-link class="user-detail-app-button"
            	to=/>Skdue</router-link></h2>
			<!-- <router-link class="user-detail-button" style=" background: none; border: 2px solid var(--white);" 
            	to=/>Login</router-link> -->
			<router-link class="user-detail-button" style=" background: var(--green); border: 2px solid var(--green);" 
            	to=/>Login</router-link>
		</div>

		<div v-else>
			<h2><div class="user-detail-app-button" @click="redirectUserHome()">Skdue</div></h2>
			<div class="user-detail-login" @click="() => TogglePopup('buttonTrigger')">
				<div>{{ this.user_name }}</div>
				<div v-if="popupTriggers.buttonTrigger">
					<div class="user-detail-tab">
						<!-- <form @submit.prevent="logoutData"> -->
						<button class="user-detail-button-tp" @click="() => logoutData()">Logout</button>
						<!-- </form> -->
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
			}
		}
	},
    mounted () {
        this.getUserName()
    },
	methods: {
        getUserName() {
            // const calendar_slug = this.$route.params.calendar_slug
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

		logoutData(e){
			// e.preventDefault();
			axios.delete(`/api/v2/logout`, this.dataLogout)
				.then(response => {
				this.clearlogout(response.data);
				console.log(response.data);
				// console.log(response.data.slug);
			})
				.catch(error => {
				console.log(error)
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
	color: var(--white);
	width: 200px;
    border: 1px solid transparent;
    padding: 5px;
	font-size: 22px;
	transform: translate(0, -20px);
	cursor: pointer;
}
.user-detail-login:hover {
	border: 1px solid var(--white-op-1);
}
.user-detail-tab {
    background-color: var(--white);
    box-shadow: 0px 0px 1px 0px var(--black-op-1), 0px 0px 40px 0px var(--black-op-2);
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
    color: var(--white);
    cursor: pointer;
    text-decoration: none;
}
.user-detail-app-button:active {
	color: var(--white-dark);
}
.user-detail-button-tp {
    background: none;
    border: none;
    color: var(--black);
    cursor: pointer;
    font-size: 18px;
    width: 100%;
    padding: 8px 15px 8px 15px;
    text-align: left;
}
.user-detail-button-tp:hover {
    background-color: var(--green);
    color: var(--white);
}
.user-detail-button {
    color: var(--white);
    cursor: pointer;
    font-size: 22px;
    width: 100px;
    padding: 4px 15px 4px 15px;
    text-align: center;
	border-radius: 40px;
	text-decoration: none;
}
</style>