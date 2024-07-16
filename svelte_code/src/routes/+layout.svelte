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
<div data-theme="friend_theme" class="min-h-screen box-border custom-back">
  <slot></slot>
</div>

<style>

 .custom-back {
    --s: 50px; /* control the size*/
    --c1: #f8ecc9;
    --c2: #727c7e;
    --c3: #2c2e2a;
  
    --p:at 45% 40%,#0000 75%,;
    --g1:conic-gradient(var(--p) var(--c1) 0);
    --g2:conic-gradient(var(--p) var(--c2) 0);
    background:
      var(--g1),var(--g2) calc(2*var(--s)) 0,
      var(--g2) calc(3*var(--s)) var(--s),
      var(--g1) var(--s) var(--s) var(--c3);
    background-size: calc(4*var(--s)) calc(2*var(--s));
  }


  /*
      background: linear-gradient(
        45deg,
        transparent 15%,
        #64628a 15%,
        #64628a 20%,
        transparent 20%,
        transparent 80%,
        #64628a 80%,
        #64628a 85%,
        transparent 85%
      ),
      linear-gradient(
        135deg,
        transparent 15%,
        #64628a 15%,
        #64628a 20%,
        transparent 20%,
        transparent 80%,
        #64628a 80%,
        #64628a 85%,
        transparent 85%
      ),
      radial-gradient(
        circle at top,
        transparent 9%,
        #64628a 10%,
        #64628a 15%,
        transparent 16%
      ),
      radial-gradient(
        circle at bottom,
        transparent 9%,
        #64628a 10%,
        #64628a 15%,
        transparent 16%
      ),
      radial-gradient(
        circle at right,
        transparent 9%,
        #64628a 10%,
        #64628a 15%,
        transparent 16%
      ),
      radial-gradient(
        circle at left,
        transparent 9%,
        #64628a 10%,
        #64628a 15%,
        transparent 16%
      );
    background-size: 2em 2em;
    background-color: #e6cccc;
    opacity: 0.6;
  }
  */
</style>
