// vite.config.js

export default ({
  base: './',
  build: {
    rollupOptions: {
      input: {
        main: './index.html'
      }
    }
  }
})
