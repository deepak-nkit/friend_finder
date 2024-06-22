<script lang='ts'>
    import type { PageData } from "./$types";

	/** @type {import('./$types').PageData} */
	export let data: PageData;
	
</script>

<form method="POST" action="?/logout">
  <div class="logout">
    <button type="submit">Logut</button>
  </div>
</form>

<div class="nav">
  <h1>Hello User</h1>
</div>
{JSON.stringify(data)}
