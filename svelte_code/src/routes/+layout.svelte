<div class="main">
  <div class="navbar">
    <a href="/login">
      Login
    </a>
    <a href="/register"> Register </a>
  </div>
  <div>
    <slot />
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }
  .main {
    display: flex;
    flex-direction: column;
    width: 100vw;
    align-items: center;
    gap: 20px;
  }
  .navbar {
    box-shadow: 0 10px 3px -10px gray;
    background: #EDEDFF;
    /*gap: 20px;*/
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
  }
  .navbar > a {
  box-sizing: border-box;
        height: 100%;
        text-decoration: none;
        color: black;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 15px;
  }
  .navbar > a:hover {
    background-color: #CDCDED;
  }
</style>
