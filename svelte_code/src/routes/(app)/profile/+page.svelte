<script lang="ts">
    import { Pencil } from "lucide-svelte";
  import UserTileBig from "../UserTileBig.svelte";
  import type { PageData } from "./$types";
  import Map from "../component/map.svelte";

  export let data: PageData;
</script>

<UserTileBig user_info={data.self_profile} show_email={true} />

<div class="flex w-full justify-center">
  <a class="btn btn-primary" href="/profile/edit"> <Pencil size={16} /> Edit </a>
</div>

<div class="w-3">
  <Map />
</div>
