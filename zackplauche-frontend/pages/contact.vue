<template>
  <div class="grid place-content-center min-h-screen-navbar px-5 bg-cover bg-center bg-fixed" style="background-image: url('/zion-the-lion-xpxS5sNzhmQ-unsplash.jpg')">
    <Form @submit.prevent="submitForm()">

      <header class="text-center">
        <h1 class="text-7xl font-serif text-blue-dark">Get In Touch</h1>
        <p class="mt-2">Have a business inquiry? Tell me about your project below!</p>
      </header>

      <div class="flex gap-5">
        <Field type="text" name="First name" placeholder="Bob" required v-model="formData.firstName" />
        <Field type="text" name="Last name" placeholder="Ross" required v-model="formData.lastName" />
      </div>
      <Field type="email" name="Email" placeholder="rossman@bobross.com" required />
      <Field type="textarea" name="Reason For Contact" required placeholder="I'm looking for help with..." />

      <button type="submit" class="btn bg-blue-dark hover:bg-blue focus:bg-blue text-white rounded-lg mt-5 w-full py-2">Submit</button>
    </Form>
  </div>
</template>

<script setup>  
const formData = ref({
  firstName: '',
  lastName: '',
  email: '',
  message: '',
})

const initialFormData = formData.value

const submitForm = () => {
  let data = formData.value 
  // Do something.
  formData.value = initialFormData
}

useHead({ title: 'Contact' })
</script>