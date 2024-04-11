


let firstTierContent = `
Some text
`

const tiers = [
    {
        title: 'Basic Subscription',
        level: 1,
        active: false,
        monthlyRate: 20,
        monthlyRateLink: 'https://subscriptions.zoho.com/subscribe/d58df800c51bb801ece92220f7c801166a2bba0f6b053217afe8ded60e8a6aa6/Basicmonthly20',
        annualRate: 199,
        annualRateLink: 'https://subscriptions.zoho.com/subscribe/d58df800c51bb801ece92220f7c801166a2bba0f6b053217afe8ded60e8a6aa6/Basicannual21',
        features: [
            'Single Membership to Peer Network (online platform)',
            'Individual Competency Assessment',
            'Benchmark Reports',
            'Member Pricing for CPE Certified Events (approx. 12 CPEs per year)',
        ]
    },
    {
        title: 'Full Subscription',
        level: 2,
        active: true,
        monthlyRate: 125,
        monthlyRateLink: 'https://subscriptions.zoho.com/subscribe/d58df800c51bb801ece92220f7c801166a2bba0f6b053217afe8ded60e8a6aa6/Monthly20',
        annualRate: 1500,
        annualRateLink: 'https://subscriptions.zoho.com/subscribe/d58df800c51bb801ece92220f7c801166a2bba0f6b053217afe8ded60e8a6aa6/Annual',
        features: [
            'Leadership Assessment with Role/Title Benchmark',
            'LMS access for up to 3 team Members',
            'Benchmarking Diagnostic Tools',
            'SME led online Q&A - Office Hours',
            '1-hour Linkedin profile/bio/resume consultation',
            'AchieveNEXT will provide a recommendation to serve on boards (partner of The Boardlist)',
        ]
    },
    {
        title: 'Performance Cohorts',
        level: 3,
        active: true,
        monthlyRate: 500,
        monthlyRateLink: 'https://subscriptions.zoho.com/subscribe/d58df800c51bb801ece92220f7c801166a2bba0f6b053217afe8ded60e8a6aa6/Cohort_monthly',
        annualRate: 6000,
        annualRateLink: 'https://subscriptions.zoho.com/subscribe/d58df800c51bb801ece92220f7c801166a2bba0f6b053217afe8ded60e8a6aa6/Cohort',
        features: [
            'Group Coaching',
            'Meet every 6 weeks',
            'Private online discussion group', 
            'Personalized Assessment reports',
            'One-time 1-1 session with an executive coach',
            'Quarterly tabletop exercises from leading technical and industry experts',
            'Complimentary access to AchieveNEXT\'s annual conference'
        ]
    }
]


const ScrollCard = {
    template: /*html*/
        `<div class="scroll-card">
            <slot>
                <div class="scroll-card-title">{{ tier.title }}</div>
                <div class="scroll-card-price" style="margin-bottom: 10px;">\${{ price }}<span class="scroll-card-subscription-model-abbreviation">/{{ subscriptionModelAbbr }}</span></div>
                <div class="scroll-card-features">
                    <ul class="scroll-card-features-list">
                        <li v-if="tier.level > 1" style="list-style: none; font-weight: bold; margin-bottom: 10px;">Everything from the previous tier, plus...</li>
                        <li v-for="feature in tier.features" class="scroll-card-feature">{{ feature }}</li>
                    </ul>
                </div>
                <a class="scroll-card-subscribe-button" :href="link">Subscribe</a>
            </slot>
        </div>`,
    props: {
        tier: Object,
        subscriptionModel: String,
    },
    computed: {
        price() { 
            if (this.subscriptionModel === 'Monthly') { return this.tier.monthlyRate }
            else if (this.subscriptionModel === 'Annually') { return this.tier.annualRate}
        },
        subscriptionModelAbbr() {
            if (this.subscriptionModel === 'Monthly') { return 'mo' } 
            else if (this.subscriptionModel == 'Annually') { return 'yr' }
        },
        link() {
            if (this.subscriptionModel === 'Monthly') { return this.tier.monthlyRateLink}
            else if (this.subscriptionModel === 'Annually') { return this.tier.annualRateLink}
        }
    },
}


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

        <transition name="fade" mode="out-in">

            <!-- NOTE FOR NON-CODERS & THE CURIOUS: Edit the content inside of this tag to edit the first card -->
            <ScrollCard v-if="currentLevel === 0">
                <div v-html="firstTierContent"></div>
            </ScrollCard>

            <ScrollCard v-else-if="currentLevel === tiers[0].level && tiers[0].active === true" :tier="tiers[0]" :subscription-model="subscriptionModel"></ScrollCard>
            <ScrollCard v-else-if="currentLevel === tiers[1].level && tiers[1].active === true" :tier="tiers[1]" :subscription-model="subscriptionModel"></ScrollCard>
            <ScrollCard v-else-if="currentLevel === tiers[2].level && tiers[2].active === true" :tier="tiers[2]" :subscription-model="subscriptionModel"></ScrollCard>

        </transition>`,
    components: {
        ScrollCard,
    },
    setup() { return { tiers, firstTierContent } },
    data() {
        return {
            currentLevel: 0,
            subscriptionModel: 'Monthly',
        }
    },
    computed: {

        activeTiers() {
            return this.tiers.filter(tier => tier.active)
        }
    },
    methods: {
        range: n => Array.from(Array(n).keys())
    }
}

const app = Vue.createApp(App)

app.mount('.scroll-card-container')