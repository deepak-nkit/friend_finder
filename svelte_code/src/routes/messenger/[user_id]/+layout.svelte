<script>
</script>
<div class="container">
  <div>
    <p>message: {message}</p>
  </div>
  <div class="message_box">
    <textarea placeholder="Type message" class="message"></textarea>
    <button type="submit" >send</button>
  </div>
  <slot />
</div>

<style>

  :global(body){
    padding:0;
    margin:0;
    background-colour:#cb5f5f;
    color:white;
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
