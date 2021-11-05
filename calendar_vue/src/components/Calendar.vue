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
      today.setHours(0, 0, 0)
      this.day_select = today

      this.calendarOptions.events.forEach(elements => {
        let event = this.convertEventDateTime(elements)
        if((event["start_date"] <= today) && (today <= event["end_date"])){
          // console.log(event)
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
      select.setHours(0, 0, 0)
      this.day_select = select

      this.calendarOptions.events.forEach(elements => {
        let event = this.convertEventDateTime(elements)
        if((event["start_date"] <= select) && (select <= event["end_date"])){
          // console.log(event)
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
      let start_date = new Date(events.start.substring(0, 10) + " 00:00:00")
      let end_date = new Date(events.end.substring(0, 10) + " 00:00:00")
      let start_time = events.start.substring(11, 16)
      let end_time = events.end.substring(11, 16)
      let allday = false

      let start_date_check = events.start.substring(0, 10).replace('-','')
      let end_date_check = events.end.substring(0, 10).replace('-','')

      if ((start_date < this.day_select) && (this.day_select < end_date)){
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
    </header>
    <div class='calendar-sidebar'>
      <EventDetails>
        <h1>{{ String(this.day_select).substring(0, 15) }}</h1>
        <div v-for="item in this.event_details">
          <div v-if="item['allday']">
            <p>allday</p>
            <p>{{ item["name"] }}</p>
          </div>
        </div>
        <div v-for="item in this.event_details">
          <div v-if="!item['allday']">
            <div v-if="(item['start_date'] < this.day_select)">
              <p>00:00 {{ item["end_time"] }} {{ item["name"] }}</p>
            </div>
            <div v-else-if="this.day_select < item['end_date']">
              <p>{{ item["start_time"] }} 00:00 {{ item["name"] }}</p>
            </div>
            <div v-else>
              <p>{{ item["start_time"] }} {{ item["end_time"] }} {{ item["name"] }}</p>
            </div>
          </div>
          <!-- <p>{{ item["end_date"].getTime() }}</p> -->

            <!-- <p>{{ item }}</p>
            <p>{{ item[1].substring(11, 19) + " " + item[1].substring(0, 10) }}</p>

            <p>{{ new Date(item[2].substring(0, 10) + " " + item[2].substring(11, 19)) }}</p>
            <h1>{{ item[1] }}</h1>

            <p>from {{ item[1] }}</p>
            <p>to {{ item[2] }}</p>

            <h3>Tag </h3> <p class="app-details"> {{ item[4] }} </p>

            <h3>Description</h3>
            <p class="app-details">{{ item[3] }}</p> -->
        </div>

        <p v-if="this.event_details.length==0">
          <h1>No event found on this day.</h1>
          <h3>Sorry I'm Afriad you are sociopathy. What did you waiting! Try create new events now.</h3>

        </p>


        <!-- <h1>{{ event_details[0] }}</h1>
        <div class="app-details">
          <p>from {{ event_details[1] }}</p>
          <p>to {{ event_details[2] }}</p>
        </div>
        <div v-if="event_details[3] != ''">
          <h3>Description</h3>
          <p class="app-details">{{ event_details[3] }}</p>
        </div>
        <div class="calendar-sidebar-footer">
          <button class="app-button-main" @click="this.modalActive = !this.modalActive"
            type="button" name="button">Done</button>
        </div> -->
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
  width: 20%; /* Set the width of the sidebar */
  position: fixed; /* Fixed Sidebar (stay in place on scroll) */
  z-index: 1; /* Stay on top */
  top: 0; /* Stay at the top */
  left: 0;
  overflow-x: hidden; /* Disable horizontal scroll */
  margin-top: 65px;
  padding: 10px 40px 10px 40px;
  font-size: 20px;
}
.calendar-sidebar-footer {
  position: fixed;
  bottom: 5%;
  left: 10%;
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
