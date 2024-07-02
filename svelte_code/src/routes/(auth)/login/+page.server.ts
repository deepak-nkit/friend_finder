import { error, fail, json, redirect } from "@sveltejs/kit";
import type { PageServerLoad, Actions } from "./$types";
import { BACKEND_API } from "$lib/backend_api";
import { formSchema } from "./form_schema";
import { superValidate } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";

export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get("session_token");
	if (token !== undefined && token !== "") {
		let client = await BACKEND_API.getClient();

		let response = await client.get_current_user(null, null, {
			headers: {
				Authorization: token,
			},
			validateStatus(status) {
          return [401, 200].includes(status)
      },
		});

		if (response.status == 200) {
			redirect(303, "/");
		}
	}

	return {
		form: await superValidate(zod(formSchema)),
	};
};

export const actions: Actions = {
	default: async ({ request, cookies }) => {
		const form = await superValidate(request, zod(formSchema));
		if (!form.valid) {
			return fail(400, { form });
		}

		const client = await BACKEND_API.getClient();

		const response = await client.login(null, {
			email: form.data.email,
			password: form.data.password,
		});

		if (response.status != 200 && response.status !== 401) {
			// TODO: take this error out of `email` field
			form.errors.email = ["Something went wrong"];
			return fail(500, { form });
		} else if (response.status === 401) {
			form.errors.email = ["Invalid email or password"];
			return fail(401, { form });
		} else {
			cookies.set("session_token", response.data.session_token, {
				maxAge: 3600 * 24 * 365 * 100,
				path: "/",
			});
			redirect(303, "/");
		}
	},
};
