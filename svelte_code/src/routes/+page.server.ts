import { error, json, redirect } from "@sveltejs/kit";
import { applyAction } from "$app/forms";
import type { PageServerLoad } from './$types';


export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get("session_token");
	if (token === undefined || token == "") {
		redirect(303, "/login");
	}

	const response = await fetch(`${BACKEND_BASE_URL}:8000/suggestion`, {
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
	return data;
};

/** @type {import('./$types').Actions} */
export const actions = {
	logout: async (event) => {
		const token = event.cookies.get("session_token");
		if (token !== undefined) {
			const response = await fetch(`${BACKEND_BASE_URL}:8000/logout`, {
				method: "POST",
				headers: {
					authorization: token,
				},
			});

			event.cookies.set("session_token", "", {
				maxAge: 1,
				path: "/",
			});
			// No need to redirect here, load function executes after action and handles redirection to login page
		}
	},

	add_friend: async ({ cookies, request }) => {
		const token = cookies.get("session_token");

		const form_data = await request.formData();
		const username = form_data.get("username");
		if (token === undefined) {
			redirect(303, "/login");
		}
		const response = await fetch(`${BACKEND_BASE_URL}:8000/add_friend`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				authorization: token,
			},
			body: JSON.stringify({
				username,
			}),
		});
		console.log(response);
		if (!response.ok) {
			return error(500, {
				message: `Some error occurred. [status=${response.status}]`,
			});
		} else {
			let data = await response.json();
			return {
				success: true,
			};
		}
	},
};
