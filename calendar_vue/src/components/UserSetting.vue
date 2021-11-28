<template>
	<div>
		<CalendarNavbar />
		<div :style="'left:0px; height: 100%; width: 100%; position: fixed; overflow-x: hidden; background-color:'
			+ app_colors[this.color_theme['type']]['bg']" v-if="this.set_delay">
			<body>
			<div class="calendar-hr" :style="'width: 100%; color:'+app_colors[this.color_theme['type']]['main']">
					<center><a style="font-size: 40px">User Setting</a></center>
					<p></p>
					<center><img id="current_img" :src="img" class="avatar"></center>
					<p></p>
					<center>
						<form @submit.prevent="onUpload" class="event-create-form">
							<center><textarea class="event-create-textarea" type="name"
								required v-model="display"	placeholder="Display name"
								maxlength="20" rows="1" cols="50"></textarea></center>
							<p></p>
							<center><textarea class="event-create-textarea" type="description"
								v-model="description" placeholder="Description (optional)"
								maxlength="600" rows="5" cols="50"></textarea></center>
							<p></p>
							<!-- Upload Img -->
							<center>
								<div>
									<a :style="'font-size: 28px;  color:'+app_colors[this.color_theme['type']]['main']">Upload profile image</a><br>
									<p style="display: none" onload="this.style.display=''"></p>
									<img class="avatar" id="image_preview" style="display: none" onload="this.style.display=''"/><br>
									<p></p>
									<input :style="'color:'+app_colors[this.color_theme['type']]['main']" type="file" @change="onFileSelected" accept=".jpg, .jpeg, .png" class="inputfile">
									<label for="file">Choose an image</label>
								</div>
							</center>
							<!-- End -->
							<center><table>
								<tr>
									<p></p>
									<div><center :style="'font-size:30px; color:'+app_colors[this.color_theme['type']]['main']">Tag</center></div><br>
									<div>
										<div v-if="this.available_tag.length < 9">
											<input style="width: 270px;" class="event-create-textarea"
												placeholder="MyNewTag" maxlength="10" v-model="tag">
										</div>
										<!-- <p v-for="[key, color] of Object.entries(set_color)" :style="'font-size:22px; color:'+app_colors[this.color_theme['type']]['main']"> -->
										<a v-if="0<this.tag_name.length"><center :style="'color:'+this.color_item[this.tag_name[0]]"><div class='tag-options'><div @click='tagEdit(this.tag_name[0])'>edit</div> {{ this.tag_name[0] }} <div @click='tagDelete(this.tag_name[0])'>delete</div></div></center>
										<div class="flex-container">
											<div @click="userColorTag1('red')" id="color1" :style="'cursor:pointer; background-color:'+tag_colors['red']">.</div>
											<div @click="userColorTag1('yellow')" id="color1" :style="'cursor:pointer; background-color:'+tag_colors['yellow']">.</div>
											<div @click="userColorTag1('blue')" id="color1" :style="'cursor:pointer; background-color:'+tag_colors['blue']">.</div>
											<div @click="userColorTag1('green')" id="color1" :style="'cursor:pointer; background-color:'+tag_colors['green']">.</div>
											<div @click="userColorTag1('pink')" id="color1" :style="'cursor:pointer; background-color:'+tag_colors['pink']">.</div>
											<div @click="userColorTag1('purple')" id="color1" :style="'cursor:pointer; background-color:'+tag_colors['purple']">.</div>
											<div @click="userColorTag1('orange')" id="color1" :style="'cursor:pointer; background-color:'+tag_colors['orange']">.</div>
										</div>
										</a>
										<a v-if="1<this.tag_name.length"><center :style="'color:'+this.color_item[this.tag_name[1]]"><div class='tag-options'><div @click='tagEdit(this.tag_name[1])'>edit</div>{{ this.tag_name[1] }}<div @click='tagDelete(this.tag_name[1])'>delete</div></div></center>
										<div class="flex-container">
											<div @click="userColorTag2('red')" id="color2" :style="'cursor:pointer; background-color:'+tag_colors['red']">.</div>
											<div @click="userColorTag2('yellow')" id="color2" :style="'cursor:pointer; background-color:'+tag_colors['yellow']">.</div>
											<div @click="userColorTag2('blue')" id="color2" :style="'cursor:pointer; background-color:'+tag_colors['blue']">.</div>
											<div @click="userColorTag2('green') " id="color2" :style="'cursor:pointer; background-color:'+tag_colors['green']">.</div>
											<div @click="userColorTag2('pink')" id="color2" :style="'cursor:pointer; background-color:'+tag_colors['pink']">.</div>
											<div @click="userColorTag2('purple')" id="color2" :style="'cursor:pointer; background-color:'+tag_colors['purple']">.</div>
											<div @click="userColorTag2('orange')" id="color2" :style="'cursor:pointer; background-color:'+tag_colors['orange']">.</div>
										</div>
										</a>
										<a  v-if="2<this.tag_name.length"><center :style="'color:'+this.color_item[this.tag_name[2]]"><div class='tag-options'><div @click='tagEdit(this.tag_name[2])'>edit</div>{{ this.tag_name[2] }}<div @click='tagDelete(this.tag_name[2])'>delete</div></div></center>
										<div class="flex-container">
											<div @click="userColorTag3('red')" id="color3" :style="'cursor:pointer; background-color:'+tag_colors['red']">.</div>
											<div @click="userColorTag3('yellow')" id="color3" :style="'cursor:pointer; background-color:'+tag_colors['yellow']">.</div>
											<div @click="userColorTag3('blue')" id="color3" :style="'cursor:pointer; background-color:'+tag_colors['blue']">.</div>
											<div @click="userColorTag3('green')" id="color3" :style="'cursor:pointer; background-color:'+tag_colors['green']">.</div>
											<div @click="userColorTag3('pink')" id="color3" :style="'cursor:pointer; background-color:'+tag_colors['pink']">.</div>
											<div @click="userColorTag3('purple')" id="color3" :style="'cursor:pointer; background-color:'+tag_colors['purple']">.</div>
											<div @click="userColorTag3('orange')" id="color3" :style="'cursor:pointer; background-color:'+tag_colors['orange']">.</div>
										</div>
										</a>
										<a v-if="3<this.tag_name.length"><center :style="'color:'+this.color_item[this.tag_name[3]]"><div class='tag-options'><div @click='tagEdit(this.tag_name[3])'>edit</div>{{ this.tag_name[3] }}<div @click='tagDelete(this.tag_name[3])'>delete</div></div></center>
										<div class="flex-container">
											<div @click="userColorTag4('red')" id="color4" :style="'cursor:pointer; background-color:'+tag_colors['red']">.</div>
											<div @click="userColorTag4('yellow')" id="color4" :style="'cursor:pointer; background-color:'+tag_colors['yellow']">.</div>
											<div @click="userColorTag4('blue')" id="color4" :style="'cursor:pointer; background-color:'+tag_colors['blue']">.</div>
											<div @click="userColorTag4('green')" id="color4" :style="'cursor:pointer; background-color:'+tag_colors['green']">.</div>
											<div @click="userColorTag4('pink')" id="color4" :style="'cursor:pointer; background-color:'+tag_colors['pink']">.</div>
											<div @click="userColorTag4('purple')" id="color4" :style="'cursor:pointer; background-color:'+tag_colors['purple']">.</div>
											<div @click="userColorTag4('orange')" id="color4" :style="'cursor:pointer; background-color:'+tag_colors['orange']">.</div>
										</div>
										</a>
										<a v-if="4<this.tag_name.length"><center :style="'color:'+this.color_item[this.tag_name[4]]"><div class='tag-options'><div @click='tagEdit(this.tag_name[4])'>edit</div>{{ this.tag_name[4] }}<div @click='tagDelete(this.tag_name[4])'>delete</div></div></center>
										<div class="flex-container" >
											<div @click="userColorTag5('red')" id="color5" :style="'cursor:pointer; background-color:'+tag_colors['red']">.</div>
											<div @click="userColorTag5('yellow')" id="color5" :style="'cursor:pointer; background-color:'+tag_colors['yellow']">.</div>
											<div @click="userColorTag5('blue')" id="color5" :style="'cursor:pointer; background-color:'+tag_colors['blue']">.</div>
											<div @click="userColorTag5('green')" id="color5" :style="'cursor:pointer; background-color:'+tag_colors['green']">.</div>
											<div @click="userColorTag5('pink')" id="color5" :style="'cursor:pointer; background-color:'+tag_colors['pink']">.</div>
											<div @click="userColorTag5('purple')" id="color5" :style="'cursor:pointer; background-color:'+tag_colors['purple']">.</div>
											<div @click="userColorTag5('orange')" id="color5" :style="'cursor:pointer; background-color:'+tag_colors['orange']">.</div>
										</div>
										</a>
										<!-- </p> -->
									</div>
								</tr>
								<tr>
									<center :style="'font-size:30px; color:'+app_colors[this.color_theme['type']]['main']"><div :style="'color:'+color_font_theme">Theme</div></center>
									<center><div class="theme-container">
										<div style="cursor: pointer;" @click="defalutTheme">defalut</div>
										<div style="cursor: pointer; background-color: black;" @click="darkTheme">dark</div>
										<div :style="'cursor: pointer; background-color:'+tag_colors['purple']" @click="purpleTheme">purple</div>
									</div></center>
								</tr>
							</table></center>
							<div class="sync" style="font-size:30px; text-align: center">
								<GoogleCalSync :color_theme="this.color_theme"/><br>
							</div>
							<div class="event-create-footer">
								<button class="app-button-main" :style="'background-color:'+app_colors[this.color_theme['name']]['sub-2']" type="submit">Done</button>
							</div>
						</form>
					</center>
				</div>
			</body>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import CalendarNavbar from './CalendarNavbar.vue'
import { TAG_COLORS, APP_COLORS } from './ColorHandle'
import GoogleCalSync from './GoogleCalSync'

export default({
    components: {
        CalendarNavbar,
		GoogleCalSync
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
			color_tag: {},
			app_colors: APP_COLORS,
			tag_colors: TAG_COLORS,
			tag_name: [],
			color_item: {},
			name_theme: "",
			type_theme: "",
			color_font_theme: "",
			tag: '',
			set_delay: false,
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
			axios
                .get(`/api/v2/me`)
			    .then( response => {
				this.user_name = response.data["user"]["username"]
				response.data["available_tag"].forEach(elements => {
                this.available_tag.push(elements["tag"])
				})
			})
        },
		getUserDetail(){
			this.token = localStorage.token
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
        			this.color_tag = this.user_data.color
					console.log("color tag=", this.color_theme)
					this.color_item = this.color_tag
					console.log(this.color_item)
					console.log("color", this.tag_colors)
					this.name_theme = this.color_theme["name"]
					this.type_theme = this.color_theme["type"]
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
					for (let j=0; j<this.user_data.custom_tag.length; j++){
						this.tag_name.push((Object.entries(this.set_color)[j][0]))
					}
					this.set_delay = true
					console.log(this.tag_name.length)
				})
				
		},
        onFileSelected(event) {
			this.selectedFile = event.target.files[0]
			// render image preview
			var fr = new FileReader()
			fr.readAsDataURL(this.selectedFile)
			fr.onload = function(e) {
			var img = document.getElementById('image_preview')
			img.src = this.result
			}
        },
        onUpload() {
			var apiDataForm = new FormData()
			apiDataForm.append("file", this.selectedFile)
			apiDataForm.append("display_name", this.display)
			apiDataForm.append("about", this.description)
			apiDataForm.append("color", JSON.stringify(this.color_item))
			apiDataForm.append("theme_name", this.name_theme)
			apiDataForm.append("theme_type", this.type_theme)
			axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
			axios
				.put(`/api/v2/me/user_setting`, apiDataForm)
				.then(response => {
					this.tagCreate()
					console.log(response.data)
					window.location.reload()
					})
				.catch(function(error) {
					console.log(error),
					alert("Opps, " + error)
			})
		},
		tagCreate() {
			if (this.tag != '') {
				if (!this.available_tag.includes(this.tag)) {
					this.available_tag.push(this.tag)
					axios.post(`/api/v2/me/add_new_tag`, {"tag":this.tag})
						.then(function(response) {
							console.log("create new Tag", response)
						})
				} else {
					alert("This new tag is already exists")
				}
			}
		},
    tagDelete(tag){
      if(confirm("Are you sure you want to delete '"+ tag +"' tag \nIt will also delete event under the tag.")){
      axios.delete(`/api/v2/me/add_new_tag?tag=${tag}`)
      .then(function(response) {
          window.location.reload()
      })
    }
    },
    tagEdit(tag){
      let new_name = prompt("Please enter your new tag name");
      if (new_name != null) {
      const changed_tag = {
				"old_name" : tag,
				"new_name" : new_name,
			}
			axios.put(`/api/v2/me/add_new_tag`, changed_tag)
				.then(function(response) {
				})
			window.location.reload()
    }
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
		userColorTag1(color){
			this.color_item[this.tag_name[0]]=color
		},
		userColorTag2(color){
			this.color_item[this.tag_name[1]]=color
		},
		userColorTag3(color){
			this.color_item[this.tag_name[2]]=color
		},
		userColorTag4(color){
			this.color_item[this.tag_name[3]]=color
		},
		userColorTag5(color){
			this.color_item[this.tag_name[4]]=color
		},
		darkTheme(){
			this.name_theme = "theme-2"
			this.type_theme = "dark"
			this.color_font_theme = "#262626"
		},
		defalutTheme(){
			this.name_theme = "theme-1"
			this.type_theme = "light"
			this.color_font_theme = "#006664"
		},
		purpleTheme(){
			this.name_theme = "theme-3"
			this.type_theme = "light"
			this.color_font_theme = "#4D3D9E"
		},
	}
})
</script>

<style lang="scss" scoped>
@import './../assets/style.css';

.calendar-hr {
    position: relative;
	opacity: 0.8;
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
.event-create-footer {
	display: flex;
	justify-content: space-evenly;
}
.avatar {
  	vertical-align: middle;
  	width: 250px;
  	height: 250px;
  	border-radius: 50%;
 	object-fit: cover;
}
.avatar img {
	margin: -10px 0px 0px -180px;
}
.flex-container {
  	display: flex;
  	flex-wrap: nowrap;
  	background-color: rgb(230, 230, 230);
  	border-radius: 8px;
}
.flex-container > div {
	vertical-align: middle;
	border-radius: 50%;
	background-color: #f1f1f1;
	width: 25px;
	height: 25px;
	margin: 10px;
	text-align: center;
	line-height: 75px;
	font-size: 30px;
	text-indent: -9999px;
	}
	.flex-container div:hover {
		box-shadow: inset 0 -150px 0 0 rgba(243, 243, 243, 0.5)
	}
	.theme-container {
	width: 63%;
	display: flex;
	flex-wrap: nowrap;
	background-color: rgb(230, 230, 230);
	border-radius: 16px;
	padding: 20px;
	text-align: 'justify';
}

.theme-container > div {
	vertical-align: middle;
	border-radius: 50%;
	background-color: #006664;
	width: 25px;
	height: 25px;
	margin: 20px;
	line-height: 75px;
	font-size: 15px;
}
.theme-container div:hover {
	box-shadow: inset 0 -150px 0 0 rgba(243, 243, 243, 0.5)
}
.inputfile {
	width: 150px;
	height: 30px;
	opacity: 0;
	overflow: hidden;
	position: absolute;
	// z-index: 0;
	cursor: pointer;
}
.inputfile + label {
    font-family: 'Heebo', sans-serif;
	font-size: 0.75rem;
	font-weight: 500;
	letter-spacing: 0.025rem;
	font-style: normal;
	text-transform: uppercase;
	color: #EF2D56;
	background-color: #FFFFFF;
	border-radius: 1.25rem;
	-webkit-border-radius: 1.25rem;
	-moz-border-radius: 1.25rem;
	padding: 0.35rem 0.75rem;
	border-style: solid;
	border-width: 0.125rem;
	border-color: #EF2D56;
	width: 200px;
	// z-index: -1;
}
.inputfile:focus + label{
	outline: 1px dotted #000;
	outline: -webkit-focus-ring-color auto 5px;
}
.inputfile + label:hover {
    background-color: rgb(238, 211, 211);
	cursor: pointer;
}
::-webkit-scrollbar {
  	width: 20px;
}

::-webkit-scrollbar-track {
  	background-color: transparent;
}

::-webkit-scrollbar-thumb {
	background-color: #d6dee1;
	border-radius: 20px;
	border: 6px solid transparent;
	background-clip: content-box;
}

::-webkit-scrollbar-thumb:hover {
  	background-color: #a8bbbf;
}
@page {
    size: 11.7in 16.5in;
    margin: 27mm 16mm 27mm 16mm;
}
html {
    height: 235%;
}
body {
    min-height: 235%;
}
.sync {
	padding-top: 3%;
}
.tag-options * {
  white-space: nowrap;
  display: inline;
  padding: 1%;
  color: black;
  border-radius: 8px;
  cursor: pointer;
  margin: 0 30px 0 30px;
  background: rgb(230, 230, 230);
}
</style>
