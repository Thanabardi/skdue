<template>
	<div class="calendar-navbar-bg">
        <Search />
        <EventCreate />
        <UserConfig />
        <FollowedList />
	</div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import Search from './search'
import EventCreate from './EventCreate'
import UserConfig from './UserConfig'
import FollowedList from './FollowedList'

export default {
    components: {
        Search,
        EventCreate,
        UserConfig,
        FollowedList
	},
    data() {
		return {
            follow: '',
		}
	},
    mounted () {
        this.getFollowList()
    },
    methods: {
        getFollowList() {
            // const calendar_slug = this.$route.params.calendar_slug
            axios.get(`/api/v2/me/follow`).then( response => {
                console.log(response.data)
            })
        },
	}
}
</script>

<style lang='scss' scoped>

@import './../assets/style.css';

.calendar-navbar-bg {
    background: var(--main-green);
    height: 65px;
    z-index: 5;
    position: fixed !important;
    top: 0px;
    left: 0px;
    right: 0px;
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
