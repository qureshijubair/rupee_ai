<svelte:head>
	<title>Login Page • Rupee AI</title>
	<meta name="description" content="Login Page, Rupee AI" />
</svelte:head>

<script>
  import Captcha from '$lib/components/Captcha.svelte';
  import { captchaValue } from '../stores.js';

  let captchaComponent;
  let captchaResponse = "";  // Store the captcha input
  let email = "";
  let password = "";
  let rememberMe = false;
  let formError = ""; // Store the specific error message
  let captchaSolved = false; // Track captcha status


  function handleCaptchaSubmit(isCorrect) {  // Receive the boolean from Captcha
    captchaSolved = isCorrect;
    if (captchaSolved) {
      captchaResponse = $captchaValue; // Set the validated captcha value
    }
  }

  async function handleLogin() {
    // Ensure captchaResponse is reset on each login attempt
    captchaResponse = ""; 
    captchaSolved = false;
    if (!captchaComponent.submitCaptcha()) { // Directly call submitCaptcha on component instance.
      console.error("Captcha not yet solved");
      formError = "Please solve the CAPTCHA";
      return;
    }

    try {
      const response = await fetch('/api/login', {
        // ...other options
        body: JSON.stringify({ 
          email, 
          password, 
          captcha: $captchaValue,  // Access the value from the store directly
          rememberMe 
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json(); // Get error data from response
        formError = errorData.message || "Login failed";  // Set the error message
      }

      else {
        formError = ""; // Clear any previous error
        const data = await response.json();
        console.log("Login successful:", data);
        // ... redirect or update UI as needed ...
      }
    } 
    catch (error) {
      formError = "A network error occurred."; // Handle network or other errors
      console.error("Login error:", error);
    }
  }
</script>

<div class="container mx-auto mt-6 mb-10 max-w-md">
  <div class="bg-white p-6 rounded-lg shadow-md">
      <h3 class="text-2xl font-semibold text-gray-800 mb-4">Please sign in</h3>

      <form on:submit|preventDefault={handleLogin}>
        <div class="mb-4">
          <label for="email" class="block text-gray-700 text-sm font-bold mb-2">Email address</label>
          <input type="email" bind:value={email} id="email" name="email" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" required>
        </div>

        <div class="mb-4">
          <label for="password" class="block text-gray-700 text-sm font-bold mb-2">Password</label>
          <input type="password" bind:value={password} id="password" name="password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" required>
        </div>

        <div class="mb-6 flex items-center">
          <input type="checkbox" bind:checked={rememberMe} id="rememberMe" class="rounded text-indigo-600 focus:ring-0">
          <label for="rememberMe" class="ml-2 text-sm text-gray-700">Remember me</label>
        </div>

        <Captcha bind:this={captchaComponent} onSubmit={handleCaptchaSubmit} />
        
        <button disabled={!captchaSolved}
          type="submit"
          class="w-full bg-indigo-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
        >
          Log In
        </button>
      </form>

      {#if formError}
        <p class="text-red-500 mt-3 text-center">{formError}</p>
      {/if}
  </div>
</div>

<style lang='postcss'>

  @import '../../app.css';

  /* Most styles are now handled by Tailwind, so you probably don't need this block */
</style>