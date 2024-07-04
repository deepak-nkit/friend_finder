<script lang="ts">
  import SuperDebug, { superForm } from "sveltekit-superforms";
  import { formSchema } from "./form_schema";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { X } from "lucide-svelte";
  import { toast } from "svelte-sonner";
  import FormError from "$lib/components/FormError.svelte";

  export let data;

  const { form, errors, enhance } = superForm(data.form, {
    validators: zodClient(formSchema),
    dataType: 'json',
    onError: (e) => {
      console.error(e);
      // TODO: make red
      toast.error(`Something went wrong at server`);
    },
  });

  let currentTopic = "";
  let topics: string[] = [];
  $: {
    currentTopic = currentTopic.replace(/,/g, "");
  }
  $: {
    form.update(
      ($form) => {
        $form.topics = topics;
        return $form;
      },
    );
  }

  function addTopic(topic: string) {
    if (topic === "") {
      return;
    }
    if (topics.includes(topic)) {
      return;
    }
    topics.push(topic);
    topics = topics;
  }

  function removeTopic(topic: string) {
    topics = topics.filter((x) => x !== topic);
  }
</script>

<form
  method="POST"
  use:enhance
  class="card glass p-10 flex flex-col gap-1 md:w-[32rem]"
>
  <h1 class="text-center text-4xl mb-8 mt-4">Register</h1>

  <label>
    <span class="label-text">Username</span>
    <input
      class="input input-bordered"
      type="text"
      placeholder="Pick something cool!"
      name="username"
      bind:value={$form.username}
    />
    <FormError errors={$errors.username} />
  </label>

  <label>
    <span class="label-text">Email</span>
    <input
      class="input input-bordered"
      type="email"
      placeholder="Your email"
      name="email"
      bind:value={$form.email}
    />
    <FormError errors={$errors.email} />
  </label>

  <label>
    <span class="label-text">Password</span>
    <input
      class="input input-bordered"
      type="password"
      placeholder="********"
      name="password"
      bind:value={$form.password}
    />
    <FormError errors={$errors.password} />
  </label>

  <label>
    <span class="label-text">Pincode</span>
    <input
      class="input input-bordered"
      type="text"
      inputmode="numeric"
      placeholder=""
      name="pincode"
      maxlength="6"
      bind:value={$form.pincode}
    />
    <FormError errors={$errors.pincode} />
  </label>

  <label>
    <span class="label-text">Topics</span>
    <input
      class="input input-bordered"
      type="text"
      inputmode="numeric"
      placeholder=""
      bind:value={currentTopic}
      on:keydown={(e) => {
        if (e.key === "," || e.key === "Enter") {
          // Allow form submit if there is nothing typed in input box
          if (currentTopic === "") {
            return;
          }

          e.preventDefault();
          addTopic(currentTopic);
          currentTopic = "";
        }
      }}
    />
    <div class="p-1 flex flex-wrap gap-2">
      {#each topics as topic}
        <span
          class="border rounded-2xl bg-gray-200 px-2 flex align-middle items-center gap-2"
        >
          <span>{topic}</span>
          <button
            type="button"
            class="inline hover:bg-gray-300 rounded-3xl p-[0.2rem] h-fit"
            on:click={() => removeTopic(topic)}
          >
            <X size={14} />
          </button>
        </span>
      {/each}
    </div>
    {#if $errors.topics !== undefined}
      <FormError errors={Object.values($errors.topics).flat()} />
    {/if}
  </label>

  <button type="submit" class="btn btn-primary">Submit</button>
  <div class="flex justify-around">
    <a class="btn btn-ghost btn-sm" href="/login">Login</a>
  </div>
</form>
<SuperDebug data={{$form, topics}} />
