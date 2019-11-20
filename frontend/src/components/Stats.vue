
<template>
  <div class="small">
    <line-chart :chart-data="data" :options="options" :width="1500" :height="700"></line-chart>
  </div>
</template>

<script>
  import LineChart from './LineChart.js'
  import axios from 'axios'

  export default {
    components: {
      LineChart
    },
    data () {
      return {
        data: {},
        options:{
          legend: { display: true },
          title: {
            display: true,
            text: 'League Table over Time'
          },
          scales:{
            yAxes: [{
              scaleLabel:{
                display: true,
                labelString: 'Position'
              },
              ticks: {
                reverse: true,
                stepSize: 1,
                min:1,
                max:10
              }
            }],
            xAxes: [{
              scaleLabel:{
                display: true,
                labelString: 'Gameweek'
              }

            }]
          }

        }
      }
    },
    created() {
      axios.get("http://localhost:3000/api/tablehistory")
          .then(res => this.data = res.data['data'])
          .catch(err => console.log(err));
    },
  }
</script>

<style scoped>
</style>