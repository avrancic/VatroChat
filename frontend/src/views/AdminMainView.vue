<template>
    <div class="admin">
        <nav id="sidebar" v-bind:class="(leftNavIsOpen) ? 'active' : ''">
            <div class="sidebar-header">
                <h1>VatroChat</h1>
            </div>

            <br>
            <ul class="text-secondary">
                <li>
                    <RouterLink :to="{ name: 'AdminEmployees' }">Employees list</RouterLink>
                </li>
                <li>
                    <RouterLink :to="{ name: 'AdminUsers' }">Korisnici</RouterLink>
                </li>
            </ul>
        </nav>

        <div id="body">
            <nav class="navbar navbar-expand-lg navbar-white bg-white">
                <button type="button" id="sidebarCollapse" class="btn btn-light"
                    @click="leftNavIsOpen = !leftNavIsOpen">| |
                    |</button>

                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="nav navbar-nav ms-auto">
                        <li class="nav-item dropdown">
                            <div class="nav-dropdown">
                                <a href="#" id="nav2" class="nav-item nav-link dropdown-toggle text-secondary"
                                    data-bs-toggle="dropdown" aria-expanded="false">
                                    <span>{{ (currentUser != null) ? currentUser : "" }}</span>
                                </a>
                                <div class="dropdown-menu dropdown-menu-end nav-link-menu">
                                    <ul class="nav-list">
                                        <li><a href="" class="dropdown-item" @click.prevent="logOut">Logout</a></li>
                                    </ul>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </nav>

            <div class="content">
                <router-view />
            </div>
        </div>
    </div>
</template>

<script>
import { useAuthStore } from '@/stores/authStore';

export default {
    setup() {
        const authStore = useAuthStore();

        return { authStore };
    },
    data: () => ({
        leftNavIsOpen: false
    }),
    computed: {
        currentUser() {
            return this.authStore.getIme + " " + this.authStore.getPrezime;
        },
    },
    methods: {
        logOut() {
            this.$store.dispatch('auth/logout');
            this.$router.push('/login');
        }
    },
    created() {
        document.title = "Administration"
    }
};
</script>

<style>
#app .admin {
    font-family: sans-serif;
    display: flex;
    width: 100%;
    align-items: stretch;
    overflow-x: hidden
}

#app .admin {
    width: 100%;
    height: 100%;
    background: #f4f6fa;
    font-family: "Lato", "Helvetica Neue", Arial, Helvetica, sans-serif;
    font-size: 1rem;
    color: #444;
}

.content {
    padding-top: 30px
}

.wrapper {
    display: flex;
    width: 100%;
    align-items: stretch;
    overflow-x: hidden
}

#body {
    width: 100%;
    padding: 0;
    min-height: 100vh;
    transition: all 0.3s;
}

#body>.navbar {
    padding: 0 1.5rem;
    min-height: 54px;
    box-shadow: none;
    border-bottom: 1px solid rgba(101, 109, 119, .16);
}

a,
a:hover,
a:focus {
    color: inherit;
    text-decoration: none;
    transition: all 0.3s;
}

.btn.focus,
.btn:focus {
    box-shadow: none;
}

.btn.btn-square {
    border-radius: 0;
}

.table td,
.table th {
    vertical-align: middle;
}

.nav-tabs {
    border-bottom: 2px solid #dee2e6;
}

.nav-tabs .nav-item {
    margin-bottom: -2px;
}

.nav-tabs .nav-link {
    border: none;
    -webkit-transition: color .1s ease;
    transition: color .1s ease;
    color: inherit;
}

.nav-tabs .nav-item.show .nav-link,
.nav-tabs .nav-link.active {
    color: #007bff;
    background-color: #fff;
    border-bottom: 2px solid #22a1f9;

}

#sidebar h1 {
    color: black;
    text-align: center;
}

#sidebar {
    min-width: 250px;
    max-width: 250px;
    background: #fff;
    color: #fff;
    transition: all 0.3s;
    border-right: 1px solid #e6ecf5;
}

#sidebar.active {
    margin-left: -250px;
}

#sidebar .sidebar-header {
    padding: .4rem 1rem;
    border-bottom: 1px solid rgba(101, 109, 119, .16);
    max-height: 55px;
}

#sidebar ul {
    padding: 0 0;
}

#sidebar ul p {
    color: #fff;
    padding: 10px;
}

#sidebar ul li a {
    padding: .8rem 1.5rem;
    font-size: 1rem;
    display: block;
}

#sidebar ul li a .fas {
    min-width: 20px;
    margin-right: 5px;
    text-align: center;
}

#sidebar ul li a:hover,
#sidebar ul li a.active {
    color: #fff;
    background: #2196F3;
}

#sidebar ul li.active>a,
a[aria-expanded="true"] {
    color: inherit;
}

#sidebar ul ul a {
    font-size: 1rem;
    background: #EEEEEE;
}

#sidebar a[data-toggle="collapse"] {
    position: relative;
}

#sidebar .dropdown-toggle::after {
    display: block;
    position: absolute;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    display: none;
}

@media (max-width: 768px) {
    #sidebarCollapse span {
        display: none;
    }
}

@media (max-width: 768px) {
    .display-absolute {
        position: relative;
    }
}

@media (max-width: 680px) {
    #body.active .navbar-collapse {
        display: -ms-flexbox !important;
        display: flex !important;
        -ms-flex-preferred-size: auto;
        flex-basis: auto;
    }

    .nav-dropdown .nav-link-menu {
        position: fixed !important;
        top: 52px !important;
        width: 100% !important;
        margin-top: 0;
    }

    .nav-dropdown .nav-link {
        padding: 10px;
    }

    .nav-dropdown .nav-link-menu::before {
        right: 50%;
    }

    #body .navbar-collapse {
        display: none !important;
    }

    #body .nav-dropdown .nav-item span {
        display: none !important;
    }

    .btn-header {
        display: none;
    }
}

@media (min-width: 200px) {
    .navbar-expand-lg .navbar-collapse {
        display: -ms-flexbox !important;
        display: flex !important;
        -ms-flex-preferred-size: auto;
        flex-basis: auto;
    }

    .navbar-expand-lg .navbar-nav {
        -ms-flex-direction: row;
        flex-direction: row;
    }
}
</style>