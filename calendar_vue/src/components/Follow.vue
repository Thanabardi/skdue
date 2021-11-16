<template>
<div class="follow-main" v-if="(fs != '') && this.is_fetch">
  {{ this.follow_name }}
  <div v-if="this.token != ''">
    <button v-if="(fs == 'Unfollow') || (fs == 'UNFOLLOW')" style="background-color: var(--gray); width: 90px;"
      type="button" name="button" class="follow-button"
      @click="() => follow_button()">UNFOLLOW</button>
    <button v-if="(fs == 'Follow') || (fs == 'FOLLOW')" style="background-color: var(--green); width: 90px;"
      type="button" name="button" class="follow-button"
      @click="() => follow_button()">FOLLOW</button>
    </div>
</div>
<div v-else style="padding: 14px;"></div>
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
      calendar_slug: "",
      token: "",
      follow_name: "",
      is_fetch: false,
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
      this.is_fetch = true
    },
    getUser() {
      const calendar_slug = this.$route.params.calendar_slug
      const calendar_type = this.$route.params.calendar_type
      this.calendar_slug = calendar_slug.replace(/-/g,' ')

      console.log("TOKEN:", localStorage.token)
      this.token = localStorage.token


      console.log("slug =", calendar_slug)
      axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
      axios
        .get(`/api/v2/${calendar_type}/${calendar_slug}`)
        .then(response => {
          this.setCalendarOwner(response.data),
          this.follow_name = response.data.user.username
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

.follow-main {
  display: flex;
  justify-content: space-between;
  padding: 0 35px 0 35px;
  color: var(--yellow);
  font-weight: 600;
}
.follow-button {
  border: 0;
  padding: 4px 8px;
  color: var(--white);
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  border-radius: 4px;
}
</style>
