<template>
  <div>
    <body class="app-body">
      <router-view/>
    </body>
  </div>
</template>

<script>
import EventCreate from './components/EventCreate'
export default {
  components: {
    EventCreate
  }
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