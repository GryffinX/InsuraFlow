<script lang="ts">
    import { api } from '$lib/api/axios';
    import { onMount } from 'svelte';
    import { Button } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import CheckCircle from 'lucide-svelte/icons/check-circle';
    import Clock from 'lucide-svelte/icons/clock';
    import Filter from 'lucide-svelte/icons/filter';
    import Mail from 'lucide-svelte/icons/mail';
    import Phone from 'lucide-svelte/icons/phone';
    import Search from 'lucide-svelte/icons/search';
    import Users from 'lucide-svelte/icons/users';
    import XCircle from 'lucide-svelte/icons/x-circle';

    let users = $state<any[]>([]);
    let isLoading = $state(true);
    let searchQuery = $state('');
    let selectedRole = $state('all');
    let selectedStatus = $state('all');
    let showFilters = $state(false);
    
    let debounceTimer: any;
    function handleSearch() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            fetchUsers();
        }, 300);
    }

    onMount(fetchUsers);

    async function fetchUsers() {
        isLoading = true;
        try {
            const params: any = { 
                search: searchQuery
            };
            if (selectedRole !== 'all') params.role = selectedRole;
            if (selectedStatus !== 'all') params.is_verified = selectedStatus === 'verified';

            const res = await api.get('users/', { params });
            const data = res.data.results || res.data;
            users = data;
            console.log("Admin Users API Response:", res.data);
        } catch (error) {
            toast.error('Failed to load users');
        } finally {
            isLoading = false;
        }
    }

    async function verifyUser(userId: number) {
        try {
            await api.patch(`users/${userId}/verify/`);
            toast.success('User verified successfully');
            fetchUsers();
        } catch (error: any) {
            toast.error('Failed to verify user');
        }
    }

    async function rejectUser(userId: number) {
        if (!confirm('Are you sure you want to reject and deactivate this user?')) return;
        try {
            await api.patch(`users/${userId}/reject/`);
            toast.success('User rejected');
            fetchUsers();
        } catch (error: any) {
            toast.error('Failed to reject user');
        }
    }

    function getRoleColor(role: string) {
        switch (role) {
            case 'admin': return 'bg-rose-500/14 text-rose-200 border-rose-300/18';
            case 'provider': return 'bg-indigo-500/14 text-indigo-200 border-indigo-300/18';
            case 'agent': return 'bg-amber-500/14 text-amber-200 border-amber-300/18';
            case 'surveyor': return 'bg-emerald-500/14 text-emerald-200 border-emerald-300/18';
            default: return 'bg-slate-500/12 text-slate-200 border-slate-300/14';
        }
    }

    const roles = ['all', 'customer', 'agent', 'provider', 'surveyor', 'admin'];
    const statuses = ['all', 'verified', 'pending'];
</script>

<div class="max-w-7xl mx-auto px-4 py-8">
    <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-50 tracking-tight">User Management</h1>
        <p class="text-slate-300 mt-1">Global system oversight of all registered users and their roles.</p>
    </div>

    <!-- Search & Filters Bar (Reusing Policy patterns) -->
    <div class="space-y-4 mb-8">
        <div class="dashboard-toolbar flex flex-col gap-4 md:flex-row md:items-center">
            <div class="relative flex-grow">
                <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                <input
                    type="text"
                    placeholder="Search by name, email..."
                    class="dashboard-control pl-11"
                    bind:value={searchQuery}
                    oninput={handleSearch}
                />
            </div>
            
            <div class="flex gap-2">
                <Button variant="outline" onclick={() => showFilters = !showFilters}>
                    <Filter class="w-4 h-4 mr-2" /> {showFilters ? 'Hide' : ''} Filters
                </Button>
            </div>
        </div>

        {#if showFilters}
            <div class="dashboard-filter-panel grid grid-cols-1 gap-6 animate-in slide-in-from-top-2 duration-200 md:grid-cols-2">
                <div class="space-y-2">
                    <label for="users-role-filter" class="text-xs font-bold text-slate-300 uppercase tracking-wider">Filter by Role</label>
                    <select 
                        id="users-role-filter"
                        bind:value={selectedRole} 
                        onchange={fetchUsers}
                        class="dashboard-control text-sm"
                    >
                        {#each roles as role}
                            <option value={role}>{role.charAt(0).toUpperCase() + role.slice(1)}</option>
                        {/each}
                    </select>
                </div>
                <div class="space-y-2">
                    <label for="users-status-filter" class="text-xs font-bold text-slate-300 uppercase tracking-wider">Verification Status</label>
                    <select 
                        id="users-status-filter"
                        bind:value={selectedStatus} 
                        onchange={fetchUsers}
                        class="dashboard-control text-sm"
                    >
                        {#each statuses as status}
                            <option value={status}>{status.charAt(0).toUpperCase() + status.slice(1)}</option>
                        {/each}
                    </select>
                </div>
            </div>
        {/if}
    </div>

    <!-- Users Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#if isLoading}
            {#each Array(6) as _}
                <div class="dashboard-card h-48 animate-pulse"></div>
            {/each}
        {:else if users.length === 0}
            <div class="dashboard-empty-state col-span-full py-20 text-center">
                <Users class="w-12 h-12 text-slate-600 mx-auto mb-4" />
                <p class="text-slate-300">No users found.</p>
            </div>
        {:else}
            {#each users as user}
                <div class="dashboard-card group flex flex-col p-6 transition-all duration-300 hover:-translate-y-1 hover:border-violet-300/24 hover:shadow-[0_26px_70px_rgba(76,29,149,0.28)]">
                    <div class="flex items-start justify-between mb-4">
                        <div class="flex h-12 w-12 items-center justify-center rounded-2xl border border-white/6 bg-white/6 text-xl font-bold text-slate-200 transition-colors group-hover:border-violet-300/20 group-hover:bg-violet-500/16 group-hover:text-violet-100">
                            {user.username?.charAt(0).toUpperCase()}
                        </div>
                        <div class="flex flex-col items-end gap-2">
                            <span class={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest border ${getRoleColor(user.role)}`}>
                                {user.role}
                            </span>
                            {#if user.is_verified}
                                <span class="flex items-center gap-1 text-[10px] font-bold text-emerald-300 uppercase">
                                    <CheckCircle class="w-3 h-3" /> Verified
                                </span>
                            {:else}
                                <span class="flex items-center gap-1 text-[10px] font-bold text-amber-300 uppercase">
                                    <Clock class="w-3 h-3" /> Pending
                                </span>
                            {/if}
                        </div>
                    </div>
                    
                    <div class="space-y-3 flex-grow">
                        <div>
                            <h3 class="font-bold text-slate-50 leading-tight">{user.username}</h3>
                            <p class="mt-1 flex items-center gap-1 text-xs text-slate-300">
                                <Mail class="w-3 h-3" /> {user.email}
                            </p>
                            <p class="mt-1 text-[10px] font-mono text-slate-500">{user.formatted_id}</p>
                        </div>
                        
                        <div class="flex items-center justify-between border-t border-white/6 pt-3">
                            <div class="flex items-center gap-3">
                                {#if user.phone}
                                    <div class="rounded-lg border border-white/6 bg-white/5 p-1.5 text-slate-400" title={user.phone}>
                                        <Phone class="w-3.5 h-3.5" />
                                    </div>
                                {/if}
                            </div>
                            <span class="text-[10px] font-bold uppercase text-slate-500">ID: #{user.id}</span>
                        </div>
                    </div>

                    {#if !user.is_verified && user.role !== 'admin'}
                        <div class="mt-4 flex gap-2 border-t border-white/8 pt-4">
                            <Button class="flex-grow text-xs h-9" onclick={() => verifyUser(user.id)}>
                                <CheckCircle class="w-3 h-3 mr-1" /> Approve
                            </Button>
                            <Button variant="outline" class="h-9 flex-grow border-rose-300/22 bg-rose-500/8 text-xs text-rose-200 hover:bg-rose-500/14 hover:text-rose-100" onclick={() => rejectUser(user.id)}>
                                <XCircle class="w-3 h-3 mr-1" /> Reject
                            </Button>
                        </div>
                    {/if}
                </div>
            {/each}
        {/if}
    </div>
</div>
