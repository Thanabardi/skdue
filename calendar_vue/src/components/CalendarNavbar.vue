<template>

	<div  v-if="this.is_fetch" class="calendar-navbar-bg" :style="'background-color:'+app_colors[this.color_theme['name']]['main']">
        <Search :color_theme="this.color_theme"/>
        <EventCreate :color_theme="this.color_theme"/>
        <UserConfig :color_theme="this.color_theme"/>
        <FollowedList :color_theme="this.color_theme"/>
        		<div class="sync">
							<GoogleCalSync />
				</div>
	</div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import Search from './search'
import EventCreate from './EventCreate'
import UserConfig from './UserConfig'
import FollowedList from './FollowedList'

import GoogleCalSync from './GoogleCalSync'

import { TAG_COLORS, APP_COLORS } from './ColorHandle'


export default {
    components: {
        Search,
        EventCreate,
        UserConfig,
        FollowedList,
				GoogleCalSync
	},
    data() {
		return {
            follow: '',
            tag_colors: TAG_COLORS,
            app_colors: APP_COLORS,
            is_fetch: false,
            color_theme: {"type" : "light", "name" : "theme-1"},
		}
	},
    mounted () {
        this.getFollowList()
        this.getColor()
    },
    methods: {
        getFollowList() {
            this.token = localStorage.token
			// console.log("slug =", calendar_slug)
			axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
            // const calendar_slug = this.$route.params.calendar_slug
            axios.get(`/api/v2/me/follow`).then( response => {
                console.log(response.data)
            })
        },
        getColor() {
            axios.get(`/api/v2/me/user_setting`)
            .then(response => {
                this.color_theme["type"] = response.data["setting"]["theme_type"]
                this.color_theme["name"] = response.data["setting"]["theme_name"]
            })
            .catch(error => {
                console.log(error)
            })
            this.is_fetch = true
        },
	}
}
</script>

<style lang='scss' scoped>

@import './../assets/style.css';

.calendar-navbar-bg {
    height: 65px;
    z-index: 5;
    position: fixed !important;
    top: 0px;
    left: 0px;
    right: 0px;
}
.sync {
	margin-left: 10px;
}
// .user-detail {
//     position: absolute;
//     right: 1%;
//     border-radius: 2px;
//     width: 200px;
//     border: 1px solid;
//     padding: 5px;
//     top: 9px;
// }
// .user-detail:hover {
//     border: 1px solid var(--white-op-1);
// }
// .user-detail-tab {
//     background-color: var(--white);
//     box-shadow: 0px 0px 1px 0px var(--black-op-1), 0px 0px 40px 0px var(--black-op-2);
//     position: absolute;
//     width: 210px;
//     margin-top: 6px;
//     overflow-x: hidden;
//     right: 0;
//     border-radius: 2px;
//     text-align: left;
// }
// .user-detail-button-tp {
//     background: none;
//     border: none;
//     color: var(--black);
//     cursor: pointer;
//     font-size: 18px;
//     width: 100%;
//     padding: 8px 15px 8px 15px;
//     text-align: left;
// }
// .user-detail-button-tp:hover {
//     background-color: var(--green);
//     color: var(--white);
// }

</style>
