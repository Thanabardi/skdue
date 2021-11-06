<script>
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import EventCreate from './EventCreate'
import Search from './search'
import EventDetails from './EventDetails'
import {ref} from 'vue'
import axios from 'axios'
export default {
  components: {
    FullCalendar, // make the <FullCalendar> tag available
    Search,
    EventCreate
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
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth", //,timeGridWeek,timeGridDay
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
      event_details: [],
      modalActive: true,
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
  return {modalActive};
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
      let all_event = data.event
      for (let t=0; t<tag.length; t++){
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
          // console.log(this.calendarOptions.events[i])
        }
      }
    this.setTodayEvents();
    },
    getCalendarEvents() {
      const calendar_slug = this.$route.params.calendar_slug
      const calendar_type = this.$route.params.calendar_type

      console.log("TOKEN:", localStorage.token)

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
      });
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
    }
  },
};
</script>


<template>
  <div>
    <header class="calendar-header">
      <h2><router-link class="app-button-tp" style="text-decoration: none;"
        to=/>Skdue</router-link></h2>
      <Search />
      <EventCreate />
      <!-- Logout button -->
      <form @submit.prevent="logoutData" class="form-form">
        <button class="logout-button">Logout</button>
      </form>
      <!-- End logout -->
    </header>
    <div class='calendar-sidebar'>
      <EventDetails>
        <p style="line-height: 0px;">follow v-if plz hidden unless template will k-boom</p>
        <h2 style="text-align: center;">{{ this.day[new Date(this.day_select).getDay()] }}, 
          {{ new Date(this.day_select).getDate() }}
          {{ this.month[new Date(this.day_select).getMonth()] }}
          {{ new Date(this.day_select).getFullYear() }}
        </h2>
        <div style="overflow-x: hidden;height: 74%;">
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
                    <tr><td style="width: 105px;">00:00-{{ item["end_time"] }}</td>
                      <td>{{ item["name"] }}</td></tr>
                    <tr><td colspan="2" style="font-weight: 500; color: var(--black-light);">
                        {{ item["description"] }}</td></tr>
                    </table>
                  </div>
                  <div v-if="this.day_select < item['end_date']">
                    <table class="calendar-table">
                    <tr><td style="width: 105px;">{{ item["start_time"] }}-00:00</td>
                      <td>{{ item["name"] }}</td></tr>
                    <tr><td colspan="2" style="font-weight: 500; color: var(--black-light);">
                        {{ item["description"] }}</td></tr>
                    </table>
                  </div>
                  <div v-if="item['start_date'] == item['end_date']">
                    <table class="calendar-table">
                    <tr><td style="width: 105px;">{{ item["start_time"] }}-{{ item["end_time"] }}</td>
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
        <hr class="calendar-hr" style="position: absolute; bottom: 125px; left: 32px; width: 82%;">
        <div class="calendar-sidebar-footer">
          <button class="app-button-tp" @click="doSomething()"
            type="button" name="button" style="font-size: 20px; color: var(--white-op-1);">Manage View</button>
        </div>
      </EventDetails>
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

.calendar-header {

  background: var(--main-green);
  color: var(--main-green);
  font-size: 25px;
  font-weight: 500px;
  line-height: 0px;
  height: 65px;
  display: flex;
  justify-content: space-evenly;
  z-index: 5;
  position: fixed !important;
  top: 0px;
  left: 0px;
  right: 0px;
}
.calendar-sidebar {
  background: var(--main-green-light);
  color: var(--white);
  height: 100%; /* Full-height: remove this if you want "auto" height */
  width: 23%; /* Set the width of the sidebar */
  position: fixed; /* Fixed Sidebar (stay in place on scroll) */
  z-index: 1; /* Stay on top */
  top: 0; /* Stay at the top */
  left: 0;
  overflow-x: hidden; /* Disable horizontal scroll */
  margin-top: 65px;
  padding: 10px 10px 10px 10px;
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
  position: fixed;
  bottom: 2%;
  left: 9%;

}
.calendar-hr {
  border: 1px solid var(--white-op-2);
  width: 90%;
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
</style>
