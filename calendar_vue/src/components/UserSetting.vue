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
                    <form @submit.prevent="eventCreate" class="event-create-form">
						<center><textarea class="event-create-textarea" type="name"
							required v-model="display_name"	placeholder="Display name"
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
                                <button @click="onUpload">Upload</button>
                            </div>
                        </center>
						<table class="event-create-table">
							<tr>
								<center><td>Tag</td></center>
								<td style="width: 400px;">
									<button type="button" v-for="tag in available_tag" :key="tag"
										class="event-create-tag-bt" @click="() => this.tag = tag">
										{{ tag }}</button></td>
							</tr>
						</table>
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
            display_name: '',
			available_tag: [],
			description: '',
			usertag: [],
            img: '',
            token: "asdad",
			fs: "follow",
            selectedFile: null,
		}
	},
	mounted () {
		this.getUserDetail()
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
			axios
				.get(`/api/v2/me/user_setting`)
				.then(response => {
					this.user_data = response.data
					console.log(this.user_data)
					this.display_name = this.user_data.setting.display_name
					this.description = this.user_data.setting.about
					this.img = "http://127.0.0.1:8000"+this.user_data.setting.image
					console.log(this.img)
				})
		},
        onFileSelected(event) {
            this.selectedFile = event.target.files[0]
        },
        onUpload() {
            axios.put()
        }
	},
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
