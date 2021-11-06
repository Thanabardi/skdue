<template>
  <!-- <h2>  +++ !!!!          ตรงนี้ไอภูมิ    !!!!  +++     </h2> -->
  <div class="follow_button" v-if="fs != ''">
      <button type="button" name="button" @click="() => follow_button()">{{this.fs}}</button>
    </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
	setup () {},
	data() {
		return {
      option : "",
      follow_id : "",
      owner_id :0,
      fs:"Follow",
		}
	},
  mounted() {
      this.getUser()
    },
	methods: {
    follow_button() {
      const follow = {
      	"option" : this.fs.toLowerCase(),
      	"follow_id" : this.owner_id,
      }
      console.log(follow)
      axios.post(`/api/v2/me/follow`, follow)
      	.then(function(response) {
      		console.log(response)
      		// window.location.reload()
      		})
      	.catch(function(error) {
      		console.log(error),
      		alert("Opps, " + error + "Please Login First")
        })
      if (this.fs.toLowerCase() == 'follow') {
        this.fs = 'UNFOLLOW'
      }
      else if (this.fs.toLowerCase() == 'unfollow') {
        this.fs = 'FOLLOW'
      }
    },
    setCalendarOwner(data) {
          //set owner_id
    this.owner_id = data.user.id
    console.log('owner_id=',this.owner_id,'id_type',typeof this.owner_id)
    // check follow status
    axios
      .get(`/api/v2/me`)
      .then(response => {
        if (response.data.user.id == this.owner_id) {
          this.fs = '';
          console.log('done')
        }
      })
      .catch(error => {
        console.log(error)
      })
    axios
      .get(`/api/v2/me/follow`)
      .then(response => {
        response.data.forEach(user=>{
          if(user.followed == this.owner_id){
            this.fs = 'UNFOLLOW';
          }
          else if (user.user == this.owner_id) {
            this.fs = '';
          }
          console.log('user',user.user)
          console.log('owner',this.owner_id)
        })

      })
      .catch(error => {
        console.log(error)
      })
    },
    getUser() {
      const calendar_slug = this.$route.params.calendar_slug
      const calendar_type = this.$route.params.calendar_type

      console.log("TOKEN:", localStorage.token)


      console.log("slug =", calendar_slug)
      axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
      axios
        .get(`/api/v2/${calendar_type}/${calendar_slug}`)
        .then(response => {
          this.setCalendarOwner(response.data)
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
