<script lang="ts">
    import { api } from '$lib/api/axios';
    import { auth } from '$lib/stores/auth.svelte';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import ArrowLeft from 'lucide-svelte/icons/arrow-left';

    let formData = $state({
        title: '',
        description: '',
        policy_type: 'health',
        coverage_amount: '',
        premium_amount: '',
        is_active: true
    });

    let isLoading = $state(false);

    onMount(() => {
        if (auth.user?.role !== 'admin' && auth.user?.role !== 'provider') {
            toast.error('Only admins and providers can create policies');
            goto('/policies');
        }
    });

    async function handleSubmit(e: Event) {
        e.preventDefault();
        isLoading = true;
        try {
            await api.post('policies/', formData);
            toast.success('New policy plan created successfully');
            await goto('/policies', { invalidateAll: true });
        } catch (error: any) {
            toast.error(error.response?.data?.error || error.response?.data?.detail || 'Failed to create policy');
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="max-w-3xl mx-auto px-4 py-12">
    <div class="mb-10 flex items-center gap-6 animate-fade-in">
        <a href="/policies" class="p-3 hover:bg-white/10 rounded-2xl transition-all group border border-white/5 hover:border-violet-500/30">
            <ArrowLeft class="w-6 h-6 text-slate-400 group-hover:text-violet-200" />
        </a>
        <div>
            <h1 class="text-4xl font-black text-slate-50 tracking-tight">Create New Policy Plan</h1>
            <p class="text-slate-400 mt-1 font-medium">Design a new insurance offering for the catalog.</p>
        </div>
    </div>

    <form onsubmit={handleSubmit} class="dashboard-card p-10 space-y-10 relative overflow-hidden">
        <div class="absolute top-0 right-0 w-64 h-64 bg-violet-600/5 blur-[100px] -z-10 rounded-full"></div>
        
        <div class="space-y-8">
            <Input
                label="Policy Title"
                placeholder="e.g. Comprehensive Family Health"
                required
                bind:value={formData.title}
                class="bg-white/[0.03] border-white/10 text-slate-50 placeholder:text-slate-600 focus:border-violet-500/50 transition-all rounded-2xl h-14"
            />
            
            <div class="space-y-2">
                <label for="new-policy-description" class="block text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Description</label>
                <textarea 
                    id="new-policy-description"
                    class="block w-full rounded-2xl border-white/10 bg-white/[0.03] text-slate-50 shadow-sm focus:border-violet-500/50 focus:ring-0 sm:text-sm transition-all border p-5 outline-none placeholder:text-slate-600 min-h-[140px]" 
                    placeholder="Describe the coverage and benefits..."
                    bind:value={formData.description}
                    required
                ></textarea>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="space-y-2">
                    <label for="new-policy-type" class="block text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Policy Type</label>
                    <select 
                        id="new-policy-type"
                        class="block w-full rounded-2xl border-white/10 bg-white/[0.03] text-slate-50 shadow-sm focus:border-violet-500/50 focus:ring-0 sm:text-sm transition-all border p-4 outline-none font-bold h-14 appearance-none cursor-pointer"
                        bind:value={formData.policy_type}
                    >
                        <option value="health" class="bg-[#0b0a24]">Health</option>
                        <option value="motor" class="bg-[#0b0a24]">Motor</option>
                        <option value="life" class="bg-[#0b0a24]">Life</option>
                        <option value="travel" class="bg-[#0b0a24]">Travel</option>
                    </select>
                </div>
                
                <Input label="Coverage Amount ($)" type="number" placeholder="50000" bind:value={formData.coverage_amount} required class="bg-white/[0.03] border-white/10 text-slate-50 h-14 rounded-2xl" />
                <Input label="Annual Premium ($)" type="number" placeholder="1200" bind:value={formData.premium_amount} required class="bg-white/[0.03] border-white/10 text-slate-50 h-14 rounded-2xl" />
                
                <div class="flex items-center gap-4 pt-4 ml-1">
                    <div class="relative flex items-center">
                        <input type="checkbox" id="is_active" bind:checked={formData.is_active} class="w-5 h-5 bg-white/5 border-white/10 rounded-lg text-violet-600 focus:ring-violet-500/50 focus:ring-offset-0 transition-all cursor-pointer" />
                    </div>
                    <label for="is_active" class="text-sm font-bold text-slate-300 cursor-pointer select-none">Active and available for purchase</label>
                </div>
            </div>
        </div>

        <div class="pt-8 border-t border-white/8 flex justify-end gap-6">
            <a href="/policies">
                <Button variant="outline" type="button" class="px-8 h-12 rounded-xl font-bold border-white/10 hover:bg-white/5 text-slate-300">Cancel</Button>
            </a>
            <Button type="submit" loading={isLoading} class="px-10 h-12 rounded-xl font-black shadow-[0_12px_40px_rgba(124,58,237,0.25)]">
                Create Policy
            </Button>
        </div>
    </form>
</div>
