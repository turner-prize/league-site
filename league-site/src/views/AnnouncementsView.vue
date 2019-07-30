<template>
  <div id="announcementsView">
    <Announcements v-on:send-announcement="sendAnnouncement" />
    <Dropdowns />
    <Stats />
  </div>
</template>

<script>
import Announcements from '../components/Announcements.vue'
import Dropdowns from '../components/Dropdowns.vue'

export default {
  name: 'app',
  components: {
    Announcements,
    Dropdowns
  },
  methods:{
    sendAnnouncement(msg){
      console.log(msg);
    },
  },
  }
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>