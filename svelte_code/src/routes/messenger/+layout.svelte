<script lang="ts">
  export let username:string
</script>

  <slot />
<div class="container">
  <div class="side_box">
    <div class="user_box">
      <img src="" alt="profile" class="profile" />
      <div class="username">Saini_saini</div>
    </div>
    <div class="tag">message</div>
    <div class="usernames">
      <p>{username}</p>
      <br>
    </div>
    <div class="content">
      <div class="message"></div>
    </div>
  </div>
</div>

<style>

  :global(body){
    padding:0;
    margin:0;
    background-colour:#cb5f5f;
  }
  .container{
    height: 100vh;
    display: flex;
  }
  .side_box{
    width:300px;
    display: flex;
    flex-direction: column;
    padding: 10px;
    background-color:#EDEDFF;
  }
  .user_box{
    display: flex;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid black;
  }

  .profile{
    height: 40px;
    width:40px;
    border-radius:50%;
    margin-right: 10px;
  }

  .username{
    font-size: 15px;
    font-weight:bold;
  }
   
  .main{
    display: flex;
    flex-direction: column; 
    align-items: center;
    justify-content: center;
    background-color:#a2b79f ;
    }
  .message{
    text-align: center;
    font-size:20xp;
  }

</style>
