<template>
  <div id="draftView">
    <br>
      <form @submit.prevent="postPlayers">
        <Dropdowns
        :playerList="managerList.filter(c => c.teamName != null)"
        name="mangers"
        v-model="Manager"
        positionName="Choose Manager">
        </Dropdowns>
        <br>
        <br>
        <Dropdowns 
        :playerList="playerList.filter(c => c.element_type == 1)"
        name="goalkeeper"
        v-model="GK"
        positionName="Choose Goalkeeper">
        </Dropdowns>
        <!-- {{GK}} -->
        <br>
        <Dropdowns 
        :playerList="playerList.filter(c => c.element_type == 2)"
        v-model="DF1"
        v-on:input="updatePlayer"
        positionName="Choose Defender 1">
        </Dropdowns>
        <!-- {{DF1}} -->
        <br>
        <Dropdowns v-bind:playerList="playerList.filter(c => c.element_type == 2)"
        v-model="DF2"
        v-on:input="updatePlayer"
        positionName="Choose Defender 2"/>
        <br>
        <Dropdowns v-bind:playerList="playerList.filter(c => c.element_type == 3)"
        v-model="MF1"
        positionName="Choose Midfielder 1"/>
        <br>   
        <Dropdowns v-bind:playerList="playerList.filter(c => c.element_type == 3)"
        v-model="MF2"
        positionName="Choose Midfielder 2"/>
        <br>  
        <Dropdowns v-bind:playerList="playerList.filter(c => c.element_type == 4)"
        v-model="FWD"
        positionName="Choose Forward"/>
      <br>
      <br>
      <br>
      <input type="submit" value="Submit" class="btn">
    </form>
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
      managerList:[],
      GK: {},
      DF1: {},
      DF2: {},
      MF1: {},
      MF2: {},
      FWD: {},
      Manager: {}

    }
  },
  methods:{
    sendAnnouncement(msg){
      console.log(msg);
    },
    postPlayers(){
      const playerData = {
          Manager:this.Manager,
          GK:this.GK,
          DF1:this.DF1,
          DF2:this.DF2,
          MF1:this.MF1,
          MF2:this.MF2,
          FWD:this.FWD
      }
      console.log(playerData)
      axios.post("http://127.0.0.1:5000/sendplayers",playerData)
          .then(res => console.log(res))
          .catch(err => console.log(err));
    },
    updatePlayer(playerData){
        console.log(playerData.id)
    }
  },
    created() {
      axios.get("http://127.0.0.1:5000/players")
          .then(res => this.playerList = res.data)
          .catch(err => console.log(err));
      axios.get("http://127.0.0.1:5000/managers")
          .then(res => this.managerList = res.data)
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