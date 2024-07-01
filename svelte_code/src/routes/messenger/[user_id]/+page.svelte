<script>
  /** @type {import('./$types').PageData} */
  export let data; // layout.server + page.server
</script>

<div class="container">
  {#each data.data.message as msg}
    <div class="message_shows">
      <p>id:{msg.sent_by} message: {msg.message}</p>
      <br>
    </div>
  {/each}
  <div class="message_box">
    <form action="?/send" method="post" >
      <textarea placeholder="Type message" name="message"></textarea>
      <button type="submit" >send</button>
    </form>
  </div>
</div>

<style>
  .home {
    border: 1px solid gray;
    color: black;
  }
  .container {
    height: 100vh;
    display: flex;
  }
  .message_shows p {
    color: black;
  }

  .message {
    text-align: center;
    font-size: 20xp;
  }
</style>
