import { z } from "zod";
 
export const formSchema = z.object({
  content: z.string().regex(/[^ ]/).transform(x => x.trim()),
  client_id: z.string().uuid()
});
 
export type FormSchema = typeof formSchema;


