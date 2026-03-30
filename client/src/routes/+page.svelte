<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { Button } from '$lib/components';
	import { ShieldCheck, ArrowRight, Zap, Lock, Globe } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	onMount(() => {
		if (auth.user) {
			goto('/dashboard');
		}
	});
</script>

<div class="relative overflow-hidden">
	<!-- Hero Section -->
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 text-center lg:pt-32 lg:pb-32">
		<h1 class="mx-auto max-w-4xl font-display text-5xl font-medium tracking-tight text-slate-900 sm:text-7xl">
			Insurance management <span class="relative whitespace-nowrap text-indigo-600">
				<span class="relative">made simple</span>
			</span>
		</h1>
		<p class="mx-auto mt-6 max-w-2xl text-lg tracking-tight text-slate-700">
			InsuraFlow helps you manage policies, process claims, and connect with agents in one unified platform. Fast, secure, and transparent.
		</p>
		<div class="mt-10 flex justify-center gap-x-6">
			<a href="/register">
				<Button size="lg" class="rounded-full px-8">
					Get started <ArrowRight class="ml-2 h-5 w-5" />
				</Button>
			</a>
			<a href="#features">
				<Button variant="outline" size="lg" class="rounded-full px-8">
					Learn more
				</Button>
			</a>
		</div>
	</div>

	<!-- Features Section -->
	<div id="features" class="bg-white py-24 sm:py-32 border-t border-slate-100">
		<div class="mx-auto max-w-7xl px-6 lg:px-8">
			<div class="mx-auto max-w-2xl lg:text-center">
				<h2 class="text-base font-semibold leading-7 text-indigo-600">Faster Processing</h2>
				<p class="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">Everything you need to manage risk</p>
			</div>
			<div class="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
				<dl class="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
					{#each [
						{ name: 'Instant Claims', description: 'File claims in minutes and track their status in real-time.', icon: Zap },
						{ name: 'Secure Vault', description: 'Your policy documents are encrypted and accessible anywhere.', icon: Lock },
						{ name: 'Global Network', description: 'Connect with certified agents and surveyors worldwide.', icon: Globe }
					] as feature}
						<div class="flex flex-col items-center text-center">
							<div class="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
								<feature.icon class="h-8 w-8" />
							</div>
							<dt class="text-xl font-bold leading-7 text-slate-900">{feature.name}</dt>
							<dd class="mt-4 flex flex-auto flex-col text-base leading-7 text-slate-600">
								<p class="flex-auto">{feature.description}</p>
							</dd>
						</div>
					{/each}
				</dl>
			</div>
		</div>
	</div>
</div>
