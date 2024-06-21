import { error, json, redirect } from "@sveltejs/kit";

/** @type {import('./$types').Actions} */

/** @type {import('./$types').Actions} */
export const actions = {
	default: async (event) => {
		const form = await event.request.formData();
		const username = form.get("username");
		const email = form.get("email");
		const password = form.get("password");
		const pincode = form.get("pincode");
		const topics = form.get("topics");

		let data = { username, email, password, pincode, topics };

		const response = await fetch("http://localhost:8000/register", {
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
