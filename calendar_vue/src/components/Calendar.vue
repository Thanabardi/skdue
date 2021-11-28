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
      // tag_list: [], // store all tag name
      my_tag_list: [], // store my tag name
      follow_name_list: [], // store follow name
      public_tag: [],
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
      color_tag: {},
      follow_list: {},
      app_colors: APP_COLORS,
      tag_colors: TAG_COLORS,
      dataLogout:{
        "status":"logout"
      },
      user_name: '',
      calendar_slug: this.$route.params.calendar_slug.replace(/-/g,' '),
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
    // this.getTag()
    // this.getFollow()
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
      let tag = data.tag

      this.event_response = data
      this.tag_status["my_tag"] = {}
      this.tag_status["follow_id"] = {}

      this.tag_status["follow_id"]["not_me"] = true
      this.my_tag_list.forEach(element => {this.tag_status["my_tag"][element] = true})
      this.follow_list["id"].forEach(element => {this.tag_status["follow_id"][element] = true})

      let event = this.event_response.event; // get event
      for (const tag in event){
        for (const event_all in event[tag]){
          this.handleRenderEvent(event[tag][event_all])
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
      axios.get(`/api/v2/me/${calendar_slug}`)
        .then( response => {this.calendar_id = response.data.calendar.id})
      axios.get(`/api/v2/${calendar_type}/${calendar_slug}`)
        .then(response => {
          this.public_tag = response.data.tag
          this.setCalendarEvents(response.data)
        })
        .catch(error => {
          console.log(error)
        })

    },
    getTag() {
			axios.get(`/api/v2/me`)
				.then( response => {
          this.user_name = response.data["user"]["username"]
					response.data["available_tag"].forEach(elements => {
						if (elements["user"] == response.data["user"]["id"]) {
							this.my_tag_list.push(elements["tag"])
            } else if (elements["user"] == 1) {
              this.my_tag_list.push(elements["tag"])
              this.color_tag[elements['tag']] = "default"
            }
					})
				})
    },
    getColor() {
      axios.get(`/api/v2/me/user_setting`)
      .then(response => {
        this.color_theme["type"] = response.data["setting"]["theme_type"]
        this.color_theme["name"] = response.data["setting"]["theme_name"]
        this.color_tag = response.data["color"]
        this.getFollow()
        this.getTag()
      })
      .catch(error => {
        console.log(error)
      })
    },
    getFollow() {
      this.follow_list["id"] = []
      axios.get(`/api/v2/me/follow`)
      .then(response => {
        response.data.forEach(element => {
          this.follow_list[element["followed_calendar"]] = element["followed_calendar_slug"].replace(/-/g,' ')
          this.follow_list["id"].push(element["followed_calendar"])
          this.follow_name_list.push(element["followed_calendar_slug"].replace(/-/g,' '))
          this.color_tag[element["followed_calendar_slug"].replace(/-/g,' ')] = "follow"
        });
      })
      .catch(error => {
        console.log(error)
      })
    },
    getFollow() {
      axios.get(`/api/v2/me/follow`)
      .then(response => {
        response.data.forEach(element => {
          this.follow_list[element["followed_calendar"]] = element["followed_calendar_slug"].replace(/-/g,' ')
        });
      })
      .catch(error => {
        console.log(error)
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
      let event_owner = ""
      let event_check = ""
      let color = ""

      let start_date_check = start_date.replace(/-/g,'')
      let end_date_check = end_date.replace(/-/g,'')
      let day_select_check = this.day_select.replace(/-/g,'')

      if ((start_date_check < day_select_check) && (day_select_check < end_date_check)){
        allday = true
      }
      else if ((start_date_check == end_date_check) && (start_time == "00:00") && (end_time == "23:59")) {
        allday = true
      }

      let is_mine = (events.from_calendar_id == this.calendar_id)
      if ((this.user_name == this.calendar_slug)) {
        if (is_mine) {
          event_check = ["my_tag", events.tag]
          color = this.tag_colors[this.color_tag[events.tag]]
        } else {
          event_owner = this.follow_list[events.from_calendar_id]
          event_check = ["follow_id", (events.from_calendar_id).toString()]
          color = this.tag_colors["follow"]
        }
      } else {
        event_check = ["follow_id", "not_me"]
      }
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
        "is_mine" : is_mine,
        "detail_display" : false,
        "event_owner" : event_owner,
        "event_check" : event_check,
        "color": color
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
    handleRenderEvent(event) {
      let event_color
      if ((this.user_name == this.calendar_slug) && (event.calendar == this.calendar_id)) {
        event_color = this.tag_colors[this.color_tag[event.tag_text]]
      } else {
        event_color = "rgba(180, 180, 180, 0.9)"
      }
      this.calendarOptions.events.push({
        id: event.id,
        title: event.name,
        start: event.start_date,
        end: event.end_date,
        description: event.description,
        slug: event.slug,
        tag : event.tag_text,
        color: event_color,
        from_calendar_id : event.calendar
      })
    },
    handlefiltertag(tag_text){
      // only change status in `this.tag_status`
      // var checkBox = document.getElementById(tag_text);
      if (this.my_tag_list.includes(tag_text)) {
        this.tag_status["my_tag"][tag_text] = ! this.tag_status["my_tag"][tag_text]
			} else {
        this.tag_status["follow_id"][tag_text] = ! this.tag_status["follow_id"][tag_text]
      }

      // whenever status has been changed, call a re-rederevent function
      this.calendarOptions.events = []
      let event = this.event_response.event; // get event
      let calendar_id = this.event_response.calendar.id; // get calendar id
      for (const tag in event){
        if (this.my_tag_list.includes(tag) && (this.tag_status["my_tag"][tag])) {
          for (const event_all in event[tag]){
            if(calendar_id == event[tag][event_all]["calendar"]) {
              this.handleRenderEvent(event[tag][event_all])
            }
          }
        }
      }
      for (const tag in event){
        for (const event_all in event[tag]){
          if(this.tag_status["follow_id"][event[tag][event_all]["calendar"]]) {
            this.handleRenderEvent(event[tag][event_all])
          }
        }
      }
      FullCalendar.calendar.currentData.calendarApi.refetchEvents()
    },
    handlefilterEvent(event){
      event["detail_display"] = !event["detail_display"]
    },
  },
};
</script>


<template>
  <div :style="'height: 100%; width: 100%; position: fixed; background-color:'
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
              <button v-if="item['allday'] && this.tag_status[item['event_check'][0]][item['event_check'][1]] && 
                item['start_date'] == item['end_date']"
                class="calendar-detail-bg"
                :style="'background-color:'+item['color']"
                v-on:click.right="TogglePopup('editTrigger', $event, item)"
                v-on:click.left="handlefilterEvent(item)">
                <table class="calendar-table">
                  <tr><td style="width: 1000px; text-align: center;">{{ item["name"] }}</td></tr>
                  <!-- event detail -->
                  <tr v-if="item['detail_display']" style="font-weight: 500; opacity: 0.8;">
                    <td colspan="2">
                      <table style="line-height: 18px">
                        <tr v-if="item['event_owner'] != ''"><td>From:</td><td>{{ item["event_owner"] }}</td></tr>
                        <tr><td style="width: 110px;">Tag:</td><td>{{ item['tag'] }}</td></tr>
                        <tr><td>Start:</td><td>{{ new Date(item["start_date"]).toLocaleDateString("en-GB") }} {{ item["start_time"] }}</td></tr>
                        <tr><td>End:</td><td>{{ new Date(item["end_date"]).toLocaleDateString("en-GB") }} {{ item["end_time"] }}</td></tr>
                      </table>
                    </td>
                  </tr>
                  <tr v-if="item['detail_display']">
                    <td colspan="2" v-if="item['detail_display']" style="font-weight: 500; opacity: 0.8;">{{ item["description"] }}</td>
                  </tr>
                  <!-- event detail -->
                </table>
              </button>
              <button v-if="item['allday'] && this.tag_status[item['event_check'][0]][item['event_check'][1]] && 
                item['start_date'] != item['end_date']" 
                class="calendar-detail-bg"
                :style="'background-color:'+item['color']"
                v-on:click.right="TogglePopup('editTrigger', $event, item)"
                v-on:click.left="handlefilterEvent(item)">
                <table class="calendar-table">
                  <tr><td style="width: 1000px; text-align: center;">{{ item["name"] }}</td></tr>
                  <!-- event detail -->
                  <tr v-if="item['detail_display']" style="font-weight: 500; opacity: 0.8;">
                    <td colspan="2">
                      <table style="line-height: 18px">
                        <tr v-if="item['event_owner'] != ''"><td>From:</td><td>{{ item["event_owner"] }}</td></tr>
                        <tr><td style="width: 110px;">Tag:</td><td>{{ item['tag'] }}</td></tr>
                        <tr><td>Start:</td><td>{{ new Date(item["start_date"]).toLocaleDateString("en-GB") }} {{ item["start_time"] }}</td></tr>
                        <tr><td>End:</td><td>{{ new Date(item["end_date"]).toLocaleDateString("en-GB") }} {{ item["end_time"] }}</td></tr>
                      </table>
                    </td>
                  </tr>
                  <tr v-if="item['detail_display']">
                    <td colspan="2" v-if="item['detail_display']" style="font-weight: 500; opacity: 0.8;">{{ item["description"] }}</td>
                  </tr>
                  <!-- event detail -->
                </table>
              </button>
            </div>
            <!-- list of all day event -->

            <!-- list of other event -->
            <hr class="calendar-hr">
            <div v-for="item in this.event_details" :key="item">
              <div v-if="!item['allday'] && this.tag_status[item['event_check'][0]][item['event_check'][1]]">
                <button v-if="(item['start_date'] < this.day_select)" class="calendar-detail-bg" 
                  :style="'background-color:'+item['color']"
                  v-on:click.right="TogglePopup('editTrigger', $event, item)"
                  v-on:click.left="handlefilterEvent(item)">
                  <table class="calendar-table">
                    <tr><td style="width: 110px; vertical-align: text-top">00:00-{{ item["end_time"] }}</td>
                      <td>{{ item["name"] }}</td></tr>
                    <!-- event detail -->
                    <tr v-if="item['detail_display']" style="font-weight: 500; opacity: 0.8;">
                      <td colspan="2">
                        <table style="line-height: 18px">
                          <tr v-if="item['event_owner'] != ''"><td>From:</td><td>{{ item["event_owner"] }}</td></tr>
                          <tr><td style="width: 110px;">Tag:</td><td>{{ item['tag'] }}</td></tr>
                          <tr><td>Start:</td><td>{{ new Date(item["start_date"]).toLocaleDateString("en-GB") }} {{ item["start_time"] }}</td></tr>
                          <tr><td>End:</td><td>{{ new Date(item["end_date"]).toLocaleDateString("en-GB") }} {{ item["end_time"] }}</td></tr>
                        </table>
                      </td>
                    </tr>
                    <tr v-if="item['detail_display']">
                      <td colspan="2" v-if="item['detail_display']" style="font-weight: 500; opacity: 0.8;">{{ item["description"] }}</td>
                    </tr>
                    <!-- event detail -->
                  </table>
                </button>
                <button v-if="this.day_select < item['end_date']" class="calendar-detail-bg"
                  :style="'background-color:'+item['color']"
                  v-on:click.right="TogglePopup('editTrigger', $event, item)"
                  v-on:click.left="handlefilterEvent(item)">
                  <table class="calendar-table">
                    <tr><td style="width: 110px; vertical-align: text-top">{{ item["start_time"] }}-00:00</td>
                      <td>{{ item["name"] }}</td></tr>
                    <!-- event detail -->
                    <tr v-if="item['detail_display']" style="font-weight: 500; opacity: 0.8;">
                      <td colspan="2">
                        <table style="line-height: 18px">
                          <tr v-if="item['event_owner'] != ''"><td>From:</td><td>{{ item["event_owner"] }}</td></tr>
                          <tr><td style="width: 110px;">Tag:</td><td>{{ item['tag'] }}</td></tr>
                          <tr><td>Start:</td><td>{{ new Date(item["start_date"]).toLocaleDateString("en-GB") }} {{ item["start_time"] }}</td></tr>
                          <tr><td>End:</td><td>{{ new Date(item["end_date"]).toLocaleDateString("en-GB") }} {{ item["end_time"] }}</td></tr>
                        </table>
                      </td>
                    </tr>
                    <tr v-if="item['detail_display']">
                      <td colspan="2" v-if="item['detail_display']" style="font-weight: 500; opacity: 0.8;">{{ item["description"] }}</td>
                    </tr>
                    <!-- event detail -->
                  </table>
                </button>
                <button colspan="2" v-if="item['start_date'] == item['end_date']" class="calendar-detail-bg"
                  :style="'background-color:'+item['color']"
                  v-on:click.right="TogglePopup('editTrigger', $event, item)"
                  v-on:click.left="handlefilterEvent(item)">
                  <table class="calendar-table">
                    <tr><td style="width: 110px; ;vertical-align: text-top">{{ item["start_time"] }}-{{ item["end_time"] }}</td>
                      <td>{{ item["name"] }}</td></tr>
                    <!-- event detail -->
                    <tr v-if="item['detail_display']" style="font-weight: 500; opacity: 0.8;">
                      <td colspan="2">
                        <table style="line-height: 18px">
                          <tr v-if="item['event_owner'] != ''"><td>From:</td><td>{{ item["event_owner"] }}</td></tr>
                          <tr><td style="width: 110px;">Tag:</td><td>{{ item['tag'] }}</td></tr>
                          <tr><td>Start:</td><td>{{ new Date(item["start_date"]).toLocaleDateString("en-GB") }} {{ item["start_time"] }}</td></tr>
                          <tr><td>End:</td><td>{{ new Date(item["end_date"]).toLocaleDateString("en-GB") }} {{ item["end_time"] }}</td></tr>
                        </table>
                      </td>
                    </tr>
                    <tr v-if="item['detail_display']">
                      <td colspan="2" v-if="item['detail_display']" style="font-weight: 500; opacity: 0.8;">{{ item["description"] }}</td>
                    </tr>
                    <!-- event detail -->
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
        <button v-if="(this.token!='') && (this.user_name == this.calendar_slug)" class="app-button-tp"
          style="color: rgba(255, 255, 255, 0.8); font-size: 20px;"
          v-on:click.left="TogglePopup('sidebarTrigger', $event)">Manage View</button>
        <div v-else style="padding: 14px;"></div>
      </div>
      <!-- side bar footer -->

      <!-- Tag filters -->
      <div style="text-align: center;" v-if="popupTriggers.sidebarTrigger">
        <div class='calendar-sidebar' :style="'background-color:'+app_colors[this.color_theme['name']]['sub-1']">
          <div style="position: absolute; overflow-x: hidden; 
            top: 0px; bottom: 140px; color; width: 95%;">
            
            <!-- My Tag filters -->
            <p style="font-size: 20px; text-align: left; padding-left: 20px;">My Tags</p>
            <hr class="calendar-hr">
            <div class="filter-tag-bg">
              <div style="padding: 5px 0px 5px 0" v-for="tag_text in this.my_tag_list" :key="tag_text">
                <input v-if="this.tag_status['my_tag'][tag_text]" type="checkbox" v-bind:id="tag_text" 
                  v-on:click.left="handlefiltertag(tag_text)" checked>
                <input v-else type="checkbox" v-bind:id="tag_text" v-on:click.left="handlefiltertag(tag_text)">
                <label :style="'color:'+tag_colors[this.color_tag[tag_text]]"> {{ tag_text }} </label><br>
              </div>
            </div>
            <!-- My Tag filters -->

            <!-- Follow Tag filters -->
            <p style="font-size: 20px; text-align: left; padding-left: 20px;">Follow</p>
            <hr class="calendar-hr">
            <div class="filter-tag-bg" >
              <div style="padding: 5px 0px 5px 0" v-for="tag_text in this.follow_name_list" :key="tag_text">
                <input v-if="this.tag_status['follow_id'][Object.keys(this.follow_list).find(key => this.follow_list[key] == tag_text)]" type="checkbox" v-bind:id="tag_text" 
                  v-on:click.left="handlefiltertag(Object.keys(this.follow_list).find(key => this.follow_list[key] == tag_text))" checked>
                <input v-else type="checkbox" v-bind:id="tag_text" v-on:click.left="handlefiltertag(Object.keys(this.follow_list).find(key => this.follow_list[key] == tag_text))">
                <label :style="'max-height: 20%; color:'+app_colors[this.color_theme['type']]['main']"> {{ tag_text }} </label><br>
              </div>
            </div>
            <!-- Follow Tag filters -->

          </div>
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
            <EditRemove :popup="popupTriggers.editTrigger" :detail="popupTriggers.select_event" 
              :color_theme="this.color_theme" :color_tag="this.color_tag" @closed="swap"/>
      </div>


        <!-- <button class="app-button-main" v-on:click.left="TogglePopup('editTrigger', $event)">Edit</button>
        <button class="app-button-gray" v-on:click.left="TogglePopup('editTrigger', $event)">Delete</button> -->
    </div>
    <!-- edit event -->

    <FullCalendar class="calendar-app-main" :options="calendarOptions" :color_theme="this.color_theme" 
      :style="'color:'+app_colors[this.color_theme['type']]['main-0']">
      <template v-slot:eventContent="arg">
        <b>{{ arg.timeText }}</b>
        <i>{{ arg.event.title }}</i>
      </template>
    </FullCalendar>

    <!-- show tags -->
    <div style="font-size: 15px; left: 27% ;position: fixed; width: 71%; height: 45px; overflow-x: hidden;">
      <div v-if="(this.token!='') && (this.user_name == this.calendar_slug)">
        <div style="display: inline-block; padding-top: 8px;" v-for="tag_text in this.my_tag_list" :key="tag_text">
          <label :style="'margin-right: 15px; padding: 2px 10px 2px 10px; border-radius: 8px; color: white; background-color:'
            +tag_colors[this.color_tag[tag_text]]" v-if="this.tag_status['my_tag'][tag_text]"> {{ tag_text }} </label><br>
        </div>
        <div style="display: inline-block; padding-top: 8px;" v-for="tag_text in this.follow_name_list" :key="tag_text">
          <label :style="'margin-right: 15px; padding: 2px 10px 2px 10px; border-radius: 8px; color:'+
            app_colors[this.color_theme['type']]['main-0']+'; background-color: rgba(200, 200, 200, 0.6)'"
            v-if="this.tag_status['follow_id'][Object.keys(this.follow_list).find(key => this.follow_list[key] == tag_text)]"> {{ tag_text }} </label><br>
        </div>
      </div>
      <div v-else>
        <div style="display: inline-block; padding-top: 8px;" v-for="tag_text in this.public_tag" :key="tag_text">
          <label :style="'margin-right: 15px; padding: 2px 10px 2px 10px; border-radius: 8px; color:'+
            app_colors[this.color_theme['type']]['main-0']+'; background-color: rgba(200, 200, 200, 0.6)'"
            > {{ tag_text }} </label><br>
        </div>
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
  background-color: rgba(220, 220, 220, 0.5);
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
  -webkit-text-stroke: 0.4px rgba(0, 0, 0, 0.5);
  font-weight: 550;
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
