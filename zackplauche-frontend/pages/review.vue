<template>
  <!-- <div class="min-h-screen-navbar grid place-content-center px-5 py-10 bg-center bg-cover bg-no-repeat bg-fixed"
    style="background-image: url('/paul-pastourmatzis-8kDOOrs608I-unsplash.jpg')">
    <Form @submit.prevent="submitForm">
      <header class="text-center">
        <h1 class="text-6xl md:text-7xl text-blue-dark font-serif">Write a Review</h1>
      </header>
      <Field type="textarea" name="Review" v-model="reviewData.text" required placeholder="Write your review here..."/>
      <Field type="file" name="Good Image of Yourself" ref="clientImageField" required />
      <div class="flex gap-5">
        <Field name="First name" v-model="reviewData.clientFirstName" required />
        <Field name="Last name" v-model="reviewData.clientLastName" required />
      </div>
      <div class="flex gap-5">
        <Field name="Role" v-model="reviewData.clientRole" required />
        <Field name="Company" v-model="reviewData.clientCompany" required />
      </div>
      <button type="submit" class="btn w-full bg-blue hover:bg-light-blue transition-colors rounded-lg">Submit</button>
    </Form>
  </div> -->
</template>

<script setup>
// 
// const { reviewModel } = useModels()


// const router = useRouter()

// const reviewData = ref({
//   text: '',
//   clientFirstName: '',
//   clientLastName: '',
//   clientRole: '',
//   clientCompany: '',
// })

// const clientImageField = ref(null)

// const submitForm = async () => {
//   // const clientImage = clientImageField.value.input.files[0]
//   // const formData = new FormData()
//   // for (let [key, value] of Object.entries(reviewData.value)) { formData.append(key, value) }
//   // let newModel = await reviewModel.post(formData)
//   // if (newModel && newModel.id) {
//     // router.push({ name: 'index' })
//   // }
// }

// useHead({ title: 'Write a Review' })
</script>