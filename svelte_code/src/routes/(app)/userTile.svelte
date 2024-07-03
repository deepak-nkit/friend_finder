<script lang="ts">
  import { MessageSquare, UserPlus, UserRoundCheck } from "lucide-svelte";
  import type { Components } from "../../backend_openapi";
  import { formatDistance } from "date-fns";
    import { enhance } from "$app/forms";

  export let user_info: Components.Schemas.UserWithTopics;

  let href = `/user/${user_info.user.username}`;
</script>

<div class="border rounded-2xl border-gray-300 shadow-sm flex sm:h-32 h-48 sm:w-96 w-84 sm:grow-0 grow">
  <a {href} class="h-full w-auto aspect-square flex-grow-0">
    <figure class="h-full w-full">
      <img
        src="https://img.daisyui.com/images/stock/photo-1635805737707-575885ab0820.jpg"
        class="h-full w-full p-5 rounded-full"
        alt="Movie"
      />
    </figure>
  </a>

  <div class="grow flex flex-col m-3">
    <a {href} class="basis-0 grow flex gap-2 flex-col">
      {#if user_info.user.name !== null}
        <h5>{user_info.user.name}</h5>
      {/if}
      <h3 class="text-lg font-bold hover:underline">
        @{user_info.user.username}
      </h3>
      <p class="text-sm">
        Joined {formatDistance(user_info.user.joined_on, new Date())} ago
      </p>
    </a>
    <!-- TODO: it overflows on small devices -->
    <div class=" basis-0 flex-grow-0 justify-end self-end flex flex-wrap gap-2">
      <a href="/chat/{user_info.user.username}" class="btn btn-ghost btn-sm">
        <MessageSquare size={16} /> Chat</a
      >
      {#if !user_info.is_friend}
        <form method="POST" use:enhance action="?/add_friend">
          <input type="text" name="user_id" value={user_info.user.id} hidden />
          <button type="submit" class="btn btn-ghost btn-sm h-fit text-sky-900">
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
</div>

<!-- <div class="card card-side bg-base-100 shadow-xl max-h-32 max-w-64"> -->
<!-- <figure> -->
<!-- <img -->
<!-- src="https://img.daisyui.com/images/stock/photo-1635805737707-575885ab0820.jpg" -->
<!-- alt="Movie" /> -->
<!-- </figure> -->
<!-- <div class="card-body"> -->
<!-- <h2 class="card-title">DS</h2> -->
<!-- <p>3 days ago</p> -->
<!-- <div class="card-actions justify-end"> -->
<!-- <button class="btn btn-primary">Chat</button> -->
<!-- </div> -->
<!-- </div> -->
<!-- </div> -->
