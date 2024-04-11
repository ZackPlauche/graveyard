<template>
    <main class="pricing-page py-5 container">
        <h1 class="text-center mb-3">Pricing</h1>
        <TierCardList :items="tiers" />
    </main>
</template>

<script>
import TierCardList from "../components/Tiers/TierCardList.vue";

// TODO: Link from dynamic_preferences instead of js Array of Objects
const tiers = [
    {
        title: 'Tier 1',
        price: 9.99,
        features: ['thing 1', 'thing 2', 'thing 3'],
        specialfeature: 'everything from tier 2, plus...'
    },
    {
        title: 'Tier 2',
        price: 29.99,
        recommended: true,
    },
    {
        title: 'Tier 3',
        price: 49.99,
    }
]

export default {
    components: {
        TierCardList,
    },
    setup() {
        return { tiers }
    }
};
</script>
