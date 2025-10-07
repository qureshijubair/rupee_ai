<svelte:head>
<title>Logout Page • Rupee AI</title>
<meta name="description" content="Logout Page, Rupee AI" />
</svelte:head>

<div class="container mt-3 mb-5">
<div class="row mx-auto">
	<div class="row mx-auto my-5 text-center">
			<h4>Are you sure you want to Logout ?</h4>
			<form method="POST" action="/logout">
				<button class="btn btn-outline-dark" type="submit">Log Out</button>
			</form>
	</div>
</div>
</div>

<style>
	h4 {
		color: var(--bs-dark);
	}
</style>