<template>
  <div id="draftView" v-if="renderComponent">
    <br>
      <form @submit.prevent="postPlayers">
        <Dropdowns
        :options="managerList.filter(c => c.teamName != null)"
        name="mangers"
        v-model="Manager"
        positionName="Choose Manager">
        </Dropdowns>
        <br>
        <br>
        <Dropdowns 
        :options="playerList.filter(c => c.element_type == 1)"
        name="goalkeeper"
        v-model="GK"
        positionName="Choose Goalkeeper">
        </Dropdowns>
        <!-- {{GK}} -->
        <br>
        <Dropdowns 
        :options="playerList.filter(c => c.element_type == 2)"
        v-model="DF1"
        v-on:input="updatePlayer"
        positionName="Choose Defender 1">
        </Dropdowns>
        <!-- {{DF1}} -->
        <br>
        <Dropdowns 
        :options="playerList.filter(c => c.element_type == 2)"
        v-model="DF2"
        v-on:input="updatePlayer"
        positionName="Choose Defender 2"/>
        <br>
        <Dropdowns
        :options="playerList.filter(c => c.element_type == 3)"
        v-model="MF1"
        positionName="Choose Midfielder 1"/>
        <br>   
        <Dropdowns 
        :options="playerList.filter(c => c.element_type == 3)"
        v-model="MF2"
        positionName="Choose Midfielder 2"/>
        <br>  
        <Dropdowns 
        :options="playerList.filter(c => c.element_type == 4)"
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
import Dropdowns from '../components/Dropdowns.vue'

export default {
  name: 'app',
  components: {
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
        Manager: {},
        renderComponent: true,
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
      axios.post("http://127.0.0.1:5000/draftplayers",playerData)
          .then(res => console.log(res))
          .then(res => this.forceReRender())
          .then(res => this.getPlayerData())
          .catch(err => console.log(err));
    },
    updatePlayer(playerData){
        console.log(playerData.id)
    },
    getPlayerData(){
      axios.get("http://127.0.0.1:5000/players")
          .then(res => this.playerList = res.data)
          .catch(err => console.log(err));
      axios.get("http://127.0.0.1:5000/managers")
          .then(res => this.managerList = res.data)
          .catch(err => console.log(err));
    },
    forceReRender(){
      console.log('rerendering')
      this.renderComponent = false;
      this.$nextTick(()=>{
        this.renderComponent=true;
      }

      )
    }
  },
    created() {
      this.getPlayerData();
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