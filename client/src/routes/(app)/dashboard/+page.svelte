<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { api } from '$lib/api/axios';
	import { onMount } from 'svelte';
	import { Shield, FileText, Activity, CreditCard, ChevronRight } from 'lucide-svelte';
	import { Button } from '$lib/components';

	let stats = $state({
		policies: 0,
		claims: 0,
		activeReports: 0,
		pendingSettlements: 0
	});

    let recentPolicies = $state([]);
    let recentClaims = $state([]);
	let isLoading = $state(true);

	onMount(async () => {
		try {
			const [policiesRes, claimsRes] = await Promise.all([
				api.get('/policies/'),
				api.get('/claims/')
			]);
			stats.policies = policiesRes.data.count || policiesRes.data.length;
			stats.claims = claimsRes.data.count || claimsRes.data.length;
            recentPolicies = policiesRes.data.results?.slice(0, 3) || policiesRes.data.slice(0, 3);
            recentClaims = claimsRes.data.results?.slice(0, 3) || claimsRes.data.slice(0, 3);
		} catch (error) {
			console.error('Failed to fetch dashboard data', error);
		} finally {
			isLoading = false;
		}
	});
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
	<div class="mb-8">
		<h1 class="text-3xl font-bold text-slate-900">Welcome, {auth.user?.username}!</h1>
		<p class="text-slate-500 mt-1">Here's what's happening with your insurance today.</p>
	</div>

	<!-- Stats Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
		{#each [
			{ label: 'Total Policies', value: stats.policies, icon: Shield, color: 'text-blue-600', bg: 'bg-blue-50' },
			{ label: 'Active Claims', value: stats.claims, icon: FileText, color: 'text-amber-600', bg: 'bg-amber-50' },
			{ label: 'Inspection Reports', value: stats.activeReports, icon: Activity, color: 'text-indigo-600', bg: 'bg-indigo-50' },
			{ label: 'Settlements', value: stats.pendingSettlements, icon: CreditCard, color: 'text-emerald-600', bg: 'bg-emerald-50' }
		] as stat}
			<div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
				<div class="flex items-center justify-between mb-4">
					<div class={stat.bg + " p-3 rounded-xl " + stat.color}>
						<stat.icon class="w-6 h-6" />
					</div>
					<span class="text-2xl font-bold text-slate-900">{stat.value}</span>
				</div>
				<p class="text-sm font-medium text-slate-500">{stat.label}</p>
			</div>
		{/each}
	</div>

	<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
		<!-- Recent Policies -->
		<div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
			<div class="p-6 border-b border-slate-100 flex items-center justify-between">
				<h2 class="text-lg font-bold text-slate-900">Recent Policies</h2>
				<a href="/policies" class="text-sm font-medium text-indigo-600 hover:text-indigo-500">View all</a>
			</div>
			<div class="divide-y divide-slate-100">
				{#if isLoading}
					<div class="p-6 text-center text-slate-500">Loading...</div>
				{:else if recentPolicies.length === 0}
					<div class="p-6 text-center text-slate-500">No policies found.</div>
				{:else}
					{#each recentPolicies as policy}
						<div class="p-6 hover:bg-slate-50 transition-colors flex items-center justify-between">
							<div class="flex items-center space-x-4">
								<div class="bg-slate-100 p-2 rounded-lg">
									<Shield class="w-5 h-5 text-slate-600" />
								</div>
								<div>
									<p class="text-sm font-bold text-slate-900">{policy.policy_number}</p>
									<p class="text-xs text-slate-500">{policy.insurance_type} • {policy.status}</p>
								</div>
							</div>
							<ChevronRight class="w-5 h-5 text-slate-300" />
						</div>
					{/each}
				{/if}
			</div>
		</div>

		<!-- Recent Claims -->
		<div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
			<div class="p-6 border-b border-slate-100 flex items-center justify-between">
				<h2 class="text-lg font-bold text-slate-900">Recent Claims</h2>
				<a href="/claims" class="text-sm font-medium text-indigo-600 hover:text-indigo-500">View all</a>
			</div>
			<div class="divide-y divide-slate-100">
				{#if isLoading}
					<div class="p-6 text-center text-slate-500">Loading...</div>
				{:else if recentClaims.length === 0}
					<div class="p-6 text-center text-slate-500">No claims found.</div>
				{:else}
					{#each recentClaims as claim}
						<div class="p-6 hover:bg-slate-50 transition-colors flex items-center justify-between">
							<div class="flex items-center space-x-4">
								<div class="bg-slate-100 p-2 rounded-lg">
									<FileText class="w-5 h-5 text-slate-600" />
								</div>
								<div>
									<p class="text-sm font-bold text-slate-900">Claim #{claim.id}</p>
									<p class="text-xs text-slate-500">{claim.status} • {new Date(claim.incident_date).toLocaleDateString()}</p>
								</div>
							</div>
							<ChevronRight class="w-5 h-5 text-slate-300" />
						</div>
					{/each}
				{/if}
			</div>
		</div>
	</div>
</div>
