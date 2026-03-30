<script lang="ts">
	import { api } from '$lib/api/axios';
	import { onMount } from 'svelte';
	import { Shield, Plus, Search, Filter } from 'lucide-svelte';
	import { Button, Input } from '$lib/components';
	import { toast } from 'svelte-sonner';

	let policies = $state([]);
	let isLoading = $state(true);
	let searchQuery = $state('');

	onMount(fetchPolicies);

	async function fetchPolicies() {
		isLoading = true;
		try {
			const res = await api.get('/policies/', {
				params: { search: searchQuery }
			});
			policies = res.data.results || res.data;
		} catch (error) {
			toast.error('Failed to load policies');
		} finally {
			isLoading = false;
		}
	}

	function getStatusClass(status: string) {
		switch (status.toLowerCase()) {
			case 'active': return 'bg-emerald-50 text-emerald-700 border-emerald-100';
			case 'expired': return 'bg-red-50 text-red-700 border-red-100';
			case 'pending': return 'bg-amber-50 text-amber-700 border-amber-100';
			default: return 'bg-slate-50 text-slate-700 border-slate-100';
		}
	}
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
	<div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
		<div>
			<h1 class="text-3xl font-bold text-slate-900 tracking-tight">Policies</h1>
			<p class="text-slate-500 mt-1">Manage and track all your insurance coverage.</p>
		</div>
		<Button>
			<Plus class="w-5 h-5 mr-2" /> New Policy
		</Button>
	</div>

	<!-- Search & Filters -->
	<div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row gap-4 mb-8">
		<div class="relative flex-grow">
			<Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
			<input
				type="text"
				placeholder="Search policies by number, type..."
				class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 transition-all sm:text-sm"
				bind:value={searchQuery}
				onchange={fetchPolicies}
			/>
		</div>
		<Button variant="outline">
			<Filter class="w-4 h-4 mr-2" /> Filters
		</Button>
	</div>

	<!-- Policies Grid -->
	{#if isLoading}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each Array(6) as _}
				<div class="bg-white h-48 rounded-2xl border border-slate-200 animate-pulse"></div>
			{/each}
		</div>
	{:else if policies.length === 0}
		<div class="text-center py-20 bg-white rounded-2xl border-2 border-dashed border-slate-200">
			<Shield class="w-12 h-12 text-slate-300 mx-auto mb-4" />
			<h3 class="text-lg font-medium text-slate-900">No policies found</h3>
			<p class="text-slate-500 mt-1">Try adjusting your search or create a new policy.</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each policies as policy}
				<div class="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all group overflow-hidden">
					<div class="p-6">
						<div class="flex justify-between items-start mb-4">
							<div class="bg-indigo-50 p-3 rounded-xl text-indigo-600 group-hover:scale-110 transition-transform">
								<Shield class="w-6 h-6" />
							</div>
							<span class={"px-3 py-1 rounded-full text-xs font-bold border " + getStatusClass(policy.status)}>
								{policy.status}
							</span>
						</div>
						<h3 class="text-lg font-bold text-slate-900 mb-1">{policy.policy_number}</h3>
						<p class="text-sm font-medium text-slate-500 mb-4">{policy.insurance_type}</p>
						
						<div class="space-y-3 pt-4 border-t border-slate-100">
							<div class="flex justify-between text-sm">
								<span class="text-slate-500">Premium</span>
								<span class="font-bold text-slate-900">${policy.premium_amount}</span>
							</div>
							<div class="flex justify-between text-sm">
								<span class="text-slate-500">Coverage</span>
								<span class="font-bold text-slate-900">${policy.coverage_amount}</span>
							</div>
						</div>
					</div>
					<div class="bg-slate-50 p-4 border-t border-slate-100 flex justify-between items-center">
						<span class="text-xs font-medium text-slate-500">
							Ends {new Date(policy.expiry_date).toLocaleDateString()}
						</span>
						<Button size="sm" variant="ghost" class="h-8">Details</Button>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
