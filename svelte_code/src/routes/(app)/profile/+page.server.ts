import { error, json, redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import { BACKEND_API } from "$lib/backend_api";
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
			self_profile: response.data,
		};
	} else {
		unreachable();
	}
};
