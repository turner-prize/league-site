<template>
  <div id="app">
    <Table v-bind:tableData="tableData" />
  </div>
</template>

<script>
import Table from '../components/Table.vue'
import axios from 'axios'

export default {
  name: 'app',
  components: {
    Table,
  },
  data() {
    return {
        tableData: [],
      }
  },
  created() {
      console.log('created');
      axios.get("http://127.0.0.1:5000/table")
          .then(res => this.tableData = res.data)
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