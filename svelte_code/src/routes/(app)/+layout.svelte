<script lang="ts">
  import { CircleUserRound, LogOut, Send } from "lucide-svelte";

  let val = "";
  let timer: number | undefined;
  export let inputval = "";

   const debounce = (v: string) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      val = v;
      if (inputval.length > 1){
        finder();
      }
    }, 750);
  };

  export async function finder() {
    const response = await fetch(`/roll/?inputval=${encodeURIComponent(inputval)}`, {
      method: "GET",
      headers: {
        "content-type": "application/json",
      },
    });

    console.log("--------------------", response);
   user: await response.json();
  }
</script>

<nav class="navbar bg-base-100 shadow fixed top-0 z-10 bg-slate-300">
  <div class="flex-1">
    <a href="/" class="btn btn-ghost text-xl">Friend Finder</a>
  </div>

  <div class="flex gap-8">
    <div class=" flex-col form-control sm:max-w-50">
      <input
        type="text"
        placeholder="Search"
        class="input input-bordered"
        bind:value={inputval}
        on:keyup={(event) => debounce(event.key)}
      />
      <div class="flex-col">
        <p>{inputval}</p>
      </div>
    </div>

    <div class="flex-none gap-5 mr-8">
      <a href="/chat" class="btn btn-ghost btn-circle">
        <div class="indicator">
          <Send />
        </div>
      </a>
      <div class="dropdown dropdown-end">
        <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
          <CircleUserRound />
        </div>
        <ul
          tabindex="0"
          role="listbox"
          class="flex flex-col gap-2 dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-4 shadow items-stretch"
        >
          <li>
            <a href="/profile" class="btn btn-sm w-full btn-ghost"> Profile </a>
          </li>
          <li>
            <form method="POST" action="/login?/logout" class="w-full">
              <button class="btn btn-sm w-full btn-ghost" type="submit"
                >Logout</button
              >
            </form>
          </li>
        </ul>
      </div>
    </div>
  </div>
</nav>

<div class="pt-20 m-auto max-w-screen-lg md:px-5 px-2">
  <slot></slot>
</div>
