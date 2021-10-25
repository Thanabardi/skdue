<template>
    <div class="calendar-detail">
        <!-- <h1>List of events</h1> -->
        <!-- <div v-for="e in calendar_events" v-bind:key="e.id">
            <h2>{{ e.name }}</h2>
            <p>{{ e.description }}</p>
            <p>{{ e.start_date }}</p>
            <p>{{ e.end_date }}</p>
            <router-link v-bind:to="e.get_absolute_url">View detail</router-link>
        </div> -->
        <Calendar />
    </div>
</template>

<script>
import Calendar from "../components/Calendar"
import axios from 'axios'

export default {
  name: 'Home',
  components: {
    Calendar,
  },
  data() {
      return {

      }
  },
  mounted() {

  },
  methods: {
    //   getCalendarEvents() {
    //       const calendar_slug = this.$route.params.calendar_slug

    //       axios
    //         .get(`/api/calendar/${calendar_slug}`)
    //         .then(response => {
    //             for(let i=0; i<response.data.length; i++) {
    //                 this.calendar_events.push(response.data[i])
    //             }

    //             // pass data
    //         })
    //         .catch(error => {
    //             console.log(error)
    //         })
    //   }
  }
}
</script>
