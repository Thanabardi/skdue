<template>
  <div>
    <body class="app-body">
      <router-view/>
    </body>
  </div>
</template>

<script>
import EventCreate from './components/EventCreate'
import axios from 'axios'

export default {
  components: {
    EventCreate
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
        axios.defaults.headers.common['Authorization'] = ""
    }
  },
}
</script>

<style lang="scss">

.app-body {
  position: absolute;
  top: 20px;
  right: 0px;
  left: 0px;
}

</style>
