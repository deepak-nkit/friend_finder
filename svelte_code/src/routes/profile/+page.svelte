<script>
  /** @type {import('./$types').PageData} */
	export let data;
</script>



<div class="profile_pic">
  <img src="https://i.pinimg.com/originals/a9/bc/a0/a9bca0b755b69a00e869053acac1eca6.png" alt="profile">
</div>

<div style="margin-top: 40px;">
  <h2>username: {data.username}</h2>
  <h6>User_id: {data.user_id}</h6>
  <h2>email: {data.email}</h2>
  <h2>pincode: {data.pincode}</h2>
  <h3>Age : {data.days_ago}days ago</h3>
  <h3>Topics: {data.topics}</h3>
  {#if data.name}
    <h3>Name: {data.name}</h3>
  {/if}
  {#if data.address}
    <h3>Address: {data.address}</h3>
  {/if}
  {#if data.contact}
    <h3>contact: {data.contact}</h3>
  {/if}
</div>

<style>
  .profile {
    text-align: center;
  }

  .profile_pic {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px; /* Add some space below the profile picture */
  }

  .profile_pic img {
    height: 150px;
    width: 150px;
    border-radius: 50%;
    box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.16), 0px 0px 0px 3px rgb(51, 51, 51);
  }
  /*
  

</style>
