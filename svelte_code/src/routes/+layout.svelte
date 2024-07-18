<script lang="ts">
  import { Toaster } from "svelte-sonner";
  import "../app.css";
  import "nprogress/nprogress.css";
  import NProgress from "nprogress";

  import { navigating } from "$app/stores";

  NProgress.configure({
    // Full list: https://github.com/rstacruz/nprogress#configuration
    minimum: 0.16,
  });

  $effect(() => {
    if ($navigating) {
      NProgress.start();
    } else NProgress.done();
  });
</script>

<Toaster position="top-center" />

<!-- <div data-theme="cupcake"> -->
<!-- <div data-theme="friend_theme"> -->
<div data-theme="friend_theme" class="min-h-screen box-border custom-back bg-cover">
  <slot></slot>
</div>

<style>
  .custom-back{
    background-image: url('../../src/lib/static/bg.jpg');
  }
</style>
