<template>
    <div class="home">
        <GoogleCallback />
    </div>
</template>



<script>
import axios from 'axios'
import GoogleCallback from '../components/GoogleCallback.vue'

export default {
  name: 'Home',
  components: {
      GoogleCallback
  },
}
</script>