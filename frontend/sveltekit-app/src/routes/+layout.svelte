<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { invalidate } from '$app/navigation';
  import rise_ai_logo_1 from '$lib/images/logo_hires_transparent.png';

  export let data;

  let scrollYPosition = 0;

  // WARNING: Potential memory leak. Re-evaluate the need for this interval and consider alternate data fetching strategies.
  onMount(() => {
    const interval = setInterval(() => {
      invalidate('/'); // Why are you constantly invalidating the home route? This is likely causing unnecessary load.
    }, 2000);
    return () => clearInterval(interval);
  });

  let showMobileMenu = false; // More descriptive variable name

  function capitalizeFirstLetter(string) {
    return string.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  }

  function urlNavigate(str, i = 3) {
    const regex = new RegExp(`(?:[^/]*\/){${i}}`);
    const match = str.match(regex);
    return match ? [match[0].replace(/\/$/, ''), str.slice(match[0].length)] : [str, ''];
  }
</script>

<svelte:window bind:scrollY={scrollYPosition} />

<div class="app">
  <header class="sticky top-0 z-50 bg-white border-b-4 border-gray-800">  
    <nav class="container mx-auto py-2 flex items-center justify-between">
      <div class="flex items-center">
        <a href="/" aria-label="Rise AI Logo" target="_blank">
          <img src={rise_ai_logo_1} alt="Rise AI logo" class="w-24 h-auto" />
        </a>
        <span class="ml-2 text-2xl font-bold text-gray-800"><i class="bi bi-currency-rupee mr-[-0.3125rem]"></i>upee AI</span>
      </div>
      <button 
        class="md:hidden p-2 rounded-md bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-white"
        on:click={() => showMobileMenu = !showMobileMenu}
      >
        {#if showMobileMenu}
          <i class="bi bi-x"></i>
        {:else}
          <i class="bi bi-list"></i>
        {/if}
      </button>
      <div class="hidden md:flex space-x-4">
        <a href="/" class:active={$page.url.pathname === '/'} class="nav-link">Home</a>
        <a href="/about" class:active={$page.url.pathname === '/about'} class="nav-link">About</a>
        <a href="/chat" class:active={$page.url.pathname === '/chat'} class="nav-link">Chat</a>
        {#if data.loginStatus}
          <a href="/logout" class="nav-link inline-flex items-center" class:active={$page.url.pathname === '/logout'}>Logout <i class="bi bi-unlock-fill ml-1"></i></a>
        {:else}
          <a href="/login" class="nav-link inline-flex items-center" class:active={$page.url.pathname === '/login'}>Login <i class="bi bi-lock-fill ml-1"></i></a>
        {/if}
      </div>
    </nav>
    {#if showMobileMenu}
      <div class="md:hidden bg-white absolute top-full left-0 w-full border border-gray-300 rounded-b-md">
        <a href="/" class="block px-4 py-2 hover:bg-gray-100">Home</a>
        <a href="/about" class="block px-4 py-2 hover:bg-gray-100">About</a>
        <a href="/chat" class="block px-4 py-2 hover:bg-gray-100">Chat</a>
        {#if data.loginStatus}
          <a href="/logout" class="block px-4 py-2 hover:bg-gray-100">Logout</a>
        {:else}
          <a href="/login" class="block px-4 py-2 hover:bg-gray-100">Login</a>
        {/if}
      </div>
    {/if}
    <div class="fixed bottom-3 right-3" class:hidden={scrollYPosition === 0}>
      <a href="{$page.url.pathname}" class="bg-green-500 text-white p-2 rounded-full">
        <i class="bi bi-caret-up-fill"></i>
      </a>
    </div>
  </header>


  {#if $page.url.pathname !== '/'}
    <div class="container mx-auto my-3">
      <nav aria-label="breadcrumb">
        <ol class="flex justify-center">
          {#each $page.url.pathname.split('/') as route, i}
            {#if i === 0}
              <li class="breadcrumb-item text-gray-500">
                  <a href="/" class="text-gray-800 hover:underline">Home</a>
              </li>
            {:else}
                <li class="mx-2 text-gray-500">
                  {#if i === $page.url.pathname.split('/').length - 1}
                    {capitalizeFirstLetter(route.replace(/-/g, ' '))}
                  {:else}
                    <a href="{urlNavigate($page.url.pathname, i + 1)[0]}" class="text-gray-800 hover:underline">{capitalizeFirstLetter(route.replace(/-/g, ' '))}</a>
                  {/if}
                </li>
            {/if}
          {/each}
        </ol>
      </nav>
    </div>
  {/if}

  <main>
    <slot />
  </main>


  <footer class="bg-white border-t-4 border-gray-800 mt-8">
    <div class="container mx-auto py-8">
      <div class="flex flex-col lg:flex-row justify-between">
        <div class="lg:w-7/12 mb-6 lg:mb-0">
           <a href="/" target="_blank" aria-label="Rise AI Logo" class="flex items-center justify-center md:justify-start mb-3">
                  <img src={rise_ai_logo_1} alt="Rise AI Logo" class="w-24 h-auto" />
            </a>
          <h3 class="text-xl md:text-2xl font-bold text-gray-800 text-center md:text-left mb-3"><i class="bi bi-currency-rupee mr-[-0.3125rem]"></i>upee AI</h3>
          <p class="text-gray-500 text-center md:text-left">Your Personal Finance Assistance Chatbot</p>
        </div>
        <div class="lg:w-5/12"></div>
      </div>
      <div class="border-t border-gray-300 pt-5 mt-8 text-gray-500 text-sm flex flex-col sm:flex-row justify-between items-center">
        <p>© 2025 Rupee AI. All rights reserved.</p>
        <p>By <a href="mailto:services.nrsgn@8shield.net" target="_blank" class="text-gray-800 hover:underline"><i class="bi bi-currency-rupee mr-[-0.3125rem]"></i> AI Labs</a></p>
      </div>
    </div>
  </footer>
</div>

<style lang='postcss'>
  
  @import '../app.css';
  
  .nav-link {
    @apply text-gray-800 hover:text-white hover:bg-gray-800 py-2 px-4 rounded-md transition duration-300;  /* Apply Tailwind styles here */
    @apply relative; /* Fix for active link styling */
  }

  .nav-link.active {
    @apply bg-gray-800 text-white; /* Styles for active link */
  }

   /* Breadcrumb styles: these would be better in the component or global CSS. */
   .breadcrumb-item {
      @apply text-gray-500;
   }
</style>