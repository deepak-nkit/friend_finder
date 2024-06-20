<script>
  import '$lib/style.css';
</script>
  
<div class="box_1">
  <span class="clos">
      <ion-icon name="close-outline"></ion-icon>
  </span>
  <div class="form-box login" id="login_info">
      <h2>Login</h2>
      <form method="POST" class="form-box login">
          <div>
              <label for="email"><b>Email</b></label>
              <input type="email" id="email" placeholder="Enter Email" name="email" required>
          </div>
          <div>
              <label for=" password"><b>Password</b></label>
              <input type="password" id="password" placeholder="Enter Password" name="psw" required>
          </div>
          <button type="button"  class="submit">Log in</button> 
          <a href="/forgot" class="forgot">forgotten password</a>
          <hr class="line">
          <div class="new">
              <p class="account">Don't have account?
                  <a href="/register" id="show_register_pg">Register</a>
              </p>
          </div>
      </form>
  </div>
</div>
