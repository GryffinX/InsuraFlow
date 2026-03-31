<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { api } from '$lib/api/axios';
	import { Button } from '$lib/components';
	import { ShieldCheck, ArrowRight, Zap, Lock, Globe, Shield } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';

	let policies = $state([]);
	let isLoading = $state(true);

	onMount(async () => {
		if (auth.user) {
			goto('/dashboard');
			return;
		}
		
		try {
			const res = await api.get('/policies/');
			policies = (res.data.results || res.data).slice(0, 3);
		} catch (error) {
			console.error('Failed to load featured policies');
		} finally {
			isLoading = false;
		}
	});

	function handleApply() {
		if (!auth.user) {
			toast.info('Please log in to apply for a policy');
			goto('/login');
		} else {
			goto('/policies');
		}
	}
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
			<a href="#policies">
				<Button variant="outline" size="lg" class="rounded-full px-8">
					Browse Policies
				</Button>
			</a>
		</div>
	</div>

	<!-- Featured Policies Section -->
	<div id="policies" class="bg-slate-50 py-24 sm:py-32 border-t border-slate-100">
		<div class="mx-auto max-w-7xl px-6 lg:px-8">
			<div class="mx-auto max-w-2xl text-center mb-16">
				<h2 class="text-base font-semibold leading-7 text-indigo-600">Featured Plans</h2>
				<p class="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">Available Insurance Policies</p>
			</div>

			{#if isLoading}
				<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
					{#each Array(3) as _}
						<div class="bg-white h-64 rounded-2xl border border-slate-200 animate-pulse"></div>
					{/each}
				</div>
			{:else if policies.length > 0}
				<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
					{#each policies as policy}
						<div class="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all p-8 flex flex-col group">
							<div class="bg-indigo-50 w-12 h-12 rounded-xl flex items-center justify-center text-indigo-600 mb-6 group-hover:scale-110 transition-transform">
								<Shield class="w-6 h-6" />
							</div>
							<h3 class="text-xl font-bold text-slate-900 mb-2">{policy.policy_number}</h3>
							<p class="text-slate-500 mb-6 uppercase tracking-wider text-xs font-bold">{policy.policy_type} Insurance</p>
							
							<div class="mt-auto space-y-4">
								<div class="flex justify-between items-center text-sm border-t border-slate-100 pt-4">
									<span class="text-slate-500">Coverage</span>
									<span class="font-bold text-slate-900">${policy.coverage_amount}</span>
								</div>
								<Button class="w-full" onclick={handleApply}>Apply Now</Button>
							</div>
						</div>
					{/each}
				</div>
				<div class="mt-12 text-center">
					<a href="/policies">
						<Button variant="ghost" class="text-indigo-600">
							View all policies <ArrowRight class="ml-2 h-4 w-4" />
						</Button>
					</a>
				</div>
			{:else}
				<div class="text-center py-12 bg-white rounded-2xl border-2 border-dashed border-slate-200">
					<p class="text-slate-500">No public policies available at the moment.</p>
				</div>
			{/if}
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
