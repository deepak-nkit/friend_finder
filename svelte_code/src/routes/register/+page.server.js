import { error, json, redirect } from "@sveltejs/kit";
import { Backend_Base_URL } from "$lib/backend_url";

/** @type {import('./$types').Actions} */

/** @type {import('./$types').PageServerLoad} */
export async function load({ cookies }) {
	// const id = cookies.get("id")
	const token = cookies.get("session_token");
	if (token !== undefined && token !== "") {
		const response = await fetch(`${Backend_Base_URL}:8000/loged_in`, {
			method: "GET",
			headers: {
				authorization: token,
			},
		});
		if (response.ok) {
			redirect(303, "/");
		}
	}
}

/** @type {import('./$types').Actions} */
export const actions = {
	default: async (event) => {
		const form = await event.request.formData();
		let username = form.get("username");
		console.log("*******",username)
		const email = form.get("email");
		const password = form.get("password");
		const pincode = form.get("pincode");
		const topics = form.get("topics");

		// if (username.includes(' ')){
		// 	return error (100 , {message: "Space not allowed"})
		// }
		// username = encodeURIComponent(username)

		let data = { username, email, password, pincode, topics };

		const response = await fetch(`${Backend_Base_URL}:8000/register`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(data),
		});
		if (!response.ok) {
			return error(505, { message: "registration failed ! try again" });
		} else {
			const data = await response.json();
			let token = data.session_token;
			event.cookies.set("session_token", token, {
				maxAge: 3600 * 24 * 365 * 100,
				path: "/",
			});
			redirect(303, "/");
		}
	},
};
