<template>
    <div class="dropdown">
        <input v-if="Object.keys(selectedItem).length === 0" ref="dropdowninput" v-model.trim="inputValue" class="dropdown-input"
        type="text" placeholder="User follow list" />
        <div v-else @click="resetSelection" class="dropdown-selected">
            {{ selectedItem.followed_name }}
        </div>
        <div v-show="inputValue && apiLoaded" class="dropdown-list">
            <div @click="selectItem(item)" v-show="itemVisible(item)" v-for="item in itemList" :key="item.followed_name" class="dropdown-item">
                <div style="display:flex; justify-content:space-between">
                    <div>{{ item.followed_name }}</div>
                    <div>Calendars</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Calendar from '../components/Calendar.vue'
import EventDetails from '../components/EventDetails.vue'
import { globalLocales } from '@fullcalendar/common'

export default ({
    data() {
		return {
            selectedItem: {},
			follow: '',
            inputValue: '',
            itemList: [],
            apiLoaded: false,
		}
	},
    mounted () {
        this.getFollowList()
    },
    methods: {
        getFollowList() {
            // const calendar_slug = this.$route.params.calendar_slug
            axios.get(`/api/v2/me/follow`).then( response => {
                console.log("fs data=", response.data)
                this.itemList = response.data
                this.apiLoaded = true
            })
        },
        itemVisible (item) {
            let currentName = item.followed_name.toLowerCase()
            let currentInput = this.inputValue.toLowerCase()
            return currentName.includes(currentInput)
        },
        resetSelection () {
            this.selectedItem = {}
            this.$nextTick( () => this.$refs.dropdowninput.focus() )
            this.$emit('on-item-reset')
        },
        async selectItem (theItem) {
            this.selectedItem = theItem 
            this.inputValue = ''
            this.$emit('on-item-selected', theItem)
            await this.$router.push({ path: `/calendar/${theItem.followed_name}` })
            this.$router.go()
        },
	}
})
</script>


<style scoped>
.dropdown{
  position: absolute;
  width: 85%;
  padding-top: 0px;
  left: 35%;
  top: 0px;
  transform: translate(-50%);
  /* max-width: 400px; */
  /* margin: 0 auto; */
}
.dropdown-input {
	background: var(--main-green);
	font-size: 20px;
	padding: 8px 20px;
	width:100%;
	border: none;
	border-radius: 4px;
}
/* .dropdown-input:focus, .dropdown-selected:hover{
  background: #fff;
  border-color: #e2e8f0;
}
.dropdown-input::placeholder{
  opacity: 0.7;
}
.dropdown-selected{
  font-weight: bold;
  cursor: pointer;
} */
.dropdown-list{
  background: var(--white);
  position: absolute;
  width: 105%;
  max-height: 500px;
  margin-top: 4px;
  overflow-x: hidden;
  box-shadow: 0px 0px 1px 0px var(--black-op-1), 0px 0px 40px 0px var(--black-op-2);
  border-radius: 2px;
  font-size: 20px;
  color: var(--black);
}
.dropdown-item{
  padding: 5px 16px;
  width: 96%;
  cursor: pointer;
}
.dropdown-item:hover{
  background: var(--white-dark);
}
.dropdown-item-flag{
  max-width: 24px;
  max-height: 18px;
  margin: auto 12px auto 0px;
}
::placeholder {
  color: white;
  opacity: 1; /* Firefox */
}

:-ms-input-placeholder { /* Internet Explorer 10-11 */
 color: white;
}

::-ms-input-placeholder { /* Microsoft Edge */
 color: white;
}
</style>