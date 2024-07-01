import { error, json, redirect } from "@sveltejs/kit";

/** @type {import('./$types').Actions} */

/** @type {import('./$types').PageServerLoad} */
export const load = async ({ cookies }) => {
	const token = cookies.get("session_token");
	if (token === undefined || token == "") {
		redirect(303, "/login");
	}
	const response = await fetch("http://localhost:8000/suggestion", {
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
	return data ;
};


/** @type {import('./$types').Actions} */
export const actions = {
	logout: async (event) => {
		const token = event.cookies.get("session_token");
		if (token !== undefined) {
			const response = await fetch("http://localhost:8000/logout", {
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
	}
