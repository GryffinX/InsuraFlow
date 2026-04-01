<script lang="ts">
    import { api } from '$lib/api/axios';
    import { auth } from '$lib/stores/auth.svelte';
    import { onMount } from 'svelte';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { Users, Search, UserPlus, Shield, Mail, Phone, Calendar, Filter } from 'lucide-svelte';

    let users = $state<any[]>([]);
    let isLoading = $state(true);
    let searchQuery = $state('');

    onMount(fetchUsers);

    async function fetchUsers() {
        isLoading = true;
        try {
            const res = await api.get('users/', {
                params: { search: searchQuery }
            });
            users = res.data.results || res.data;
        } catch (error) {
            toast.error('Failed to load users');
        } finally {
            isLoading = false;
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
</script>

<div class="max-w-7xl mx-auto px-4 py-8">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div>
            <h1 class="text-3xl font-bold text-slate-900 tracking-tight">User Management</h1>
            <p class="text-slate-500 mt-1">Manage all registered users and their roles.</p>
        </div>
        <Button>
            <UserPlus class="w-5 h-5 mr-2" /> Add New User
        </Button>
    </div>

    <!-- Search & Filters -->
    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row gap-4 mb-8">
        <div class="relative flex-grow">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
                type="text"
                placeholder="Search by name, email, phone..."
                class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 transition-all sm:text-sm"
                bind:value={searchQuery}
                onchange={fetchUsers}
            />
        </div>
        <Button variant="outline">
            <Filter class="w-4 h-4 mr-2" /> Filters
        </Button>
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
                <div class="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm hover:shadow-md transition-all group">
                    <div class="flex items-start justify-between mb-4">
                        <div class="w-12 h-12 bg-slate-100 rounded-2xl flex items-center justify-center text-slate-600 font-bold text-xl group-hover:bg-indigo-100 group-hover:text-indigo-600 transition-colors">
                            {user.username?.charAt(0).toUpperCase()}
                        </div>
                        <span class={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest border ${getRoleColor(user.role)}`}>
                            {user.role}
                        </span>
                    </div>
                    
                    <div class="space-y-3">
                        <div>
                            <h3 class="font-bold text-slate-900 line-ignore leading-tight">{user.username}</h3>
                            <p class="text-xs text-slate-500 flex items-center gap-1 mt-1">
                                <Mail class="w-3 h-3" /> {user.email}
                            </p>
                        </div>
                        
                        <div class="pt-3 border-t border-slate-50 flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                {#if user.phone}
                                    <div class="p-1.5 bg-slate-50 rounded-lg text-slate-400" title={user.phone}>
                                        <Phone class="w-3.5 h-3.5" />
                                    </div>
                                {/if}
                                {#if user.dob}
                                    <div class="p-1.5 bg-slate-50 rounded-lg text-slate-400" title={user.dob}>
                                        <Calendar class="w-3.5 h-3.5" />
                                    </div>
                                {/if}
                            </div>
                            <Button variant="ghost" size="sm" class="text-xs font-bold text-indigo-600">Edit Profile</Button>
                        </div>
                    </div>
                </div>
            {/each}
        {/if}
    </div>
</div>
