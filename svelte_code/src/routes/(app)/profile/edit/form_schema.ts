import { dev } from "$app/environment";
import { z } from "zod";

let min_password_length = 8;
if (dev) {
	min_password_length = 2;
}

let pincode = z.string()
		.length(6, "pincode should be of length 6")
		.regex(/^\d+$/)


export const formSchema = z.object({
	username: z
		.string()
		.min(1)
		.regex(/^[a-zA-Z0-9_]+$/, "Only alphabet, numbers and _ are allowed"),
	email: z.string().email(),
	name: z
		.string()
		.min(1)
		.regex(/^[a-zA-Z ]+$/, "Only alphabet, and space are allowed"),
	address: z
		.string(),
	latitude: z
		  .number(),

	longitude: z
		  .number(),

	topics: z.array(
		z
			.string()
			.min(1)
			.regex(/^[^,]+$/),
	),
});

export type FormSchema = typeof formSchema;
