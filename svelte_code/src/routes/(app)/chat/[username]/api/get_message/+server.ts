import { error, redirect } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";
import { BACKEND_API } from "$lib/backend_api";

export const GET: RequestHandler = async ({ url, cookies, params }) => {
	const token = cookies.get("session_token")!;
	const client = await BACKEND_API.getClient();

	let before_id = null;
	if (url.searchParams.get("before_id")) {
		before_id = Number.parseInt(url.searchParams.get("before_id")!);
	}

	const message_response = await client.get_messages(
		{
			before_id,
			username: params.username,
			authorization: token,
		},
		null,
		{},
	);

	return new Response(JSON.stringify(message_response.data), {
		headers: {
			"content-type": "application/json",
		},
	});
};
