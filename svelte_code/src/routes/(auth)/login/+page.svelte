<script lang="ts">
  import { superForm } from "sveltekit-superforms";
  import { formSchema } from "./form_schema";
  import { zodClient } from "sveltekit-superforms/adapters";
  import FormError from "$lib/components/FormError.svelte";
  import { toast } from "svelte-sonner";

  export let data;

  const { form, errors, enhance } = superForm(data.form, {
    validators: zodClient(formSchema),
    onError: (e) => {
      console.error(e);
      // TODO: make red
      toast.error(`Something went wrong at server`);
    },
  });
</script>

<form
  method="POST"
  action="?/login"
  use:enhance
  class="card glass p-10 flex flex-col gap-6 w-full"
>
  <h1 class="text-center text-4xl mb-8 mt-4">Login</h1>
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

  <button type="submit" class="btn btn-primary">Submit</button>

  <div class="flex justify-around">
    <a href="/register">
      <button type="button" class="btn btn-ghost btn-sm">Register </button>
    </a>
    <button type="button" class="btn btn-ghost btn-sm">Forgot Password</button>
  </div>
</form>
