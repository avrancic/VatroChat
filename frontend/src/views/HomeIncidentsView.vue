<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { format } from 'date-fns';

import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

import IncidentsDataService from "@/services/incidentsDataService";

const router = useRouter();

const incidents = ref([]);
const workers = ref([]);

const activeAddEditModal = ref(false);
const activeRemoveModal = ref(false);
const searchQuery = ref('');

const currentId = ref(null);

const addEditForm = ref({
    id: null,
    title: null,
    open_from: null,
    open_until: null,
    location: null,
    workers: null
});

const handleIncidentClick = (id) => {
    router.push({ path: '/incident', query: { id } });
};

const openRemoveModal = (id = null) => {
    currentId.value = id;

    activeRemoveModal.value = true;
};
const closeRemoveModal = () => {
    activeRemoveModal.value = false;
};
const openAddEditModal = (id = null) => {
    const incidentToEdit = incidents.value.find(incident => incident.id === id);

    if (incidentToEdit) {
        addEditForm.value = {
            id: incidentToEdit.id,
            title: incidentToEdit.title,
            open_from: incidentToEdit.open_from,
            open_until: incidentToEdit.open_until,
            location: incidentToEdit.location,
            workers: incidentToEdit.workers
        };
    } else {
        addEditForm.value = {
            id: null,
            title: null,
            open_from: null,
            open_until: null,
            location: null,
            workers: null
        };
    }

    activeAddEditModal.value = true;

    currentId.value = id;
};
const closeAddEditModal = () => {
    activeAddEditModal.value = false;
};

const addEditItem = () => {
    const itemToEdit = incidents.value.find(i => i.id === currentId.value);

    if (!itemToEdit) {
        IncidentsDataService.create(addEditForm.value)
            .then((response) => {
                incidents.value.push(response.data);

                closeAddEditModal();
            })
            .catch(error => {
                console.log(error);
            });
    } else {
        IncidentsDataService.update(itemToEdit.id, addEditForm.value)
            .then((response) => {
                const index = incidents.value.findIndex(i => i.id === currentId.value);
                incidents.value[index] = response.data;
                closeAddEditModal();
            })
            .catch(error => {
                console.log(error);
            });
    }
};

const removeIncident = () => {
    const index = incidents.value.findIndex(incident => incident.id === currentId.value);

    if (index !== -1) {
        incidents.value.splice(index, 1);
    }

    closeRemoveModal();
};

const filterIncidents = () => {
    return incidents.value.filter(incident => {
        for (const key in incident) {
            if (Object.hasOwnProperty.call(incident, key)) {
                const value = incident[key];
                if (value && value.toString().toLowerCase().includes(searchQuery.value.toLowerCase())) {
                    return true;
                }
            }
        }
        return false;
    });
};

const getData = () => {
    IncidentsDataService.getAll()
        .then(response => {
            incidents.value = response.data;
        })
        .catch(e => {
            console.log(e);
        });

    IncidentsDataService.getWorkers()
        .then(response => {
            workers.value = response.data;
        })
        .catch(e => {
            console.log(e);
        });
}

const workersLabel = ({ name, surname }) => {
    return `${name} ${surname}`;
}

getData();
</script>

<template>
    <div class="page-content container">
        <div class="row mt-5">
            <div class="col">
                <input type="text" class="form-control form-input p-2 ps-3" placeholder="Search anything..."
                    v-model="searchQuery">
            </div>

            <div class="col-auto text-end">
                <input type="submit" value="Dodaj intervenciju" class="btn btn-success" @click="openAddEditModal">
            </div>
        </div>

        <MasonryWall class="row mt-4" :items="filterIncidents()" :ssr-columns="1" :column-width="400">
            <template #default="{ item, index }">
                <div :style="{ height: `${item}px` }" class="card incident-card-body shadow-sm"
                    @click="handleIncidentClick(item.id)">
                    <h5 class="mb-3">{{ item.title }}</h5>
                    <small class="text-muted p-t-30 db mt-2">Razdoblje:</small>
                    <div>{{ format(item.open_from, 'dd.MM.yyyy hh:mm') }}{{ (item.open_until != null ? " -> " +
                        format(item.open_until, 'dd.MM.yyyy hh:mm') : "") }}</div>
                    <small class="text-muted p-t-30 db mt-2">Adresa:</small>
                    <div>{{ item.location }}</div>
                    <small class="text-muted p-t-30 db mt-2">Radnici:</small>
                    <div>{{ item.workers.map(entry => entry.name + ' ' + entry.surname).join(', ') }}</div>
                    <div class="mt-auto d-flex justify-content-end pt-4">
                        <button class="btn btn-outline-primary btn-sm me-2"
                            @click.stop="openAddEditModal(item.id)">Edit</button>
                        <button class="btn btn-outline-danger btn-sm"
                            @click.stop="openRemoveModal(item.id)">Remove</button>
                    </div>
                </div>
            </template>
        </MasonryWall>
    </div>

    <!-- Edit/Add Incident Modal -->
    <div class="modal fade" id="editModal" tabindex="-1" aria-hidden="true"
        :class="{ show: activeAddEditModal, 'd-block modal-open': activeAddEditModal }">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Dodaj/Uredi intervenciju</h5>
                    <button type="button" class="btn-close" @click="closeAddEditModal"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="incident-title" class="col-form-label">Naslov:</label>
                            <input type="text" class="form-control" id="incident-title" v-model="addEditForm.title">
                        </div>
                        <div class="mb-3">
                            <label for="incident-from" class="col-form-label">Od:</label>
                            <Datepicker v-model="addEditForm.open_from" :enableTimePicker="true"
                                format="dd.MM.yyyy HH:mm" />
                        </div>
                        <div class="mb-3">
                            <label for="incident-to" class="col-form-label">Do:</label>
                            <Datepicker v-model="addEditForm.open_until" :enableTimePicker="true"
                                format="dd.MM.yyyy HH:mm" />
                        </div>
                        <div class="mb-3">
                            <label for="incident-location" class="col-form-label">Adresa:</label>
                            <input type="text" class="form-control" id="incident-location"
                                v-model="addEditForm.location">
                        </div>
                        <div class="mb-3">
                            <label for="incident-workers" class="col-form-label">Radnici:</label>
                            <multi-select v-model="addEditForm.workers" :options="workers" :hide-selected="true"
                                track-by="id" :multiple="true" :custom-label="workersLabel">
                            </multi-select>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="closeAddEditModal">Odustani</button>
                    <button type="button" class="btn btn-primary" @click="addEditItem">Spremi</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Remove Incident Modal -->
    <div class="modal fade" id="removeModal" tabindex="-1" aria-hidden="true"
        :class="{ show: activeRemoveModal, 'd-block modal-open': activeRemoveModal }">
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Potvrda brisanja</h5>
                    <button type="button" class="btn-close" @click="closeRemoveModal"></button>
                </div>
                <div class="modal-body">
                    <p>Jeste li sigurni da želite obrisati ovu intervenciju?</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="closeRemoveModal">Odustani</button>
                    <button type="button" class="btn btn-danger" @click="removeIncident">Obriši</button>
                </div>
            </div>
        </div>
    </div>

    <div v-if="activeAddEditModal || activeRemoveModal" class="modal-backdrop fade show"></div>

</template>

<style scoped>
.card {
    cursor: pointer;
    user-select: none;
}

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