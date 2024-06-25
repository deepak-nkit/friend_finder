<script lang="ts">
  import type { PageData } from "./$types";
  /** @type {import('./$types').PageData} */
  export let data: PageData;

  console.log(data)
</script>

<h2>It'z {data.username} </h2>
<div>
  <h5>UserId:{data.user_id}<h5>
 <h3>name: {data.name}</h3>
 <h3>username: {data.username}</h3>
 <h3>Joined : {data.joined}</h3>
 <h3>topics: {data.topics}</h3>
 <h3>email: {data.email}</h3>
 <h3>addrss: {data.address}</h3>
</div>

