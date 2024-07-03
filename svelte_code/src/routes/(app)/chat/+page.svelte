<script>
    import { Send } from 'lucide-svelte';

  /** @type {import('./$types').PageData} */
  export let data; // layout.server + page.server
</script>

<div class="flex flex-row gap-2 justify-center items-center h-full">
<Send size={24} /> <span class="text-lg"> Send Message </span>
</div>
