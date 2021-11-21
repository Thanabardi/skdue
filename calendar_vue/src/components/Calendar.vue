<script>
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import CalendarNavbar from './CalendarNavbar'
import EventCreate from './EventCreate'
import Follow from './Follow'
import Search from './search'
import EventDetails from './EventDetails'

import EditRemove from './EditRemove'

import { TAG_COLORS, APP_COLORS } from './ColorHandle'

import {ref} from 'vue'
import axios from 'axios'
export default {
  components: {
    FullCalendar, // make the <FullCalendar> tag available
    CalendarNavbar,
    Search,
    EventCreate,
    Follow,
    EditRemove,
  },
  data: function () {
    return {
      calendarOptions: {
        timeZone: "UTC",
        plugins: [
          dayGridPlugin,
          timeGridPlugin,
          interactionPlugin, // needed for dateClick
        ],
        customButtons: {
          myCustomButton: {
            text: 'Year',
            click: function() {
              // alert('clicked the custom button!');
            }
          }
        },
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "prevYear,myCustomButton,nextYear" //,timeGridWeek,timeGridDay
        },
        initialView: "dayGridMonth",
        // initialEvents: INITIAL_EVENTS,
        events: [],
        // editable: true,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        select: this.handleDateSelect,
        // eventClick: this.handleEventClick,
        eventsSet: this.handleEvents,
        /* you can update a remote database when these fire:
        eventAdd:
        eventChange:
        eventRemove:
        */
      },
      editEvent: false,
      editEventList: [],
      currentEvents: [],
      calendar_events: [],
      event_in_selected_date: [], //added in iter4
      event_response: {}, // data from response
      tag_status: {}, // a dict for which tag gonna show in calendar
      tag_list: [], // store all tag name
      my_tag_list: [], // store my tag name
      follow_tag_list: [], // store follow tag name
      event_details: [],
      modalActive: true,
      calendar_id: Number,
      token: "",
      day_select: "",
      day: [
        'Sunday','Monday','Tuesday','Wednesday',
        'Thursday','Friday','Saturday'
        ],
      month: [
        'January','February','March','April',
        'May','June','July','August','September',
        'October','November','December'
        ],
      color_theme: {"type" : "light", "name" : "theme-1"},
      is_fetch: false,
      color_tag: {},
      app_colors: APP_COLORS,
      tag_colors: TAG_COLORS,
      dataLogout:{
        "status":"logout"
      }
    };
  },
  setup() {  //EventDetails
  let modalActive = ref(false);

  const popupTriggers = ref({
    sidebarTrigger: false,
    editTrigger: false,
    select_event: {},
  });
  const TogglePopup = (trigger, e=0, item=0) => {
    //handle edit followed event
    if (trigger == 'editTrigger' && item.is_mine == false){
      return
    }
    else {
    e.preventDefault()
    console.log('is_this_mine',item)
    popupTriggers.value[trigger] = !popupTriggers.value[trigger]
    popupTriggers.value["select_event"]= [
        item.name,
        item.description,
        item.start_date,
        item.start_time,
        item.end_date,
        item.end_time,
        item.tag,
        item.slug
      ]
    }
  }
  return {
    modalActive,
    popupTriggers,
    TogglePopup
  }
  },
  mounted() {
    this.getCalendarEvents()
    this.getColor()
    this.getTag()
  },
  methods: {
    setTodayEvents() {
      this.event_details = []
      let today = new Date()
      this.day_select = today.getFullYear()+"-"+
        ("0" + (today.getMonth() + 1)).slice(-2)+"-"+
        ("0" + today.getDate()).slice(-2)

      let day_select_check = this.day_select.replace(/-/g,'')

      this.calendarOptions.events.forEach(elements => {
        let event = this.convertEventDateTime(elements)
        let start_date_check = event["start_date"].replace(/-/g,'')
        let end_date_check = event["end_date"].replace(/-/g,'')
        if((start_date_check <= day_select_check) && (day_select_check <= end_date_check)){
          this.event_details.push(event)
        }
      });
    },
    setCalendarEvents(data){
      this.calendar_id = data.calendar.id
      console.log(data.event)
      let tag = data.tag
      this.tag_list = data.tag // check this line
      let all_event = data.event
      this.event_response = data
      console.log("RESPONSE", this.event_response)
      for (let t=0; t<tag.length; t++){
        // init tag status
        this.tag_status[tag[t]] = true;

        let d = all_event[tag[t]]
        // console.log(d)
        this.calendar_events = d
        // console.log(this.calendar_events)
        for(let i=0; i<d.length; i++) {
          this.calendarOptions.events.push({
            id: d[i].id,
            title: d[i].name,
            start: d[i].start_date,
            end: d[i].end_date,
            description: d[i].description,
            slug: d[i].slug,
            tag : d[i].tag_text,
            from_calendar_id: d[i].calendar,
          })
        }
      }
    this.setTodayEvents();
    },
    getCalendarEvents() {
      const calendar_slug = this.$route.params.calendar_slug
      const calendar_type = this.$route.params.calendar_type

      this.token = localStorage.token

      console.log("slug =", calendar_slug)
      axios.defaults.headers.common["Authorization"] = "Token " + localStorage.token
      axios.get(`/api/v2/${calendar_type}/${calendar_slug}`)
        .then(response => {
          this.setCalendarEvents(response.data)
        })
        .catch(error => {
          console.log(error)
        })

    },
    getColor() {
      axios.get(`/api/v2/me/user_setting`)
      .then(response => {
        this.color_theme["type"] = response.data["setting"]["theme_type"]
        this.color_theme["name"] = response.data["setting"]["theme_name"]
        this.color_tag = response.data["color"]
      })
      .catch(error => {
        console.log(error)
      })
      this.is_fetch = true
    },
    getTag() {
			axios.get(`/api/v2/me`)
				.then( response => {
					response.data["available_tag"].forEach(elements => {
						if (elements["user"] == response.data["user"]["id"]) {
							this.my_tag_list.push(elements["tag"])
						} else {
              this.follow_tag_list.push(elements["tag"])
            }
					})
				})
    },
    handleWeekendsToggle() {
      this.calendarOptions.weekends = !this.calendarOptions.weekends; // update a property
    },
    handleDateSelect(selectInfo) {
      // let title = prompt("Please enter a new title for your event"); //input the title name of event
      // let calendarApi = selectInfo.view.calendar;
      // calendarApi.unselect(); // clear date selection
      // if (title) {
      //   // if use fill the input
      //   calendarApi.addEvent(
      //     {
      //     id: createEventId(),
      //     title,
      //     start: selectInfo.startStr,
      //     end: selectInfo.endStr,
      //     allDay: selectInfo.allDay,
      //     //color: 'red',
      //     //textColor: 'black',
      //   });
      // }
      this.event_details = []
      let select = selectInfo.start
      this.day_select = select.getFullYear()+"-"+
        ("0" + (select.getMonth() + 1)).slice(-2)+"-"+
        ("0" + select.getDate()).slice(-2)

      let day_select_check = this.day_select.replace(/-/g,'')

      this.calendarOptions.events.forEach(elements => {
        let event = this.convertEventDateTime(elements)
        let start_date_check = event["start_date"].replace(/-/g,'')
        let end_date_check = event["end_date"].replace(/-/g,'')
        if((start_date_check <= day_select_check) && (day_select_check <= end_date_check)){
          this.event_details.push(event)
        }
      }
    );
      // sort by start time
      function compare( a, b ) {
        if ( a.start_time < b.start_time ){
          return -1;
        }
        if ( a.start_time > b.start_time ){
          return 1;
        }
        return 0;
      }
      this.event_details.sort( compare );
      console.log('sort',this.event_details)
    },
    changeIntForDateTime(dateTimeList){
      console.log(dateTimeList)
      let list = [];
      dateTimeList.forEach(e => {
        if (e.length == 1) {
          e="0"+e;
        }
        list.push(e);
      })
      return list
      ;

    },
    handleEventClick(clickInfo) {
      
    },
    swap(value){
      console.log('PIDDDDD')
      this.popupTriggers.editTrigger = false
      console.log(this.popupTriggers.select_event)
    },
    handleEvents(events) {
      this.currentEvents = events;
    },
    convertEventDateTime(events) {
      let start_date = events.start.substring(0, 10)
      let end_date = events.end.substring(0, 10)
      let start_time = events.start.substring(11, 16)
      let end_time = events.end.substring(11, 16)
      let allday = false

      let start_date_check = start_date.replace(/-/g,'')
      let end_date_check = end_date.replace(/-/g,'')
      let day_select_check = this.day_select.replace(/-/g,'')

      if ((start_date_check < day_select_check) && (day_select_check < end_date_check)){
        allday = true
      }
      else if ((start_date_check == end_date_check) && (start_time == "00:00") && (end_time == "23:59")) {
        allday = true
      }

      let is_mine = events.from_calendar_id == this.calendar_id

      return {
				"name" : events.title,
				"description" : events.description,
				"start_date" : start_date,
        "start_time" : start_time,
				"end_date" : end_date,
        "end_time" : end_time,
        "tag" : events.tag,
        "allday" : allday,
        "slug" : events.slug,
        "is_mine" : is_mine
			}
    },
    clearData(data){
      localStorage.setItem("token", "")
      this.$router.push({ path: `/`});
    },
    logoutData(e){
      e.preventDefault();

      axios.get(`/api/v2/logout`, this.dataLogout)
        .then(response => {
        this.clearData(response.data);
          // console.log(response.data);
          // console.log(response.data.slug);
      })
        .catch(error => {
        console.log(error)
      })
    },
    handlefiltertag(tag_text){
      // only change status in `this.tag_status`
      var checkBox = document.getElementById(tag_text);
      if (checkBox.checked==false){
        this.tag_status[tag_text] = false
        }
      else if (checkBox.checked==true){
        this.tag_status[tag_text] = true
      }
      console.log(this.tag_status)

      // whenever status has been changed, call a re-rederevent function
      this.calendarOptions.events = []
      let event = this.event_response.event; // get event
      for(let i=0; i<this.tag_list.length; i++) {
        // using this.event_response
        let tag = this.tag_list[i]
        let tagged_event = event[tag]
        if(this.tag_status[tag]) {
          // console.log(tag, this.tag_status[tag])
          for(let j=0; j<event[tag].length; j++) {
            this.calendarOptions.events.push({
              id: tagged_event[j].id,
              title: tagged_event[j].name,
              start: tagged_event[j].start_date,
              end: tagged_event[j].end_date,
              description: tagged_event[j].description,
              slug: tagged_event[j].slug,
              tag : tagged_event[j].tag_text
            })
          }
        }
      }
      FullCalendar.calendar.currentData.calendarApi.refetchEvents()
    },
  },
};
</script>


<template>
  <!-- <div> -->
      <!-- <form @submit.prevent="logoutData" class="form-form">
        <button class="logout-button">Logout</button>
      </form> -->
    <!-- <CalendarNavbar /> -->

<!--
    <div class='calendar-sidebar'>
      <EventDetails>

        <Follow />
        <h2 style="text-align: center;">{{ this.day[new Date(this.day_select).getDay()] }}
          {{ (this.day_select.substring(8, 10)) }}
          {{ this.month[new Date(this.day_select).getMonth()] }}
          {{ (this.day_select.substring(0, 4)) }}
        </h2>
        <div style="overflow-x: hidden; height: 76%;"> -->

  <div v-if="this.is_fetch" :style="'height: 100%; width: 100%; position: fixed; background-color:'
    +app_colors[this.color_theme['type']]['sub']">
    <CalendarNavbar :color_theme="this.color_theme"/>



    <div class='calendar-sidebar' :style="'background-color:'+app_colors[this.color_theme['name']]['sub-1']">
      <Follow :color_theme="this.color_theme"/>
      <h2 style="text-align: center;">{{ this.day[new Date(this.day_select).getDay()] }}
        {{ (this.day_select.substring(8, 10)) }}
        {{ this.month[new Date(this.day_select).getMonth()] }} 
        {{ (this.day_select.substring(0, 4)) }}
      </h2>
        <!-- list of all event -->

        <div style="position: absolute; overflow-x: hidden; 
          top: 140px; bottom: 140px; color; rgba(255, 255, 255, 0.6); width: 95%;">
          
          <div v-if="this.event_details.length!=0">
            <p>All-Day Event</p>
            <!-- list of all day event -->

            <div v-for="item in this.event_details" :key="item">
                <button v-if="item['allday']" class="calendar-detail-bg"
                  :style="'background-color:'+tag_colors[this.color_tag[item['tag']]]"
                  v-on:click.right="TogglePopup('editTrigger', $event, item)">

                  <!-- v-on:click.right="TogglePopup('editTrigger', $event, item)"> -->

                  <table class="calendar-table">
                  <tr><td style="width: 1000px; text-align: center;">{{ item["name"] }}</td></tr>
                  <tr><td colspan="2" style="font-weight: 500; opacity: 0.8;">
                      {{ item["description"] }}</td></tr>
                  </table>
                </button>
            </div>
            <!-- list of all day event -->

            <!-- list of other event -->
            <hr class="calendar-hr">
            <div v-for="item in this.event_details" :key="item">
              <div v-if="!item['allday']">
                <button v-if="(item['start_date'] < this.day_select)" class="calendar-detail-bg"
                  :style="'background-color:'+tag_colors[this.color_tag[item['tag']]]"
                  v-on:click.right="TogglePopup('editTrigger', $event, item)">
                  <table class="calendar-table">
                  <tr><td style="width: 110px;">00:00-{{ item["end_time"] }}</td>
                    <td>{{ item["name"] }}</td></tr>
                  <tr><td colspan="2" style="font-weight: 500; opacity: 0.8;">
                      {{ item["description"] }}</td></tr>
                  </table>
                </button>
                <button v-if="this.day_select < item['end_date']" class="calendar-detail-bg"
                  :style="'background-color:'+tag_colors[this.color_tag[item['tag']]]"
                  v-on:click.right="TogglePopup('editTrigger', $event, item)">
                  <table class="calendar-table">
                  <tr><td style="width: 110px;">{{ item["start_time"] }}-00:00</td>
                    <td>{{ item["name"] }}</td></tr>
                  <tr><td colspan="2" style="font-weight: 500; opacity: 0.8;">
                      {{ item["description"] }}</td></tr>
                  </table>
                </button>
                <button v-if="item['start_date'] == item['end_date']" class="calendar-detail-bg"
                  :style="'background-color:'+tag_colors[this.color_tag[item['tag']]]"
                  v-on:click.right="TogglePopup('editTrigger', $event, item)">
                  <table class="calendar-table">
                  <tr><td style="width: 110px;">{{ item["start_time"] }}-{{ item["end_time"] }}</td>
                    <td>{{ item["name"] }}</td></tr>
                  <tr><td colspan="2" style="font-weight: 500; opacity: 0.8;">
                      {{ item["description"] }}</td></tr>
                  </table>
                </button>
              </div>
            </div>
            <!-- list of other event -->

          </div>
          <!-- list of all event -->

        <div v-else>
          <p style="font-size: 20px; text-align: center;">
            You have no events scheduled today</p>
        </div>
      </div>
      <!-- side bar footer -->
      <div class="calendar-sidebar-footer">
        <hr class="calendar-hr">
        <button v-if="(this.token!='') && (this.fs!='')" class="app-button-tp"
          style="color: rgba(255, 255, 255, 0.8); font-size: 20px;"
          v-on:click.left="TogglePopup('sidebarTrigger', $event)">Manage View</button>
      </div>
      <!-- side bar footer -->

      <!-- Tag filters -->
      <div style="text-align: center;" v-if="popupTriggers.sidebarTrigger">
        <div class='calendar-sidebar' :style="'background-color:'+app_colors[this.color_theme['name']]['sub-1']">

          <!-- My Tag filters -->
          <p style="font-size: 20px; text-align: left; padding-left: 20px;">My Tags</p>
          <hr class="calendar-hr">
          <div class="filter-tag-bg">
            <div style="padding: 5px 0px 5px 0" v-for="tag_text in this.my_tag_list" :key="tag_text">
              <input type="checkbox" v-bind:id="tag_text" v-on:click.left="handlefiltertag(tag_text)" checked>
              <label :style="'color:'+tag_colors[this.color_tag[tag_text]]"> {{ tag_text }} </label><br>
            </div>
          </div>
          <!-- My Tag filters -->

          <!-- Follow Tag filters -->
          <p style="font-size: 20px; text-align: left; padding-left: 20px;">Follow</p>
          <hr class="calendar-hr">
          <div class="filter-tag-bg" >
            <div style="padding: 5px 0px 5px 0" v-for="tag_text in this.follow_tag_list" :key="tag_text">
              <input type="checkbox" v-bind:id="tag_text" v-on:click.left="handlefiltertag(tag_text)" checked>
              <label :style="'max-height: 20%; color:'+app_colors[this.color_theme['type']]['main']"> {{ tag_text }} </label><br>
            </div>
          </div>
          <!-- Follow Tag filters -->

          <div class="calendar-sidebar-footer">
            <hr class="calendar-hr">
            <button class="app-button-tp" v-on:click.left="TogglePopup('sidebarTrigger', $event)"
              type="button" name="button" style="color: rgba(255, 255, 255, 0.8); font-size: 20px;">Back</button>
          </div>
        </div>
      </div>
    </div>
    <!-- Tag filters -->

    <!-- edit event -->
    <div v-if="popupTriggers.editTrigger">
      <div class="editremove">
            <EditRemove :popup="popupTriggers.editTrigger" :detail="popupTriggers.select_event" :color_theme="this.color_theme" @closed="swap"/>
      </div>


        <!-- <button class="app-button-main" v-on:click.left="TogglePopup('editTrigger', $event)">Edit</button>
        <button class="app-button-gray" v-on:click.left="TogglePopup('editTrigger', $event)">Delete</button> -->
    </div>
    <!-- edit event -->

    <FullCalendar class="calendar-app-main" :options="calendarOptions" :color_theme="this.color_theme" :style="'color:'+app_colors[this.color_theme['type']]['main']">
      <template v-slot:eventContent="arg">
        <b>{{ arg.timeText }}</b>
        <i>{{ arg.event.title }}</i>
      </template>
    </FullCalendar>

    <!-- show tags -->
    <div style="font-size: 15px; left: 27% ;position: fixed; width: 71%; height: 45px; overflow-x: hidden;">
      <div style="display: inline-block; padding-top: 8px;" v-for="tag_text in this.my_tag_list" :key="tag_text">
        <label :style="'margin-right: 15px; padding: 2px 10px 2px 10px; border-radius: 8px; color: white; background-color:'
          +tag_colors[this.color_tag[tag_text]]" v-if="this.tag_status[tag_text]"> {{ tag_text }} </label><br>
      </div>
      <div style="display: inline-block; padding-top: 8px;" v-for="tag_text in this.follow_tag_list" :key="tag_text">
        <label :style="'margin-right: 15px; padding: 2px 10px 2px 10px; border-radius: 8px; background-color: rgba(200, 200, 200, 0.5); color:'+
          app_colors[this.color_theme['type']]['main-0']"
          v-if="this.tag_status[tag_text]"> {{ tag_text }} </label><br>
      </div>
    </div>
    <!-- show tags -->
  </div>
</template>


<style lang='scss' scoped>

@import './../assets/style.css';

.editremove {
  height: 65px;
  z-index: 10;
  position: fixed !important;
}

.calendar-sidebar {
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
}
.calendar-sidebar p{
  font-size: 18px;
  text-align: center;
  opacity: 0.8;
}
.calendar-detail-bg {
  background-color: rgba(255, 255, 255, 0.5);
  border-collapse: collapse;
  padding: 5px;
  display: block;
  margin: 20px auto 20px auto;
  justify-items: center;
  width: 90%;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}
.calendar-table{
  color: white;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
  width: 100%;
  font-size: 20px;
  padding-left: 5px;
  font-weight: 550;
  word-break: break-word;
  text-align: left;
}
.calendar-sidebar-footer {
  position: absolute;
  bottom: 100px;
  width: 95%;
  text-align: center;
}
.calendar-hr {
  border: 1px solid;
  opacity: 0.8;
  width: 90%;
}
.filter-tag-bg {
  background-color: rgba(255, 255, 255, 0.6);
  padding: 10px 20px 10px 20px;
  display: block;
  margin: 20px auto 20px auto;
  text-align: left;
  width: 70%;
  border-radius: 8px;
  overflow-x: hidden;
}
b { /* used for event dates/times */
  margin-right: 3px;
}
.calendar-app-main {
  padding: 10px;
  font-size: 18px;
  overflow: hidden;
}
.fc { /* the calendar root */
  margin: 3% 2% 0% 26%; /* Same as the sidebar width and nav bar heigh*/
  max-height: 85vh;
}
::-webkit-scrollbar {
    display: none;
}
// checkbox style sliding
// .flipswitch {
//   position: relative;
//   background: white;
//   width: 50px;
//   height: 20px;
//   top: 18px;
//   -webkit-appearance: initial;
//   border-radius: 3px;
//   -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
//   outline: none;
//   font-size: 14px;
//   font-family: Trebuchet, Arial, sans-serif;
//   font-weight: bold;
//   cursor: pointer;
//   border: 7px solid #ddd;
// }

// .flipswitch:after {
//   position: absolute;
//   top: 0%;
//   display: block;
//   line-height: 32px;
//   width: 45%;
//   height: 90%;
//   background: #fff;
//   box-sizing: border-box;
//   text-align: center;
//   transition: all 0.3s ease-in 0s;
//   color: black;
//   border: #888 1px solid;
//   border-radius: 3px;
// }

// .flipswitch:after {
//   left: 2%;
//   content: "Hide";
// }

// .flipswitch:checked:after {
//   left: 53%;
//   content: "Show";
// }
</style>
