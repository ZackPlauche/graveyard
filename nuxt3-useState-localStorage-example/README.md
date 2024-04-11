# Nuxt 3 useState localStorage example
Example project to see how to avoid a few 500 errors when trying to use localStorage

## Main Code 
```ts
// composables/useUsers.ts
interface User { 
  name: string
}

export const useUsers = () => {
  const users = useState<User[]>('users', () => [])

  if (process.client) {  // <- MUST HAVE WRAPPED AROUND WHERE YOU WANT TO USE localStorage
    users.value = JSON.parse(localStorage.getItem('users') || '[]')
  }

  const createUser = (user: User) => {
    users.value.push(user)
    if (process.client) { // <- Everytime
      localStorage.setItem('users', JSON.stringify(users.value))
    }
  }

  return { users, createUser }
}
```