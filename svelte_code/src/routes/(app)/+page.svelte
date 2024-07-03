<script lang="ts">
  import type { PageData, ActionData } from "./$types";
  import UserTile from "./userTile.svelte";

  export let data: PageData;
</script>

<div class="gap-8 flex flex-col items-center">
  <span class="text-5xl font-normal">
    Hello <span class="">@{data.user_profile.user.username}</span>
  </span>
  <div class="flex flex-wrap justify-around gap-y-10 w-full">
    {#each data.suggestions as suggest}
      <UserTile user_info={suggest}></UserTile>
    {/each}
  </div>
</div>
