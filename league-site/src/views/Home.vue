<template>
  <div id="app">
    <Announcements v-on:send-announcement="sendAnnouncement" />
  </div>
</template>

<script>
import Announcements from '../components/Announcements.vue'
import axios from 'axios'

export default {
  name: 'app',
  components: {
    Announcements,
  },
  methods:{
    sendAnnouncement(msg){
      console.log(msg);
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
