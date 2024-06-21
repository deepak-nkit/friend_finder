import { error, json, redirect } from "@sveltejs/kit";

/** @type {import('./$types').Actions} */

/**
...  token check by server
...   
*/

// /** @type {import('./$types').PageServerLoad} */
// export async function load({ cookies }) {
// 	const token = cookies.get("session_token");
// 	if (token !== undefined) {
// 		const response = await fetch("http://localhost:8000/loged_in", {
// 			method: "GET",
// 			headers: {
// 				authorization: token,
// 			},
// 		});
// 		if (!response.ok) {
// 			redirect(303, "/");
// 		}
// 	}
// }

/** @type {import('./$types').Actions} */
export const actions = {
	logout: async (event) => {
		console.log("------------------------------**--")
		const token = event.cookies.get("session_token");
		console.log(token)
		if (token !== undefined) {
			const response = await fetch("http://localhost:8000/logout", {
				method: "POST",
				headers: {
					authorization: token,
				},
			});
			console.log(response)
			event.cookies.set("session_token",'',{
				maxAge:1,
				path:("/")

			})
			redirect(303,"/login")
		}
	},
};
