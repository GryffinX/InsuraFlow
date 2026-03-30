<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { Navbar } from '$lib/components';
	import { Toaster } from 'svelte-sonner';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="min-h-screen bg-slate-50 flex flex-col">
	<Navbar />
	<main class="flex-grow">
		{@render children()}
	</main>
	<Toaster position="top-right" />
</div>
