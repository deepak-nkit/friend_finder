<script lang="ts">

  import type { PageData } from "./$types";
    import UserBox from "./userBox.svelte";

  import Home from './home.svelte'
  /** @type {import('./$types').PageData} */
  export let data: PageData;

</script>

<Home></Home>
<br />
<div class="nav">
  <h1>Hello User</h1>
</div>

<!-- <form method="POST" action="?/logout"> -->
  <!-- <div class="logout"> -->
    <!-- <button type="submit">Logut</button> -->
  <!-- </div> -->
<!-- </form> -->

{#each data.suggestion as suggest}
      <a href={`/user/${suggest.username}`}>
      <UserBox username = {suggest.username}  days_ago = {suggest.days_ago}  topics = {suggest.topic}></UserBox> 
      </a>
{/each}

<style>
  a {
    text-decoration: none;
    color: black;
  }
</style>
