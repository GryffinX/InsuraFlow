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

<div class="max-w-3xl mx-auto px-4 py-8">
    <div class="mb-8 flex items-center gap-4">
        <a href="/policies" class="p-2 hover:bg-slate-100 rounded-full transition-colors">
            <ArrowLeft class="w-6 h-6 text-slate-600" />
        </a>
        <div>
            <h1 class="text-3xl font-bold text-slate-900 tracking-tight">Create New Policy Plan</h1>
            <p class="text-slate-500 mt-1">Design a new insurance offering for the catalog.</p>
        </div>
    </div>

    <form onsubmit={handleSubmit} class="bg-white rounded-3xl border border-slate-200 shadow-xl overflow-hidden p-8 space-y-8">
        <div class="space-y-6">
            <Input
                label="Policy Title"
                placeholder="e.g. Comprehensive Family Health"
                required
                bind:value={formData.title}
            />
            
            <div class="space-y-1">
                <label for="new-policy-description" class="block text-sm font-medium text-slate-700">Description</label>
                <textarea 
                    id="new-policy-description"
                    class="block w-full rounded-xl border-slate-200 bg-slate-50 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-all border p-4 outline-none" 
                    rows="4"
                    placeholder="Describe the coverage and benefits..."
                    bind:value={formData.description}
                    required
                ></textarea>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-1">
                    <label for="new-policy-type" class="block text-sm font-medium text-slate-700">Policy Type</label>
                    <select 
                        id="new-policy-type"
                        class="block w-full rounded-xl border-slate-200 bg-slate-50 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-all border p-3 outline-none font-medium"
                        bind:value={formData.policy_type}
                    >
                        <option value="health">Health</option>
                        <option value="motor">Motor</option>
                        <option value="life">Life</option>
                        <option value="travel">Travel</option>
                    </select>
                </div>
                
                <Input label="Coverage Amount ($)" type="number" placeholder="50000" bind:value={formData.coverage_amount} required />
                <Input label="Annual Premium ($)" type="number" placeholder="1200" bind:value={formData.premium_amount} required />
                
                <div class="flex items-center gap-2 pt-8">
                    <input type="checkbox" id="is_active" bind:checked={formData.is_active} class="w-4 h-4 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500" />
                    <label for="is_active" class="text-sm font-medium text-slate-700">Active and available for purchase</label>
                </div>
            </div>
        </div>

        <div class="pt-6 border-t border-slate-100 flex justify-end gap-4">
            <a href="/policies">
                <Button variant="outline" type="button">Cancel</Button>
            </a>
            <Button type="submit" loading={isLoading} class="px-8">
                Create Policy
            </Button>
        </div>
    </form>
</div>
