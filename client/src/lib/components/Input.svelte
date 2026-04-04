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

<div class="space-y-2 group">
	{#if label}
		<label class="ml-1 block text-xs font-bold uppercase tracking-[0.22em] text-slate-400 transition-colors group-focus-within:text-violet-300" for={props.id}>
			{label}
		</label>
	{/if}
	<input
		class={cn(
			'input-field',
			error ? 'border-rose-400/50 bg-rose-950/30 focus:shadow-[0_0_0_4px_rgba(251,113,133,0.12)]' : '',
			className
		)}
		{type}
		bind:value
		{...props}
	/>
	{#if error}
		<p class="mt-1.5 ml-1 text-xs font-bold text-rose-300 animate-fade-in">{error}</p>
	{/if}
</div>
