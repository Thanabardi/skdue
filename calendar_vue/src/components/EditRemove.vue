<template>
	<div class="event-create">
		<!-- <button v-if="(this.token!='') && (this.fs!='')" class="app-button-tp" style="font-size: 40px; line-height: 30px;"
			@click="() => TogglePopup('buttonTrigger')">+</button> -->

		<div style="text-align: center;" v-if="this.popup && (this.token!='') && (this.fs!='')" >
<!--  -->
			<div class="event-create-popup-bg">
				<div class="event-create-popup" :style="'background-color:'+app_colors[this.color_theme['type']]['sub-0']+
					';color:'+app_colors[this.color_theme['type']]['main']" >
					<h1 style="font-size: 50px;">Edit Event</h1>

					<form @submit.prevent="eventCreate" class="event-create-form" :style="'color:'+app_colors[this.color_theme['type']]['main']">
						<textarea class="event-create-textarea" type="name"
								placeholder="Title"
							maxlength="60" v-model="detail[0]" rows="1" cols="50"></textarea>
						<p></p>
						<textarea class="event-create-textarea" type="description"
						 placeholder="Description (optional)"
							maxlength="600" v-model="detail[1]" rows="5" cols="50"></textarea>
						<table class="event-create-table">
							<tr>
								<td>Start</td>
								<td>Date  <input class="event-create-input" type="date"
                    v-model="detail[2]"></td>
							</tr>
							<tr>
								<td></td>
								<td>Time  <input class="event-create-input" type="time"
									v-model="detail[3]"></td>
							</tr>
							<tr>
								<td>End</td>
								<td>Date  <input class="event-create-input" type="date"
									v-model="detail[4]"></td>
							</tr>
							<tr>
								<td></td>
								<td>Time  <input class="event-create-input" type="time"
									v-model="detail[5]"></td>
							</tr>
							<tr>
								<td>Tag</td>
								<td style="width: 270px; float: right;">
									<div style="padding: 18px 10px 18px; text-align: left; width: 250px" 
										class="event-create-input">{{detail[6]}}</div>
								</td>
							</tr>
							<tr>
								<td ></td>
								<td style="width: 400px;">
                  <!-- <button type="button" v-for="tag in available_tag" :key="tag"
										class="event-create-tag-bt"  @click="() => this.tag = tag">
										{{ tag }}</button> -->
										<button type="button" v-for="tag in available_tag" :key="tag"
											class="event-create-tag-bt" v-on:click.left="this.detail[6] = tag"
											v-on:click.right="TagEdit($event)" :style="'background-color:'
											+ this.tag_colors[color_tag[tag]]">{{ tag }}</button>

                  <!-- <div class="tag-button"  v-for="tag in available_tag" :key="tag">
                    <button type="button" class="event-create-tag-bt" autofocus  @click="() => this.tag = tag">
  										{{ tag }}</button> -->
                  <!-- </div> -->

                  				</td>
							</tr>
						</table>
						<div class="app-button-tp"
							style="color:red; line-height: 24px; margin:auto; font-weight: 500;width: 110px"
							@click="() => deleteEvent()">Delete Event</div>
						<div class="event-create-footer">
							<button class="app-button-main" type="submit"
								:style="'background-color:'+app_colors[this.color_theme['name']]['sub-2']">Done</button>
							<button class="app-button-gray"
								:style="'background-color:'+app_colors[this.color_theme['type']]['main-1']"
							 	@click="() => close()">Cancel</button>
						</div>

					</form>



				</div>

			</div>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { TAG_COLORS, APP_COLORS } from './ColorHandle'

export default {
  props: {
    popup: Boolean,
    detail: Object,
	color_theme: {},
	color_tag: {},
  },
	setup (props) {
    console.log('popup',props.popup)
    const popupTriggers = ref({
			buttonTrigger: props.popup,
		});

		const TogglePopup = (trigger) => {
			popupTriggers.value[trigger] = !popupTriggers.value[trigger]
      console.log(props.popup, popupTriggers.value['buttonTrigger'])

		}
		return {
      popupTriggers,
      TogglePopup
		}
	},
	data() {
		return {
			user_name: '',
			available_tag: [],
			name: '',
			description: '',
			start_date: '',
			start_time: '',
			end_date: '',
			end_time: '',
			token: "asdad",
			fs: "follow",
			tag_colors: TAG_COLORS,
			app_colors: APP_COLORS,
		}
	},
	mounted () {
        this.getUserNameAndTag()

    },
	methods: {
    log() {
    },
    close() {
      this.$emit('closed')
    },
		checkOwner(owner) {
			axios
				.get(`/api/v2/me`)
				.then(response => {
					console.log(response.data.user.id == owner)
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



      		axios.get(`/api/v2/${calendar_type}/${calendar_slug}`)
    			.then(response => {
        			this.user_name = response.data.user.username
					this.checkOwner(response.data.user.id)
				})
				axios.get(`/api/v2/me`)
					.then( response => {
					this.user_name = response.data["user"]["username"]
					response.data["available_tag"].forEach(elements => {
						if (elements["user"] == response.data["user"]["id"]) {
							this.available_tag.push(elements["tag"])
						} else if (elements["user"] == 1) {
							this.available_tag.push(elements["tag"])
							this.color_tag[elements['tag']] = "default"
						}
					})
				})
			
        },
		deleteEvent() {
			const start_date_time = this.detail[2] + " " + this.detail[3] + ":00"
			const end_date_time = this.detail[4] + " " + this.detail[5] + ":00"
			const event = {
				"name" : this.detail[0],
				"description" : this.detail[1],
				"start_date" : start_date_time,
				"end_date" : end_date_time,
				"tag" : this.detail[6]
			}

			axios.delete(`/api/v2/me/${this.user_name}/${this.detail[7]}`)
				.then(function(response) {
					console.log(response),
					window.location.reload()
					})
				.catch(function(error) {
					console.log(error),
					alert("Opps, " + error)
					})

		},
		eventCreate() {
			const start_date_time = this.detail[2] + " " + this.detail[3] + ":00"
			const end_date_time = this.detail[4] + " " + this.detail[5] + ":00"
			const event = {
				"name" : this.detail[0],
				"description" : this.detail[1],
				"start_date" : start_date_time,
				"end_date" : end_date_time,
				"tag" : this.detail[6]
			}

			// console.log(this.name)
			// console.log(this.description)
			// console.log(start_date_time)
			// console.log(end_date_time)
			// console.log(this.tag)

			console.log(event)
			axios.put(`/api/v2/me/${this.user_name}/${this.detail[7]}`, event)
				.then(function(response) {
					console.log(response),
					window.location.reload()
					})
				.catch(function(error) {
					console.log(error),
					alert("Opps, " + error)
					})
		}
	},
}

</script>

<style lang='scss' scoped>

@import './../assets/style.css';

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
	background-color: #3788d8;
	color: white;
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
::-webkit-scrollbar {
    display: none;
}
</style>
