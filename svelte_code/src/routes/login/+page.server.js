import { error, json, redirect } from "@sveltejs/kit";
/** @type {import('./$types').Actions} */

/** @type {import('./$types').PageServerLoad} */
export async function load({ cookies }) {
	// const id = cookies.get("id")
	const token = cookies.get("session_token");
	if (token !== undefined && token !== "") {
		const response = await fetch("http://localhost:8000/loged_in", {
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
		const email = form.get("email");
		const password = form.get("password");
		const response = await fetch("http://localhost:8000/login", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				email,
				password,
			}),
		});

		if (!response.ok && response.status !== 400) {
			return error(505, { message: `Some error occurred. [status=${response.status}]` });
		} else if (response.status === 400) {
			return {
				success: false,
				message: "Invalid username or password",
				status: response.status
			}
		}
		else {

			
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
