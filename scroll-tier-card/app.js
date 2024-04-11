const App = {
    template: /*html*/
        `<div class="scroll-card-bar">
            <button 
                class="scroll-card-bar-dot button-reset" 
                :class="{ active: currentLevel === 0 }" 
                @click="currentLevel = 0"
                ></button>
            <button 
                v-for="tier in activeTiers" 
                class="scroll-card-bar-dot button-reset" 
                :class="{ active: currentLevel === tier.level }" 
                @click="currentLevel = tier.level"
                ></button>
        </div>

        <transition name="fade">
            <div class="scroll-card-subscription-model" :style="currentLevel !== 0 ? '':'opacity: 0;'">
                <button 
                    class="scroll-card-subscription-model-option button-reset" 
                    :class="{ active: subscriptionModel === 'Monthly' }" 
                    @click="subscriptionModel = 'Monthly'"
                    >Monthly</button>
                <button 
                    class="scroll-card-subscription-model-option button-reset" 
                    :class="{ active: subscriptionModel === 'Annually' }" 
                    @click="subscriptionModel = 'Annually'"
                    >Annually</button>
            </div>
        </transition>

        <transition-group name="fade" mode="out-in">

            <!-- NOTE FOR NON-CODERS & THE CURIOUS: Edit the content inside of this tag to edit the first card -->
            <ScrollCard v-if="currentLevel === 0" :key="0">
                This is a great start. It is clear that you value Peer Networking and benchmarking.
                <br>
                <br>
                Contact us to learn more: <a href="mailto:info@achievenext.com">info@achievenext.com</a>
            </ScrollCard>
            <ScrollCard v-for="(tier, index) in filteredTiers" :tier="tier" :subscription-model="subscriptionModel" :key="tier.level" />

        </transition-group>`,
    components: {
        ScrollCard,
    },
    setup() { return { tiers } },
    data() {
        return {
            currentLevel: 0,
            subscriptionModel: 'Monthly',
        }
    },
    computed: {
        activeTiers() {
            return this.tiers.filter(tier => tier.active)
        },
        filteredTiers() {
            let currentLevel = this.currentLevel
            return this.tiers.filter(tier => currentLevel === tier.level && tier.active) ;
        }
    },
    methods: {
        range: n => Array.from(Array(n).keys())
    }
}

