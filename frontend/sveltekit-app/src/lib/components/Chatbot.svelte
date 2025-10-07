<script>
	import {
		beforeUpdate,
		afterUpdate
	} from 'svelte';

	import { markdown } from '../scripts/drawdown';

	let div;
	let autoscroll = false;

	export let aiModelValue;
	export let useCaseValue;
	export let userAgeValue;
	export let userOccupationValue;
	export let userMonthlySalaryValue;
	export let userLanguageValue;

	const array = ["Namaste! Please ask your question..", "Hey there! Ask me anything..", "Hi 👋🏽 What's your question?", "I am Rupee AI, your personal Financial Advisor. Feel free to ask me anything!", "Welcome to Rupee AI. 🙏 Ask me a question."];

	const randomPromptIndex = Math.floor(Math.random() * array.length);
	const getInitialPrompt = array[randomPromptIndex];

	beforeUpdate(() => {
		if (div) {
			const scrollableDistance = div.scrollHeight - div.offsetHeight;
			autoscroll = div.scrollTop > scrollableDistance - 20;
		}
	});

	afterUpdate(() => {
		if (autoscroll) {
			div.scrollTo(0, div.scrollHeight);
		}
	});

	const pause = (ms) => new Promise((fulfil) => setTimeout(fulfil, ms));

	const typing = { author: 'chatbot', text: '...' };

	let comments = [];		

	async function fetchResponse(user_question) {
		// Get the current date and time in Asia/Kolkata timezone (UTC+5:30)
    const date = new Date();

    // Format date in "YYYY-MM-DD HH:MM:SS" format in Asia/Kolkata timezone
    const formattedTimestamp = new Intl.DateTimeFormat('en-GB', {
			timeZone: 'Asia/Kolkata',
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit',
			hour12: false
    }).format(date);

    // Clean up the format to remove extra space or comma
    const cleanedTimestamp = formattedTimestamp.replace(',', '').replace(/\//g, '-');

    console.log(cleanedTimestamp); // This should now work and output the time

		// Preparing question template
		let question = {
			"user": {
				"id": "1234"
			},
			"conversation": {
				"platform": "web",
				"id": "2344",
				"message": user_question,
				"timestamp": cleanedTimestamp
			}
		};

		let response;

		try {
			response = await fetch('/api', {
				method: 'POST',
				body: JSON.stringify({ question }),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			
			if (!response.ok) {
				return ("description: Invalid API response coming to frontend from frontend server, status: " + response.statusText + " ("+response.status+")");
			} else {
				const data = await response.json();

				// format markdown to HTML
				// Drawdown JS: https://github.com/adamvleggett/drawdown
				// Reference: https://stackoverflow.com/questions/1319657/javascript-to-convert-markdown-textile-to-html-and-ideally-back-to-markdown-t
				return markdown(data);
			}
		} catch (error) {
			return ('description: Error sending API request at frontend, status: ' + error.message + ' (status: 400)');
		}
	}

	async function handleKeydown(event) {
		if (event.key === 'Enter' && event.target.value) {
			const comment = {
				author: 'user',
				text: (event.target.value).trim()
			};

			comments = [...comments, comment];

			// empty input box
			event.target.value = '';

			await pause(200 * (1 + Math.random()));
			comments = [...comments, typing];

			const reply = {
				author: 'chatbot',
				text: await fetchResponse(comment.text)
			};

			await pause(500 * (1 + Math.random()));
			comments = [...comments, reply].filter(comment => comment !== typing);
		}
	}
</script>

<div class="d-flex flex-column chat-window">
	<div class="chat" bind:this={div}>
		<header class="d-flex flex-column">
			<h1 class="fs-1"><i class="bi bi-robot"></i></h1>

			<article class="chatbot">
				<span>{getInitialPrompt}</span>
			</article>
		</header>

		{#each comments as comment}
			<article class={comment.author}>
				<span>{@html comment.text}</span>
			</article>
		{/each}
	</div>

	<textarea name="promptBox" class="rounded-bottom overflow-auto" on:keydown={handleKeydown}/>
</div>

<style>
	.chat-window {
		background: var(--bs-gray-200);
		position: relative;
		font-size: min(2.5vh, 1rem);
		width: auto;
		height: 30rem;
		border: 0.2rem solid #000000;
		border-radius: 1rem;
		box-sizing: border-box;
		filter: drop-shadow(1px 1px 0px #000000) drop-shadow(2px 2px 0px #000000) drop-shadow(3px 3px 0px #000000)
	}

	.chat-window::after {
		position: absolute;
		content: '';
		background: var(--bs-dark);
		width: 60%;
		height: 0.5rem;
		left: 20%;
		top: 0;
		border-radius: 0 0 0.5rem 0.5rem
	}

	@media (prefers-reduced-motion) {
		.chat {
			scroll-behavior: auto;
		}
	}

	header {
		height: 100%;
		padding: 4rem 0 0 0;
	}

	h1 {
		flex: 1;
		font-size: 1.4rem;
		text-align: center;
	}

	.chat {
		height: 0;
		flex: 1 1 auto;
		padding: 0 1rem;
		overflow-y: auto;
		scroll-behavior: smooth;
	}

	article {
		margin: 0 0 0.5rem 0;
	}

	.user {
		text-align: right;
	}

	span {
		padding: 0.5rem 1rem;
		display: inline-block;
	}

	.chatbot span {
		background-color: var(--bs-gray-400);
		border-radius: 1rem 1rem 1rem 0rem;
		color: var(--bs-dark);
		font-family: Georgia, Garamond, 'Times New Roman', Times, serif;
	}

	.user span {
		background-color: var(--bs-dark);
		color: var(--bs-light);
		border-radius: 1rem 1rem 0rem 1rem;
		word-break: break-all;
    font-family: Verdana, Helvetica, 'Trebuchet MS', Arial, Tahoma, sans-serif;
	}

	textarea {
		margin: 0.5rem 1rem 1rem 1rem;
	}
</style>
