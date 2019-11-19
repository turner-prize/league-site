<template>
  <div id="app">
    <draftboard v-bind:draftBoardData="draftBoardData" />
    <form @submit.prevent="postPlayers">
        <Dropdowns
        :options="playerList.filter(c => c.teamName != null)"
        name="mangers"
        v-model="Manager"
        positionName="Choose Manager">
        </Dropdowns>
        <input type="submit" value="Submit" class="btn">
    </form>
  </div>
</template>

<script>
import draftboard from '../components/DraftBoard.vue'
import Dropdowns from '../components/Dropdowns.vue'
import axios from 'axios'

export default {
  name: 'app',
  components: {
    draftboard,
  },
  data() {
    return {
        draftBoardData: [],
      }
  },
  created() {
      console.log('created');
      axios.get("http://127.0.0.1:5000/draftboard")
          .then(res => this.draftBoardData = res.data)
          .catch(err => console.log(err));
      
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