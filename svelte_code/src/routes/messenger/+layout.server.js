import { error, json, redirect } from "@sveltejs/kit";
import { Backend_Base_URL } from "$lib/backend_url";

/** @type {import('./$types').LayoutServerLoad} */
export async function load({ cookies }) {
	const token = cookies.get("session_token");
	if (token !== undefined && token !== "") {
		const response = await fetch(`${Backend_Base_URL}:8000/inbox`, {
			method: "GET",
			headers: {
				authorization: token,
			},
		});
		if (!response.ok) {
			return error(500, "Somthing Went Wrong");
		} else {
			const data = await response.json();
			return {
				sidebar_data: data,
			};
		}
	}
}
