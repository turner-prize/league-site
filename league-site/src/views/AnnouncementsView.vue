<template>
  <div id="announcementsView">
    <Announcements v-on:send-announcement="sendAnnouncement" />
    <br>
      <form @submit="postPlayers">
        <Dropdowns 
        :playerList="playerList.filter(c => c.element_type == 1)"
        v-on:update-player="updatePlayer"
        positionName="Choose Goalkeeper">
        </Dropdowns>
        <br>
        <Dropdowns 
        :playerList="playerList.filter(c => c.element_type == 2)"
        v-on:update-player="updatePlayer"
        positionName="Choose Defender 1">
        </Dropdowns>
        <br>
        <!-- <Dropdowns v-bind:playerList="playerList.filter(c => c.element_type == 2)"
        v-on:update-player="updatePlayer"
        positionName="Choose Defender 2"/>
        <br>
        <Dropdowns v-bind:playerList="playerList.filter(c => c.element_type == 3)"
        v-on:update-player="updatePlayer"
        positionName="Choose Midfielder 2"/>
        <br>   
        <Dropdowns v-bind:playerList="playerList.filter(c => c.element_type == 3)"
        v-on:update-player="updatePlayer"
        positionName="Choose Midfielder 2"/>
        <br>  
        <Dropdowns v-bind:playerList="playerList.filter(c => c.element_type == 4)"
        v-on:update-player="updatePlayer"
        positionName="Choose Forward"/> -->
      <br>
      <br>
      <br>
      <input type="submit" value="Submit" class="btn">
    </form>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
  </div>
</template>

<script>
import axios from 'axios'
import Announcements from '../components/Announcements.vue'
import Dropdowns from '../components/Dropdowns.vue'

export default {
  name: 'app',
  components: {
    Announcements,
    Dropdowns
  },
  data(){
    return{
      playerList: [],
    }
  },
  methods:{
    sendAnnouncement(msg){
      console.log(msg);
    },
    updatePlayer(playerData){
      this.playerValue = playerData.first_name
      console.log(this.playerValue)
      return this.playerValue
    },
    postPlayers(){
      console.log('hiya');
    }
  },
    created() {
      axios.get("http://127.0.0.1:5000/players")
          .then(res => this.playerList = res.data)
          .catch(err => console.log(err));
    }
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