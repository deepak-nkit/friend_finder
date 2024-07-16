<script lang="ts">
  import { page } from "$app/stores";

  export let data;
  $: current_user = $page.params["username"];
  $: user_names = data.inbox_users.map((x) => x.user.username);
  $: is_extra_user = current_user !== undefined && !user_names.includes(current_user);
</script>

<div class="flex h-[85dvh] flex-row gap-5 items-stretch ">
  <ul class="menu bg-base-200 w-56 rounded h-full gap-3">
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

