<script lang="ts">
  export let data;
</script>

<div class="container">
  <div class="side_box">
    <div class="user_box">
      <img src="" alt="profile" class="profile" />
      <div class="username">{data.sidebar_data.current_username}</div>
    </div>
    <div class="tag">message</div>
    {#each data.sidebar_data.user as user}
      <a href={`/messenger/${user.user_id}`}>
        <div class="usernames">
          <p>{user.username}</p>
          <br />
        </div>
      </a>
    {/each}
  </div>
  <slot />
</div>

<style>
  .container {
    height: 100vh;
    display: flex;
  }
  .side_box {
    width: 300px;
    display: flex;
    flex-direction: column;
    padding: 10px;
    background-color: rgb(243, 237, 229);
  }
  .user_box {
    display: flex;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid black;
  }

  .profile {
    height: 40px;
    width: 40px;
    border-radius: 50%;
    margin-right: 10px;
  }

  .username {
    font-size: 15px;
    font-weight: bold;
  }
</style>
