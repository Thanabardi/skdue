<template>
    <div class="follow-list" @click="() => TogglePopup('buttonTrigger')">
		<div v-if="this.calendar_slug == this.user_name">Home</div>
        <div v-else>{{ this.calendar_slug }}</div>
		<div v-if="popupTriggers.buttonTrigger && this.user_name != ''">
		    <div class="follow-list-tab">
				<button v-for="name in followed_name" :key="name" @click="redirectFollowedCalendar(name)" 
                    class="follow-list-button-tp"> {{ name }}</button>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';

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
            followed_name: [],
            apiLoaded: false,
            calendar_slug: '',
            user_name: '',
		}
	},
    mounted () {
        this.getFollowList()
    },
    methods: {
        getFollowList() {
            const calendar_slug = this.$route.params.calendar_slug
            this.calendar_slug = calendar_slug.replace(/-/g,' ')
            axios.get(`/api/v2/me/follow`).then( response => {
                this.user_name = response.data[0]["user_name"]
                response.data.forEach(elements => {
				this.followed_name.push(elements["followed_name"])
					})
            })
        },
        async redirectFollowedCalendar(followed) {
			await this.$router.push({ path: `/me/` })
			await this.$router.replace({ path: `/calendar/${followed}` })
        },
	}
})
</script>


<style scoped>
.follow-list {
    color: var(--white);
    left: 10%;
    position: absolute;
    right: 2%;
    border-radius: 2px;
    width: 260px;
    border: 1px solid transparent;
    padding: 5px;
	top: 12px;
    border: 1px solid var(--white-op-1);
    font-size: 22px;
    cursor: pointer;
}
.follow-list:hover {
	border: 1px solid var(--white-op-1);
}
.follow-list-tab {
    background-color: var(--white);
    box-shadow: 0px 0px 1px 0px var(--black-op-1), 0px 0px 40px 0px var(--black-op-2);
    position: absolute;
    width: 272px;
    margin-top: 10px;
    overflow-x: hidden;
    right: 0;
    border-radius: 2px;
    text-align: left;
    max-height: 200px;
}
.follow-list-button-tp {
    background: none;
    border: none;
    color: var(--black);
    cursor: pointer;
    font-size: 18px;
    width: 100%;
    padding: 5px 15px 5px 15px;
    text-align: left;
}
.follow-list-button-tp:hover {
    background-color: var(--white-dark);
}
::-webkit-scrollbar {
    display: none;
}
</style>