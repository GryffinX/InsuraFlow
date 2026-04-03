<script lang="ts">
	import { api } from '$lib/api/axios';
	import { auth } from '$lib/stores/auth.svelte';
	import { onMount } from 'svelte';
	import { FileText, Plus, Search, Filter, AlertCircle, Clock, CheckCircle2, UserCheck, X } from 'lucide-svelte';
	import { Button } from '$lib/components';
	import { toast } from 'svelte-sonner';

	let claims = $state<any[]>([]);
	let isLoading = $state(true);
	let searchQuery = $state('');
	
	let surveyors = $state<any[]>([]);
	let showAssignModal = $state(false);
	let selectedClaimId = $state<number | null>(null);
	let selectedSurveyorId = $state('');

	onMount(async () => {
		fetchClaims();
	});

	async function fetchClaims() {
		isLoading = true;
		try {
			const res = await api.get('claims/', {
				params: { 
					search: searchQuery,
					limit: 100 
				}
			});
			const data = res.data.results || (Array.isArray(res.data) ? res.data : []);
			claims = data;
			console.log("Claims API Response:", res.data);
		} catch (error) {
			console.error('Failed to load claims', error);
			toast.error('Failed to load claims');
		} finally {
			isLoading = false;
		}
	}

	async function fetchSurveyors() {
		try {
			const res = await api.get('surveyors/');
			const data = res.data.results || res.data;
			surveyors = data;
			console.log("Surveyors API response:", res.data);
		} catch (error) {
			console.error('Failed to load surveyors', error);
			toast.error('Failed to load surveyors');
		}
	}

	async function assignSurveyor() {
		if (!selectedClaimId || !selectedSurveyorId) return;
		try {
			await api.post(`claims/${selectedClaimId}/assign_surveyor/`, {
				surveyor_id: selectedSurveyorId
			});
			toast.success('Surveyor assigned successfully');
			showAssignModal = false;
			fetchClaims();
		} catch (error: any) {
			toast.error(error.response?.data?.error || 'Failed to assign surveyor');
		}
	}

	function openAssignModal(claimId: number) {
		selectedClaimId = claimId;
		fetchSurveyors();
		showAssignModal = true;
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
		{#if auth.user?.role === 'customer'}
			<a href="/claims/new">
				<Button>
					<Plus class="w-5 h-5 mr-2" /> File a Claim
				</Button>
			</a>
		{/if}
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

	<!-- Claims List with Scrollable Container -->
	<div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
		<div class="overflow-x-auto max-h-[600px] overflow-y-auto">
			<table class="w-full text-left border-collapse">
				<thead>
					<tr class="bg-slate-50 border-b border-slate-200 sticky top-0 z-10">
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
											<p class="text-xs text-slate-500">Policy: {claim.user_policy?.policy_number || 'N/A'}</p>
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
								<td class="px-6 py-4 text-right flex justify-end gap-2">
									{#if (auth.user?.role === 'provider' || auth.user?.role === 'admin' || auth.user?.role === 'agent') && claim.status === 'filed'}
										<Button variant="outline" size="sm" onclick={() => openAssignModal(claim.id)}>
											<UserCheck class="w-4 h-4 mr-1" /> Assign
										</Button>
									{/if}
									<a href={`/claims/${claim.id}`}>
										<Button variant="ghost" size="sm">View Details</Button>
									</a>
								</td>
							</tr>
						{/each}
					{/if}
				</tbody>
			</table>
		</div>
	</div>
</div>

{#if showAssignModal}
	<div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
		<div class="bg-white rounded-3xl w-full max-w-md overflow-hidden shadow-2xl flex flex-col">
			<div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
				<h2 class="text-xl font-bold text-slate-900">Assign Surveyor</h2>
				<button onclick={() => showAssignModal = false} class="p-2 hover:bg-slate-200 rounded-full transition-colors">
					<X class="w-6 h-6" />
				</button>
			</div>
			
			<div class="p-6 space-y-4">
				<p class="text-sm text-slate-500">Select a surveyor to review Claim #{selectedClaimId}.</p>
				
				<div class="space-y-2">
					<label class="block text-sm font-bold text-slate-700 uppercase tracking-wider" for="surveyor">
						Surveyor
					</label>
					<select
						id="surveyor"
						class="block w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-indigo-500 transition-all font-medium"
						bind:value={selectedSurveyorId}
					>
						<option value="">Choose a surveyor</option>
						{#each surveyors as s}
							<option value={s.id}>{s.username} ({s.email})</option>
						{/each}
					</select>
				</div>
			</div>
			
			<div class="p-6 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
				<Button variant="ghost" onclick={() => showAssignModal = false}>Cancel</Button>
				<Button onclick={assignSurveyor} disabled={!selectedSurveyorId}>Confirm Assignment</Button>
			</div>
		</div>
	</div>
{/if}
