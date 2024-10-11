<script>
  import { onMount } from "svelte";

  let currentSection = 0;

  // Handle the scrolling behavior
  function handleScroll() {
    const scrollY = window.scrollY;
    const sectionHeight = window.innerHeight;
    currentSection = Math.floor(scrollY / sectionHeight);
  }

  // Add scroll event listener on mount
  onMount(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  });

  // Log when the iframe map is loaded or when it fails to load
  function handleMapLoad() {
    console.log('Map loaded successfully');
  }

  function handleMapError() {
    console.error('Failed to load the map');
  }
</script>

<style>
  #app {
    font-family: Arial, sans-serif;
  }

  .section {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2rem;
    color: white;
    background-color: #333;
  }

  #map-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    z-index: -1;
  }

  iframe {
    width: 100%;
    height: 100%;
    border: none;
  }

  /* Adjust the scrolly-telling content */
  .scrolly-telling-content {
    position: fixed;
    top: 0;
    right: 0; /* Align to the right */
    width: 30%; /* Make it smaller */
    height: 100vh;
    padding: 10px;
    background-color: rgba(0, 0, 0, 0.6); /* Add a slight background for contrast */
    color: white;
    z-index: 1;
    overflow-y: auto; /* Allow scrolling within the content */
  }

  .section {
    margin-bottom: 50px;
    text-align: left; /* Align text to the left */
  }
</style>

<!-- Map Container -->
<div id="map-container">
  <iframe 
    src="/mrt_tagged_bus_stops_map.html" 
    title="MRT Tagged Bus Stops Map"
    on:load={handleMapLoad}
    on:error={handleMapError}>
  </iframe>
</div>

<!-- Scrolly-telling Content (moved to right and made smaller) -->
<div class="scrolly-telling-content">
  <div class="section" style="background-color: #1e1e1e">
    <h2>Scroll Down to Explore - Section {currentSection}</h2>
  </div>

  <div class="section" style="background-color: #2e2e2e">
    <h2>MRT and Bus Stops Integration - Section {currentSection}</h2>
  </div>

  <div class="section" style="background-color: #3e3e3e">
    <h2>Optimal Bus Routes - Section {currentSection}</h2>
  </div>

  <div class="section" style="background-color: #4e4e4e">
    <h2>Data Insights - Section {currentSection}</h2>
  </div>
</div>
