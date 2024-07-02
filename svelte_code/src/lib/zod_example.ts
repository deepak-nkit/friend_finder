import {z} from 'zod'


const UserInformation = z.object({
  name: z.string().email(),
  age: z.number()
})


UserInformation.parse({name: "ankit@a.com", age: 3})

