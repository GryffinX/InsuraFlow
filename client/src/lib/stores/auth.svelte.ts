import { browser } from '$app/environment';
import { api } from '$lib/api/axios';

export interface User {
    id: number;
    username: string;
    email: string;
    role: 'customer' | 'agent' | 'surveyor' | 'admin';
}

function createAuthStore() {
    let user = $state<User | null>(null);
    let loading = $state(true);

    if (browser) {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            user = JSON.parse(storedUser);
        }
        loading = false;
    }

    async function login(credentials: any) {
        const response = await api.post('/auth/login/', credentials);
        const { access, refresh } = response.data;
        
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        
        // Fetch user info
        const userResponse = await api.get('/auth/me/');
        const userData = userResponse.data;
        
        localStorage.setItem('user', JSON.stringify(userData));
        user = userData;
    }

    async function register(userData: any) {
        return await api.post('/auth/register/', userData);
    }

    async function verifyOtp(email: string, otp: string) {
        await api.post('/auth/verify-otp/', { email, otp });
    }

    async function resendOtp(email: string) {
        await api.post('/auth/resend-otp/', { email });
    }

    async function logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        user = null;
        if (browser) window.location.href = '/login';
    }

    return {
        get user() { return user; },
        get loading() { return loading; },
        login,
        register,
        verifyOtp,
        resendOtp,
        logout
    };
}

export const auth = createAuthStore();
