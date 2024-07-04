import { error, fail, json, redirect } from "@sveltejs/kit";
import { applyAction } from "$app/forms";
import type { Actions, PageServerLoad } from "./$types";
import { BACKEND_API } from "$lib/backend_api";
import { unreachable } from "$lib/utils";
import { superValidate } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";
import { formSchema } from "./form_schema";

export const load: PageServerLoad = async ({ cookies, params }) => {
	const token = cookies.get("session_token");
	if (token === undefined || token == "") {
		redirect(303, "/login");
	}

	const client = await BACKEND_API.getClient();
	const messages_response = await client.get_messages(
		{
			username: params.username,
			authorization: token,
		},
		null,
		{
			validateStatus(status) {
				return [401, 200].includes(status);
			},
		},
	);

	if (messages_response.status !== 200) {
		redirect(303, "/login");
	}

	const profile_response = await client.self_user_profile(null, null, {
		headers: {
			Authorization: token,
		},
		validateStatus(status) {
			return [401, 200].includes(status);
		},
	});

	if (profile_response.status !== 200) {
		redirect(303, "/login");
	}

	return {
		messages: messages_response.data,
		self_user: profile_response.data,
		form: await superValidate(zod(formSchema)),
	};
};

export const actions: Actions = {
	default: async ({ request, cookies, params }) => {
		let token = cookies.get("session_token");
		if (!token) {
			return redirect(303, "/login");
		}

		const form = await superValidate(request, zod(formSchema));
		if (!form.valid) {
			return fail(400, { form });
		}

		const client = await BACKEND_API.getClient();

		const response = await client.send_message(
			{
				username: params.username,
				authorization: token,
			},
			{
				message: form.data.content,
				client_id: form.data.client_id,
			},
		);
		return {
		  message: response.data,
		  form
		}
	},
};
