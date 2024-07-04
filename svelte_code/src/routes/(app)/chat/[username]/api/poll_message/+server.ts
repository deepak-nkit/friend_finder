import { error, redirect } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";
import { BACKEND_API } from "$lib/backend_api";

export const GET: RequestHandler = async ({ url, cookies, params }) => {
	const token = cookies.get("session_token")!;
	const client = await BACKEND_API.getClient();
	const poll_response = await client.poll_message(
		{
			after_id: Number.parseInt(url.searchParams.get("after_id")!),
			username: params.username,
			authorization: token,
		},
		null,
		{},
	);

	return new Response(JSON.stringify(poll_response.data), {
		headers: {
			"content-type": "application/json",
		},
	});
};
