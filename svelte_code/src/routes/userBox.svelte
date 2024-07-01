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
    <form method="post"  action="/message" >
      <textarea name="message" placeholder="Type Message" class="message" ></textarea>
      <button type="submit">Send</button>
    </form>
  </div>
</div>

<style>
  .main:hover {
    background-color: #fafafa;
  }
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
  .message{
    align-items: center;
    width:300px;
    height: 50px;
    color:black;
    font-weight: 400px;
    background-color: #c4c4c4;
    border: 1px solid black;
    border-radius:17px 17px;
    padding-left: 10px;
  }
</style>
