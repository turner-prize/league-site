<template>
  <div class="announcements">
    <div class = "title">
    Message:
    </div>
    <div class = "announcementForm">
      <form @submit.prevent="sendAnnouncement">
        <div class="accouncementText">
          <textarea type="text" v-model="msg" name="msg"></textarea>
        </div>
        <div class = "accouncementSubmit">
        <input type="submit" value="Submit" class="button">
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Announcements',
  data(){
    return{
      msg: ''
    }
  },
  methods: {
    sendAnnouncement(){
      this.$emit('send-announcement',this.msg);
      this.msg = '';
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.announcements {
  width: 300px;
  border-radius: 5px;
  /*background-color: #f2f2f2;*/
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  margin: 0 auto;
}

textarea[type=text], select {
  height: 100px;
  width:100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input[type=submit] {
  background-color: #4CAF50;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type=submit]:hover {
  background-color: #45a049;
}
</style>
