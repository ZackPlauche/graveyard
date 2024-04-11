
<template>
    <header>
        <Navbar>
            <transition name="fade" mode="out-in">
                <ul class="nav-link-list" key="admin-menu" v-if="$route.path.includes('admin')">
                    <li><router-link class="nav-link" :to="{ name: 'Dashboard' }">Dashboard</router-link></li>
                    <li><router-link class="nav-link" :to="{ name: 'Home' }">Logout</router-link></li>
                </ul>
                <ul class="nav-link-list" v-else>
                    <li><router-link class="nav-link" :to="{ name: 'Home' }">Home</router-link></li>
                    <li><router-link class="nav-link" :to="{ name: 'Pricing' }">Pricing</router-link></li>
                    <li><router-link class="nav-link" :to="{ name: 'Login' }">Login</router-link></li>
                    <li><router-link class="nav-link" :to="{ name: 'Register' }">Sign Up</router-link></li>
                </ul>
            </transition>
        </Navbar>
    </header>
    <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
            <component :is="Component"></component>
        </transition>
    </router-view>
</template>

<script>
import Navbar from '@/components/Navbar.vue'

export default {
    components: {
        Navbar
    }
}

</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Urbanist&display=swap');

* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

$primary: #21abde;
$secondary: #dedb21;
$warning: #c2bf20;
$success: #1ab81a;
$danger: red;
$dark: #1b1b1b;
$black: #000;


$colors: (primary: $primary,
  primary-light: lighten($primary, 20%),
  primary-superlight: lighten($primary, 40%),
  secondary: $secondary,
  secondary-light: lighten($secondary, 20%),
  secondary-superlight: lighten($secondary, 40%),
  dark: $dark,
  dark-light: lighten($dark, 20%),
  dark-superlight: lighten($dark, 40%),
  success: $success,
  success-light: lighten($success, 20%),
  success-superlight: lighten($success, 40%),
  danger: $danger,
  danger-light: lighten($danger, 20%),
  danger-superlight: lighten($danger, 40%),
  warning: $warning,
  warning-light: lighten($warning, 20%),
  warning-superlight: lighten($warning, 40%),
  "black": black,
);

$background-colors: (
  primary: white,
  secondary: whitesmoke,
);

.theme-dark {
    --secondary-bg: #1b1b1b;
    --primary-bg: black;
    --text-color: white;
}

:root {
  --base-font: 'Quicksand', sans-serif;
  --display-font: 'Urbanist', sans-serif;
  --text-color: black;
  --text-dark: $dark;

  @each $color-name, $color in $colors {
    --#{$color-name}: #{$color};
  }

  @each $color-name, $color in $background-colors {
    --#{$color-name}-bg: #{$color};
  }
}

body {
  font-family: var(--base-font);
  color: var(--text-color);
  background-color: var(--primary-bg);
}

button {
    background-color: transparent;
    border: none;
}

header {
    position: relative;
}

a {
  color: var(--primary);
}

button {
  font-family: var(--base-font);
}

header {
  position: sticky;
  top: 0;
  z-index: 1000;
}


h1, .h1 { font-size: 60px }
h2, .h2 { font-size: 40px }
h3, .h3 { font-size: 36px }
h4, .h4 { font-size: 32px }
h5, .h5 { font-size: 28px }
h6, .h6 { font-size: 24px }

.lead {
  font-size: 24px;
  color: var(--dark);
}

h1, h2, h3, h4, h5, h6, p, ul, li, div {
    color: var(--text-color);
}

// Fontawesome Icons 
.fas { vertical-align: middle; }

// Utilities

.container {
  margin: 0 auto;
  width: 95%;
  max-width: 1400px;
}

.flex {display: flex}
.flex-center { 
    justify-content: center;
    align-items: center;
}
.justify-center { justify-content: center }
.align-center { align-items: center }

.block {display: block}

.text-center { text-align: center }
.text-left { text-align: left }
.text-right { text-align: right }

.vh-100 { min-height: 100vh }
.w-100 { width: 100% }

.pt-1 { padding-top: 10px }
.pt-2 { padding-top: 20px }
.pt-3 { padding-top: 30px }
.pt-4 { padding-top: 40px }
.pt-5 { padding-top: 50px }

.pb-1 { padding-bottom: 10px }
.pb-2 { padding-bottom: 20px }
.pb-3 { padding-bottom: 30px }
.pb-4 { padding-bottom: 40px }
.pb-5 { padding-bottom: 50px }

.py-1 { padding: 10px 0 }
.py-2 { padding: 20px 0 }
.py-3 { padding: 30px 0 }
.py-4 { padding: 40px 0 }
.py-5 { padding: 50px 0 }

.mb-1 { margin-bottom: 10px }
.mb-2 { margin-bottom: 20px }
.mb-3 { margin-bottom: 30px }
.mb-4 { margin-bottom: 40px }
.mb-5 { margin-bottom: 50px }

.mx-auto {margin: 0 auto}

.background-image {
    position: absolute;
    height: 100%;
    width: 100%;
    object-fit: cover;
    object-position: center;
    z-index: -1;
}

// Positions

.absolute { position: absolute }
.relative { position: relative }

.top {top: 0}
.right {right: 0}
.bottom {bottom: 0}
.left {left: 0}
.inset {inset: 0}

.middle {
  left: 50%;
  transform: translateX(-50%);
}

// Text Colors
@each $color-name in map-keys($colors) {
  .text-#{$color-name} {
    color: var(--#{$color-name})
  }
}

.text-white {
  color: white;
  --text-color: white;
}

// Background Colors
@each $color-name in map-keys($background-colors) {
  .bg-#{$color-name} {
    background-color: var(--#{$color-name}-bg);
  }
}

// Buttons

.btn {
  display: inline-block;
  border: none;
  cursor: pointer;
  white-space: nowrap;
  outline: none;
  text-decoration: none;
  transition: background-color .2s ease, color .2s ease, border .2s ease, box-shadow .2s ease;
  padding: 10px 20px;
  font-size: 18px;
  border-radius: 5px;
  -webkit-tap-highlight-color: transparent;
}

@each $color-name,
$color in $colors {
  .btn-#{$color-name} {
    background-color: $color;
    color: white;

    &:hover {
      background-color: lighten($color, 12.5%);
    }
  }
}


.btn-sm {
  padding: 10px 15px;
}

.btn-md {
  padding: 15px 20px;
  font-size: 18px;
  border-radius: 5px;
}

.btn-hero {
  padding: 20px 25px;
  font-size: 28px;
  font-weight: 500;
  border-radius: 5px;
}

.btn-disabled {
    background-color: lightgrey;
    color: white;
}

// Overlay 

.overlay {
  position: relative;

  &>* {
    position: relative;
    z-index: 1;
  }

  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
  }

  &-dark::after {
    background-color: black
  }

  &-light::after {
    background-color: white
  }

  @for $num from 1 through 9 {
    &-#{$num}::after {
      opacity: $num * .1
    }
  }
}


input:not([type="checkbox"]):not([type="color"]),
textarea,
select {
  padding: 10px;
  font-size: 18px;
  border: none;
  box-shadow: inset 0 0 0 1px lightgrey;
  border-radius: 5px;
  transition: box-shadow .2s ease;
  outline: none;
  width: 100%;
  font-family: var(--base-font);
  background-color: var(--primary-bg);
  color: var(--text-color);
  -webkit-tap-highlight-color: transparent;

  &:hover,
  &:focus {
    box-shadow: inset 0 0 0 1px var(--primary-light);
  }

  @at-root .field.field-danger & {
    box-shadow: inset 0 0 0 1px var(--danger-light);
  }
}

.field {
  width: 100%;

  &:not(:last-of-type) {
    margin-bottom: 10px;
  }
}

.field-row {
  display: flex;
  width: 100%;
  gap: 10px;
  white-space: nowrap;
}

fieldset {
  border: none;
  margin-bottom: 20px;
}

label {
  color: var(--text-dark);
  font-size: 18px;
  display: block;
}

form label {
  margin-bottom: 5px;
}


// Transitions

.fade-enter-active,
.fade-leave-active {
  transition: opacity .3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// Animations

@keyframes fade-in {
    from { opacity: 0}
    to {opacity: 1}
}

.fade-in {
    animation: fade-in .3s ease;
}

.ghost { opacity: .5 }

</style>
