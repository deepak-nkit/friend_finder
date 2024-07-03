<script lang="ts">
  import {
    MapPin,
    MessageSquare,
    Star,
    UserPlus,
    UserRoundCheck,
  } from "lucide-svelte";
  import type { PageData } from "./$types";
  import { formatDistance } from "date-fns";
  import UserTileBig from "../../UserTileBig.svelte";
  import { enhance } from "$app/forms";
  export let data: PageData;
  $: user_info = data.profile_data;
  $: href = `/user/${user_info.user.username}`;
</script>

<div class="flex flex-col gap-8">
  <UserTileBig {user_info} />
  <div class="flex flex-wrap gap-8">
    <a href="/chat/{user_info.user.username}" class="btn btn-outline btn-sm">
      <MessageSquare size={16} /> Chat
    </a>
    {#if !user_info.is_friend}
      <form method="POST" use:enhance action="?/add_friend">
        <input type="text" name="user_id" value={user_info.user.id} hidden />
        <button type="submit" class="btn btn-primary btn-sm h-fit">
          <UserPlus size={16} /> Add Friend
        </button>
      </form>
    {:else}
      <span class="btn btn-ghost disabled btn-sm h-fit text-green-900">
        <UserRoundCheck size={16} /> Friend
      </span>
    {/if}
  </div>
</div>
