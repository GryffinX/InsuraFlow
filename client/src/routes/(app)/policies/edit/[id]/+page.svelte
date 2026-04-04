<script lang="ts">
    import { page } from '$app/state';
    import { api } from '$lib/api/axios';
    import { auth } from '$lib/stores/auth.svelte';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { Save, ArrowLeft } from 'lucide-svelte';

    const id = page.params.id;
    let formData = $state<any>(null);
    let isLoading = $state(true);
    let isSubmitting = $state(false);

    onMount(async () => {
        if (auth.user?.role !== 'admin' && auth.user?.role !== 'provider') {
            toast.error('Only admins and policy-owning providers can edit policies');
            goto('/policies');
            return;
        }

        try {
            const res = await api.get(`policies/${id}/`);
            const data = res.data;
            formData = {
                title: data.title,
                description: data.description,
                policy_type: data.policy_type,
                coverage_amount: data.coverage_amount,
                premium_amount: data.premium_amount,
                is_active: data.is_active
            };
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to load policy');
            goto('/policies');
        } finally {
            isLoading = false;
        }
    });

    async function handleSubmit(e: Event) {
        e.preventDefault();
        isSubmitting = true;
        try {
            await api.patch(`policies/${id}/`, formData);
            toast.success('Policy updated successfully');
            await goto('/policies', { invalidateAll: true });
        } catch (error: any) {
            toast.error(error.response?.data?.error || error.response?.data?.detail || 'Failed to update policy');
        } finally {
            isSubmitting = false;
        }
    }
</script>

<div class="max-w-3xl mx-auto px-4 py-12">
    <div class="mb-8 flex items-center gap-4">
        <button onclick={() => history.back()} class="p-2 hover:bg-slate-100 rounded-full transition-colors">
            <ArrowLeft class="w-6 h-6 text-slate-600" />
        </button>
        <h1 class="text-3xl font-bold text-slate-900">Edit Policy</h1>
    </div>

    {#if isLoading}
        <div class="bg-white rounded-3xl p-8 border border-slate-200 animate-pulse space-y-6">
            <div class="h-10 bg-slate-100 rounded w-1/2"></div>
            <div class="h-32 bg-slate-50 rounded"></div>
            <div class="grid grid-cols-2 gap-6">
                <div class="h-10 bg-slate-50 rounded"></div>
                <div class="h-10 bg-slate-50 rounded"></div>
            </div>
        </div>
    {:else if formData}
        <form onsubmit={handleSubmit} class="bg-white rounded-3xl border border-slate-200 shadow-xl overflow-hidden p-8 space-y-8">
            <div class="space-y-6">
                <Input label="Policy Title" bind:value={formData.title} required />
                
                <div class="space-y-1">
                    <label class="block text-sm font-medium text-slate-700">Description</label>
                    <textarea 
                        class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none" 
                        rows="4"
                        bind:value={formData.description}
                        required
                    ></textarea>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="space-y-1">
                        <label class="block text-sm font-medium text-slate-700">Policy Type</label>
                        <select 
                            class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none"
                            bind:value={formData.policy_type}
                        >
                            <option value="health">Health</option>
                            <option value="motor">Motor</option>
                            <option value="life">Life</option>
                            <option value="travel">Travel</option>
                        </select>
                    </div>
                    <Input label="Coverage Amount ($)" type="number" bind:value={formData.coverage_amount} required />
                    <Input label="Annual Premium ($)" type="number" bind:value={formData.premium_amount} required />
                    
                    <div class="flex items-center gap-2 pt-8">
                        <input type="checkbox" id="is_active" bind:checked={formData.is_active} class="w-4 h-4 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500" />
                        <label for="is_active" class="text-sm font-medium text-slate-700">Active and Available for Sale</label>
                    </div>
                </div>
            </div>

            <div class="pt-6 border-t border-slate-100 flex justify-end gap-4">
                <Button variant="outline" type="button" onclick={() => history.back()}>Cancel</Button>
                <Button type="submit" loading={isSubmitting} class="px-8">
                    <Save class="w-4 h-4 mr-2" /> Save Changes
                </Button>
            </div>
        </form>
    {/if}
</div>
