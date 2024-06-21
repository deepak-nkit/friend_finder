<script lang="ts">
  import "$lib/style.css";
</script>

<div class="box_1">
  <div class="form-box register" id="register">
    <h2>Register</h2>
    <form method="POST">
      <div>
        <label><b>Username</b></label>
        <input
          type="text"
          placeholder="Enter Username"
          name="username"
          required
        />
      </div>

      <div>
        <label><b>Email</b></label>
        <input type="email" placeholder="Enter Email" name="email" required />
      </div>

      <div>
        <label><b>Password</b></label>
        <input
          type="password"
          placeholder="Enter Password"
          name="password"
          required
        />
      </div>
      <div>
        <label><b>Pincode</b></label>
        <input
          type="number"
          placeholder="Enter Pincode"
          name="pincode"
          required
        />
      </div>

      <div>
        <div class="topic_set">
          <label><b>Enter Your Interested Topics</b></label>
          <input
            type="text"
            placeholder="Enter Topic and Press Enter"
            name="topics"
          />
        </div>
      </div>

      <button type="submit" class="registration">Register</button>
      <hr class="line" />
      <div class="new">
        <p class="account">
          Already have an account
          <a href="/login" id="show_login_pg">Login</a>
        </p>
      </div>
    </form>
  </div>
</div>
