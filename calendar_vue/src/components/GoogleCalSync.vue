<template>
	<div class="google">
		<div v-if="(this.token!='') && (this.fs!='')" class="app-button-tp" :style="'font-weight: bold;border-radius: 20px;font-size: 20px; color:'
			+app_colors[this.color_theme['name']]['sub-2']+'; position: absolute; left: 50%; transform: translate(-50%, -50%); width: 200px;'"
			@click="() => syncGoogleCalEvent()">SYNC WITH GOOGLE</div>
	</div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { TAG_COLORS, APP_COLORS } from './ColorHandle'

export default {
	setup () {
	},
	data() {
		return {
			token: "asdad",
			fs: "follow",
			tag_colors: TAG_COLORS,
            app_colors: APP_COLORS,
		}
	},
	props: {
		color_theme: {},
    },
	mounted () {
        this.getUserNameAndTag()
    },
	methods: {
		checkOwner(owner) {
			axios
				.get(`/api/v2/me`)
				.then(response => {
					// console.log(response.data.user.id == owner)
					if (response.data.user.id == owner) {
						this.fs = 'follow';
					}
					else {
						this.fs = ''
					}
				})
				.catch(error => {
					console.log(error)
				})
		},
        getUserNameAndTag() {
					const calendar_slug = this.$route.params.calendar_slug
          const calendar_type = this.$route.params.calendar_type
			       this.token = localStorage.token

          axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
          axios
            .get(`/api/v2/${calendar_type}/${calendar_slug}`)
            .then(response => {
              this.user_name = response.data.user.username
				      this.checkOwner(response.data.user.id)
			    })

        },
		async syncGoogleCalEvent() {
      	await axios.get(`/oauth/sync-event/`)
			.then(response => {
				console.log('sync-event',response.data);
				window.location.reload()
			})
			.catch(error => {
				alert("Please log in with Google")
				console.log(error)
			})
		}
	},
}

</script>

<style lang='scss' scoped>

@import './../assets/style.css';

</style>
