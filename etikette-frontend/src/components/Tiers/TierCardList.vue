<template>
<ul class="pricing-card-list">
    <li v-for="item in items">
        <PricingCard v-bind="item"></PricingCard>
    </li>
</ul>
</template>

<script>
import PricingCard from './TierCard.vue'

export default {
    components: {
        PricingCard
    },
    props: {
        items: Array
    }
}
</script>

<style lang="scss">
</style>