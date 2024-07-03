import { error, json, redirect } from "@sveltejs/kit";
import { BACKEND_API } from "$lib/backend_api";
import { unreachable } from "$lib/utils";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, cookies }) => {
	const token = cookies.get("session_token");
	const username = params.username;
	if (token === undefined || token == "") {
		redirect(303, "/login");
	}
	let client = await BACKEND_API.getClient();

	let response = await client.user_profile(
		{
			username: username,
			authorization: token,
		},
		null,
		{
			validateStatus(status) {
				return [401, 200].includes(status);
			},
		},
	);

	if (response.status === 401) {
		return redirect(303, "/login");
	} else if (response.status === 200) {
		return {
			profile_data: response.data,
		};
	} else {
		unreachable();
	}
}

export const actions: Actions = {
	add_friend: async ({ request, cookies }) => {
		let token = cookies.get('session_token')
		if (!token) {
			return redirect(303, '/login')
		}
		let user_id = (await request.formData()).get('user_id')?.toString()
		if (!user_id) {
			unreachable()
		}
		

		const client = await BACKEND_API.getClient();

		const response = await client.add_friend(
			{
				authorization: token
			},
			{
				user_id: Number.parseInt(user_id)
			},
		);

		return {
			submitted: true,
			user_id: user_id
		}
		
	},
};
