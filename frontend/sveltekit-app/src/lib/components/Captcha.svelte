<script>
	import { onMount } from "svelte";
	import { captchaValue } from '../../routes/stores.js';

	export let onSubmit; // Callback prop

	let captchaInputText = '';
	let outputOk = '';
	let outputNotOk = '';
	let noCaptchaTextEntered = '';

	let canvas;
	let ctx;
	let captchaText = '';

	// alphaNums contains the characters with which you want to create the CAPTCHA
	const alphaNums = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];

	onMount(() => {
		ctx = canvas.getContext('2d');
		generateCaptcha();
	});

	onMount(() => {
		ctx = canvas.getContext('2d');
		generateCaptcha();
	});


	function generateCaptcha() {
		ctx.font = "2rem Verdana, Geneva, Tahoma, sans-serif";
		ctx.strokeStyle = "#ff0000";
		ctx.fillStyle = "#00ff00";

		let emptyArr = [];
		for (let i = 1; i <= 5; i++) {
			emptyArr.push(alphaNums[Math.floor(Math.random() * alphaNums.length)]);
		}
		captchaText = emptyArr.join('');
		captchaValue.update(() => captchaText);
		ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear before drawing
		ctx.fillText(captchaText, canvas.width/4, canvas.height/2); // Redraw
		drawLines();
	}

	function drawLines() { // Separate function for better readability
		for (let k=0; k<3; k++) {
			ctx.beginPath();
			ctx.moveTo(Math.random() * canvas.width, Math.random() * canvas.height);
			ctx.lineTo(Math.random() * canvas.width, Math.random() * canvas.height);
			ctx.stroke();
		}
	}

	function submitCaptcha() {
		const isValid = captchaInputText === captchaText; // Check captcha validity

		if (!captchaInputText) {
			noCaptchaTextEntered = "Please enter characters before you click submit.";
			outputOk = "";
			outputNotOk = "";
		} 
		else if (isValid) {
			noCaptchaTextEntered = "";
			outputOk = "Correct!";
			outputNotOk = "";
			captchaInputText = ''; // Clear input
		} 
		else {
			noCaptchaTextEntered = "";
			outputOk = "";
			outputNotOk = "Incorrect, please try again.";
		}
		
		return isValid; // Return true if correct, false otherwise
	}

	function refreshCaptcha() {
		captchaInputText = '';
		noCaptchaTextEntered = "";
		outputOk = "";
		outputNotOk = "";
		generateCaptcha();  // Call generateCaptcha directly
	}

</script>

<div class="mx-auto my-4 w-full flex flex-col items-center justify-center text-center border border-green-500 rounded bg-green-100 p-4">
	<canvas bind:this={canvas} class="mx-auto my-2 w-3/4 h-12 text-red-500" width="200" height="48"></canvas>
	<div class="captcha-form w-full">
		<input 
			type="text" 
			bind:value={captchaInputText} 
			on:keydown={(e) => e.key === "Enter" && submitCaptcha()}
			class="w-full text-center border border-gray-300 px-2 py-1 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
			placeholder="Enter Captcha" 
		/>

		<div class="mt-2 flex justify-between">
			<button on:click|preventDefault={submitCaptcha} class="bg-gray-800 text-white px-3 py-1 rounded-md text-sm hover:bg-gray-700">Submit</button>
			<button on:click|preventDefault={refreshCaptcha} class="bg-white text-gray-800 border border-gray-300 px-3 py-1 rounded-md text-sm hover:bg-gray-100"><i class="bi bi-arrow-clockwise mr-1"></i> Refresh</button>
		</div>
	</div>

  {#if noCaptchaTextEntered}{/if} <span class="text-blue-500 mt-2">{noCaptchaTextEntered}</span>
  {#if outputOk}<span class="text-green-500 mt-2">{outputOk}</span>{/if}
  {#if outputNotOk}<span class="text-red-500 mt-2">{outputNotOk}</span>{/if}
</div>

<style lang='postcss'>

  @import '../../app.css';

	/* These styles are now handled by Tailwind classes, so this block can be removed */
</style>