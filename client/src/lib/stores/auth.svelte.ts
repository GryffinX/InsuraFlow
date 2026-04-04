import { browser } from '$app/environment';
import { api } from '$lib/api/axios';

export interface User {
    id: number;
    username: string;
    email: string;
    role: 'customer' | 'agent' | 'surveyor' | 'provider' | 'admin';
    phone?: string;
    address?: string;
    dob?: string;
    formatted_id?: string;
}

function createAuthStore() {
    let user = $state<User | null>(
        browser && localStorage.getItem('user') 
            ? JSON.parse(localStorage.getItem('user')!) 
            : null
    );
    let loading = $state(false);

    async function login(credentials: any) {
        console.log('Attempting login to http://127.0.0.1:8000/api/token/');
        const response = await api.post('http://127.0.0.1:8000/api/token/', credentials);
        console.log('Login response:', response.data);
        const { access, refresh } = response.data;
        
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        
        // Fetch user info
        console.log('Fetching user info from http://127.0.0.1:8000/api/auth/me/');
        const userResponse = await api.get('http://127.0.0.1:8000/api/auth/me/');
        const userData = userResponse.data;
        
        localStorage.setItem('user', JSON.stringify(userData));
        user = userData;
    }

    async function register(userData: any) {
        console.log('Attempting registration to http://127.0.0.1:8000/api/auth/register/');
        const response = await api.post('http://127.0.0.1:8000/api/auth/register/', userData);
        console.log('Registration response:', response.data);
        return response.data;
    }

    function logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        user = null;
    }

    return {
        get user() { return user; },
        get loading() { return loading; },
        login,
        register,
        logout
    };
}

export const auth = createAuthStore();
