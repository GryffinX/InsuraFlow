<script lang="ts">
	import { cn } from '$lib/utils';
	import type { HTMLInputAttributes } from 'svelte/elements';

	interface Props extends HTMLInputAttributes {
		label?: string;
		error?: string;
        value?: string | number;
	}

	let { class: className, label, error, type = "text", value = $bindable(), ...props }: Props = $props();
</script>

<div class="space-y-1">
	{#if label}
		<label class="block text-sm font-medium text-slate-700" for={props.id}>
			{label}
		</label>
	{/if}
	<input
		class={cn(
			'block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none',
			error ? 'border-red-500' : 'border-slate-300',
			className
		)}
		{type}
		bind:value
		{...props}
	/>
	{#if error}
		<p class="text-xs text-red-500 mt-1">{error}</p>
	{/if}
</div>
