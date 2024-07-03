import { z } from "zod";
 
export const formSchema = z.object({
  content: z.string().regex(/[^ ]/).transform(x => x.trim()),
});
 
export type FormSchema = typeof formSchema;


