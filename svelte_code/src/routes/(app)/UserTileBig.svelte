<script lang="ts">
  import { formatDistance } from "date-fns";
  import type { Components } from "../../backend_openapi";
  import { Mail, MapPin, Star } from "lucide-svelte";

  export let user_info: Components.Schemas.UserWithTopics;

  export let show_email: boolean = false;
</script>

<div class="flex h-64 w-full items-center">
  <div class="h-full aspect-square">
    <img
      src="https://img.daisyui.com/images/stock/photo-1635805737707-575885ab0820.jpg"
      class="h-full w-full p-12 rounded-full aspect-square"
      alt="?"
    />
  </div>
  <div class="grow flex flex-col m-3">
    <div class="basis-0 grow flex gap-6 flex-col">
      <div class="flex flex-col gap-2">
        <h3 class="text-4xl font-bold hover:underline">
          @{user_info.user.username}
        </h3>
        <p class="text-md">
          Joined {formatDistance(user_info.user.joined_on, new Date())} ago
        </p>
      </div>
      <div class="flex flex-col gap-1">
        <p class="text-lg flex gap-2 items-center">
          <MapPin size={20} />
          {user_info.user.pincode}
        </p>
        <p class="text-lg flex gap-2 items-center">
          <Star size={20} />
          {user_info.topics.map((x) => x.name).join(" | ")}
        </p>
        {#if show_email}
          <p class="text-lg flex gap-2 items-center">
            <Mail size={20} />
            {user_info.user.email}
          </p>
        {/if}
      </div>
    </div>
  </div>
</div>
