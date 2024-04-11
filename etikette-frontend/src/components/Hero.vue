<template>
    <section class="hero" :style="{ backgroundImage: `url('${image}')` }">
        <div class="hero-body container">
            <slot>
                <h1>Hero Section</h1>
                <span class="hero-subtitle">Subtitle</span>
                <div class="hero-button-wrapper">
                    <div class="btn btn-hero btn-primary">Get Started</div>
                </div>
                <span class="hero-subtitle"></span>
                <div class="hero-buttons"></div>
            </slot>
        </div>
    </section>
</template>

<script>
export default {
    props: {
        image: {
            type: String,
            default: '',
        }
    }
}
</script>

<style lang="scss">

.hero {
    display: flex;
    align-items: center;
    min-height: calc(100vh - var(--navbar-height));
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

.hero-body {
    text-align: center;
}

.hero h1,
.hero-title {
    font-size: 60px;
    margin-bottom: 10px;
}

.hero-subtitle {
    display: block;
    font-size: 36px;
    margin-bottom: 30px;
}

.hero-button-container {
    display: flex;
    gap: 15px;
}

.hero-button {
}
</style>