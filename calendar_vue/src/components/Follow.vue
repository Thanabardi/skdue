<template>
    <button type="button" name="button" @click="() => follow_button()">Follow</button>
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
      option : "",
      follow_id : "",
		}
	},
	methods: {
		follow_button() {
      console.log(this.owner_id)
			const follow = {
				"option" : "follow",
				"follow_id" : this.owner_id,
			}
			axios.post(`/api/v2/user/me/`, follow)
				.then(function(response) {
					console.log(response)
					// window.location.reload()
					})
				.catch(function(error) {
					console.log(error),
					alert("Opps, " + error)
					})
		},
    getUser() {

      console.log("TOKEN:", localStorage.token)

      axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
      axios
        .get(`/api/v2/me`)
        .then(response => {
          // this.setCalendarEvents(response.data)
          console.log(response.data)
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

</style>
