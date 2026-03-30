<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';

	let { children } = $props();

	onMount(() => {
		if (browser && !auth.user && !auth.loading) {
			goto('/login');
		}
	});

	$effect(() => {
		if (browser && !auth.user && !auth.loading) {
			goto('/login');
		}
	});
</script>

{#if auth.loading}
	<div class="min-h-[calc(100vh-64px)] flex items-center justify-center">
		<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
	</div>
{:else if auth.user}
	{@render children()}
{/if}
