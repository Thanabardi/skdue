<template>
	<div class="google">
		<button v-if="(this.token!='') && (this.fs!='')" class="app-button-tp" style="font-size: 40px; line-height: 30px;"
			@click="() => syncGoogleCalEvent()">SYNC</button>
	</div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
	setup () {
	},
	data() {
		return {
			token: "asdad",
			fs: "follow",
		}
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

              	response.data;
                  // console.log(response.data.slug);
              })
              .catch(error => {
              console.log(error)
              })
      window.location.reload()
		}
	},
}

</script>

<style lang='scss' scoped>

@import './../assets/style.css';

.app-button-tp {
    background-color: black;
	color: white;
	border-radius: 23%;
}
</style>
