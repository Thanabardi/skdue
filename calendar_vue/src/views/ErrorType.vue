<template>
<body>
    <div class="Home">
        <ErrorHandle />
    </div>
</body>
</template>



<script>
import ErrorHandle from '../components/ErrorHandle.vue'

export default {
  name: 'Home',
  components: {
    ErrorHandle
  },
}
</script>