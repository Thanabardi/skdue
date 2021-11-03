<template>
  <div class="dropdown">
    <input v-if="Object.keys(selectedItem).length === 0" ref="dropdowninput"
      v-model.trim="inputValue" class="dropdown-input"
      type="text" placeholder="Search Skdue" />
    <div v-else @click="resetSelection" class="dropdown-selected">
      {{ selectedItem.name }}</div>
    <div v-show="inputValue && apiLoaded" class="dropdown-list">
      <div @click="selectItem(item)" v-show="itemVisible(item)" 
        v-for="item in itemList.calendar" :key="item.name" class="dropdown-item">
        <div style="display:flex; justify-content:space-between">
          <div>{{ item.name }}</div>
          <div>Calendars</div>
        </div>
      </div>
      <div @click="selectItemEvents(item)" v-show="itemVisible(item)" 
        v-for="item in itemList.event" :key="item.name" class="dropdown-item">
        <div style="display:flex; justify-content:space-between">
          <div>{{ item.name }}</div>
          <div>Events</div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
import Calendar from '../components/Calendar.vue'
import EventDetails from '../components/EventDetails.vue'
import { globalLocales } from '@fullcalendar/common'

export default {
  data () {
    return {
      selectedItem: {},
      inputValue: '',
      itemList: [],
      apiLoaded: false,
    }
  },
  mounted () {
    this.getList()
  },
  components: {
    Calendar, // make the <FullCalendar> tag available
    EventDetails
  },
  methods: {
    resetSelection () {
      this.selectedItem = {}
      this.$nextTick( () => this.$refs.dropdowninput.focus() )
      this.$emit('on-item-reset')
    },
    async selectItem (theItem) {
      this.selectedItem = theItem 
      this.inputValue = ''
      this.$emit('on-item-selected', theItem)
      await this.$router.push({ path: `/calendar/${theItem.slug}` })
      this.$router.go()
    },
    slice_slug(slug){
      var str = slug;
      var url_calendar = "";
      for(var i =1; i< str.length;i++){
		    url_calendar += str[i];
        if (str[i] == '/'){
          break;
        }
      }
      return url_calendar
    },
    async selectItemEvents (theItem){
      this.selectedItemEvent = theItem 
      this.inputValue = ''
      this.$emit('on-item-selected', theItem)
      await this.$router.push({ path: `/search` })
      await this.$router.replace({ path: `/calendar/${this.slice_slug(theItem.get_absolute_url)}` })
      Calendar.components.FullCalendar.calendar.currentData.calendarApi.gotoDate(theItem.start_date)
    },
    itemVisible (item) {
      let currentName = item.name.toLowerCase()
      let currentInput = this.inputValue.toLowerCase()
      return currentName.includes(currentInput)
    },
    getList () {
      axios.get('/api/calendar/search').then( response => {
        this.itemList = response.data
        this.apiLoaded = true
      })
    }
  }
}
</script>

<style lang='scss' scoped>

@import './../assets/style.css';

.dropdown{
  position: absolute;
  width: 40%;
  // padding-top: 0px;
  left: 50%;
  transform: translate(-50%, -9px);
  /* max-width: 400px; */
  /* margin: 0 auto; */
}
.dropdown-input {
	background: var(--white);
	font-size: 20px;
	padding: 8px 20px;
	width: 100%;
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
</style>
