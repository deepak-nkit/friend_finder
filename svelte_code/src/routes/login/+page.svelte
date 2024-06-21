  <script>
	/** @type {import('./$types').PageData} */
	export let data;

	/** @type {import('./$types').ActionData} */
	export let form;
</script>

{#if form != null}
	<p>Successfully logged in! Welcome back, {form}</p>
{/if}

<!-- <script> -->
  <!-- import "$lib/style.css"; -->
  <!-- export let  form; -->
<!-- </script> -->
<!-- {#if form?  } -->

<div class="box_1">
  <span class="clos">
    <ion-icon name="close-outline"></ion-icon>
  </span>
  <div class="form-box login" id="login_info">
    <h2>Login</h2>
    <form method="POST" class="form-box login">
      <div>
        <label for="email"><b>Email</b></label>
        <input
          type="email"
          id="email"
          placeholder="Enter Email"
          name="email"
          required
        />
      </div>
      <div>
        <label for=" password"><b>Password</b></label>
        <input
          type="password"
          id="password"
          placeholder="Enter Password"
          name="password"
          required
        />
      </div>
      <button type="submit" class="submit">Log in</button>
      <a href="/forgot" class="forgot">forgotten password</a>
      <hr class="line" />
      <div class="new">
        <p class="account">
          Don't have account?
          <a href="/register" id="show_register_pg">Register</a>
        </p>
      </div>
    </form>
  </div>
</div>
