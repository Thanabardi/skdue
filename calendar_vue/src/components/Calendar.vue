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
        // selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        // select: this.handleDateSelect,
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
      event_response: {}, // data from response
      tag_status: {}, // a dict for which tag gonna show in calendar
      tag_list: [], // store all tag name
      event_details: [],
      modalActive: false,
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
    setCalendarEvents(data){
      let tag = data.tag
      this.tag_list = data.tag // check this line
      let all_event = data.event
      this.event_response = data
      console.log("RESPONSE", this.event_response)
      for (let t=0; t<tag.length; t++){
        // init tag status
        this.tag_status[tag[t]] = true;

        let d = all_event[tag[t]]
        
        this.calendar_events = d
        
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
      let title = prompt("Please enter a new title for your event"); //input the title name of event
      let calendarApi = selectInfo.view.calendar;
      calendarApi.unselect(); // clear date selection
      if (title) {
        // if use fill the input
        calendarApi.addEvent(
          {
          id: createEventId(),
          title,
          start: selectInfo.startStr,
          end: selectInfo.endStr,
          allDay: selectInfo.allDay,
          //color: 'red',
          //textColor: 'black',
        });
      }
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
    <header class="calendar-header">
      <h2><router-link class="app-button-tp" style="text-decoration: none;"
        to=/>Skdue</router-link></h2>
      <Search />
      <EventCreate />
    </header>
    <div class='calendar-sidebar'>
      <EventDetails v-show="modalActive">
        <h1>{{ event_details[0] }}</h1>
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
        </div>
      </EventDetails>

      <!-- Tag filter render -->
      <div v-for="tag_text in this.tag_list" :key="tag_text"> 
        <input class="flipswitch" type="checkbox" v-bind:id="tag_text" @click="handlefiltertag(tag_text)" checked>
        <label v-bind:for="tag_text"> {{ tag_text }} </label><br>
      </div>
      <!-- End filter-->
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
