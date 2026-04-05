<script lang="ts">
	import { api } from '$lib/api/axios';
	import { auth } from '$lib/stores/auth.svelte';
	import { onMount } from 'svelte';
	import ArrowUpDown from 'lucide-svelte/icons/arrow-up-down';
	import Check from 'lucide-svelte/icons/check';
	import Edit from 'lucide-svelte/icons/edit';
	import Filter from 'lucide-svelte/icons/filter';
	import Plus from 'lucide-svelte/icons/plus';
	import Search from 'lucide-svelte/icons/search';
	import Shield from 'lucide-svelte/icons/shield';
	import ShoppingCart from 'lucide-svelte/icons/shopping-cart';
	import Trash2 from 'lucide-svelte/icons/trash-2';
	import Users from 'lucide-svelte/icons/users';
	import X from 'lucide-svelte/icons/x';
	import { Button } from '$lib/components';
	import { toast } from 'svelte-sonner';

	let policies = $state<any[]>([]);
	let isLoading = $state(true);
	let searchQuery = $state('');
	let selectedType = $state('all');
	let sortBy = $state('premium_amount');
	let minPrice = $state('');
	let maxPrice = $state('');
	let compareList = $state<any[]>([]);
	let showCompare = $state(false);
	let showFilters = $state(false);
	
	let showCustomers = $state(false);
	let selectedPolicyCustomers = $state<any[]>([]);
	let selectedPolicyTitle = $state('');

	let debounceTimer: any;
	function handleSearch() {
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(() => {
			fetchPolicies();
		}, 300);
	}

	onMount(fetchPolicies);

	async function fetchPolicies() {
		isLoading = true;
		try {
			const params: any = { 
				search: searchQuery,
				ordering: sortBy
			};
			if (selectedType !== 'all') params.policy_type = selectedType;
			if (minPrice) params.premium_amount__gte = minPrice;
			if (maxPrice) params.premium_amount__lte = maxPrice;

			const res = await api.get('policies/', { params });
			console.log("Policies API Response:", res.data);
			policies = res.data.results || res.data;
		} catch (error) {
			console.error('Failed to load policies', error);
			toast.error('Failed to load policies');
		} finally {
			isLoading = false;
		}
	}

	async function buyPolicy(policyId: number) {
		try {
			await api.post(`policies/${policyId}/buy/`);
			toast.success('Policy purchased successfully!');
			fetchPolicies();
		} catch (error: any) {
			toast.error(error.response?.data?.error || 'Failed to purchase policy');
		}
	}

	function toggleCompare(policy: any) {
		if (compareList.find(p => p.id === policy.id)) {
			compareList = compareList.filter(p => p.id !== policy.id);
		} else if (compareList.length < 3) {
			compareList = [...compareList, policy];
		} else {
			toast.error('You can compare up to 3 policies');
		}
	}

	async function deletePolicy(id: number) {
		if (!confirm('Are you sure you want to delete this policy?')) return;
		try {
			await api.delete(`policies/${id}/`);
			toast.success('Policy deleted successfully');
			compareList = compareList.filter((policy) => policy.id !== id);
			if (showCustomers) {
				showCustomers = false;
				selectedPolicyCustomers = [];
				selectedPolicyTitle = '';
			}
			fetchPolicies();
		} catch (error: any) {
			toast.error(error.response?.data?.error || error.response?.data?.detail || 'Failed to delete policy');
		}
	}

	async function viewCustomers(policy: any) {
		try {
			const res = await api.get(`policies/${policy.id}/customers/`);
			selectedPolicyCustomers = res.data;
			selectedPolicyTitle = policy.title;
			showCustomers = true;
		} catch (error) {
			toast.error('Failed to load customers');
		}
	}

	const policyTypes = ['all', 'health', 'motor', 'life', 'travel'];
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
	<div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
		<div>
			<h1 class="text-3xl font-bold text-slate-50 tracking-tight">Explore Policies</h1>
			<p class="mt-1 text-lg text-slate-300">Compare and find the best coverage for your needs.</p>
		</div>
		{#if auth.user?.role === 'provider' || auth.user?.role === 'admin'}
			<a href="/policies/new">
				<Button>
					<Plus class="w-5 h-5 mr-2" /> Add New Policy
				</Button>
			</a>
		{/if}
	</div>

	<!-- Search & Filters Bar -->
	<div class="space-y-4 mb-8">
		<div class="dashboard-toolbar flex flex-col gap-4 md:flex-row md:items-center">
			<div class="relative flex-grow">
				<Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
				<input
					type="text"
					placeholder="Search by title, provider..."
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
					onchange={fetchPolicies}
					class="dashboard-control min-w-[220px] text-sm font-semibold"
				>
					<option value="premium_amount">Price: Low to High</option>
					<option value="-premium_amount">Price: High to Low</option>
					<option value="-coverage_amount">Coverage: High to Low</option>
				</select>
			</div>

			{#if compareList.length > 0}
				<Button variant="outline" onclick={() => showCompare = true} class="relative">
					Compare ({compareList.length})
					<span class="absolute -top-2 -right-2 flex h-5 w-5 items-center justify-center rounded-full bg-violet-500 text-[10px] font-bold text-white shadow-[0_10px_22px_rgba(139,92,246,0.45)]">
						{compareList.length}
					</span>
				</Button>
			{/if}
		</div>

		{#if showFilters}
			<div class="dashboard-filter-panel grid grid-cols-1 gap-6 animate-in slide-in-from-top-2 duration-200 md:grid-cols-3">
				<div class="space-y-2">
					<label for="policy-type-filter" class="text-xs font-bold uppercase tracking-wider text-slate-300">Policy Type</label>
					<select 
						id="policy-type-filter"
						bind:value={selectedType} 
						onchange={fetchPolicies}
						class="dashboard-control text-sm"
					>
						{#each policyTypes as type}
							<option value={type}>{type.charAt(0).toUpperCase() + type.slice(1)}</option>
						{/each}
					</select>
				</div>
				<div class="space-y-2">
					<label for="min-premium-filter" class="text-xs font-bold uppercase tracking-wider text-slate-300">Min Premium ($)</label>
					<input 
						id="min-premium-filter"
						type="number" 
						bind:value={minPrice} 
						oninput={handleSearch}
						placeholder="0"
						class="dashboard-control text-sm" 
					/>
				</div>
				<div class="space-y-2">
					<label for="max-premium-filter" class="text-xs font-bold uppercase tracking-wider text-slate-300">Max Premium ($)</label>
					<input 
						id="max-premium-filter"
						type="number" 
						bind:value={maxPrice} 
						oninput={handleSearch}
						placeholder="10000"
						class="dashboard-control text-sm" 
					/>
				</div>
			</div>
		{/if}
	</div>

	<!-- Policies Grid -->
	{#if isLoading}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{#each Array(6) as _}
				<div class="dashboard-card h-64 animate-pulse"></div>
			{/each}
		</div>
	{:else if policies.length === 0}
		<div class="dashboard-empty-state py-24 text-center">
			<Shield class="mx-auto mb-4 w-16 h-16 text-slate-600" />
			<h3 class="text-xl font-bold text-slate-50">No policies found</h3>
			<p class="mt-2 text-slate-300">Try broadening your filters or search terms.</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{#each policies as policy}
				<div class="dashboard-card group flex flex-col overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:border-violet-300/22 hover:shadow-[0_28px_75px_rgba(76,29,149,0.28)]">
					<div class="p-8 flex-grow">
						<div class="flex justify-between items-start mb-6">
							<div class="rounded-2xl border border-violet-300/12 bg-violet-500/14 p-4 text-violet-200 transition-transform duration-300 group-hover:scale-110">
								<Shield class="w-8 h-8" />
							</div>
							<div class="text-right">
								<p class="text-3xl font-black text-slate-50">${parseFloat(policy.premium_amount).toLocaleString()}</p>
								<p class="text-xs font-bold uppercase tracking-widest text-slate-400">per year</p>
							</div>
						</div>
						
						<a href={`/policies/${policy.id}`}>
							<h3 class="mb-2 text-xl font-bold leading-tight text-slate-50 transition-colors hover:text-violet-200">{policy.title}</h3>
						</a>
						<p class="mb-6 line-clamp-2 text-sm font-medium text-slate-300">{policy.description}</p>

						<div class="grid grid-cols-2 gap-4 mb-8">
							<div class="rounded-2xl border border-white/6 bg-black/15 p-3">
								<p class="mb-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">Coverage</p>
								<p class="text-sm font-bold text-slate-50">${parseFloat(policy.coverage_amount).toLocaleString()}</p>
							</div>
							<div class="rounded-2xl border border-white/6 bg-black/15 p-3">
								<p class="mb-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">Provider</p>
								<p class="truncate text-sm font-bold text-slate-50">{policy.provider?.company_name || 'N/A'}</p>
							</div>
						</div>

						<div class="space-y-3">
							{#each ['Instant Approval', 'Paperless Process', '24/7 Support'] as feature}
								<div class="flex items-center gap-2 text-sm text-slate-200">
									<Check class="w-4 h-4 text-emerald-300" />
									{feature}
								</div>
							{/each}
						</div>
					</div>

					<div class="p-6 pt-0 mt-auto flex flex-wrap gap-3">
						{#if auth.user?.role === 'customer'}
							{#if policy.is_owned}
								<Button variant="success" class="pointer-events-none flex-grow">
									<Check class="w-4 h-4 mr-2" /> Owned
								</Button>
							{:else}
								<Button class="flex-grow" onclick={() => buyPolicy(policy.id)}>
									<ShoppingCart class="w-4 h-4 mr-2" /> Buy Now
								</Button>
							{/if}
						{:else if !auth.user}
							<a href="/login" class="flex-grow">
								<Button class="w-full">Login to Buy</Button>
							</a>
						{/if}

						{#if auth.user?.role === 'provider' || auth.user?.role === 'admin'}
							<div class="flex gap-2 w-full">
								<Button variant="outline" class="flex-grow" onclick={() => viewCustomers(policy)}>
									<Users class="w-4 h-4 mr-2" /> Customers
								</Button>
								<a href={`/policies/edit/${policy.id}`} class="flex-grow">
									<Button variant="outline" class="w-full">
										<Edit class="w-4 h-4 mr-2" /> Edit
									</Button>
								</a>
								<Button variant="danger" onclick={() => deletePolicy(policy.id)}>
									<Trash2 class="w-4 h-4" />
								</Button>
							</div>
						{/if}

						<Button 
							variant="outline" 
							onclick={() => toggleCompare(policy)}
							class={compareList.find(p => p.id === policy.id) ? 'border-violet-300/28 bg-violet-500/14 text-violet-100' : 'w-full md:w-auto'}
						>
							<ArrowUpDown class="w-4 h-4" />
						</Button>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<!-- Comparison Modal -->
{#if showCompare}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/72 p-4 backdrop-blur-md">
		<div class="dashboard-modal-panel flex max-h-[90vh] w-full max-w-5xl flex-col overflow-hidden">
			<div class="flex items-center justify-between border-b border-white/8 bg-white/[0.03] p-6">
				<h2 class="text-2xl font-bold text-slate-50">Compare Policies</h2>
				<button onclick={() => showCompare = false} class="rounded-full p-2 text-slate-300 transition-colors hover:bg-white/8 hover:text-white">
					<X class="w-6 h-6" />
				</button>
			</div>
			
			<div class="p-8 overflow-x-auto">
				<table class="w-full border-collapse">
					<thead>
						<tr>
							<th class="px-6 py-4 text-left text-xs font-bold uppercase tracking-widest text-slate-400">Features</th>
							{#each compareList as p}
								<th class="py-4 px-6 text-center min-w-[200px]">
									<div class="mx-auto mb-3 w-fit rounded-2xl border border-violet-300/12 bg-violet-500/14 p-3 text-violet-200">
										<Shield class="w-6 h-6" />
									</div>
									<p class="text-lg font-bold text-slate-50">{p.title}</p>
								</th>
							{/each}
						</tr>
					</thead>
					<tbody class="divide-y divide-white/6">
						<tr>
							<td class="px-6 py-6 font-bold text-slate-300">Premium</td>
							{#each compareList as p}
								<td class="px-6 py-6 text-center text-xl font-black text-slate-50">${parseFloat(p.premium_amount).toLocaleString()}</td>
							{/each}
						</tr>
						<tr>
							<td class="px-6 py-6 font-bold text-slate-300">Coverage</td>
							{#each compareList as p}
								<td class="px-6 py-6 text-center font-bold text-slate-50">${parseFloat(p.coverage_amount).toLocaleString()}</td>
							{/each}
						</tr>
						<tr>
							<td class="px-6 py-6 font-bold text-slate-300">Provider</td>
							{#each compareList as p}
								<td class="px-6 py-6 text-center font-medium text-slate-200">{p.provider?.company_name || 'N/A'}</td>
							{/each}
						</tr>
						<tr>
							<td class="px-6 py-6 font-bold text-slate-300">Type</td>
							{#each compareList as p}
								<td class="px-6 py-6 text-center">
									<span class="rounded-full border border-white/8 bg-white/6 px-3 py-1 text-xs font-bold uppercase tracking-wider text-slate-200">
										{p.policy_type}
									</span>
								</td>
							{/each}
						</tr>
					</tbody>
				</table>
			</div>
			
			<div class="flex justify-end gap-4 border-t border-white/8 bg-white/[0.03] p-8">
				<Button variant="outline" onclick={() => { compareList = []; showCompare = false; }}>Clear All</Button>
				<Button onclick={() => showCompare = false}>Close</Button>
			</div>
		</div>
	</div>
{/if}

<!-- Customers Modal -->
{#if showCustomers}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/72 p-4 backdrop-blur-md">
		<div class="dashboard-modal-panel flex max-h-[90vh] w-full max-w-3xl flex-col overflow-hidden">
			<div class="flex items-center justify-between border-b border-white/8 bg-white/[0.03] p-6">
				<div>
					<h2 class="text-2xl font-bold text-slate-50">Policy Customers</h2>
					<p class="text-sm text-slate-300">{selectedPolicyTitle}</p>
				</div>
				<button onclick={() => showCustomers = false} class="rounded-full p-2 text-slate-300 transition-colors hover:bg-white/8 hover:text-white">
					<X class="w-6 h-6" />
				</button>
			</div>
			
			<div class="p-6 overflow-y-auto">
				{#if selectedPolicyCustomers.length === 0}
					<div class="text-center py-12">
						<Users class="mx-auto mb-4 h-12 w-12 text-slate-600" />
						<p class="text-slate-300">No customers have purchased this policy yet.</p>
					</div>
				{:else}
					<div class="space-y-4">
						{#each selectedPolicyCustomers as up}
							<div class="flex items-center justify-between rounded-2xl border border-white/8 bg-white/[0.04] p-4">
								<div class="flex items-center gap-4">
									<div class="flex h-10 w-10 items-center justify-center rounded-full border border-violet-300/12 bg-violet-500/14 font-bold text-violet-100">
										{up.user?.username?.charAt(0).toUpperCase() || 'U'}
									</div>
									<div>
										<p class="font-bold text-slate-50">{up.user?.username || 'Unknown User'}</p>
										<p class="text-xs text-slate-300">{up.user?.email}</p>
									</div>
								</div>
								<div class="text-right">
									<p class="text-sm font-medium text-slate-100">Purchased: {new Date(up.purchase_date).toLocaleDateString()}</p>
									<span class="text-[10px] font-bold uppercase tracking-widest text-emerald-300">{up.status}</span>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
			
			<div class="flex justify-end border-t border-white/8 bg-white/[0.03] p-6">
				<Button onclick={() => showCustomers = false}>Close</Button>
			</div>
		</div>
	</div>
{/if}
