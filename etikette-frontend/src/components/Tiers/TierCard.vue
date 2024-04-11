<template>
    <router-link to="" class="pricing-card" :class="{ recommended: recommended }">
        <div class="text-center">
            <h3 class="pricing-card-title mb-1">{{ title }}</h3>
            <div v-if="recommended" class="pricing-card-recommended-banner">⭐ Recommended ⭐</div>
            <div class="pricing-card-price mb-1">${{ price }}</div>
        </div>
        <div v-if="features && features.length > 0" class="pricing-card-features">
            <div class="pricing-card-subtitle text-center mb-2">Includes</div>
            <ul class="pricing-card-features-list">
                <li v-if="specialFeature" class="pricing-card-special-feature">{{ specialFeature }}</li>
                <li v-for="feature in features" class="pricing-card-feature">{{ feature }}</li>
            </ul>
        </div>
        <button class="btn pricing-card-button w-100">Select</button>
    </router-link>
</template>

<script>
export default {
    props: {
        title: String,
        price: Number,
        features: {
            type: Array,
            default: [],
        },
        recommended: Boolean,
        previousTitle: String,
        specialFeature: String,
    }
}
</script>

<style lang="scss">

$pricing-card-padding: 20px;

    .pricing-card-list {
        display: flex;
        list-style: none;
        gap: 20px;
        justify-content: center;
        align-items: center;
        
        @media screen and (max-width: 1300px) {
            flex-flow: column;
            gap: 30px;
        }
    }

    .pricing-card {
        display: block;
        text-decoration: none;
        box-shadow: 0 .5px 2px grey;
        max-width: 400px;
        width: 400px;
        transition: transform .3s ease;
        padding: $pricing-card-padding;
        border-radius: 15px;
        background-color: var(--primary-bg);
        
        &:hover {
            transform: translateY(-5px);
        }
    }


    .pricing-card-subtitle {
        font-size: 28px;
        font-weight: 500;
    }

    .pricing-card-price {
        font-size: 24px;
    }

    .pricing-card-features {
        margin-bottom: 15px;
    }

    .pricing-card-feature {
        text-align: left;
        padding: 5px 0 5px 10px;;
        font-size: 18px;
        list-style: inside;

        &:not(:last-of-type) {
            border-bottom: 1px solid lightgrey;
        }
        
    }
    
    .pricing-card-button {
        font-size: 20px;
    }
    
    .pricing-card-button {
        border-radius: 5px;
        background-color: white;
        color: black;
        border: 1px solid black;
    }
    
    .pricing-card:hover .pricing-card-button {
        background-color: var(--primary);
        color: white;
        border: 1px solid var(--primary);
    }
    
    .pricing-card-recommended-banner {
        background-color: var(--primary-superlight);
        padding: 7.5px;
        margin: 0 (-$pricing-card-padding) 10px;
        font-size: 16px;
        font-weight: 600;
    }

    .pricing-card-special-feature {
        margin: 0 (-$pricing-card-padding);
        background-color: #d2ffd2;
        list-style: none;
        padding: 7.5px 30px;
        font-weight: 600;
        margin-bottom: 10px;
    }

</style>