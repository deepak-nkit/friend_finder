<script lang="ts">
  import type { PageData } from "./$types";
  import UserBox from "./userBox.svelte";

  import Home from "./home.svelte";
  import Layout from "./+layout.svelte";
  /** @type {import('./$types').PageData} */
  export let data: PageData;
  export let form;
</script>

<div class="main">
  <Home></Home>
  <br />
  <div class="nav">
    <h1>Hello User</h1>
  </div>

  {#each data.suggestion as suggest}
    <UserBox
      name={suggest.name}
      username={suggest.username}
      days_ago={suggest.days_ago}
      topics={suggest.topic}
      user_id={suggest.user_id}
      submitted={Boolean(form?.success)}
    ></UserBox>
  {/each}
</div>

<style>
  .nav {
    width: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
