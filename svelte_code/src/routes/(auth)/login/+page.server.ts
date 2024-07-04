import { fail, redirect } from "@sveltejs/kit";
import type { PageServerLoad, Actions } from "./$types";
import { BACKEND_API } from "$lib/backend_api";
import { formSchema } from "./form_schema";
import { superValidate } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";
import { unreachable } from "$lib/utils";

export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get("session_token");
	if (token !== undefined && token !== "") {
		let client = await BACKEND_API.getClient();

		let response = await client.get_current_user(null, null, {
			headers: {
				Authorization: token,
			},
			validateStatus(status) {
				return [401, 200].includes(status);
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
	login: async ({ request, cookies }) => {
		const form = await superValidate(request, zod(formSchema));
		if (!form.valid) {
			return fail(400, { form });
		}

		const client = await BACKEND_API.getClient();

		const response = await client.login(
			null,
			{
				email: form.data.email,
				password: form.data.password,
			},
			{
				validateStatus(status) {
					return [401, 200].includes(status);
				},
			},
		);

		if (response.status === 401) {
			form.errors.email = ["Invalid email or password"];
			return fail(401, { form });
		} else if (response.status === 200) {
			cookies.set("session_token", response.data.session_token, {
				maxAge: 3600 * 24 * 365 * 100,
				path: "/",
				// TODO(security): find a better alternative
				httpOnly: false,
			});
			redirect(303, "/");
		} else {
			unreachable();
		}
	},
	logout: async ({ cookies }) => {
		const token = cookies.get('session_token')
		if (!token) {
			return redirect(303, "/login")
		}
		

		const client = await BACKEND_API.getClient();
		await client.logout(null, null, {
			headers: {
				Authorization: token,
			},

			validateStatus(status) {
				return [401, 200].includes(status);
			},
		});

		cookies.set('session_token', '', {
			maxAge: 0,
			path: '/'
		})

		redirect(303, "/login");
	},
};
