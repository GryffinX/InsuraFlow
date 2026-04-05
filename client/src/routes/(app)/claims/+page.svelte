<script lang="ts">
	import { api } from '$lib/api/axios';
	import { auth } from '$lib/stores/auth.svelte';
	import { onMount } from 'svelte';
	import AlertCircle from 'lucide-svelte/icons/alert-circle';
	import CheckCircle2 from 'lucide-svelte/icons/check-circle-2';
	import Clock from 'lucide-svelte/icons/clock';
	import FileText from 'lucide-svelte/icons/file-text';
	import Filter from 'lucide-svelte/icons/filter';
	import Plus from 'lucide-svelte/icons/plus';
	import Search from 'lucide-svelte/icons/search';
	import UserCheck from 'lucide-svelte/icons/user-check';
	import X from 'lucide-svelte/icons/x';
	import { Button } from '$lib/components';
	import { toast } from 'svelte-sonner';

	let claims = $state<any[]>([]);
	let isLoading = $state(true);
	let searchQuery = $state('');
	let selectedStatus = $state('all');
	let selectedDateRange = $state('all');
	let sortBy = $state('-claim_date');
	let showFilters = $state(false);
	
	let surveyors = $state<any[]>([]);
	let showAssignModal = $state(false);
	let selectedClaimId = $state<number | null>(null);
	let selectedSurveyorId = $state('');

	let debounceTimer: any;
	const statusOptions = ['all', 'filed', 'under_review', 'approved', 'rejected', 'settled'];
	const dateRangeOptions = ['all', 'today', 'last_7_days', 'last_30_days', 'this_year'];

	function formatDateForApi(date: Date) {
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		return `${year}-${month}-${day}`;
	}

	function getDateRangeStart(range: string) {
		const today = new Date();
		const start = new Date(today);

		switch (range) {
			case 'today':
				return formatDateForApi(today);
			case 'last_7_days':
				start.setDate(today.getDate() - 7);
				return formatDateForApi(start);
			case 'last_30_days':
				start.setDate(today.getDate() - 30);
				return formatDateForApi(start);
			case 'this_year':
				start.setMonth(0, 1);
				return formatDateForApi(start);
			default:
				return null;
		}
	}

	function handleSearch() {
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(() => {
			fetchClaims();
		}, 300);
	}

	onMount(async () => {
		fetchClaims();
	});

	async function fetchClaims() {
		isLoading = true;
		try {
			const params: Record<string, string | number> = {
				ordering: sortBy,
				limit: 100
			};
			if (searchQuery.trim()) params.search = searchQuery.trim();
			if (selectedStatus !== 'all') params.status = selectedStatus;
			const dateRangeStart = getDateRangeStart(selectedDateRange);
			if (dateRangeStart) params.claim_date__gte = dateRangeStart;

			const res = await api.get('claims/', {
				params
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
	<div class="space-y-4 mb-8">
		<div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center gap-4">
			<div class="relative flex-grow">
				<Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
				<input
					type="text"
					placeholder="Search by claim ID, policy number, status, customer..."
					class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
					bind:value={searchQuery}
					oninput={handleSearch}
				/>
			</div>

			<div class="flex gap-2">
				<Button variant="outline" onclick={() => showFilters = !showFilters}>
					<Filter class="w-4 h-4 mr-2" /> {showFilters ? 'Hide' : ''} Filters
				</Button>

				<select
					bind:value={sortBy}
					onchange={fetchClaims}
					class="bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500 text-sm font-medium"
				>
					<option value="-claim_date">Newest First</option>
					<option value="claim_date">Oldest First</option>
					<option value="-claim_amount">Amount: High to Low</option>
					<option value="claim_amount">Amount: Low to High</option>
				</select>
			</div>
		</div>

		{#if showFilters}
			<div class="bg-slate-100 p-6 rounded-2xl border border-slate-200 grid grid-cols-1 md:grid-cols-2 gap-6 animate-in slide-in-from-top-2 duration-200">
				<div class="space-y-2">
					<label for="claim-status-filter" class="text-xs font-bold text-slate-500 uppercase tracking-wider">Claim Status</label>
					<select
						id="claim-status-filter"
						bind:value={selectedStatus}
						onchange={fetchClaims}
						class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
					>
						{#each statusOptions as status}
							<option value={status}>{status === 'all' ? 'All' : status.replace('_', ' ')}</option>
						{/each}
					</select>
				</div>

				<div class="space-y-2">
					<label for="claim-date-filter" class="text-xs font-bold text-slate-500 uppercase tracking-wider">Claim Date</label>
					<select
						id="claim-date-filter"
						bind:value={selectedDateRange}
						onchange={fetchClaims}
						class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
					>
						{#each dateRangeOptions as range}
							<option value={range}>
								{range === 'all'
									? 'All Dates'
									: range === 'today'
										? 'Today'
										: range === 'last_7_days'
											? 'Last 7 Days'
											: range === 'last_30_days'
												? 'Last 30 Days'
												: 'This Year'}
							</option>
						{/each}
					</select>
				</div>
			</div>
		{/if}
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
