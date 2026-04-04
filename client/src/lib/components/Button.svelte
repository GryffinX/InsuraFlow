<script lang="ts">
	import { cn } from '$lib/utils';
	import type { HTMLButtonAttributes } from 'svelte/elements';

	interface Props extends HTMLButtonAttributes {
		variant?: 'primary' | 'secondary' | 'ghost' | 'outline' | 'danger' | 'success';
		size?: 'sm' | 'md' | 'lg' | 'icon';
		loading?: boolean;
	}

	let { 
		class: className, 
		variant = 'primary', 
		size = 'md', 
		loading = false,
		children,
		disabled,
		...props 
	}: Props = $props();

	const variants = {
		primary: 'border border-violet-300/20 bg-gradient-to-r from-violet-500 via-fuchsia-500 to-indigo-500 text-white shadow-[0_18px_40px_rgba(88,28,135,0.35)] hover:brightness-110 hover:shadow-[0_24px_55px_rgba(88,28,135,0.45)] active:scale-[0.985]',
		secondary: 'border border-cyan-300/15 bg-gradient-to-r from-slate-700 via-slate-800 to-slate-900 text-slate-50 shadow-[0_14px_30px_rgba(2,6,23,0.35)] hover:border-cyan-200/25 hover:text-white active:scale-[0.985]',
		outline: 'border border-white/12 bg-white/6 text-slate-100 hover:bg-white/10 hover:border-white/18 active:scale-[0.985] backdrop-blur-md',
		ghost: 'bg-transparent text-slate-300 hover:bg-white/8 hover:text-white active:scale-[0.985]',
		danger: 'border border-rose-300/20 bg-gradient-to-r from-rose-500 to-pink-600 text-white shadow-[0_18px_40px_rgba(159,18,57,0.32)] hover:brightness-105 active:scale-[0.985]',
		success: 'border border-emerald-300/20 bg-gradient-to-r from-emerald-400 to-teal-500 text-slate-950 shadow-[0_18px_40px_rgba(5,150,105,0.28)] hover:brightness-105 active:scale-[0.985]',
	};

	const sizes = {
		sm: 'px-4 py-2 text-xs font-bold uppercase tracking-[0.18em]',
		md: 'px-6 py-3 text-sm font-bold',
		lg: 'px-8 py-4 text-base font-bold',
		icon: 'p-3',
	};
</script>

<button
	class={cn(
		'inline-flex items-center justify-center rounded-2xl transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-violet-400/15 disabled:pointer-events-none disabled:opacity-50 disabled:grayscale',
		variants[variant],
		sizes[size],
		className
	)}
	disabled={disabled || loading}
	{...props}
>
	{#if loading}
		<svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
			<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
			<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
		</svg>
	{/if}
	{@render children?.()}
</button>
