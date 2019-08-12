
<template>
  <div class="small">
    <line-chart :chart-data="datacollection" :options="options"></line-chart>
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
        datacollection: {},
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
      axios.get("http://127.0.0.1:5000/tablehistory")
          .then(res => this.datacollection = res.data)
          .catch(err => console.log(err));
    },
  }
</script>

<style>
  .small {
    max-width: 600px;
    margin:  150px auto;
  }
</style>