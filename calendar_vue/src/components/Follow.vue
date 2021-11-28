<template>
<div class="follow-main" v-if="(fs != '') && this.set_delay" :style="'color:'+app_colors[this.color_theme['name']]['sub-2']">
  <img :src="img" class="avatar" style="cursor: pointer;" v-on:click.left="this.visibility = 'visible'">
  <div style="margin-left: 10px; padding-top: 4px; cursor: pointer;" v-on:click.left="this.visibility = 'visible'">{{ this.follow_name }}</div>
  <div v-if="this.token != ''">
    <button v-if="(fs == 'Unfollow') || (fs == 'UNFOLLOW')" style="background-color: rgba(190, 190, 190, 0.8); 
      width: 90px;position: absolute;right: 30px;top:16px"
      type="button" name="button" class="follow-button"
       v-on:click.left="follow_button(), this.visibility = 'visible'">UNFOLLOW</button>
    <button v-if="(fs == 'Follow') || (fs == 'FOLLOW')" :style="'width: 90px; position: absolute;right: 30px;top:16px ;background-color:'
      +app_colors[this.color_theme['name']]['sub-2']"
      type="button" name="button" class="follow-button"
      @click="() => follow_button()">FOLLOW</button>
  </div>

  <div v-if="(this.visibility == 'visible')" class='follow-sidebar' 
    :style="'background-color:'+app_colors[this.color_theme['name']]['sub-1']+';visibility:'+ this.visibility">
    <img :src="img" class="avatar" style="width: 250px; height: 250px;">
    <p style="font-size: 35px; line-height: 0px;">{{this.follow_name}}</p>
    <button v-if="(this.token != '') && ((fs == 'Unfollow') || (fs == 'UNFOLLOW'))"
      style="width: 90px; background-color: rgba(190, 190, 190, 0.8);"
      type="button" name="button" class="follow-button"
      v-on:click.left="follow_button(), this.visibility = 'hide'">UNFOLLOW</button>
    <button v-if="(this.token != '') && ((fs == 'Follow') || (fs == 'FOLLOW'))" :style="'width: 90px; background-color:'
      +app_colors[this.color_theme['name']]['sub-2']"
      type="button" name="button" class="follow-button"
      v-on:click.left="follow_button(), this.visibility = 'hide'">FOLLOW</button>
    <p style="opacity: 0.8; padding-left: 12px; position: absolute; overflow-x: hidden;top: 380px; bottom: 120px; 
      color; rgba(255, 255, 255, 0.6); width: 90%;">{{this.about}}</p>
    <div class="calendar-sidebar-footer">
      <hr class="calendar-hr">
      <button class="app-button-tp" v-on:click.left="this.visibility = 'hidden'"
        type="button" name="button" style="color: rgba(255, 255, 255, 0.8); font-size: 20px;">Hide</button>
    </div>
  </div>

</div>
<div v-else style="padding: 14px;"></div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { TAG_COLORS, APP_COLORS } from './ColorHandle'

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
      app_colors: APP_COLORS,
      tag_colors: TAG_COLORS,
      calendar_id: 0,
      img: '',
      about: '',
      visibility: 'visible',
      set_delay: false
		}
	},
    props: {
      color_theme: {},
  },
  mounted() {
      this.getUser()
    },
	methods: {
    follow_button() {
      const follow = {
      	"option" : this.fs.toLowerCase(),
      	"follow_id" : this.owner_id,
        "follow_calendar" : this.calendar_id
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
    this.calendar_id = data.calendar.id
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
            this.visibility = 'hidden'
          }
          else if (user.user == this.owner_id) {
            this.fs = '';
            this.visibility = 'visible'
          }
          console.log('user',user.user)
          console.log('owner',this.owner_id)
        })
        setTimeout(this.set_delay = true, 500)
      })
      .catch(error => {
        console.log(error)
      })
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
      axios.get(`/api/v2/calendar/${calendar_slug}/user_setting`).then(response => {
        this.img = "http://127.0.0.1:8000"+response.data.setting.image
        this.about = response.data.setting.about
        })
    },
  }
}

</script>

<style lang='scss' scoped>

@import './../assets/style.css';
.avatar {
  vertical-align: middle;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}
.follow-sidebar {
  color: white;
  height: 100%; /* Full-height: remove this if you want "auto" height */
  width: 23%; /* Set the width of the sidebar */
  position: fixed; /* Fixed Sidebar (stay in place on scroll) */
  z-index: 1; /* Stay on top */
  top: 0; /* Stay at the top */
  left: 0;
  margin-top: 65px;
  padding: 10px;
  font-size: 22px;
  text-align: center;
  overflow-x: hidden;
}
.follow-sidebar p{
  font-size: 20px;
}
.follow-main {
  display: flex;
  // justify-content: end;
  padding: 0 35px 0 35px;
  // color: rgb(255, 192, 0);
  font-weight: 600;
}
.follow-button {
  border: 0;
  padding: 4px 8px;
  color: white;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  border-radius: 4px;
}
.calendar-hr {
  border: 1px solid;
  opacity: 0.8;
  width: 90%;
}
.calendar-sidebar-footer {
  position: absolute;
  bottom: 100px;
  width: 95%;
  text-align: center;
}
::-webkit-scrollbar {
    display: none;
}
</style>
