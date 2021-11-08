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
import {ref} from 'vue'
import axios from 'axios'
export default {
  components: {
    FullCalendar, // make the <FullCalendar> tag available
    CalendarNavbar,
    Search,
    EventCreate,
    Follow,
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
        eventClick: this.handleEventClick,
        eventsSet: this.handleEvents,
        /* you can update a remote database when these fire:
        eventAdd:
        eventChange:
        eventRemove:
        */
      },
      currentEvents: [],
      calendar_events: [],
      event_in_selected_date: [], //added in iter4
      event_response: {}, // data from response
      tag_status: {}, // a dict for which tag gonna show in calendar
      tag_list: [], // store all tag name
      event_details: [],
      modalActive: true,
      token: "",
      day_select: "",
      day: ['Sunday','Monday','Tuesday','Wednesday',
        'Thursday','Friday','Saturday'],
      month: ['January','February','March','April',
        'May','June','July','August','September',
        'October','November','December'],
      dataLogout:{
        "status":"logout"
      }
    };
  },
  setup() {  //EventDetails
  let modalActive = ref(false);

  const popupTriggers = ref({
    buttonTrigger: false,
  });

  const TogglePopup = (trigger) => {
    popupTriggers.value[trigger] = !popupTriggers.value[trigger]
  }
  return {
    modalActive,
    popupTriggers,
    TogglePopup
  }
  },
  mounted() {
    this.getCalendarEvents()
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
            tag : d[i].tag_text
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
      axios
        .get(`/api/v2/${calendar_type}/${calendar_slug}`)
        .then(response => {
          console.log(response.data)
          this.setCalendarEvents(response.data)
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
    handleEventClick(clickInfo) {
      this.calendar_events.forEach(elements => {
        let event = this.convertEventDateTime(elements)
        if (elements.id == clickInfo.event.id){
          this.modalActive = true;
          // let  start_date = elements.start_date.substring(11, 16) +
          //   ", " + elements.start_date.substring(0, 10)
          // let  end_date = elements.end_date.substring(11, 16) +
          //   ", " + elements.start_date.substring(0, 10)
          // this.event_details = [
          //   elements.name,
          //   start_date,
          //   end_date,
          //   elements.description
          // ]
          this.event_details.push(event)
        }
      });
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
      return {
				"name" : events.title,
				"description" : events.description,
				"start_date" : start_date,
        "start_time" : start_time,
				"end_date" : end_date,
        "end_time" : end_time,
        "tag" : events.tag,
        "allday" : allday
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
  <div>
      <!-- <form @submit.prevent="logoutData" class="form-form">
        <button class="logout-button">Logout</button>
      </form> -->
    <CalendarNavbar />
    <div class='calendar-sidebar'>
      <EventDetails>

        <Follow />
        <h2 style="text-align: center;">{{ this.day[new Date(this.day_select).getDay()] }}
          {{ (this.day_select.substring(8, 10)) }}
          {{ this.month[new Date(this.day_select).getMonth()] }}
          {{ (this.day_select.substring(0, 4)) }}
        </h2>
        <div style="overflow-x: hidden; height: 76%;">
          <div v-if="this.event_details.length!=0">
            <p style="font-size: 18px; color: var(--white-op-1); text-align: center;">All-Day Event</p>
              <div v-for="item in this.event_details">
                  <div v-if="item['allday']">
                    <table class="calendar-table">
                    <!-- <td style="width: 105px; text-align: center;">All-Day</td> -->
                    <tr><td style="width: 1000px; text-align: center;">{{ item["name"] }}</td></tr>
                    <tr><td colspan="2" style="font-weight: 500; color: var(--black-light);">
                        {{ item["description"] }}</td></tr>
                    </table>
                  </div>
              </div>
              <hr class="calendar-hr">
              <div v-for="item in this.event_details">
                <div v-if="!item['allday']">
                  <div v-if="(item['start_date'] < this.day_select)">
                    <table class="calendar-table">
                    <tr><td style="width: 110px;">00:00-{{ item["end_time"] }}</td>
                      <td>{{ item["name"] }}</td></tr>
                    <tr><td colspan="2" style="font-weight: 500; color: var(--black-light);">
                        {{ item["description"] }}</td></tr>
                    </table>
                  </div>
                  <div v-if="this.day_select < item['end_date']">
                    <table class="calendar-table">
                    <tr><td style="width: 110px;">{{ item["start_time"] }}-00:00</td>
                      <td>{{ item["name"] }}</td></tr>
                    <tr><td colspan="2" style="font-weight: 500; color: var(--black-light);">
                        {{ item["description"] }}</td></tr>
                    </table>
                  </div>
                  <div v-if="item['start_date'] == item['end_date']">
                    <table class="calendar-table">
                    <tr><td style="width: 110px;">{{ item["start_time"] }}-{{ item["end_time"] }}</td>
                      <td>{{ item["name"] }}</td></tr>
                    <tr><td colspan="2" style="font-weight: 500; color: var(--black-light);">
                        {{ item["description"] }}</td></tr>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          <div v-else>
            <p style="font-size: 20px; color: var(--white-op); text-align: center;">
              You have no events scheduled today</p>
          </div>
        </div>

        <!-- <h1>{{ event_details[0] }}</h1>
        <div class="app-details">
          <p>from {{ event_details[1] }}</p>
          <p>to {{ event_details[2] }}</p>
        </div>
        <div v-if="event_details[3] != ''">
          <h3>Description</h3>
          <p class="app-details">{{ event_details[3] }}</p>
        </div> -->

        <div class="calendar-sidebar-footer">
          <hr class="calendar-hr">
          <!-- <button class="app-button-tp" @click="doSomething()"
            type="button" name="button" style="font-size: 20px; color: var(--white-op-1);">Manage View</button> -->
          <button v-if="(this.token!='') && (this.fs!='')" class="app-button-tp"
            style="font-size: 20px; color: var(--white-op-1);"
            @click="() => TogglePopup('buttonTrigger')">Manage View</button>
        </div>
      </EventDetails>
      <div style="text-align: center;" v-if="popupTriggers.buttonTrigger"
		  :TogglePopup="() => TogglePopup('buttonTrigger')">
        <div class="filter-tag-popup">
          <p style="font-size: 20px; color: var(--white-op-1); text-align: left; padding-left: 20px;">My Tags</p>
          <hr class="calendar-hr">
          <div class="filter-tag-bg" style="height: 20%;">
            <div style="padding: 5px 0px 5px 0" v-for="tag_text in this.tag_list" :key="tag_text">
              <input class="filter-tag" type="checkbox" v-bind:id="tag_text" @click="handlefiltertag(tag_text)" checked>
              <label v-bind:for="tag_text"> {{ tag_text }} </label><br>
            </div>
          </div>
          <p style="font-size: 20px; color: var(--white-op-1); text-align: left; padding-left: 20px;">Follow</p>
          <hr class="calendar-hr">
          <div class="filter-tag-bg" style="height: 41%;">
            <div style="padding: 5px 0px 5px 0" v-for="tag_text in this.tag_list" :key="tag_text">
              <input class="filter-tag" type="checkbox" v-bind:id="tag_text" @click="handlefiltertag(tag_text)" checked>
              <label v-bind:for="tag_text"> {{ tag_text }} </label><br>
            </div>
          </div>
          <div class="calendar-sidebar-footer">
            <hr class="calendar-hr">
            <button class="app-button-tp" @click="() => TogglePopup('buttonTrigger')"
              type="button" name="button" style="font-size: 20px; color: var(--white-op-1);">Back</button>
          </div>
        </div>
      </div>
    </div>

    <FullCalendar class="calendar-app-main" :options="calendarOptions">
      <template v-slot:eventContent="arg">
        <b>{{ arg.timeText }}</b>
        <i>{{ arg.event.title }}</i>
      </template>
    </FullCalendar>
  </div>
</template>


<style lang='scss' scoped>

@import './../assets/style.css';

.calendar-sidebar {
  background: var(--main-green-light);
  color: var(--white);
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
.calendar-table {
  background-color: var(--white-op-1);
  color: var(--black);
  border-collapse: collapse;
  padding: 5px;
  display: block;
  margin: 20px auto 20px auto;
  justify-items: center;
  width: 90%;
  border-radius: 8px;
}
.calendar-table td{
  font-size: 20px;
  padding-left: 5px;
  font-weight: 550;
  word-break: break-word;
  // text-align: center;
}
.calendar-sidebar-footer {
  position: absolute;
  bottom: 100px;
  width: 95%;
  text-align: center;

}
.calendar-hr {
  border: 1px solid var(--white-op-2);
  width: 90%;
}
.logout-button {
  background-color: #646464;
  border: none;
  color: var(--white);
  padding: 13px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 8px 2px;
  cursor: pointer;
}
.filter-tag {
  display: inline-block;
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
.filter-tag-popup {
  background: var(--main-green-light);
  color: var(--white);
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
.filter-tag-bg {
  background-color: var(--white-op-1);
  color: var(--black);
  padding: 10px 20px 10px 20px;
  display: block;
  margin: 20px auto 20px auto;
  text-align: left;
  width: 70%;
  border-radius: 8px;
  overflow-x: hidden;
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
