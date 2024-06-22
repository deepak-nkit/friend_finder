import { error, json, redirect } from "@sveltejs/kit";

/** @type {import('./$types').Actions} */



/** @type {import('./$types').PageServerLoad} */
export const load = async({ cookies }) => {
	const token = cookies.get("session_token");
	if (token === undefined) {
		redirect (303,"/login")
	}
	console.log("!!!!!!!!!!!!!!!!!")
	const response = await fetch("http://localhost:8000/suggestion", {
		method: "GET",
		headers: {
			authorization: token,
		},
	});
	console.log("@@@@@@@@@@@@@@@   ",response)
	if (response.status === 401) {
		redirect(303, "/login");
	}else if(!response.ok){
			return error(500 , "Somthing Went Wrong")
			}
	console.log("***************************")
	let data = JSON.stringify(response)
	console.log("^^^^^^----",data)
	return {
		"suggestion": JSON.stringify(response)
	}
};


// /** @type {import('./$types').Actions} */
// export const actions = {
// 	default: async (event) => {
// 		const form = await event.request.formData();
// 		const email = form.get("email");
// 		const password = form.get("password");
// 		let data = { email, password };
// 		const response = await fetch("http://localhost:8000/login", {
// 			method: "POST",
// 			headers: { "Content-Type": "application/json" },
// 			body: JSON.stringify({
// 				email,
// 				password,
// 			}),
// 		});

// 		if (!response.ok) {
// 			return error(505, { message: "Invalid email or Password" });
// 		} else {
// 			const data = await response.json();
// 			let token = data.session_token;

// 			event.cookies.set("session_token", token, {
// 				maxAge: 3600 * 24 * 365 * 100,
// 				path: "/",
// 			});
// 			redirect(303, "/");
// 		}
// 	},
// }






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
			redirect(303, "/login");
		}
	},
};
