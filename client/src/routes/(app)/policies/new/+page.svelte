<script lang="ts">
    import { api } from '$lib/api/axios';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { Shield, ArrowLeft } from 'lucide-svelte';

    let insurers = $state([]);
    let agents = $state([]);
    let users = $state([]);
    
    let formData = $state({
        policy_number: '',
        policy_holder_id: '',
        insurer_id: '',
        agent_id: '',
        policy_type: 'health',
        coverage_amount: '',
        premium_amount: '',
        end_date: ''
    });

    let isLoading = $state(false);

    onMount(async () => {
        if (auth.user?.role === 'customer') {
            formData.policy_holder_id = auth.user.id.toString();
        }
        try {
            const [insurersRes, agentsRes] = await Promise.all([
                api.get('/insurers/'),
                api.get('/agents/')
            ]);
            insurers = insurersRes.data.results || insurersRes.data;
            agents = agentsRes.data.results || agentsRes.data;
        } catch (error) {
            console.error('Failed to fetch initial data', error);
        }
    });

    async function handleSubmit(e: Event) {
        e.preventDefault();
        isLoading = true;
        try {
            await api.post('/policies/', formData);
            toast.success('Policy created successfully');
            goto('/policies');
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Failed to create policy');
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
            <h1 class="text-3xl font-bold text-slate-900">Create New Policy</h1>
            <p class="text-slate-500">Enter details to register a new insurance policy.</p>
        </div>
    </div>

    <form onsubmit={handleSubmit} class="bg-white rounded-2xl border border-slate-200 shadow-xl p-8 space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Input
                label="Policy Number"
                id="policy_number"
                placeholder="POL-123456"
                required
                bind:value={formData.policy_number}
            />
            
            <div class="space-y-1">
                <label class="block text-sm font-medium text-slate-700" for="policy_type">
                    Policy Type
                </label>
                <select
                    id="policy_type"
                    class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none"
                    bind:value={formData.policy_type}
                >
                    <option value="health">Health</option>
                    <option value="motor">Motor</option>
                </select>
            </div>

            <div class="space-y-1">
                <label class="block text-sm font-medium text-slate-700" for="insurer">
                    Insurer
                </label>
                <select
                    id="insurer"
                    class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none"
                    bind:value={formData.insurer_id}
                    required
                >
                    <option value="">Select Insurer</option>
                    {#each insurers as insurer}
                        <option value={insurer.id}>{insurer.company_name}</option>
                    {/each}
                </select>
            </div>

            <div class="space-y-1">
                <label class="block text-sm font-medium text-slate-700" for="agent">
                    Agent
                </label>
                <select
                    id="agent"
                    class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none"
                    bind:value={formData.agent_id}
                    required
                >
                    <option value="">Select Agent</option>
                    {#each agents as agent}
                        <option value={agent.id}>{agent.name}</option>
                    {/each}
                </select>
            </div>

            <Input
                label="Coverage Amount"
                type="number"
                id="coverage_amount"
                placeholder="50000"
                required
                bind:value={formData.coverage_amount}
            />

            <Input
                label="Premium Amount"
                type="number"
                id="premium_amount"
                placeholder="1200"
                required
                bind:value={formData.premium_amount}
            />

            <Input
                label="End Date"
                type="date"
                id="end_date"
                required
                bind:value={formData.end_date}
            />
            
            <Input
                label="Policy Holder ID (User ID)"
                type="number"
                id="policy_holder_id"
                placeholder="1"
                required
                bind:value={formData.policy_holder_id}
            />
        </div>

        <div class="pt-4 border-t border-slate-100 flex justify-end gap-4">
            <a href="/policies">
                <Button variant="outline" type="button">Cancel</Button>
            </a>
            <Button type="submit" loading={isLoading}>
                Create Policy
            </Button>
        </div>
    </form>
</div>
