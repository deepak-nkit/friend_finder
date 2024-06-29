<script>
  /** @type {import('./$types').PageData} */
	export let data;

</script>

<div>
  <h2>username:{data.username}</h2>
  <h6>User_id:{data.user_id}</h6>
  <h2>email:{data.email}</h2>
  <h2>pincode:{data.pincode}</h2>
  <h3>Age : {data.days_ago}days ago</h3>
  <h3>Topics:{data.topics}</h3>
  {#if data.name}
    <h3>Name:{data.name}</h3>
  {/if}
  {#if data.Address}
    <h3>Address:{data.address}</h3>
  {/if}
  {#if data.contact}
    <h3>contact:{data.contact}</h3>
  {/if}
</div>

