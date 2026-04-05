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
	const statusOptions = ['all', 'filed', 'under_review', 'approved', 'rejected'];
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
			case 'approved': return { icon: CheckCircle2, color: 'text-emerald-200', bg: 'bg-emerald-500/14 border border-emerald-300/16' };
			case 'rejected': return { icon: AlertCircle, color: 'text-rose-200', bg: 'bg-rose-500/14 border border-rose-300/16' };
			case 'filed': return { icon: Clock, color: 'text-sky-200', bg: 'bg-sky-500/14 border border-sky-300/16' };
			case 'under_review': return { icon: Clock, color: 'text-amber-200', bg: 'bg-amber-500/14 border border-amber-300/16' };
			case 'settled': return { icon: CheckCircle2, color: 'text-violet-200', bg: 'bg-violet-500/14 border border-violet-300/16' };
			default: return { icon: FileText, color: 'text-slate-200', bg: 'bg-slate-500/12 border border-slate-300/12' };
		}
	}
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
	<div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
		<div>
			<h1 class="text-3xl font-bold text-slate-50 tracking-tight">Claims</h1>
			<p class="mt-1 text-slate-300">Track and manage your insurance claims.</p>
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
		<div class="dashboard-toolbar flex flex-col gap-4 md:flex-row md:items-center">
			<div class="relative flex-grow">
				<Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
				<input
					type="text"
					placeholder="Search by claim ID, policy number, status, customer..."
					class="dashboard-control pl-11"
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
					class="dashboard-control min-w-[220px] text-sm font-semibold"
				>
					<option value="-claim_date">Newest First</option>
					<option value="claim_date">Oldest First</option>
					<option value="-claim_amount">Amount: High to Low</option>
					<option value="claim_amount">Amount: Low to High</option>
				</select>
			</div>
		</div>

		{#if showFilters}
			<div class="dashboard-filter-panel grid grid-cols-1 gap-6 animate-in slide-in-from-top-2 duration-200 md:grid-cols-2">
				<div class="space-y-2">
					<label for="claim-status-filter" class="text-xs font-bold uppercase tracking-wider text-slate-300">Claim Status</label>
					<select
						id="claim-status-filter"
						bind:value={selectedStatus}
						onchange={fetchClaims}
						class="dashboard-control text-sm"
					>
						{#each statusOptions as status}
							<option value={status}>{status === 'all' ? 'All' : status.replace('_', ' ')}</option>
						{/each}
					</select>
				</div>

				<div class="space-y-2">
					<label for="claim-date-filter" class="text-xs font-bold uppercase tracking-wider text-slate-300">Claim Date</label>
					<select
						id="claim-date-filter"
						bind:value={selectedDateRange}
						onchange={fetchClaims}
						class="dashboard-control text-sm"
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
	<div class="dashboard-table-shell overflow-hidden">
		<div class="overflow-x-auto max-h-[600px] overflow-y-auto">
			<table class="w-full text-left border-collapse">
				<thead>
					<tr class="sticky top-0 z-10 border-b border-white/8 bg-white/[0.03]">
						<th class="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-400">Claim Details</th>
						<th class="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-400">Claim Date</th>
						<th class="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-400">Amount</th>
						<th class="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-400">Status</th>
						<th class="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider text-slate-400">Action</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-white/6">
					{#if isLoading}
						{#each Array(5) as _}
							<tr class="animate-pulse">
								<td colspan="5" class="px-6 py-4"><div class="h-8 rounded bg-white/6"></div></td>
							</tr>
						{/each}
					{:else if claims.length === 0}
						<tr>
							<td colspan="5" class="px-6 py-20 text-center">
								<FileText class="mx-auto mb-4 h-12 w-12 text-slate-600" />
								<p class="font-medium text-slate-300">No claims found.</p>
							</td>
						</tr>
					{:else}
						{#each claims as claim}
							{@const status = getStatusIcon(claim.status)}
							<tr class="transition-colors hover:bg-white/[0.03]">
								<td class="px-6 py-4">
									<div class="flex items-center space-x-3">
										<div class={status.bg + " p-2 rounded-lg " + status.color}>
											<status.icon class="w-5 h-5" />
										</div>
										<div>
											<p class="text-sm font-bold text-slate-50">Claim #{claim.id}</p>
											<p class="text-xs text-slate-300">Policy: {claim.user_policy?.policy_number || 'N/A'}</p>
										</div>
									</div>
								</td>
								<td class="px-6 py-4 text-sm text-slate-300">
									{new Date(claim.claim_date).toLocaleDateString()}
								</td>
								<td class="px-6 py-4 text-sm font-bold text-slate-50">
									${claim.claim_amount}
								</td>
								<td class="px-6 py-4">
									<span class={"inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize " + status.bg + " " + status.color}>
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
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/72 p-4 backdrop-blur-md">
		<div class="dashboard-modal-panel flex w-full max-w-md flex-col overflow-hidden">
			<div class="flex items-center justify-between border-b border-white/8 bg-white/[0.03] p-6">
				<h2 class="text-xl font-bold text-slate-50">Assign Surveyor</h2>
				<button onclick={() => showAssignModal = false} class="rounded-full p-2 text-slate-300 transition-colors hover:bg-white/8 hover:text-white">
					<X class="w-6 h-6" />
				</button>
			</div>
			
			<div class="p-6 space-y-4">
				<p class="text-sm text-slate-300">Select a surveyor to review Claim #{selectedClaimId}.</p>
				
				<div class="space-y-2">
					<label class="block text-sm font-bold uppercase tracking-wider text-slate-300" for="surveyor">
						Surveyor
					</label>
					<select
						id="surveyor"
						class="dashboard-control font-medium"
						bind:value={selectedSurveyorId}
					>
						<option value="">Choose a surveyor</option>
						{#each surveyors as s}
							<option value={s.id}>{s.username} ({s.email})</option>
						{/each}
					</select>
				</div>
			</div>
			
			<div class="flex justify-end gap-3 border-t border-white/8 bg-white/[0.03] p-6">
				<Button variant="ghost" onclick={() => showAssignModal = false}>Cancel</Button>
				<Button onclick={assignSurveyor} disabled={!selectedSurveyorId}>Confirm Assignment</Button>
			</div>
		</div>
	</div>
{/if}
