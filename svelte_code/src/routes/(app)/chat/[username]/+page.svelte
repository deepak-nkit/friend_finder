<script lang="ts">
  import { page } from "$app/stores";
  import { zodClient } from "sveltekit-superforms/adapters";
  import type { PageData } from "./$types";
  import * as R from "remeda";
  import type { Components } from "../../../../backend_openapi";
  import { formSchema } from "./form_schema";
  import SuperDebug, { superForm } from "sveltekit-superforms";
 /* import { toast } from "svelte-sonner"; */
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
  import { ChatManager, type Message } from "./chat_manager.svelte";
    import { formatDistance } from "date-fns";

  /**
  page_load: 20
  new_message /poll_message

  temporary_message: user-sent
  */
  let { data } = $props<{ data: PageData }>();
  let current_chat_user = $derived($page.params.username);

  /** Maps from each chat user to chat manager */
  let chatManagers: SvelteMap<string, ChatManager> = $state(new SvelteMap());

  let currentChatManager = $derived(chatManagers.get(current_chat_user)! || new ChatManager([], ''))


  let sortedPendingMessage =  $derived([...currentChatManager.pending_messages.values()]
        .sort((a, b) => b.sent_at.getTime() - a.sent_at.getTime()))

  let chatWindow: HTMLDivElement;


  let currentTime = $state(new Date());


  setInterval(() => {
    currentTime = new Date()
  }, 1000)

  function scrollChatToBottom() {
    if (chatWindow) {
      chatWindow.firstElementChild?.scrollIntoView(); // we use flex-col-reverse, so first is last in UI
    }
  }

  /** Create chat manager as user navigates to different user chats */
  $effect(() => {
    if (!chatManagers.has(current_chat_user)) {
      let manager = new ChatManager(data.messages, current_chat_user);
      chatManagers.set(current_chat_user, manager);

      /** TODO: stop polling if user doesn't visit chat window for X amount of time */
      manager.initializePolling();
    }


    /**
      Since browsers have a limit on total concurrent HTTP connections,
      we only poll the currently visible chat user, and pause the rest
    */
    for (const [chatUser, chatManager] of chatManagers.entries()) {
      if (chatUser === current_chat_user) {
        chatManager.resumePolling()
      } else {
        chatManager.pausePolling()
      }
    }
  });

  /** Scroll to bottom on start */
  $effect(() => {
    if (chatWindow) {
      scrollChatToBottom()
    }
  });

  const { form, errors, enhance } = superForm(data.form, {
    dataType: "json",
    validators: zodClient(formSchema),
    invalidateAll: false,

    onSubmit: (d) => {
      $form.client_id = uuidv4();
      currentChatManager.register_pending_message($form.content, $form.client_id)
    },
    onError: (e) => {
      console.error(e);
      // TODO: make red
      /* toast.error(`Something went wrong at server`); */
    },
  });
</script>


  {#snippet showMessage(message: Message)}
      {#if message.sender === data.self_user.user.id}
        <div class="chat chat-end">
          <div class="chat-header">
            You
            <time class="text-xs opacity-50">{formatDistance(new Date(message.sent_at!), currentTime)} ago</time>
          </div>
          <div class="chat-bubble">{message.content}</div>
        </div>
      {:else}
        <div class="chat chat-start">
          <div class="chat-header">
            {current_chat_user}
            <time class="text-xs opacity-50">{formatDistance(new Date(message.sent_at!), currentTime)} ago</time>
          </div>
          <div class="chat-bubble">{message.content}</div>
        </div>
      {/if}
  {/snippet}

  <div class="flex flex-col h-full rounded-2xl custom_back  container">
    <div
      class="flex flex-col-reverse overflow-y-scroll grow"
      bind:this={chatWindow}
    >

      {#each sortedPendingMessage as message}
        <div class="chat chat-end">
          <div class="chat-bubble  bg-gray-500">{message.content}</div>
        </div>
      {/each}
      {#each R.reverse(currentChatManager.polled_messages) as message (message.id)}
        {@render showMessage(message)}
      {/each}
      {#each R.reverse(currentChatManager.initial_messages) as message (message.id)}
        {@render showMessage(message)}
      {/each}

    </div>

    <form use:enhance method="POST">
      <input
        class="input input-bordered bg-slate-200"
        autofocus
        type="text"
        required
        autocomplete="off"
        placeholder="Message"
        name="content"
        bind:value={$form.content}
      />
    </form>
  </div>

<style>

  .custom_back{
    background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT24NCJiDgLDxf5X1nSY98eXGSnPF-6ryCb-C4f-57oyal1w61KyxajKsak3ftJWHcaNP0&usqp=CAU");

  }
  
</style>
