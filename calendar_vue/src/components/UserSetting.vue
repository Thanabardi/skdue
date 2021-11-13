<template>
    <div>
        <div>
            <CalendarNavbar />
        </div>
        <div class="calendar-hr">
                <center><a style="font-size: 40px">User Setting</a></center>
				<p></p>
				<center><img :src="img" class="avatar"></center>
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
                                <a style="font-size: 28px">Upload profile image</a><br>
                                <p></p>
                                <input type="file" @change="onFileSelected">
                            </div>
                        </center>
						<!-- End -->
						<center><table>
							<tr>
								<p></p>
								<!-- <div><center style="font-size:30px">Tag</center></div><br>
								<div>
									<p v-for="[key, color] of Object.entries(set_color)">{{ key }} 
										<textarea>{{color}}
										</textarea>
									</p>
								</div> -->
							</tr>
						</table></center>
						<div class="event-create-footer">
							<button class="app-button-main" type="submit">Done</button>
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
		}
	},
	mounted () {
		this.getUserDetail()
		this.getUserNameAndTag()
		// this.onUpload()
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
			const main_url = "http://127.0.0.1:8000"
			axios
				.get(`/api/v2/me/user_setting`)
				.then(response => {
					this.user_data = response.data
					this.user_id = this.user_data.setting.user
					this.display = this.user_data.setting.display_name
					this.description = this.user_data.setting.about
					this.img = main_url + this.user_data.setting.image
					for (let i=0; i<this.user_data.custom_tag.length; i++){
						this.usertag.push(this.user_data.custom_tag[i].tag)
						// usertag.push(this.user_data.custom_tag[i].tag)
					}
					this.set_color = this.user_data.color
					console.log(this.usertag)
					console.log(this.set_color)
					console.log(this.img)
					console.log(this.user_id)
				})
		},
        onFileSelected(event) {
			this.selectedFile = event.target.files[0]
			console.log('file img= ', this.selectedFile)
        },
        onUpload() {
			var apiDataForm = new FormData()
			apiDataForm.append("file", this.selectedFile)
			apiDataForm.append("display_name", this.display)
			apiDataForm.append("about", this.description)
			apiDataForm.append("color", JSON.stringify({}))
			// apiDataForm.append("color", {})
			// const apiDataForm = {
			// 	"file": this.selectedFile,
			// 	"display_name": this.display,
			// 	"about": this.description,
			// 	// "color": JSON.stringify({})
			// }
			console.log(apiDataForm)
			// console.log(end_date_time)
			// console.log(this.tag)
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
.app-button-tp:hover {
    background-color: var(--white-op-2);
}
.event-create-popup-bg {
	background-color: var(--black-op-1);
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
	background: var(--white);
	color: var(--black);
	height: 100%;
	overflow-x: hidden;
	padding: 20px;
}
.event-create-form {
	color: var(--black);
	text-align: left;
	font-size: 20px;
	margin: 20x;
	padding: 10px;
}
.event-create-textarea {
	background: var(--gray-light);
	font-size: 20px;
	display: block;
	padding: 10px 20px;
	border: none;
	border-radius: 8px;
	resize: vertical;
}
.event-create-table {
	width: 100%;
	text-align: end;
	border-spacing: 20px;
}
.event-create-input {
	background: var(--gray-light);
	font-size: 20px;
	padding: 10px;
	width: 200px;
	border: none;
	border-radius: 8px;
}
.event-create-tag-bt {
	background-color: var(--gray-light);
	margin-left: 10px;
    border: 0;
    padding: 5px 10px;
    margin-top: 20px;
    color: var(--black);
    font-size: 20px;
    cursor: pointer;
    border-radius: 8px;
}
.event-create-tag-bt:focus {
	background-color: var(--green);
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
</style>
