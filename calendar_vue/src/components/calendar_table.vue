<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { INITIAL_EVENTS, createEventId } from './event-utils'
// import EventDetails from './EventDetails'
// import {ref} from 'vue'


export default {
  components: {
    EventDetails,
    FullCalendar // make the <FullCalendar> tag available
  },
  data: function() {
    return {
      calendarOptions: {
        plugins: [
          dayGridPlugin,
          timeGridPlugin,
          interactionPlugin // needed for dateClick
        ],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth' //,timeGridWeek,timeGridDay
        },
        initialView: 'dayGridMonth',
        initialEvents: INITIAL_EVENTS, // alternatively, use the `events` setting to fetch from a feed
        editable: true,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        select: this.handleDateSelect,
        eventClick: this.handleEventClick,
        eventsSet: this.handleEvents
        /* you can update a remote database when these fire:
        eventAdd:
        eventChange:
        eventRemove:
        */
      },
      currentEvents: [],
      event_details: [],
      modalActive: false
    }
  },
  // setup(){  //EventDetails
  // const modalActive = ref(false);
  // return {modalActive};
  // },
  methods: {
    handleWeekendsToggle() {
      this.calendarOptions.weekends = !this.calendarOptions.weekends // update a property
    },
    handleDateSelect(selectInfo) {
      let title = prompt('Please enter a new title for your event') //input the title name of event
      let calendarApi = selectInfo.view.calendar
      calendarApi.unselect() // clear date selection
      if (title) { // if use fill the input
        calendarApi.addEvent({
          id: createEventId(),
          title,
          start: selectInfo.startStr,
          end: selectInfo.endStr,
          allDay: selectInfo.allDay,
          //color: 'red',
          //textColor: 'black',
        }
      )
      }
    },
    handleEventClick(clickInfo) {
      //delete
      // if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
      //   clickInfo.event.remove()
      // }
      //debug
      // let calendarApi = clickInfo.view.calendar

      let event_details = [clickInfo.event.title, clickInfo.event.start, clickInfo.event.end]
      alert(event_details)
      // this.event_details = [clickInfo.event.title, clickInfo.event.start, clickInfo.event.end]
      // this.modalActive = true;



    },
    handleEvents(events) {
      this.currentEvents = events
    }
  }
}




</script>
<template>

  <!-- <EventDetails :modalActive="modalActive">
      <div class="modal-content">
        <h1>{{ event_details[0] }}</h1>
        <p>start date: {{ event_details[1] }}</p>
          <p>end date:{{ event_details[2] }}</p>
      </div>
  </EventDetails> -->



    <div class='demo-app'>
    <div class='demo-app-main'>
      <FullCalendar
        class='demo-app-calendar'
        :options='calendarOptions'
      >
        <template v-slot:eventContent='arg'>
          <b>{{ arg.timeText }}</b>
          <i>{{ arg.event.title }}</i>
        </template>
      </FullCalendar>
    </div>
  </div>

</template>



<style lang='css'>
/* h2 {
  margin: 0;
  font-size: 16px;
}
ul {
  margin: 0;
  padding: 0 0 0 1.5em;
}
li {
  margin: 1.5em 0;
  padding: 0;
}
b {
  margin-right: 3px;
}
.demo-app {
  display: flex;
  min-height: 100%;
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
}
.demo-app-main {
  flex-grow: 1;
  padding: 3em;
}
.fc {
  max-width: 1100px;
  margin: 0 auto;
} */
</style>
