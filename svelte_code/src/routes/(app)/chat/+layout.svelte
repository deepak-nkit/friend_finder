<script lang="ts">
  import { page } from "$app/stores";

  export let data;
  $: current_user = $page.params["username"];
  $: user_names = data.inbox_users.map((x) => x.user.username);
  $: is_extra_user = current_user !== undefined && !user_names.includes(current_user);
</script>

<div class="flex h-[85dvh] flex-row gap-5 items-stretch">
  <ul class="menu bg-base-200 w-56 rounded h-full">
    {#each data.inbox_users as user}
      <li>
        <a
          href="/chat/{user.user.username}"
          class:active={user.user.username === current_user}
        >
          {user.user.username}
        </a>
      </li>
    {/each}

    {#if is_extra_user}
      <li>
        <a href="/chat/{current_user}" class="active">
          {current_user}
        </a>
      </li>
    {/if}
  </ul>
  <div class="border border-slate-300 bg-base-200 grow p-2 rounded">
  <slot />
  </div>
</div>

<!-- <div class="container"> -->
<!-- <div class="side_box"> -->
<!-- <div class="user_box"> -->
<!-- <img src="" alt="profile" class="profile" /> -->
<!-- <div class="username">{data.sidebar_data.current_username}</div> -->
<!-- </div> -->
<!-- <div class="tag">message</div> -->
<!-- {#each data.sidebar_data.user as user} -->
<!-- <a href={`/chat/${user.user_id}`}> -->
<!-- <div class="usernames"> -->
<!-- <p>{user.username}</p> -->
<!-- <br /> -->
<!-- </div> -->
<!-- </a> -->
<!-- {/each} -->
<!-- </div> -->
<!-- <slot /> -->
<!-- </div> -->

<!-- <style> -->
<!-- .container { -->
<!-- height: 100vh; -->
<!-- display: flex; -->
<!-- } -->
<!-- .side_box { -->
<!-- width: 300px; -->
<!-- display: flex; -->
<!-- flex-direction: column; -->
<!-- padding: 10px; -->
<!-- background-color: rgb(243, 237, 229); -->
<!-- } -->
<!-- .user_box { -->
<!-- display: flex; -->
<!-- align-items: center; -->
<!-- padding: 10px; -->
<!-- border-bottom: 1px solid black; -->
<!-- } -->

<!-- .profile { -->
<!-- height: 40px; -->
<!-- width: 40px; -->
<!-- border-radius: 50%; -->
<!-- margin-right: 10px; -->
<!-- } -->

<!-- .username { -->
<!-- font-size: 15px; -->
<!-- font-weight: bold; -->
<!-- } -->
<!-- </style> -->
