<script lang="ts">
	import { api } from '$lib/api/axios';
	import { auth } from '$lib/stores/auth.svelte';
	import { onMount } from 'svelte';
	import { Shield, Search, Filter, ArrowUpDown, Check, Info, ShoppingCart, X, Edit, Trash2, Users, Plus } from 'lucide-svelte';
	import { Button } from '$lib/components';
	import { toast } from 'svelte-sonner';

	let policies = $state<any[]>([]);
	let isLoading = $state(true);
	let searchQuery = $state('');
	let selectedType = $state('all');
	let sortBy = $state('premium_amount');
	let compareList = $state<any[]>([]);
	let showCompare = $state(false);
	
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
			if (selectedType !== 'all') {
				params.policy_type = selectedType;
			}
			const res = await api.get('policies/', { params });
			policies = res.data.results || res.data;
			console.log("Policies fetched:", policies);
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
			toast.success('Policy purchased successfully! Check your dashboard.');
			fetchPolicies(); // Refresh to update 'is_owned' status
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
			fetchPolicies();
		} catch (error: any) {
			toast.error('Failed to delete policy');
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
			<h1 class="text-3xl font-bold text-slate-900 tracking-tight">Explore Policies</h1>
			<p class="text-slate-500 mt-1 text-lg">Compare and find the best coverage for your needs.</p>
		</div>
		{#if auth.user?.role === 'provider' || auth.user?.role === 'admin' || auth.user?.role === 'agent'}
			<a href="/policies/new">
				<Button>
					<Plus class="w-5 h-5 mr-2" /> Add New Policy
				</Button>
			</a>
		{/if}
	</div>

	<!-- Search & Filters Bar -->
	<div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm mb-8 space-y-4 md:space-y-0 md:flex md:items-center md:gap-4">
		<div class="relative flex-grow">
			<Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
			<input
				type="text"
				placeholder="Search by title, provider..."
				class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
				bind:value={searchQuery}
				oninput={handleSearch}
			/>
		</div>
		
		<div class="flex gap-2">
			<select 
				bind:value={selectedType} 
				onchange={fetchPolicies}
				class="bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500 text-sm font-medium"
			>
				{#each policyTypes as type}
					<option value={type}>{type.charAt(0).toUpperCase() + type.slice(1)}</option>
				{/each}
			</select>

			<select 
				bind:value={sortBy} 
				onchange={fetchPolicies}
				class="bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500 text-sm font-medium"
			>
				<option value="premium_amount">Price: Low to High</option>
				<option value="-premium_amount">Price: High to Low</option>
				<option value="-coverage_amount">Coverage: High to Low</option>
			</select>
		</div>

		{#if compareList.length > 0}
			<Button variant="outline" onclick={() => showCompare = true} class="relative">
				Compare ({compareList.length})
				<span class="absolute -top-2 -right-2 bg-indigo-600 text-white w-5 h-5 rounded-full text-[10px] flex items-center justify-center font-bold">
					{compareList.length}
				</span>
			</Button>
		{/if}
	</div>

	<!-- Policies Grid -->
	{#if isLoading}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{#each Array(6) as _}
				<div class="bg-white h-64 rounded-3xl border border-slate-200 animate-pulse"></div>
			{/each}
		</div>
	{:else if policies.length === 0}
		<div class="text-center py-24 bg-white rounded-3xl border-2 border-dashed border-slate-200">
			<Shield class="w-16 h-16 text-slate-200 mx-auto mb-4" />
			<h3 class="text-xl font-bold text-slate-900">No policies found</h3>
			<p class="text-slate-500 mt-2">Try broadening your filters or search terms.</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{#each policies as policy}
				<div class="bg-white rounded-3xl border border-slate-200 shadow-sm hover:shadow-xl transition-all duration-300 group flex flex-col overflow-hidden">
					<div class="p-8 flex-grow">
						<div class="flex justify-between items-start mb-6">
							<div class="bg-indigo-50 p-4 rounded-2xl text-indigo-600 group-hover:scale-110 transition-transform duration-300">
								<Shield class="w-8 h-8" />
							</div>
							<div class="text-right">
								<p class="text-3xl font-black text-slate-900">${parseFloat(policy.premium_amount).toLocaleString()}</p>
								<p class="text-xs font-bold text-slate-400 uppercase tracking-widest">per year</p>
							</div>
						</div>
						
						<a href={`/policies/${policy.id}`}>
							<h3 class="text-xl font-bold text-slate-900 mb-2 leading-tight hover:text-indigo-600 transition-colors">{policy.title}</h3>
						</a>
						<p class="text-sm font-medium text-slate-500 mb-6 line-clamp-2">{policy.description}</p>

						<div class="grid grid-cols-2 gap-4 mb-8">
							<div class="bg-slate-50 p-3 rounded-2xl">
								<p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Coverage</p>
								<p class="text-sm font-bold text-slate-900">${parseFloat(policy.coverage_amount).toLocaleString()}</p>
							</div>
							<div class="bg-slate-50 p-3 rounded-2xl">
								<p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Provider</p>
								<p class="text-sm font-bold text-slate-900 truncate">{policy.provider?.company_name || 'N/A'}</p>
							</div>
						</div>

						<div class="space-y-3">
							{#each ['Instant Approval', 'Paperless Process', '24/7 Support'] as feature}
								<div class="flex items-center gap-2 text-sm text-slate-600">
									<Check class="w-4 h-4 text-emerald-500" />
									{feature}
								</div>
							{/each}
						</div>
					</div>

					<div class="p-6 pt-0 mt-auto flex flex-wrap gap-3">
						{#if auth.user?.role === 'customer'}
							{#if policy.is_owned}
								<Button class="flex-grow bg-emerald-500 hover:bg-emerald-600 pointer-events-none">
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

						{#if auth.user?.role === 'provider' || auth.user?.role === 'admin' || auth.user?.role === 'agent'}
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
							class={compareList.find(p => p.id === policy.id) ? 'border-indigo-600 text-indigo-600' : 'w-full md:w-auto'}
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
	<div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
		<div class="bg-white rounded-3xl w-full max-w-5xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
			<div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
				<h2 class="text-2xl font-bold text-slate-900">Compare Policies</h2>
				<button onclick={() => showCompare = false} class="p-2 hover:bg-slate-200 rounded-full transition-colors">
					<X class="w-6 h-6" />
				</button>
			</div>
			
			<div class="p-8 overflow-x-auto">
				<table class="w-full border-collapse">
					<thead>
						<tr>
							<th class="text-left py-4 px-6 text-slate-400 font-bold uppercase tracking-widest text-xs">Features</th>
							{#each compareList as p}
								<th class="py-4 px-6 text-center min-w-[200px]">
									<div class="bg-indigo-50 p-3 rounded-2xl text-indigo-600 w-fit mx-auto mb-3">
										<Shield class="w-6 h-6" />
									</div>
									<p class="text-lg font-bold text-slate-900">{p.title}</p>
								</th>
							{/each}
						</tr>
					</thead>
					<tbody class="divide-y divide-slate-100">
						<tr>
							<td class="py-6 px-6 font-bold text-slate-600">Premium</td>
							{#each compareList as p}
								<td class="py-6 px-6 text-center text-xl font-black text-slate-900">${parseFloat(p.premium_amount).toLocaleString()}</td>
							{/each}
						</tr>
						<tr>
							<td class="py-6 px-6 font-bold text-slate-600">Coverage</td>
							{#each compareList as p}
								<td class="py-6 px-6 text-center font-bold text-slate-900">${parseFloat(p.coverage_amount).toLocaleString()}</td>
							{/each}
						</tr>
						<tr>
							<td class="py-6 px-6 font-bold text-slate-600">Provider</td>
							{#each compareList as p}
								<td class="py-6 px-6 text-center font-medium text-slate-700">{p.provider?.company_name || 'N/A'}</td>
							{/each}
						</tr>
						<tr>
							<td class="py-6 px-6 font-bold text-slate-600">Type</td>
							{#each compareList as p}
								<td class="py-6 px-6 text-center">
									<span class="px-3 py-1 bg-slate-100 rounded-full text-xs font-bold uppercase tracking-wider">
										{p.policy_type}
									</span>
								</td>
							{/each}
						</tr>
					</tbody>
				</table>
			</div>
			
			<div class="p-8 bg-slate-50 border-t border-slate-100 flex justify-end gap-4">
				<Button variant="outline" onclick={() => { compareList = []; showCompare = false; }}>Clear All</Button>
				<Button onclick={() => showCompare = false}>Close</Button>
			</div>
		</div>
	</div>
{/if}

<!-- Customers Modal -->
{#if showCustomers}
	<div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
		<div class="bg-white rounded-3xl w-full max-w-3xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
			<div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
				<div>
					<h2 class="text-2xl font-bold text-slate-900">Policy Customers</h2>
					<p class="text-sm text-slate-500">{selectedPolicyTitle}</p>
				</div>
				<button onclick={() => showCustomers = false} class="p-2 hover:bg-slate-200 rounded-full transition-colors">
					<X class="w-6 h-6" />
				</button>
			</div>
			
			<div class="p-6 overflow-y-auto">
				{#if selectedPolicyCustomers.length === 0}
					<div class="text-center py-12">
						<Users class="w-12 h-12 text-slate-200 mx-auto mb-4" />
						<p class="text-slate-500">No customers have purchased this policy yet.</p>
					</div>
				{:else}
					<div class="space-y-4">
						{#each selectedPolicyCustomers as up}
							<div class="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-slate-100">
								<div class="flex items-center gap-4">
									<div class="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold">
										{up.user?.username?.charAt(0).toUpperCase() || 'U'}
									</div>
									<div>
										<p class="font-bold text-slate-900">{up.user?.username || 'Unknown User'}</p>
										<p class="text-xs text-slate-500">{up.user?.email}</p>
									</div>
								</div>
								<div class="text-right">
									<p class="text-sm font-medium text-slate-900">Purchased: {new Date(up.purchase_date).toLocaleDateString()}</p>
									<span class="text-[10px] font-bold uppercase tracking-widest text-emerald-600">{up.status}</span>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
			
			<div class="p-6 bg-slate-50 border-t border-slate-100 flex justify-end">
				<Button onclick={() => showCustomers = false}>Close</Button>
			</div>
		</div>
	</div>
{/if}
