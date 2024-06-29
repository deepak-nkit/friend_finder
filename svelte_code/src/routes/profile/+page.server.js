import { error, json, redirect } from "@sveltejs/kit";
import { Backend_Base_URL } from "$lib/backend_url";

/** @type {import('./$types').PageServerLoad} */
export const load = async ({ cookies }) => {
	const token = cookies.get("session_token");
	if (token === undefined || token == "") {
		redirect(303, "/login");
	}
	const response = await fetch(`${Backend_Base_URL}:8000/profile`, {
		method: "GET",
		headers: {
			authorization: token,
		},
	});
	if (response.status === 401) {
		redirect(303, "/login");
	} else if (!response.ok) {
		return error(500, "Somthing Went Wrong");
	}
	const data = await response.json();
	console.log(data)
	return data;
};

