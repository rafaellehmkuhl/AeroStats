import { createRouter, createWebHistory, type RouteLocationNormalized, type NavigationGuardNext } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ResultsView from '../views/ResultsView.vue';
import LoginView from '../views/LoginView.vue';
import AdminDashboardView from '../views/AdminDashboardView.vue';
import { useAuthStore } from '../stores/auth';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/results',
            name: 'results',
            component: ResultsView
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView
        },
        {
            path: '/admin',
            name: 'admin',
            component: AdminDashboardView,
            meta: { requiresAuth: true, requiresAdmin: true }
        }
    ]
});

router.beforeEach((to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext) => {
    const authStore = useAuthStore();

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login');
    } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
        next('/'); // Or unauthorized page
    } else {
        next();
    }
});

export default router;
