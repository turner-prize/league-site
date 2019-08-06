<template>
<div>
  <v-data-table
    :headers="headers"
    :pagination.sync="pagination"
    :items="this.draftBoardData.filter(c => c.teamName != null)"
    :items-per-page="10"
    :disable-sort="true"
  ></v-data-table>
</div>
</template>

<script>
export default {
    name: "draftboard",
    props:['draftBoardData'],
    data() {
        return {
            headers:[
                {text: 'Draft Pick', value:'draftPick',width: "10%"},
                {text: 'Team', value:'teamName',width: "10%", align: 'center'},
                {text: 'GK', value:'gk',align: 'left'},
                {text: 'DF1', value:'df1',align: 'left'},
                {text: 'DF2', value:'df2',align: 'left'},
                {text: 'MF1', value:'mf1',align: 'left'},
                {text: 'MF2', value:'mf2',align: 'left'},
                {text: 'FWD', value:'fwd',align: 'left'},
            ],
            items:[],
        }
    },
    created(){
        console.log('here')
    }
  }
</script>

<style scoped>

div{
    width: 90%;
    margin: 0 auto;
}


</style>
