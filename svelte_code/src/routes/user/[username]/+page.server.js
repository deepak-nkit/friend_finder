import { error, json, redirect } from "@sveltejs/kit";
/** @type {import('./$types').Actions} */

/** @type {import('./$types').PageServerLoad} */
export const load = async ({ params,  cookies }) => {
	const token = cookies.get("session_token");
	const username = params.username
	if (token === undefined || token == "") {
		redirect(303, "/login");
	}
	const response = await fetch(`http://localhost:8000/user_profile/${username}`,{
		method: "GET",
		headers: {
			authorization: token,
		},
	});
	if (!response.ok) {
		return error(500, "Somthing Went Wrong");
	} else{
			const data = await response.json();
			return data ;
			}
};
	