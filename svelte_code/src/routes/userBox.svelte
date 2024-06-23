<script lang="ts">
  export let username: String;
  export let days_ago: Date;
  export let topics: String[];
</script>

<div class="main">
  <div class="suggestion">
    <div class="profile">
      <h5>Name</h5>
    </div>
    <div class="data">
      <h3>UserName : {username}</h3>
      <h4>Joined: {days_ago} Days Ago</h4>
      <h4>Topics: {topics}</h4>
    </div>
  </div>
</div>

<style>
  /*
  .main{
    width:100vh;
    padding:10px;
  }
  */

  .suggestion {
    border: 2px solid grey;
    display: flex;
    justify-content: space-evenly;
    flex-direction: column;
    width: 40vw;
    margin: 10px;
    padding: 30px;
  }
</style>
