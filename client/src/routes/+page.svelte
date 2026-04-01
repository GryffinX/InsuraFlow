<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { api } from '$lib/api/axios';
	import { Button } from '$lib/components';
	import { ShieldCheck, ArrowRight, Zap, Lock, Globe, Shield, Search } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';

	let policies = $state<any[]>([]);
	let isLoading = $state(true);

	onMount(async () => {
		try {
			const res = await api.get('policies/');
			policies = res.data.results || res.data;
		} catch (error) {
			console.error('Failed to load policies');
			toast.error('Could not fetch policies. Please try again later.');
		} finally {
			isLoading = false;
		}
	});

	async function handleBuy(policyId: number) {
		if (!auth.user) {
			toast.info('Please log in to purchase a policy');
			goto('/login');
			return;
		}
        
        try {
            await api.post(`policies/${policyId}/buy/`);
            toast.success('Policy purchased successfully!');
            
            // Refresh policies to show "Owned" status
            const res = await api.get('policies/');
            policies = res.data.results || res.data;
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Purchase failed');
        }
	}
</script>

<div class="relative overflow-hidden bg-white">
	<!-- Hero Section -->
	<div class="relative pt-16 pb-32 overflow-hidden">
		<div class="relative px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
			<div class="lg:grid lg:grid-cols-12 lg:gap-8">
				<div class="sm:text-center md:max-w-2xl md:mx-auto lg:col-span-6 lg:text-left">
					<h1>
						<span class="block text-base font-semibold text-indigo-600 uppercase tracking-wide sm:text-lg lg:text-base xl:text-lg">Introducing InsuraFlow</span>
						<span class="mt-1 block text-4xl tracking-tight font-extrabold sm:text-5xl xl:text-6xl">
							<span class="block text-slate-900">Modern Insurance</span>
							<span class="block text-indigo-600">for Everyone.</span>
						</span>
					</h1>
					<p class="mt-3 text-base text-slate-500 sm:mt-5 sm:text-xl lg:text-lg xl:text-xl">
						Secure your future with the most transparent and efficient digital insurance platform. Manage policies, file claims, and get protected in minutes.
					</p>
					<div class="mt-8 sm:max-w-lg sm:mx-auto sm:text-center lg:text-left lg:mx-0">
						<div class="flex flex-col sm:flex-row gap-4">
							<a href="/register">
								<Button size="lg" class="w-full sm:w-auto rounded-xl px-10 h-14 text-lg">
									Get Started <ArrowRight class="ml-2 h-5 w-5" />
								</Button>
							</a>
							<a href="#policies">
								<Button variant="outline" size="lg" class="w-full sm:w-auto rounded-xl px-10 h-14 text-lg">
									Browse Plans
								</Button>
							</a>
						</div>
					</div>
				</div>
				<div class="mt-12 relative sm:max-w-lg sm:mx-auto lg:mt-0 lg:max-w-none lg:mx-0 lg:col-span-6 lg:flex lg:items-center">
					<div class="relative mx-auto w-full rounded-3xl shadow-2xl overflow-hidden bg-indigo-50 border-8 border-white">
						<div class="p-8">
							<div class="flex items-center gap-4 mb-8">
								<div class="p-3 bg-white rounded-2xl shadow-sm text-indigo-600">
									<ShieldCheck class="w-8 h-8" />
								</div>
								<h3 class="text-xl font-bold text-slate-900">Trusted by 10k+ Users</h3>
							</div>
							<div class="space-y-4">
								{#each Array(3) as _}
									<div class="h-4 bg-white/50 rounded-full w-full"></div>
								{/each}
								<div class="h-4 bg-white/50 rounded-full w-2/3"></div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Policies Grid -->
	<div id="policies" class="bg-slate-50 py-24 sm:py-32 scroll-mt-16">
		<div class="mx-auto max-w-7xl px-6 lg:px-8">
			<div class="mx-auto max-w-2xl text-center mb-16">
				<h2 class="text-base font-semibold leading-7 text-indigo-600">Available Plans</h2>
				<p class="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">Choose Your Protection</p>
				<p class="mt-4 text-lg text-slate-600">Transparent pricing. Comprehensive coverage. No hidden fees.</p>
			</div>

			{#if isLoading}
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
					{#each Array(3) as _}
						<div class="bg-white h-80 rounded-3xl border border-slate-200 animate-pulse"></div>
					{/each}
				</div>
			{:else if policies.length > 0}
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
					{#each policies as policy}
						<div class="bg-white rounded-3xl border border-slate-200 shadow-sm hover:shadow-xl transition-all duration-300 p-8 flex flex-col group">
							<div class="flex justify-between items-start mb-6">
								<div class="bg-indigo-50 w-14 h-14 rounded-2xl flex items-center justify-center text-indigo-600 group-hover:scale-110 transition-transform">
									<Shield class="w-8 h-8" />
								</div>
								<span class="inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-700 uppercase tracking-wider">
									{policy.policy_type}
								</span>
							</div>
							
							<h3 class="text-2xl font-bold text-slate-900 mb-2">{policy.title}</h3>
							<p class="text-slate-500 mb-4 line-clamp-2 text-sm">{policy.description}</p>
                            <p class="text-xs text-slate-400 mb-6 font-medium uppercase tracking-tight">Provided by {policy.provider?.company_name || 'InsuraFlow'}</p>
							
							<div class="mt-auto space-y-6">
								<div class="grid grid-cols-2 gap-4 pt-6 border-t border-slate-100">
									<div>
										<p class="text-xs text-slate-400 uppercase font-bold tracking-wider">Coverage</p>
										<p class="text-lg font-bold text-slate-900">${policy.coverage_amount}</p>
									</div>
									<div class="text-right">
										<p class="text-xs text-slate-400 uppercase font-bold tracking-wider">Premium</p>
										<p class="text-2xl font-black text-indigo-600">${policy.premium_amount}</p>
									</div>
								</div>
								
								{#if policy.is_owned}
                                    <Button 
                                        class="w-full h-14 rounded-xl text-lg font-bold bg-slate-100 text-slate-500" 
                                    >
                                        Owned
                                    </Button>
                                {:else}
                                    <Button 
                                        class="w-full h-14 rounded-xl text-lg font-bold" 
                                        onclick={() => handleBuy(policy.id)}
                                    >
                                        Buy Policy
                                    </Button>
                                {/if}
							</div>
						</div>
					{/each}
				</div>
			{:else}
				<div class="text-center py-20 bg-white rounded-3xl border-2 border-dashed border-slate-200">
					<Search class="mx-auto h-12 w-12 text-slate-300" />
					<h3 class="mt-4 text-lg font-medium text-slate-900">No policies found</h3>
					<p class="mt-2 text-slate-500">Check back later for new insurance plans.</p>
				</div>
			{/if}
		</div>
	</div>

	<!-- Simple Footer -->
	<footer class="bg-white border-t border-slate-100 py-12">
		<div class="max-w-7xl mx-auto px-4 text-center">
			<p class="text-slate-400 text-sm">© 2026 InsuraFlow. All rights reserved.</p>
		</div>
	</footer>
</div>
