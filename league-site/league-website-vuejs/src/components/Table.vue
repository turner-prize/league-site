<template>
<div>
  <v-data-table
    :headers="headers"
    :items="this.tableData"
    :items-per-page="5"
    :sort-by="['points','playerScore']"
    :sort-desc="['true','true']"
    class="elevation-1"
  ></v-data-table>
</div>
</template>

<script>
export default {
    name: "Table",
    props:['tableData'],
    data() {
        return {
            headers:[
                {text: 'id', value:'id'},
                {text: 'manager', value:'manager'},
                {text: 'playerScore', value:'playerScore'},
                {text: 'points', value:'points'},
                {text: 'team', value:'team'},
            ],
            items:[],
        }
    },
  }
</script>

<style scoped>

div{
    width: 70%;
    margin: 0 auto;
}


</style>
