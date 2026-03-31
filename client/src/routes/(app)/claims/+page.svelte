<script lang="ts">
	import { api } from '$lib/api/axios';
	import { onMount } from 'svelte';
	import { FileText, Plus, Search, Filter, AlertCircle, Clock, CheckCircle2 } from 'lucide-svelte';
	import { Button } from '$lib/components';
	import { toast } from 'svelte-sonner';

	let claims = $state([]);
	let isLoading = $state(true);
	let searchQuery = $state('');

	onMount(fetchClaims);

	async function fetchClaims() {
		isLoading = true;
		try {
			const res = await api.get('/claims/', {
				params: { search: searchQuery }
			});
			claims = res.data.results || res.data;
		} catch (error) {
			toast.error('Failed to load claims');
		} finally {
			isLoading = false;
		}
	}

	function getStatusIcon(status: string) {
		switch (status.toLowerCase()) {
			case 'approved': return { icon: CheckCircle2, color: 'text-emerald-600', bg: 'bg-emerald-50' };
			case 'rejected': return { icon: AlertCircle, color: 'text-red-600', bg: 'bg-red-50' };
			case 'filed': return { icon: Clock, color: 'text-blue-600', bg: 'bg-blue-50' };
			case 'under_review': return { icon: Clock, color: 'text-amber-600', bg: 'bg-amber-50' };
			case 'settled': return { icon: CheckCircle2, color: 'text-indigo-600', bg: 'bg-indigo-50' };
			default: return { icon: FileText, color: 'text-slate-600', bg: 'bg-slate-50' };
		}
	}
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
	<div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
		<div>
			<h1 class="text-3xl font-bold text-slate-900 tracking-tight">Claims</h1>
			<p class="text-slate-500 mt-1">Track and manage your insurance claims.</p>
		</div>
		<a href="/claims/new">
			<Button>
				<Plus class="w-5 h-5 mr-2" /> File a Claim
			</Button>
		</a>
	</div>

	<!-- Search & Filters -->
	<div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row gap-4 mb-8">
		<div class="relative flex-grow">
			<Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
			<input
				type="text"
				placeholder="Search claims by ID, status..."
				class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 transition-all sm:text-sm"
				bind:value={searchQuery}
				onchange={fetchClaims}
			/>
		</div>
		<Button variant="outline">
			<Filter class="w-4 h-4 mr-2" /> Filters
		</Button>
	</div>

	<!-- Claims List -->
	<div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
		<div class="overflow-x-auto">
			<table class="w-full text-left border-collapse">
				<thead>
					<tr class="bg-slate-50 border-b border-slate-200">
						<th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Claim Details</th>
						<th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Claim Date</th>
						<th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Amount</th>
						<th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Status</th>
						<th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Action</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-slate-100">
					{#if isLoading}
						{#each Array(5) as _}
							<tr class="animate-pulse">
								<td colspan="5" class="px-6 py-4"><div class="h-8 bg-slate-50 rounded"></div></td>
							</tr>
						{/each}
					{:else if claims.length === 0}
						<tr>
							<td colspan="5" class="px-6 py-20 text-center">
								<FileText class="w-12 h-12 text-slate-200 mx-auto mb-4" />
								<p class="text-slate-500 font-medium">No claims found.</p>
							</td>
						</tr>
					{:else}
						{#each claims as claim}
							{@const status = getStatusIcon(claim.status)}
							<tr class="hover:bg-slate-50 transition-colors">
								<td class="px-6 py-4">
									<div class="flex items-center space-x-3">
										<div class={status.bg + " p-2 rounded-lg " + status.color}>
											<status.icon class="w-5 h-5" />
										</div>
										<div>
											<p class="text-sm font-bold text-slate-900">Claim #{claim.id}</p>
											<p class="text-xs text-slate-500">Policy: {claim.policy?.policy_number}</p>
										</div>
									</div>
								</td>
								<td class="px-6 py-4 text-sm text-slate-600">
									{new Date(claim.claim_date).toLocaleDateString()}
								</td>
								<td class="px-6 py-4 text-sm font-bold text-slate-900">
									${claim.claim_amount}
								</td>
								<td class="px-6 py-4">
									<span class={"inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize " + status.bg + " " + status.color}>
										{claim.status.replace('_', ' ')}
									</span>
								</td>
								<td class="px-6 py-4 text-right">
									<Button variant="ghost" size="sm">View Details</Button>
								</td>
							</tr>
						{/each}
					{/if}
				</tbody>
			</table>
		</div>
	</div>
</div>
