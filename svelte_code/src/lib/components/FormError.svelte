<script lang="ts">
  export let errors: string[] | undefined;
</script>
<div class="label flex flex-col items-start">
{#if errors !== undefined}
  {#each errors as error, i}
      <span class="label-text-alt text-red-700"> {errors.length>1?'*':''} {error} </span>
  {/each}
{/if}
</div>
