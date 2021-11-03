<template>
	<div class="user-detail">
		
		<div v-if="this.user_name == ''" class="user-detail-not-login">
			<router-link class="user-detail-button" style=" background: none; border: 2px solid var(--white);" 
            to=/>Login</router-link>
			<router-link class="user-detail-button" style=" background: var(--green); border: 2px solid var(--green);" 
            to=/>Signup</router-link>
			<!-- <button class="user-detail-button" style=" background: none; border: 2px solid var(--white);" 
				@click="() => TogglePopup('buttonTrigger')">Login</button>
			<button class="user-detail-button" style=" background: var(--green); border: 2px solid var(--green);" 
				@click="() => TogglePopup('buttonTrigger')">Signup</button> -->
		</div>

		<div v-else class="user-detail-login">
			<button class="app-button-tp" style="font-size: 22px;" 
					@click="() => TogglePopup('buttonTrigger')">{{ this.user_name }}</button>
			<div v-if="popupTriggers.buttonTrigger" 
				:TogglePopup="() => TogglePopup('buttonTrigger')">
				<div class="user-detail-tab">
					<button class="user-detail-button-tp" @click="() => TogglePopup('buttonTrigger')">Logout</button>
				</div>
			</div>
		</div>

	</div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

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
			user_name: ''
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
            })
        }
	},
}

</script>

<style lang='scss' scoped>

@import './../assets/style.css';

.user-detail {
    position: absolute;
    right: 2%;
	top: 10px;
}
.user-detail-not-login {
	display: flex;
	justify-content: space-evenly;
	top: 6px;
	width: 320px;
}
.user-detail-login {
	width: 250px;
    border: 1px solid transparent;
    padding: 5px;
}
.user-detail-login:hover {
	border: 1px solid var(--white-op-1);
}
.user-detail-tab {
    background-color: var(--white);
    box-shadow: 0px 0px 1px 0px var(--black-op-1), 0px 0px 40px 0px var(--black-op-2);
    position: absolute;
    width: 262px;
    margin-top: 10px;
    overflow-x: hidden;
    right: 0;
    border-radius: 2px;
    text-align: left;
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