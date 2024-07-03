import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";


export const load: PageServerLoad = async ({ cookies }) => {
    const token = cookies.get("session_token");
    if (token !== undefined && token !== "") {
        let client = await BACKEND_API.getClient();

        let response = await client.get_current_user(null, null, {
            headers: {
                Authorization: token,
            },
            validateStatus(status) {
                return [401, 200].includes(status);
            },
        });

        if (response.status == 200) {
            redirect(303, "/");
        }
    }

    return {
        form: await superValidate(zod(formSchema)),
    };
};
