<script lang="ts">
    import { api } from '$lib/api/axios';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { FileText, ArrowLeft } from 'lucide-svelte';

    let policies = $state([]);
    let providers = $state([]);
    
    let formData = $state({
        policy_id: '',
        service_provider_id: '',
        claim_amount: '',
        claim_reason: '',
        status: 'filed'
    });

    let isLoading = $state(false);

    onMount(async () => {
        try {
            const [policiesRes, providersRes] = await Promise.all([
                api.get('/policies/'),
                api.get('/providers/')
            ]);
            policies = policiesRes.data.results || policiesRes.data;
            providers = providersRes.data.results || providersRes.data;
        } catch (error) {
            console.error('Failed to fetch initial data', error);
        }
    });

    async function handleSubmit(e: Event) {
        e.preventDefault();
        isLoading = true;
        try {
            await api.post('/claims/', formData);
            toast.success('Claim filed successfully');
            goto('/claims');
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Failed to file claim');
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="max-w-3xl mx-auto px-4 py-8">
    <div class="mb-8 flex items-center gap-4">
        <a href="/claims" class="p-2 hover:bg-slate-100 rounded-full transition-colors">
            <ArrowLeft class="w-6 h-6 text-slate-600" />
        </a>
        <div>
            <h1 class="text-3xl font-bold text-slate-900">File New Claim</h1>
            <p class="text-slate-500">Enter details to file a new insurance claim.</p>
        </div>
    </div>

    <form onsubmit={handleSubmit} class="bg-white rounded-2xl border border-slate-200 shadow-xl p-8 space-y-6">
        <div class="space-y-6">
            <div class="space-y-1">
                <label class="block text-sm font-medium text-slate-700" for="policy">
                    Policy
                </label>
                <select
                    id="policy"
                    class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none"
                    bind:value={formData.policy_id}
                    required
                >
                    <option value="">Select Policy</option>
                    {#each policies as policy}
                        <option value={policy.id}>{policy.policy_number} ({policy.policy_type})</option>
                    {/each}
                </select>
            </div>

            <div class="space-y-1">
                <label class="block text-sm font-medium text-slate-700" for="provider">
                    Service Provider (Hospital/Garage)
                </label>
                <select
                    id="provider"
                    class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none"
                    bind:value={formData.service_provider_id}
                    required
                >
                    <option value="">Select Provider</option>
                    {#each providers as provider}
                        <option value={provider.id}>{provider.name} ({provider.provider_type})</option>
                    {/each}
                </select>
            </div>

            <Input
                label="Claim Amount"
                type="number"
                id="claim_amount"
                placeholder="5000"
                required
                bind:value={formData.claim_amount}
            />

            <div class="space-y-1">
                <label class="block text-sm font-medium text-slate-700" for="reason">
                    Reason for Claim
                </label>
                <textarea
                    id="reason"
                    rows="4"
                    class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none"
                    placeholder="Describe the incident..."
                    bind:value={formData.claim_reason}
                    required
                ></textarea>
            </div>
        </div>

        <div class="pt-4 border-t border-slate-100 flex justify-end gap-4">
            <a href="/claims">
                <Button variant="outline" type="button">Cancel</Button>
            </a>
            <Button type="submit" loading={isLoading}>
                File Claim
            </Button>
        </div>
    </form>
</div>
