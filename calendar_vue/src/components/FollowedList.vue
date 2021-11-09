<template>
    <div class="user-detail-login">
		<button class="app-button-tp" style="font-size: 22px;" 
		@click="() => TogglePopup('buttonTrigger')">{{ this.calendar_slug }}</button>
		<div v-if="popupTriggers.buttonTrigger" :TogglePopup="() => TogglePopup('buttonTrigger')">
		    <div class="user-detail-tab" v-for="item in itemList" :key="item">
				<button @click="redirectFollowedCalendar(item)" class="user-detail-button-tp"> {{ item.followed_name }}</button>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import Calendar from '../components/Calendar.vue'
import EventDetails from '../components/EventDetails.vue'
import { globalLocales } from '@fullcalendar/common'

export default ({
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
            selectedItem: {},
			follow: '',
            inputValue: '',
            itemList: [],
            apiLoaded: false,
            calendar_slug: "",
		}
	},
    mounted () {
        this.getFollowList()
    },
    methods: {
        getFollowList() {
            // const calendar_slug = this.$route.params.calendar_slug
            const calendar_slug = this.$route.params.calendar_slug
            this.calendar_slug = calendar_slug.replace(/-/g,' ')
            axios.get(`/api/v2/me/follow`).then( response => {
                console.log("fs data=", response.data)
                this.itemList = response.data
            })
        },
        async redirectFollowedCalendar(theItem) {
			await this.$router.push({ path: `/me/` })
			await this.$router.replace({ path: `/calendar/${theItem.followed_name}` })
        },
	}
})
</script>


<style scoped>
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
	transform: translate(0, -20px);
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