<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { Navbar } from '$lib/components';
	import { Toaster } from 'svelte-sonner';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>InsuraFlow</title>
	<meta name="theme-color" content="#140f33" />
</svelte:head>

<div class="min-h-screen flex flex-col">
	<Navbar />
	<main class="flex-grow">
		{@render children()}
	</main>
	<Toaster position="top-right" />
</div>
