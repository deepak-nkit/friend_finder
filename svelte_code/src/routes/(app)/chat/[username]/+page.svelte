<script lang="ts">
  import { page } from "$app/stores";
  import { zodClient } from "sveltekit-superforms/adapters";
  import type { PageData } from "./$types";
  import * as R from "remeda";
  import type { Components } from "../../../../backend_openapi";
  import { formSchema } from "./form_schema";
  import { superForm } from "sveltekit-superforms";
  import { toast } from "svelte-sonner";
  import { invalidateAll } from "$app/navigation";
  import { onDestroy, onMount } from "svelte";
  import { BACKEND_PUBLIC_URL } from "$lib/const";
  import { browser } from "$app/environment";

  export let data: PageData;
  let latest_messages: null | Components.Schemas.Message[] = null;
  let messages_in_progress: string[] = [];
  let chatWindow: HTMLDivElement;

  $: chat_user = $page.params.username;
  $: messages = R.reverse(latest_messages || data.messages);

  $: {
    latest_messages;
    messages_in_progress = [];
  }

  $: {
    if (browser && chatWindow) {
      messages;
      messages_in_progress;
      setTimeout(() => {
        chatWindow.lastElementChild?.scrollIntoView();
      }, 100);
    }
  }

  function getCookie(name: string) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop()!.split(";").shift();
    }
  }
  async function fetchLatestMessages() {
    let token = getCookie("session_token")!;
    let response = await fetch(
      BACKEND_PUBLIC_URL + `/get_messages/${chat_user}`,
      {
        headers: {
          Authorization: token,
        },
      },
    );
    if (response.ok) {
      latest_messages = await response.json();
    }
  }

  const { form, errors, enhance } = superForm(data.form, {
    validators: zodClient(formSchema),
    onSubmit: (d) => {
      messages_in_progress.push(d.formData.get('content')!.toString())
      messages_in_progress = messages_in_progress;
      d.jsonData({
        ...$form,
      })
    },
    onUpdate: (d) => {
      d.result.data.message
      
    },
    onError: (e) => {
      console.error(e);
      // TODO: make red
      toast.error(`Something went wrong at server`);
    },
  });

  // TODO: fix this! fix this!
  let interval: number | null = null;
  onMount(() => {
    interval = setInterval(() => {
      fetchLatestMessages();
    }, 5000);
    chatWindow.lastElementChild?.scrollIntoView();
  });
  onDestroy(() => {
    if (interval) {
      clearInterval(interval);
    }
  });
</script>

<div class="flex flex-col h-full rounded-2xl">
  <div class="flex flex-col overflow-y-scroll grow" bind:this={chatWindow}>
    {#each messages as message}
      {#if message.sender === data.self_user.user.id}
        <div class="chat chat-end">
          <div class="chat-bubble">{message.content}</div>
        </div>
      {:else}
        <div class="chat chat-start">
          <div class="chat-bubble">{message.content}</div>
        </div>
      {/if}
    {/each}
    {#each messages_in_progress as message}
      <div class="chat chat-end">
        <div class="chat-bubble bg-gray-100">{message}</div>
      </div>
    {/each}
  </div>

  <form
    use:enhance
    method="POST"
    on:submit={() => {
      messages_in_progress.push($form.content);
      messages_in_progress = messages_in_progress;
    }}
  >
    <input
      class="input input-bordered"
      autofocus
      type="text"
      required
      autocomplete="off"
      placeholder="Hi!"
      name="content"
      bind:value={$form.content}
    />
  </form>
</div>
