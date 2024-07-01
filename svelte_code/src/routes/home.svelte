<script>
  import ff_1 from '$lib/static/ff_1.png'
  import message02 from '$lib/static/message02.png'
</script>

<div class="navbar">
  <nav class="nav">
    <!-- Logo -->
    <div class="logo">
      <a href="/">
      <img src={ff_1} alt="Friend Finder">
      </a>
    </div>


    <div class="box">
      <!-- Messages Icon -->
      <div class="message">
        <a href = "/messenger/">
          <img src={message02} alt="messages">
        </a>
      </div>

      <!-- Logout Button -->
      <form method="POST" action="?/logout">
        <div class="logout">
          <button type="submit">Logout</button>
        </div>
      </form>

      <!-- Profile Icon -->
      <div class="profile">
        <a href="/profile">
        <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar">
        </a>
      </div>
    </div>
  </nav>
</div>


<style>
    :global(body){
        paddin:0;
        margin:0;
    }

    .navbar {
        background-color:rgb(215, 192, 192);
        padding: 10px 20px;
        width:100wh;
        box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;
    }

    .nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        width:100vw;
        margin: 0 auto;
    }

    .logo img {
        height: 60px;
    }

    .box {
        display: flex;
        align-items: center;
        
    }

    .message img,
    .profile img {
        height: 40px;
        width: 50px;
        border-radius: 50%;
        margin: 0 15px;
    }

    .logout button {
        padding: 8px 16px;
        border: none;
        border-radius: 5px;
        background-color: #d73a49;
        color: white;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .logout button:hover {
        background-color: #c72c3a;
    }

    .profile img {
        border: 2px solid #fff;
    }
</style>

