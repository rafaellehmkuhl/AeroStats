import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../api';
import router from '../router';

export const useAuthStore = defineStore('auth', () => {
    const token = ref<string | null>(localStorage.getItem('token') || null);
    const role = ref<string | null>(localStorage.getItem('role') || null);

    const isAuthenticated = computed(() => !!token.value);
    const isAdmin = computed(() => role.value === 'admin');

    const login = async (email: string, password: string) => {
        try {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const response = await api.post('/auth/login', formData);
            const { access_token, role: userRole } = response.data;

            token.value = access_token;
            role.value = userRole;

            localStorage.setItem('token', access_token);
            localStorage.setItem('role', userRole);

            router.push('/admin');
            return true;
        } catch (error) {
            console.error('Login failed:', error);
            return false;
        }
    };

    const logout = () => {
        token.value = null;
        role.value = null;
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        router.push('/login');
    };

    return {
        token,
        role,
        isAuthenticated,
        isAdmin,
        login,
        logout
    };
});
