<script lang="ts">
  import { page } from "$app/stores";
  import { zodClient } from "sveltekit-superforms/adapters";
  import type { PageData } from "./$types";
  import * as R from "remeda";
  import type { Components } from "../../../../backend_openapi";
  import { formSchema } from "./form_schema";
  import SuperDebug, { superForm } from "sveltekit-superforms";
  import { toast } from "svelte-sonner";
  import { invalidateAll } from "$app/navigation";
  import { onDestroy, onMount } from "svelte";
  import { BACKEND_PUBLIC_URL } from "$lib/const";
  import { browser } from "$app/environment";

  import { v4 as uuidv4 } from "uuid";

  /**
  page_load: 20
  new_message /poll_message

  temporary_message: user-sent
  */
  export let data: PageData;

  function create_map(messages: Components.Schemas.Message[]) {
    let map: Map<number, Components.Schemas.Message> = new Map();
    for (const message of messages) {
      map.set(message.id!, message);
    }
    return map;
  }

  $: initial_messages = create_map(data.messages);
  function sortMessagesReverse(
    message: Map<number, Components.Schemas.Message>,
  ) {
    return [...message.keys()]
      .sort((a, b) => {
        return b - a;
      })
      .map((x) => message.get(x)!);
  }
  $: initial_messages_list = sortMessagesReverse(initial_messages)

  // recieved via /polled_messages
  let polled_messages: Map<number, Components.Schemas.Message> = new Map();
  $: polled_messages_list = sortMessagesReverse(polled_messages)

  // Yet to be acknowledged by server
  let pending_messages: { client_id: string; content: string }[] = [];

  function clearState(data: any) {
    polled_messages.clear();
    polled_messages = polled_messages;
    pending_messages.length = 0;
    pending_messages = pending_messages;
  }

  $: clearState(data.messages);

  // TODO(perf): don't recalculate every time new message arrives
  $: latest_message_id = Math.max(
    ...initial_messages.keys(),
    ...polled_messages.keys(),
    0,
  );

  let chatWindow: HTMLDivElement;

  $: chat_user = $page.params.username;

  $: {
    if (browser && chatWindow) {
      polled_messages;
      pending_messages;
      setTimeout(() => {
        chatWindow.firstElementChild?.scrollIntoView();
      }, 100);
    }
  }

  async function pollMessage() {
    let response = await fetch(
      `/chat/${chat_user}/api/poll_message?after_id=${latest_message_id}`,
    );
    if (response.ok) {
      let data: Components.Schemas.Message[] = await response.json();
      if (data.length === 0) {
        return;
      }

      for (const message of data) {
        polled_messages.set(message.id!, message);
        pending_messages = pending_messages.filter(
          (x) => x.client_id != message.client_id,
        );
      }
      polled_messages = polled_messages;
      pending_messages = pending_messages;
    }
  }

  async function continuouslyPollMessage(condition: () => boolean) {
    while (condition()) {
      try {
        await pollMessage();
      } catch (e) {
        console.log("polling error: ", e);
        await new Promise((r) => setTimeout(r, 5000));
      }
    }
  }

  let clientID = uuidv4();

  $: {
    form.update(($form) => {
      console.log("========= setting, clientid", clientID);
      $form.client_id = clientID;
      return $form;
    });
  }

  const { form, errors, enhance } = superForm(data.form, {
    dataType: "json",
    validators: zodClient(formSchema),
    invalidateAll: false,

    onSubmit: (d) => {
      clientID = uuidv4();
    },
    onError: (e) => {
      console.error(e);
      // TODO: make red
      toast.error(`Something went wrong at server`);
    },
  });
  let running = true;

  onMount(() => {
    continuouslyPollMessage(() => {
      return running;
    });

    chatWindow.firstElementChild?.scrollIntoView();
  });
  onDestroy(() => {
    running = false;
  });
</script>

<div class="flex flex-col h-full rounded-2xl">
  <div
    class="flex flex-col-reverse overflow-y-scroll grow"
    bind:this={chatWindow}
  >
    {#each [...polled_messages_list, ...initial_messages_list] as message}
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
    {#each R.reverse(pending_messages) as message}
      <div class="chat chat-end">
        <div class="chat-bubble bg-gray-100">{message.content}</div>
      </div>
    {/each}
  </div>

  <form use:enhance method="POST">
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
  {latest_message_id}
</div>

<SuperDebug
  data={{
    polled_messages_list,
    initial_messages_list,
    polled_messages,
    initial_messages,
  }}
/>
