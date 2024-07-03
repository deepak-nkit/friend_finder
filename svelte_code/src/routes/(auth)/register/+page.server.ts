import { error, fail, json, redirect } from "@sveltejs/kit";
import type { PageServerLoad, Actions } from "./$types";
import { BACKEND_API } from "$lib/backend_api";
import { formSchema } from "./form_schema";
import { superValidate } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";
import type { Paths } from "../../../backend_openapi";
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
	default: async ({ request, cookies }) => {
		const form = await superValidate(request, zod(formSchema));
		if (!form.valid) {
			return fail(400, { form });
		}

		const client = await BACKEND_API.getClient();

		const data = {
			username: form.data.username,
			email: form.data.email,
			password: form.data.password,
			pincode: Number.parseInt(form.data.pincode),
			topics: form.data.topics,
		};

		console.log("================ data sending", form.data.topics)

		const response = await client.register(null, data, {
			validateStatus: (status) => {
				return [409, 200].includes(status);
			},
		});

		if (response.status === 409) {
			// TODO: the type in openapi schema is "wrong" here.
			// it does not include `detail` key.
			let data = response.data as unknown as {
				detail: Paths.Register.Responses.$409;
			};

			if (data["detail"]["unique_field"] === "email") {
				form.errors.email = ["Email is already being used."];
			} else if (data["detail"]["unique_field"] === "username") {
				form.errors.username = ["Username is already being used."];
			} else {
				unreachable();
			}
			return fail(409, { form });
		} else if (response.status === 200) {
			// -> 200
			cookies.set("session_token", response.data.session_token, {
				maxAge: 3600 * 24 * 365 * 100,
				path: "/",
			});
			redirect(303, "/");
		} else {
			unreachable();
		}
	},
};
