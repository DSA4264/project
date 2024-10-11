import App from './App.svelte';

const app = new App({
  target: document.getElementById('app'),  // This should match <div id="app"> in index.html
});

export default app;
