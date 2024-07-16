import { error, fail, json, redirect } from "@sveltejs/kit";
import type { PageServerLoad, Actions } from "./$types";
import { BACKEND_API } from "$lib/backend_api";
import { formSchema } from "./form_schema";
import type { Paths } from "../../../../backend_openapi";
import { superValidate } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";
import { unreachable } from "$lib/utils";

export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get("session_token");
	if (!token) {
		return redirect(303, "/login");
	}

	let client = await BACKEND_API.getClient();

	let response = await client.self_user_profile(
		{ authorization: token },
		null,
		{
			validateStatus(status) {
				return [401, 200].includes(status);
			},
		},
	);

	if (response.status == 401) {
		return redirect(303, "/login");
	} else if (response.status == 200) {
		return {
			form: await superValidate(zod(formSchema)),
			edit_profile: response.data,
		};
	} else {
		unreachable();
	}
};

export const actions: Actions = {
	default: async ({ request, cookies }) => {
		const form = await superValidate(request, zod(formSchema));
		if (!form.valid) {
			return fail(400, { form });
		}

		const client = await BACKEND_API.getClient();
		console.log("******edit*******");
		console.log("******let lete *******", form.data.latitude);

		const data = {
			username: form.data.username,
			email: form.data.email,
			name: form.data.name,
			address: form.data.address,
			latitude: form.data.latitude,
			longitude: form.data.longitude,
			topics: form.data.topics,
		};
		
		console.log("======*****=====****===== username ", typeof(data.username) , data.username );
		console.log("======*****=====****===== email ", typeof(data.email) , data.email);
		console.log("======*****=====****===== name ", typeof(data.name) , data.name);
		console.log("======*****=====****===== address ", typeof(data.address) , data.address);
		console.log("================latitude     ", typeof (data.latitude) , data.latitude);
		console.log("================latitude     ", typeof (data.longitude) , data.longitude);
		console.log("================ topics ", typeof form.data.topics);

		console.log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", data)
		const response = await client.edit(null, data, {
			validateStatus: (status) => {
				return [409, 200].includes(status);
			},
		});

		if (response.status === 409) {
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
				redirect(303, "/profile");
		} else {
			unreachable();
		}
	},
};
