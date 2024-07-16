<script lang="ts">
  import { X } from "lucide-svelte";
  import { toast } from "svelte-sonner";
  import type { PageData } from "./$types";
  import SuperDebug, { superForm } from "sveltekit-superforms";
  import { formSchema } from "./form_schema";
  import Map from "../../component/map.svelte";
  import FormError from "$lib/components/FormError.svelte";
  import { zodClient } from "sveltekit-superforms/adapters";
  import Layout from "../../../+layout.svelte";
  import Page from "../+page.svelte";

  export let data: PageData;
  $: user = data.edit_profile.user;
  let top = data.edit_profile.topics;
  console.log(user);
  let lat: number | null;
  let lng: number | null;

  console.log("****** top ", top);

  const { form, errors, enhance } = superForm(data.form, {
    validators: zodClient(formSchema),
    dataType: "json",
    onError: (e) => {
      console.error(e);
      // TODO: make red
      toast.error(`Something went wrong at server`);
    },
  });

  let currentTopic = "";
  let topics: string[] = [];

  for (let i = 0; i < top.length; i++) {
    topics.push(top[i].name);
  }

  $: {
    currentTopic = currentTopic.replace(/,/g, "");
  }
  $: {
    form.update(($form) => {
      $form.topics = topics;
      return $form;
    });
  }

  function addTopic(topic: string) {
    console.log("&&&",topic);
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
  console.log("********* topics ::",topics)

</script>

<div class="flex gap-8 border-2 p-4 md:w-[73rem] bg-slate-300">
  <form method="POST" class="card glass p-10 flex flex-col gap-1 md:w-[28rem]">
    <h1 class="text-center text-4xl mb-8 mt-4">Details</h1>

    <label>
      <span class="label-text">Username</span>
      <input
        class="input input-bordered"
        type="text"
        placeholder="Pick something cool!"
        name="username"
        value={user.username}
      />
    </label>

    <label>
      <span class="label-text">Email</span>
      <input
        class="input input-bordered"
        type="email"
        placeholder="Your email"
        name="email"
        value={user.email}
      />
    </label>

    <label>
      <span class="label-text">Name</span>
      <input
        class="input input-bordered"
        type="text"
        placeholder="Name"
        name="name"
      />
    </label>

    <label>
      <span class="label-text">Address</span>
      <input
        class="input input-bordered"
        type="text"
        placeholder="Address"
        name="address"
      />
    </label>

    <label>
      <span class="label-text">Add more Topics</span>
      <input
        class="input input-bordered"
        type="text"
        inputmode="numeric"
        placeholder="topic"
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

    <input type="hidden" name="latitude" value={lat} />
    <input type="hidden" name="longitude" value={lng} />
    <button type="submit" class="btn btn-primary mt-4">Submit</button>
  </form>
  <div class="max-h-full border-2">
    <Map bind:latitude={lat} bind:longitutde={lng} />
  </div>
</div>
