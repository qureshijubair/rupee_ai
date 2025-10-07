<svelte:head>
	<title>Home Page • Rupee AI</title>
	<meta name="description" content="Home Page, Rupee AI" />
</svelte:head>

<script>
	
</script>

<div class="container-fluid mt-4 mb-5">
	<div class="row mx-auto my-5 section-1">
		<div class="col-lg-12 mb-5 mb-lg-0">
			<p><span class="fs-4"><i class="bi bi-exclamation-triangle"></i></span> You need to <a href="/login">login</a> to continue...</p>
			<a class="btn btn-outline-dark" href="/chat">Let's Chat&nbsp;<span class="blink">></span></a>
		</div>
	</div>
</div>

<style>
	.blink {
    text-decoration: blink;
    animation-name: blinker;
    animation-duration: 1.25s;
    animation-timing-function: ease-in-out;
    animation-iteration-count:infinite;
  }
  @keyframes blinker {
    0% {opacity: 1.0;}
    75% {opacity: 0.0;}
  }

	/* Large devices (desktops, 992px and up) */
	@media (min-width: 992px) {
	}
</style>