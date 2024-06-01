<script setup>
import { ref } from 'vue';

const incidents = ref([]);

for (let i = 0; i < 5; i++) {
    incidents.value.push({
        id: "dsadadsadsadsa",
        open_from: "21.05.2024. 19:09",
        open_until: "21.05.2024. 19:09",
        title: "Text test test test test test..",
        workers: "Elvis Prenc, Adrian Vrančić, Berislav Vrančić, Elvis Prenc, Adrian Vrančić, Berislav Vrančić"
    });
}

const handleIncidentClick = () => {
    router.push({ path: '/' });
};

</script>

<template>
    <div class="page-content container incidents-grid">
        <div class="tab-content bg-transparent mt-5">
            <div id="incident-container" class="incidents-grid row">
                <div class="col-md-4 incident-item" v-for="incident in incidents" :key="incident.id" @click="handleIncidentClick">
                    <div class="card incident-card-body">
                        <h5 class="incident-title">{{ incident.title }}</h5>
                        <p class="incident-date">{{ incident.open_from }} -> {{ incident.open_until }}</p>
                        <div class="incident-content">{{ incident.workers }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.incident-card-body {
    position: relative;
    display: flex;
    flex-direction: column;
    background-color: #fff;
    margin-bottom: 30px;
    border: 0 solid transparent;
    border-radius: 10px;
    padding: 1.57rem;
}

.incident-title {
    margin-bottom: 0;
}

.incident-date {
    font-size: 14px;
    color: #6c757d;
}

.incident-content {
    margin-top: 10px;
}

@media (max-width: 767.98px) {
    .incident-item {
        max-width: 100%;
    }
}

@media (max-width: 991.98px) {
    .incident-item {
        max-width: 216px;
    }
}
</style>