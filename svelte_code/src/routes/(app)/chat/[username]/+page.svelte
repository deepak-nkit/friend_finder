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
  import { SvelteMap } from "svelte/reactivity";

  import {
    PromiseStatuses,
    PROMISE_RESOLVED,
    promiseStatus,
    promiseState,
    isPromiseResolved,
    isPromiseNotRejected,
  } from "promise-status-async";

  import { v4 as uuidv4 } from "uuid";
  import { PROMISE_PENDING } from "promise-status-async";

  /**
  page_load: 20
  new_message /poll_message

  temporary_message: user-sent
  */
  let { data } = $props<{ data: PageData }>();
  let chat_user = $derived($page.params.username);

  function create_map(messages: Components.Schemas.Message[]) {
    let map: Map<number, Components.Schemas.Message> = new Map();
    for (const message of messages) {
      map.set(message.id!, message);
    }
    return map;
  }

  let initial_messages = $derived(create_map(data.messages));
  function sortMessagesReverse(
    message: Map<number, Components.Schemas.Message>,
  ) {
    return [...message.keys()]
      .sort((a, b) => {
        return b - a;
      })
      .map((x) => message.get(x)!);
  }
  let initial_messages_list = $derived(sortMessagesReverse(initial_messages));

  // recieved via /polled_messages
  let polled_messages: SvelteMap<
    string,
    SvelteMap<number, Components.Schemas.Message>
  > = $state(new SvelteMap());

  let polled_messages_list = $derived(
    sortMessagesReverse(polled_messages.get(chat_user) || new SvelteMap()),
  );

  // Yet to be acknowledged by server
  let pending_messages: SvelteMap<
    string,
    { client_id: string; content: string }[]
  > = $state(new SvelteMap());

  $effect(() => {
    pending_messages.set(chat_user, []);
    polled_messages.set(chat_user, new SvelteMap());
  });

  function latestMessageID(chat_user: string) {
    return Math.max(
      ...initial_messages.keys(),
      ...(polled_messages.get(chat_user) || new SvelteMap()).keys(),
      0,
    );
  }

  let chatWindow: HTMLDivElement;

  $effect(() => {
    if (browser && chatWindow) {
      polled_messages;
      pending_messages;
      setTimeout(() => {
        chatWindow.firstElementChild?.scrollIntoView();
      }, 100);
    }
  });

  async function pollMessage(other_user: string) {
    let response = await fetch(
      `/chat/${other_user}/api/poll_message?after_id=${latestMessageID(other_user)}`,
    );
    if (response.ok) {
      let data: Components.Schemas.Message[] = await response.json();
      if (data.length === 0) {
        return;
      }

      for (const message of data) {
        polled_messages.get(other_user)!.set(message.id!, message);
        pending_messages.set(
          other_user,
          pending_messages
            .get(other_user)!
            .filter((x) => x.client_id != message.client_id),
        );
      }
      /* polled_messages = polled_messages; */
      /* pending_messages = pending_messages; */
    }
  }

  async function continuouslyPollMessage(
    condition: () => boolean,
    other_user: string,
  ) {
    console.log("========= starting new poll", other_user);
    while (other_user === chat_user && condition()) {
      try {
        await pollMessage(other_user);
      } catch (e) {
        console.log("polling error: ", e);
        await new Promise((r) => setTimeout(r, 5000));
      }
    }
  }

  /* $effect(() => { */
  /* form.update(($form) => { */
  /* $form.client_id = uuidv4(); */
  /* return $form; */
  /* }); */
  /* }); */

  const { form, errors, enhance } = superForm(data.form, {
    dataType: "json",
    validators: zodClient(formSchema),
    invalidateAll: false,

    onSubmit: (d) => {
      $form.client_id = uuidv4();
      pending_messages
        .get(chat_user)!
        .push({ client_id: $form.client_id, content: $form.content });
    },
    onError: (e) => {
      console.error(e);
      // TODO: make red
      toast.error(`Something went wrong at server`);
    },
  });
  let running = true;
  let pollers: Record<string, Promise<void> | undefined> = {};
  $effect(() => {
    chat_user;
    (async () => {
      if (
        pollers[chat_user] &&
        (await promiseStatus(pollers[chat_user])) === PROMISE_PENDING
      ) {
      console.log("returning")
        return;
      }
      pollers[chat_user] = continuouslyPollMessage(() => {
        return running;
      }, chat_user);
    })();
  });

  onMount(() => {
    browser && chatWindow.firstElementChild?.scrollIntoView();
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
    {#each R.reverse(pending_messages.get(chat_user) || []) as message}
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
</div>
