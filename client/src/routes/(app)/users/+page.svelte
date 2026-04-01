<script lang="ts">
    import { api } from '$lib/api/axios';
    import { auth } from '$lib/stores/auth.svelte';
    import { onMount } from 'svelte';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { Users, Search, UserPlus, Shield, Mail, Phone, Calendar, Filter, X } from 'lucide-svelte';

    let users = $state<any[]>([]);
    let isLoading = $state(true);
    let searchQuery = $state('');
    
    let showAddModal = $state(false);
    let isCreating = $state(false);
    let newUser = $state({
        username: '',
        email: '',
        password: '',
        role: 'customer'
    });

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
            const res = await api.get('users/', {
                params: { search: searchQuery }
            });
            users = res.data.results || res.data;
            console.log("Users fetched:", users);
        } catch (error) {
            toast.error('Failed to load users');
        } finally {
            isLoading = false;
        }
    }

    async function createUser(e: Event) {
        e.preventDefault();
        isCreating = true;
        try {
            await api.post('users/', newUser);
            toast.success('User created successfully');
            showAddModal = false;
            fetchUsers();
            newUser = { username: '', email: '', password: '', role: 'customer' };
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Failed to create user');
        } finally {
            isCreating = false;
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
        <Button onclick={() => showAddModal = true}>
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
                oninput={handleSearch}
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
                            <p class="text-[10px] font-mono text-slate-400 mt-1">{user.formatted_id}</p>
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

{#if showAddModal}
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl w-full max-w-md overflow-hidden shadow-2xl flex flex-col">
            <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
                <h2 class="text-xl font-bold text-slate-900">Add New User</h2>
                <button onclick={() => showAddModal = false} class="p-2 hover:bg-slate-200 rounded-full transition-colors">
                    <X class="w-6 h-6" />
                </button>
            </div>
            
            <form onsubmit={createUser} class="p-6 space-y-4">
                <Input label="Username" bind:value={newUser.username} required />
                <Input label="Email" type="email" bind:value={newUser.email} required />
                <Input label="Password" type="password" bind:value={newUser.password} required />
                
                <div class="space-y-1">
                    <label class="block text-sm font-medium text-slate-700">Role</label>
                    <select 
                        class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none"
                        bind:value={newUser.role}
                    >
                        <option value="customer">Customer</option>
                        <option value="agent">Agent</option>
                        <option value="provider">Provider</option>
                        <option value="surveyor">Surveyor</option>
                        <option value="admin">Admin</option>
                    </select>
                </div>

                <div class="pt-4 flex justify-end gap-3">
                    <Button variant="ghost" type="button" onclick={() => showAddModal = false}>Cancel</Button>
                    <Button type="submit" loading={isCreating}>Create User</Button>
                </div>
            </form>
        </div>
    </div>
{/if}
