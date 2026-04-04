<script lang="ts">
    import { api } from '$lib/api/axios';
    import { auth } from '$lib/stores/auth.svelte';
    import { onMount } from 'svelte';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { Users, Search, Shield, Mail, Phone, Calendar, Filter, CheckCircle, XCircle, Clock, X } from 'lucide-svelte';

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
            case 'admin': return 'bg-rose-50 text-rose-600 border-rose-100';
            case 'provider': return 'bg-indigo-50 text-indigo-600 border-indigo-100';
            case 'agent': return 'bg-amber-50 text-amber-600 border-amber-100';
            case 'surveyor': return 'bg-emerald-50 text-emerald-600 border-emerald-100';
            default: return 'bg-slate-50 text-slate-600 border-slate-100';
        }
    }

    const roles = ['all', 'customer', 'agent', 'provider', 'surveyor', 'admin'];
    const statuses = ['all', 'verified', 'pending'];
</script>

<div class="max-w-7xl mx-auto px-4 py-8">
    <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 tracking-tight">User Management</h1>
        <p class="text-slate-500 mt-1">Global system oversight of all registered users and their roles.</p>
    </div>

    <!-- Search & Filters Bar (Reusing Policy patterns) -->
    <div class="space-y-4 mb-8">
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center gap-4">
            <div class="relative flex-grow">
                <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                    type="text"
                    placeholder="Search by name, email..."
                    class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
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
            <div class="bg-slate-100 p-6 rounded-2xl border border-slate-200 grid grid-cols-1 md:grid-cols-2 gap-6 animate-in slide-in-from-top-2 duration-200">
                <div class="space-y-2">
                    <label class="text-xs font-bold text-slate-500 uppercase tracking-wider">Filter by Role</label>
                    <select 
                        bind:value={selectedRole} 
                        onchange={fetchUsers}
                        class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
                    >
                        {#each roles as role}
                            <option value={role}>{role.charAt(0).toUpperCase() + role.slice(1)}</option>
                        {/each}
                    </select>
                </div>
                <div class="space-y-2">
                    <label class="text-xs font-bold text-slate-500 uppercase tracking-wider">Verification Status</label>
                    <select 
                        bind:value={selectedStatus} 
                        onchange={fetchUsers}
                        class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
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
                <div class="h-48 bg-white rounded-3xl border border-slate-200 animate-pulse"></div>
            {/each}
        {:else if users.length === 0}
            <div class="col-span-full py-20 text-center bg-white rounded-3xl border border-slate-200">
                <Users class="w-12 h-12 text-slate-200 mx-auto mb-4" />
                <p class="text-slate-500">No users found.</p>
            </div>
        {:else}
            {#each users as user}
                <div class="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm hover:shadow-md transition-all group flex flex-col">
                    <div class="flex items-start justify-between mb-4">
                        <div class="w-12 h-12 bg-slate-100 rounded-2xl flex items-center justify-center text-slate-600 font-bold text-xl group-hover:bg-indigo-100 group-hover:text-indigo-600 transition-colors">
                            {user.username?.charAt(0).toUpperCase()}
                        </div>
                        <div class="flex flex-col items-end gap-2">
                            <span class={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest border ${getRoleColor(user.role)}`}>
                                {user.role}
                            </span>
                            {#if user.is_verified}
                                <span class="flex items-center gap-1 text-[10px] font-bold text-emerald-600 uppercase">
                                    <CheckCircle class="w-3 h-3" /> Verified
                                </span>
                            {:else}
                                <span class="flex items-center gap-1 text-[10px] font-bold text-amber-600 uppercase">
                                    <Clock class="w-3 h-3" /> Pending
                                </span>
                            {/if}
                        </div>
                    </div>
                    
                    <div class="space-y-3 flex-grow">
                        <div>
                            <h3 class="font-bold text-slate-900 leading-tight">{user.username}</h3>
                            <p class="text-xs text-slate-500 flex items-center gap-1 mt-1">
                                <Mail class="w-3 h-3" /> {user.email}
                            </p>
                            <p class="text-[10px] font-mono text-slate-400 mt-1">{user.formatted_id}</p>
                        </div>
                        
                        <div class="pt-3 border-t border-slate-50 flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                {#if user.phone}
                                    <div class="p-1.5 bg-slate-50 rounded-lg text-slate-400" title={user.phone}>
                                        <Phone class="w-3.5 h-3.5" />
                                    </div>
                                {/if}
                            </div>
                            <span class="text-[10px] text-slate-300 font-bold uppercase">ID: #{user.id}</span>
                        </div>
                    </div>

                    {#if !user.is_verified && user.role !== 'admin'}
                        <div class="mt-4 pt-4 border-t border-slate-100 flex gap-2">
                            <Button class="flex-grow text-xs h-9" onclick={() => verifyUser(user.id)}>
                                <CheckCircle class="w-3 h-3 mr-1" /> Approve
                            </Button>
                            <Button variant="outline" class="flex-grow text-xs h-9 text-rose-600 hover:bg-rose-50 border-rose-100" onclick={() => rejectUser(user.id)}>
                                <XCircle class="w-3 h-3 mr-1" /> Reject
                            </Button>
                        </div>
                    {/if}
                </div>
            {/each}
        {/if}
    </div>
</div>
