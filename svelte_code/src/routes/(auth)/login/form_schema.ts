/** Zod, form type */
	
import { z } from "zod";
 
export const formSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1, "Password can't be empty")
});
 
export type FormSchema = typeof formSchema;


