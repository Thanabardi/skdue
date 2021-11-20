<template>
    <div class="follow-list" @click="() => TogglePopup('buttonTrigger')">
		<div v-if="this.calendar_slug == this.user_name">Home</div>
        <div v-else>{{ this.calendar_slug }}</div>
		<div v-if="popupTriggers.buttonTrigger && this.user_name != ''">
		    <div class="follow-list-tab">
				<button v-for="name in followed_name" :key="name" @click="redirectFollowedCalendar()" 
                    class="follow-list-button-tp"> {{ name }}</button>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import { TAG_COLORS, APP_COLORS } from './ColorHandle'

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
            tag_colors: TAG_COLORS,
            app_colors: APP_COLORS,
            fs_slug: '',
            fs_name_display: '',
		}
	},
    props: {
		color_theme: {},
    },
    mounted () {
        this.getFollowList()
    },
    methods: {
        async getFollowList() {
            const calendar_slug = await this.$route.params.calendar_slug
            this.calendar_slug = calendar_slug.replace(/-/g,' ')
            axios.get(`/api/v2/me/follow`).then( response => {
                this.user_name = response.data[0]["user_name"]
                this.fs_slug = response.data[0]["followed_calendar_slug"]
                this.fs_name_display = this.fs_slug.replace(/-/g,' ')
                const str2 = this.fs_name_display.charAt(0).toUpperCase() + this.fs_name_display.slice(1);
                response.data.forEach(elements => {
                    if (elements["followed_name"]=='admin'){
                        elements["followed_name"]=str2
                    }
				    this.followed_name.push(elements["followed_name"])
				})
            })
        },
        async redirectFollowedCalendar() {
			await this.$router.push({ path: `/me/` })
			await this.$router.replace({ path: `/calendar/${this.fs_slug}` })
        },
	}
})
</script>


<style scoped>
.follow-list {
    color: white;
    left: 10%;
    position: absolute;
    right: 2%;
    border-radius: 2px;
    width: 260px;
    border: 1px solid transparent;
    padding: 5px;
	top: 12px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    font-size: 22px;
    cursor: pointer;
}
.follow-list-tab {
    background-color: rgb(240, 240, 240);
    box-shadow: 0px 0px 1px 0px rgba(0, 0, 0, 0.5), 0px 0px 40px 0px rgba(0, 0, 0, 0.2);
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
    color: black;
    cursor: pointer;
    font-size: 18px;
    width: 100%;
    padding: 5px 15px 5px 15px;
    text-align: left;
}
.follow-list-button-tp:hover {
    background-color: rgb(220, 220, 220);
}
::-webkit-scrollbar {
    display: none;
}
</style>