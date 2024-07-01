<script lang="ts">
  export let username: String;
  export let days_ago: Date;
  export let topics: String[];
  export let name: string | null;
  export let user_id: number;
  /** @type {import('./$types').ActionData} */
  export let submitted: Boolean;
</script>

<a href={`/user/${username}`}>
  <div class="main">
    <div class="suggestion">
      <div class="data">
        <h5>{name}</h5>
        <h3>UserName : {username}</h3>
        <h4>Joined: {days_ago} Days Ago</h4>
        <h4>Topics: {topics}</h4>
        <!-- <h4>user_id: {user_id}</h4> -->
      </div>
    </div>
  </div>
</a>

<div>
  {#if submitted}
    <button disabled>Sent</button>
  {:else}
    <form action="?/add_friend" method="POST">
      <input type="hidden" name="username" value={username} />
      <button type="submit">Add friend</button>
    </form>
  {/if}
</div>

<a href={`/messenger/${user_id}`}> <button> Chat </button></a>

<style>
  .main:hover {
    background-color: #fafafa;
  }
  .main {
    width: fit-content;
  }

  .suggestion {
    border: 2px solid grey;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    flex-direction: column;
    width: 500px;
    margin: 10px;
    padding: 30px;
  }
  .data {
    display: flex;
    align-items: center;
    flex-direction: column;
  }

  /*
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
  */
  a {
    text-decoration: none;
    color: black;
    width: max-content;
  }
</style>
