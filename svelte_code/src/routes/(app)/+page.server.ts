import { error, json, redirect } from "@sveltejs/kit";
import { applyAction } from "$app/forms";
import type { Actions, PageServerLoad } from './$types';
import { BACKEND_API } from "$lib/backend_api";
import { unreachable } from "$lib/utils";


export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get("session_token");
	if (token === undefined || token == "") {
		redirect(303, "/login");
	}

	const client = await BACKEND_API.getClient()
	const suggestion_response = await client.suggestion(null, null, {
		headers: {
			Authorization: token
		},
		validateStatus(status) {
       return  [401, 200].includes(status)
    },
	})

	if (suggestion_response.status !== 200) {
		redirect(303, "/login");
	}

	const profile_response = await client.self_user_profile(null, null, {
		headers: {
			Authorization: token
		},
		validateStatus(status) {
       return  [401, 200].includes(status)
    },
	})

	if (profile_response.status !== 200) {
		redirect(303, "/login");
	}

	return {
		user_profile: profile_response.data,
		suggestions: suggestion_response.data
	};
};

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