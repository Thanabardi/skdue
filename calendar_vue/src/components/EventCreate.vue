<template>
	<div class="event-create">
		<button v-if="(this.token!='') && (this.fs!='')" class="app-button-tp" style="font-size: 40px; line-height: 30px;"
			@click="() => TogglePopup('buttonTrigger')">+</button>

		<div style="text-align: center;" v-if="popupTriggers.buttonTrigger"
		:TogglePopup="() => TogglePopup('buttonTrigger')">
			<div class="event-create-popup-bg">
				<div class="event-create-popup">
					<h1 style="font-size: 50px;">New Event</h1>
					<form @submit.prevent="eventCreate" class="event-create-form">
						<textarea class="event-create-textarea" type="name"
							required v-model="name"	placeholder="Title"
							maxlength="60" rows="1" cols="50"></textarea>
						<p></p>
						<textarea class="event-create-textarea" type="description"
							v-model="description" placeholder="Description (optional)"
							maxlength="600" rows="5" cols="50"></textarea>
						<table class="event-create-table">
							<tr>
								<td>Start</td>
								<td>Date  <input class="event-create-input" type="date"
									required v-model="start_date"></td>
							</tr>
							<tr>
								<td></td>
								<td>Time  <input class="event-create-input" type="time"
									required v-model="start_time"></td>
							</tr>
							<tr>
								<td>End</td>
								<td>Date  <input class="event-create-input" type="date"
									required v-model="end_date"></td>
							</tr>
							<tr>
								<td></td>
								<td>Time  <input class="event-create-input" type="time"
									required v-model="end_time"></td>
							</tr>

							<tr v-if="this.available_tag.length < 5">
								<td>Tag</td>
								<td>
									<input style="width: 250px;" class="event-create-input" 
										placeholder="MyNewTag" maxlength="10" required v-model="tag">
								</td>
							</tr>
							<tr>
								<td v-if="this.available_tag.length > 5" 
									style="vertical-align: top; padding-top: 10px;">Tag</td>
								<td v-else></td>
								<td style="width: 400px;">
									<button type="button" v-for="tag in available_tag" :key="tag"
										class="event-create-tag-bt" v-on:click.left="this.tag = tag"
										v-on:click.right="TagEdit($event)">{{ tag }}</button>
								</td>
							</tr>
						</table>
						<div class="event-create-footer">
							<button class="app-button-main" type="submit">Done</button>
							<button class="app-button-gray" @click="() => TogglePopup('buttonTrigger')">Cancel</button>
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
			user_name: '',
			available_tag: [],
			name: '',
			description: '',
			start_date: '',
			start_time: '',
			end_date: '',
			end_time: '',
			tag: '',
			token: "asdad",
			fs: "follow",

		}
	},
	mounted () {
        this.getUserName(),
		this.getTag()
    },
	methods: {
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
        getUserName() {
			const calendar_slug = this.$route.params.calendar_slug
      		const calendar_type = this.$route.params.calendar_type
			this.token = localStorage.token
			console.log("slug =", calendar_slug)
			axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
			axios.get(`/api/v2/${calendar_type}/${calendar_slug}`)
				.then(response => {
					this.user_name = response.data.user.username
					this.checkOwner(response.data.user.id)
				})
        },
		getTag() {
			this.available_tag = []
			axios.get(`/api/v2/me`)
				.then( response => {
					this.user_name = response.data["user"]["username"]
					response.data["available_tag"].forEach(elements => {
						this.available_tag.push(elements["tag"])
					})
				})

        },
		eventCreate() {
			const start_date_time = this.start_date + " " + this.start_time + ":00"
			const end_date_time = this.end_date + " " + this.end_time + ":00"
			const event = {
				"name" : this.name,
				"description" : this.description,
				"start_date" : start_date_time,
				"end_date" : end_date_time,
				"tag" : this.tag
			}

			// console.log(this.name)
			// console.log(this.description)
			// console.log(start_date_time)
			// console.log(end_date_time)
			// console.log(this.tag)

			if (!this.available_tag.includes(this.tag)) {
				this.tagCreate()
			}
			axios.post(`/api/v2/me/${this.user_name}`, event)
				.then(function(response) {
					console.log(response),
					window.location.reload()
				})
				.catch(function(error) {
					console.log(error),
					alert("Opps, " + error)
				})
		},
		tagCreate() {
			if (this.tag == '') {
				alert("Tag can't be blank")
			} else if (!this.available_tag.includes(this.tag)) {
				axios.post(`/api/v2/me/add_new_tag`, {"tag":this.tag})
					.then(function(response) {
						console.log(response),
						this.getTag()
					})
					.catch(function(error) {
						console.log(error),
						alert("Opps, " + error)
					})
			} else {
				alert("This tag already exists")
			}
		},
		TagEdit(e) {
			alert("EditTag")
			e.preventDefault()
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
	width: 104%;
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
    margin-bottom: 10px;
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
</style>
