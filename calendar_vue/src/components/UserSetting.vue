<template>
    <div :style="'left:0px; height: 100%; width: 100%; position: fixed; overflow-x: hidden; background-color:' + app_colors[this.color_theme['type']]['sub']">
        <div>
            <CalendarNavbar />
        </div>
        <div class="calendar-hr" :style="'color:'+app_colors[this.color_theme['type']]['main']">
                <center><a style="font-size: 40px">User Setting</a></center>
				<p></p>
				<center><img id="current_img" :src="img" class="avatar"></center>
                <p></p>
                <center>
                    <form @submit.prevent="onUpload" class="event-create-form">
						<center><textarea class="event-create-textarea" type="name"
							required v-model="display"	placeholder="Display name"
							maxlength="60" rows="1" cols="50"></textarea></center>
						<p></p>
						<center><textarea class="event-create-textarea" type="description"
							v-model="description" placeholder="Description (optional)"
							maxlength="600" rows="5" cols="50"></textarea></center>
                        <p></p>
                        <!-- Upload Img -->
                        <center>
                            <div>
                                <a :style="'font-size: 28px;  color:'+app_colors[this.color_theme['type']]['main']">Upload profile image</a><br>
                                <p></p>
                                <input type="file" @change="onFileSelected" accept=".jpg, .jpeg, .png">
                            </div>
                        </center>
						<!-- End -->
						<center><table>
							<tr>
								<p></p>
								<div><center :style="'font-size:30px; color:'+app_colors[this.color_theme['type']]['main']">Tag</center></div><br>
								<div>
									<p v-for="[key, color] of Object.entries(set_color)" :style="'font-size:30px; color:'+app_colors[this.color_theme['type']]['main']">
										{{ key }} 
										<div class="flex-container">
											<div style="background-color: var(--green);">.</div>
											<div style="background-color: var(--black);">.</div>
											<div style="background-color: var(--yellow);">.</div>
										</div>
									</p>
								</div>
							</tr>
						</table></center>
						<div class="event-create-footer">
							<button class="app-button-main" :style="'background-color:'+app_colors[this.color_theme['name']]['main']" type="submit">Done</button>
							<button class="app-button-gray" @click="() => TogglePopup('buttonTrigger')">Cancel</button>
						</div>
					</form>
                    </center>
        </div>
    </div>
</template>

<script> 
import { ref } from 'vue';
import axios from 'axios';
import CalendarNavbar from './CalendarNavbar.vue'
import { TAG_COLORS, APP_COLORS } from './ColorHandle'

export default({
    components: {
        CalendarNavbar,
    },
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
			username: '',
            display: '',
			available_tag: [],
			description: '',
			usertag: [],
			set_color: [],
            img: '',
            token: "asdad",
			fs: "follow",
            selectedFile: null,
			color_theme: {"type" : "light", "name" : "theme-1"},
			is_fetch: false,
			color_tag: {},
			app_colors: APP_COLORS,
			tag_colors: TAG_COLORS,
		}
	},
	mounted () {
		this.getUserDetail()
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
			console.log("this is setting token=" ,this.token)
			// console.log("slug =", calendar_slug)
			axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
			axios
				.get(`/api/v2/${calendar_type}/${calendar_slug}`)
				.then(response => {
				this.user_name = response.data.user.username
				this.checkOwner(response.data.user.id)
				})
			axios
                .get(`/api/v2/me`)
			    .then( response => {
				this.user_name = response.data["user"]["username"]
				response.data["available_tag"].forEach(elements => {
                this.available_tag.push(elements["tag"])
				})
				// console.log('avaliable',this.available_tag)
			})
        },
		getUserDetail(){
			this.token = localStorage.token
			console.log("this is setting token=" ,this.token)
			// console.log("slug =", calendar_slug)
			axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
			const main_url = "http://127.0.0.1:8000"
			axios
				.get(`/api/v2/me/user_setting`)
				.then(response => {
					this.user_data = response.data
					this.user_id = this.user_data.setting.user
					this.display = this.user_data.setting.display_name
					this.description = this.user_data.setting.about
					this.img = main_url + this.user_data.setting.image
					this.color_theme["type"] = response.data["setting"]["theme_type"]
       	 			this.color_theme["name"] = response.data["setting"]["theme_name"]
        			this.color_tag = response.data["color"]
					// img url to base64
					const toDataURL = url => fetch(url)
						.then(response => response.blob())
						.then(blob => new Promise((resolve, reject) => {
						const reader = new FileReader()
						reader.onloadend = () => resolve(reader.result)
						reader.onerror = reject
						// base64
						reader.readAsDataURL(blob)
					}))
					// base64 to file object for axios put
					toDataURL(this.img)
					.then(dataUrl => {
						// console.log('Here is Base64 Url', dataUrl)
						var fileData = this.dataURLtoFile(dataUrl, "userimage.jpg");
						// console.log("Here is JavaScript File Object",fileData)
						this.selectedFile = fileData
					})
					for (let i=0; i<this.user_data.custom_tag.length; i++){
						this.usertag.push(this.user_data.custom_tag[i].tag)
						// usertag.push(this.user_data.custom_tag[i].tag)
					}
					this.set_color = this.user_data.color
					this.is_fetch = true
					// console.log(this.usertag)
					// console.log(this.set_color)
					// console.log(this.img)
					// console.log(this.user_id)
				})
		},
        onFileSelected(event) {
			this.selectedFile = event.target.files[0]
			// console.log('file img= ', this.selectedFile)
        },
        onUpload() {
			var apiDataForm = new FormData()
			apiDataForm.append("file", this.selectedFile)
			apiDataForm.append("display_name", this.display)
			apiDataForm.append("about", this.description)
			apiDataForm.append("color", JSON.stringify({}))
			axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
			axios
				.put(`/api/v2/me/user_setting`, apiDataForm)
				.then(response => {
					console.log(response.data)
					window.location.reload()
					})
				.catch(function(error) {
					console.log(error),
					alert("Opps, " + error)
			})
		},
		dataURLtoFile(dataurl, filename) {
			// create a file object of url image that was transformed as base64
			var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
			bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
			while(n--){
			u8arr[n] = bstr.charCodeAt(n);
			}
		return new File([u8arr], filename, {type:mime});
		},
	}
})
</script>

<style lang="scss" scoped>
@import './../assets/style.css';

.calendar-hr {
    position: relative;
    border: 1px solid var(--white-op-2);
    width: 90%;
    top: 50px;
}
.event-create {
    position: absolute;
    right: 25%;
    border-radius: 2px;
    width: 40px;
    top: 14px;
	height: 40px;
	line-height: 10px;
	text-align: center;
}
.event-create-popup-bg {
	background-color: rgba(0, 0, 0, 0.5);
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	z-index: 1;
	position: fixed;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 50px;

	animation-name: fade;
	animation-duration: 0.5s
}
.event-create-popup {
	color: black;
	height: 100%;
	overflow-x: hidden;
	padding: 20px;
}
.event-create-form {
	color: black;
	text-align: left;
	font-size: 20px;
	margin: 20x;
	padding: 10px;
}
.event-create-textarea {
	background: rgb(230, 230, 230);
	font-size: 20px;
	display: block;
	padding: 10px 20px;
	border: none;
	border-radius: 8px;
	resize: vertical;
}
.event-create-table {
	width: 104%;
	text-align: end;
	border-spacing: 20px;
}
.event-create-input {
	background: rgb(230, 230, 230);
	font-size: 20px;
	padding: 10px;
	width: 200px;
	border: none;
	border-radius: 8px;
}
.event-create-tag-bt {
	background-color: rgb(230, 230, 230);
	color: black;
	margin-left: 10px;
    border: 0;
    padding: 5px 10px;
    margin-bottom: 10px;
    font-size: 20px;
    cursor: pointer;
    border-radius: 8px;
}
.event-create-tag-bt:focus {
	opacity: 0.5;
}
.event-create-footer {
	display: flex;
	justify-content: space-evenly;
}
.avatar {
  vertical-align: middle;
  width: 250px;
  height: 250px;
  border-radius: 50%;
}
.avatar img {
	margin: -10px 0px 0px -180px;
}
.flex-container {
  display: flex;
  flex-wrap: nowrap;
}

.flex-container > div {
  background-color: #f1f1f1;
  width: 25px;
  height: 25px;
  margin: 10px;
  text-align: center;
  line-height: 75px;
  font-size: 30px;
  text-indent: -9999px;
}
</style>
