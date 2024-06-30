import { error, json, redirect } from "@sveltejs/kit";
/** @type {import('./$types').Actions} */
import { Backend_Base_URL } from "$lib/backend_url";


/** @type {import('./$types').PageServerLoad} */
export const load = async ({ params,  cookies }) => {
	const token = cookies.get("session_token");
	const user_id = params.user_id
	console.log("$$$$$$$",user_id)
	if (token === undefined || token == "") {
		redirect(303, "/login");
	}
	const response = await fetch(`${Backend_Base_URL}:8000/get_message/${user_id}`,{
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



/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ cookies, request , params }) => {
		const data = await request.formData();
		const user_id = params.user_id
		const token = cookies.get("session_token")
		const message = data.get('message');
		if (token !== undefined){
			const response = await fetch(`${Backend_Base_URL}:8000/message_set/${user_id}`,{
				method:"POST",
				headers: {
						authorization: token,
				},
				body: JSON.stringify(message)
				}) 
				if(!response.ok)
				{
					return error(505, {
					message: `Some error occurred. [status=${response.status}]`,
			});
				} else{
					const data = await response.json()
					console.log(data)
					return {data}
				}

  	} 
		return { success: false };
	},

};