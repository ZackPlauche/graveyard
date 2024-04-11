// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss',
  ],
  app: {
    pageTransition: {
      name: 'fade',
      mode: 'out-in',
    },
    head: {
      script: [
        // Google Tag Manager Script
        {
          innerHTML: `
                (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
                new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
                j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
                'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
                })(window,document,'script','dataLayer','GTM-KXQVQRCW');
              `
        },
        // Font Awesome Script
        { src: "https://kit.fontawesome.com/bf84f62aca.js", crossorigin: "anonymous" },
      ],
      link: [
        // Google Fonts Link
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        // @ts-ignore
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: true },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com' },
        // Google Font Stylesheet Links
        {
          rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Bentham&family=Montserrat:wght@100;200;300;400;500;600;700;800;900&display=swap'
        },
        // Favicon
        { rel: 'shortcut icon', href: '/zp-blue-favicon-128-round.png', type: 'image/x-icon' }
      ]
    },
  },
  runtimeConfig: {
    public: {
      apiUrl: process.env.NUXT_PUBLIC_API_URL || 'https://api.zackplauche.com',
    }
  }
})
