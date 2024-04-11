interface User { 
  name: string
}

export const useUsers = () => {
  const users = useState<User[]>('users', () => [])

  if (process.client) {
    users.value = JSON.parse(localStorage.getItem('users') || '[]')
  }

  const createUser = (user: User) => {
    users.value.push(user)
    if (process.client) {
      localStorage.setItem('users', JSON.stringify(users.value))
    }
  }

  return { users, createUser }
}