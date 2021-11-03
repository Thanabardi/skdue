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
    setTodayEvents(){
      this.event_details = []
      let today = new Date();
      let date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();

      let y_today = today.getFullYear()
      let m_today = (today.getMonth()+1)
      let d_today = today.getDate()

      //date.substring(5,7)
      //date.substring(8,10)

      this.calendarOptions.events.forEach(elements => {
          let start_y = elements.start.substring(0,4)
          let start_m = elements.start.substring(5,7)
          let start_d = elements.start.substring(8,10)

          let end_y = elements.end.substring(0,4)
          let end_m = elements.end.substring(5,7)
          let end_d = elements.end.substring(8,10)

          if((start_y <= y_today) && (y_today <=end_y) &&
              (start_m <= m_today) && (m_today <=end_m) &&
              (start_d <= d_today) && (d_today <=end_d)){


              var form_e = [elements.title, elements.start, elements.end, elements.description , elements.tag]
              this.event_details.push(form_e)
          }
      });
          console.log(this.calendarOptions.events.length)
          console.log('here')
          console.log(this.event_details)
    },
    setCalendarEvents(data){
      console.log(data.event)
      let tag = data.tag
      let all_event = data.event
      for (let t=0; t<tag.length; t++){
        let d = all_event[tag[t]]
        console.log(d)
        this.calendar_events = d
        console.log(this.calendar_events)
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
      console.log("slug =", calendar_slug)
      axios
        .get(`/api/v2/calendar/${calendar_slug}`)
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
      console.log(selectInfo.startStr)
      let y_select = selectInfo.startStr.substring(0,4)
      let m_select = selectInfo.startStr.substring(5,7)
      let d_select = selectInfo.startStr.substring(8,10)



      this.calendarOptions.events.forEach(elements => {
          let start_y = elements.start.substring(0,4)
          let start_m = elements.start.substring(5,7)
          let start_d = elements.start.substring(8,10)

          let end_y = elements.end.substring(0,4)
          let end_m = elements.end.substring(5,7)
          let end_d = elements.end.substring(8,10)

          if((start_y <= y_select) && (y_select <=end_y) &&
              (start_m <= m_select) && (m_select <=end_m) &&
              (start_d <= d_select) && (d_select <=end_d)){


              var form_e = [elements.title, elements.start, elements.end, elements.description , elements.tag]
              this.event_details.push(form_e)
          }
      });
          console.log(this.event_details)
    },
    handleEventClick(clickInfo) {
      this.calendar_events.forEach(elements => {
        if (elements.id == clickInfo.event.id){
          this.modalActive = true;
          let  start_date = elements.start_date.substring(11, 16) +
            ", " + elements.start_date.substring(0, 10)
          let  end_date = elements.end_date.substring(11, 16) +
            ", " + elements.start_date.substring(0, 10)
          this.event_details = [
            elements.name,
            start_date,
            end_date,
            elements.description
          ]
          return this.event_details
        }
      });
    },
    handleEvents(events) {
      this.currentEvents = events;
    },
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


        <p v-for="item in this.event_details">
            <h1>{{ item[0] }}</h1>

            <p>from {{ item[1] }}</p>
            <p>to {{ item[2] }}</p>

            <h3>Tag </h3> <p class="app-details"> {{ item[4] }} </p>

            <h3>Description</h3>
            <p class="app-details">{{ item[3] }}</p>
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
