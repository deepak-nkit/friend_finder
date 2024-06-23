<script lang="ts">

  import type { PageData } from "./$types";
    import UserBox from "./userBox.svelte";
  import userBox from './userBox.svelte'

  /** @type {import('./$types').PageData} */
  export let data: PageData;

</script>

<br />
<div class="nav">
  <h1>Hello User</h1>
</div>

<form method="POST" action="?/logout">
  <div class="logout">
    <button type="submit">Logut</button>
  </div>
</form>



<!-- {#each data.suggestion as suggest} -->
  <!-- <div class="suggestion"> -->
    <!-- <div class="profile"> -->
      <!-- <h5>Name</h5> -->
    <!-- </div> -->
    <!-- <div class="data"> -->
      <!-- <h3>UserName : {suggest.username}</h3> -->
      <!-- <h4>Joined: {suggest.days_age} Days Ago</h4> -->
      <!-- <h4>Topics: {suggest.topic}</h4> -->
    <!-- </div> -->
  <!-- </div> -->
<!-- {/each} -->

{#each data.suggestion as suggest}
      <UserBox username = {suggest.username}  days_ago = {suggest.days_ago}  topics = {suggest.topic}></UserBox> 
{/each}

