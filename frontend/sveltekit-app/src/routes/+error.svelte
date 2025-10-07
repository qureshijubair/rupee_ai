<svelte:head>
	<title>Error Page • Rupee AI</title>
	<meta name="description" content="Error Page, Rupee AI" />
</svelte:head>

<script>
	import { page } from '$app/stores';
</script>

<div class="container mt-3 mb-5">
  <div class="row mx-auto">
    <div class="row mx-auto my-5">
      <h4 class="display-4 text-center"> 
        {$page.status}&nbsp; <i class="bi bi-emoji-frown-fill small"></i>
      </h4> 
      <p class="lead text-center">Sorry! The page that you are looking for is {($page.error.message).toLowerCase()}.</p>
      <p class="text-center">Go to <a href="/">Home Page</a> &nbsp;<span>></span></p>
    </div>
  </div>
</div>

<style>
  
</style>