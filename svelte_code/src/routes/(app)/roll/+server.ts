import { BACKEND_API } from "$lib/backend_api";
import { redirect } from "@sveltejs/kit";
import { unreachable } from "$lib/utils";
import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

export const GET: RequestHandler = async ({ cookies, url }) => {
	const token = cookies.get("session_token");
	const username = url.searchParams.get("inputval")!;
	console.log("**********", username);
	if (token === undefined || token === "") {
		redirect(303, "/login");
	}

	if (!username) {
		return { error: "No Userfound" };
	}

	let client = await BACKEND_API.getClient();
	let response = await client.search_user(
		{ authorization: token },
		{ username: username },
		{
			validateStatus(status) {
				return [401, 200].includes(status);
			},
		},
	);
	if (response.status === 401) {
		redirect(303, "/");
	}
	if (response.status === 200) {
		return new Response(JSON.stringify(response.data), {
			headers: { "Content-Type": "application/json" },
		});
	}
};

// if (response.status === 200) {
	// 	return {
// 		search_data:	response.data,
// 	}
