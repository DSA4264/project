import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 3000,  // Port matches the one in your output
  },
  publicDir: 'public',  // Ensure public assets are correctly served
});
