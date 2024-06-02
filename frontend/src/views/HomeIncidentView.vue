<script setup>
import { ref, onMounted, onBeforeMount, getCurrentInstance } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { createToast } from 'mosha-vue-toastify';

import IncidentsDataService from "@/services/incidentsDataService.js";

import { format } from 'date-fns';
const internalInstance = getCurrentInstance();

const router = useRouter();
const route = useRoute();

const incident = ref();
const comments = ref([]);

const activeAddEditModal = ref(false);
const activeRemoveModal = ref(false);
const searchQuery = ref('');

const currentId = ref(null);

incident.value = {
    id: "Loading...",
    open_from: null,
    open_until: null,
    location: "Loading...",
    title: "Loading...",
    workers: []
};

onBeforeMount(() => {
    getData();
});

const addEditForm = ref({
    id: null,
    text: null,
});

const handleBackClick = () => {
    router.push({ path: '/' });
};

const openRemoveModal = (id = null) => {
    currentId.value = id;

    activeRemoveModal.value = true;
};
const closeRemoveModal = () => {
    activeRemoveModal.value = false;
};
const openAddEditModal = (id = null) => {
    const toEdit = comments.value.find(i => i.id === id);

    if (toEdit) {
        addEditForm.value = {
            text: toEdit.text
        };
    } else {
        addEditForm.value = {
            text: null
        };
    }

    activeAddEditModal.value = true;

    currentId.value = id;
};
const closeAddEditModal = () => {
    activeAddEditModal.value = false;
};

const addEditComment = () => {
    const itemToEdit = comments.value.find(i => i.id === currentId.value);

    internalInstance.appContext.config.globalProperties.$Progress.start();

    if (!itemToEdit) {
        IncidentsDataService.createComment(incident.value.id, addEditForm.value)
            .then((response) => {
                createToast({
                    title: 'Bilješka kreiranja',
                },
                    {
                        position: 'top-right',
                        showCloseButton: 'false',
                        swipeClose: 'false',
                        hideProgressBar: 'true',
                        transition: 'bounce',
                        type: 'success',
                        showIcon: 'true',
                    })

                internalInstance.appContext.config.globalProperties.$Progress.finish();
                comments.value.unshift(response.data);

                closeAddEditModal();
            })
            .catch(error => {
                createToast({
                    title: 'Greška prilikom kreiranja bilješke',
                },
                    {
                        position: 'top-right',
                        showCloseButton: 'false',
                        swipeClose: 'false',
                        hideProgressBar: 'true',
                        transition: 'bounce',
                        type: 'danger',
                        showIcon: 'true',
                    })

                internalInstance.appContext.config.globalProperties.$Progress.fail();
                console.log(error);
            });
    } else {
        IncidentsDataService.updateComment(incident.value.id, itemToEdit.id, addEditForm.value)
            .then((response) => {
                createToast({
                    title: 'Bilješka ažurirana',
                },
                    {
                        position: 'top-right',
                        showCloseButton: 'false',
                        swipeClose: 'false',
                        hideProgressBar: 'true',
                        transition: 'bounce',
                        type: 'success',
                        showIcon: 'true',
                    })

                internalInstance.appContext.config.globalProperties.$Progress.finish();
                const index = comments.value.findIndex(i => i.id === currentId.value);

                comments.value[index] = response.data;

                closeAddEditModal();
            })
            .catch(error => {
                createToast({
                    title: 'Greška prilikom ažuriranja bilješke',
                },
                    {
                        position: 'top-right',
                        showCloseButton: 'false',
                        swipeClose: 'false',
                        hideProgressBar: 'true',
                        transition: 'bounce',
                        type: 'danger',
                        showIcon: 'true',
                    })

                internalInstance.appContext.config.globalProperties.$Progress.fail();
                console.log(error);
            });
    }
};

const removeComment = () => {
    internalInstance.appContext.config.globalProperties.$Progress.start();
    IncidentsDataService.deleteComment(incident.value.id, currentId.value)
        .then(response => {
            createToast({
                title: 'Bilješka izbrisana',
            },
                {
                    position: 'top-right',
                    showCloseButton: 'false',
                    swipeClose: 'false',
                    hideProgressBar: 'true',
                    transition: 'bounce',
                    type: 'success',
                    showIcon: 'true',
                })

            internalInstance.appContext.config.globalProperties.$Progress.finish();
            const index = comments.value.findIndex(i => i.id === currentId.value);

            if (index !== -1) {
                comments.value.splice(index, 1);
            }

            closeRemoveModal();
        })
        .catch(e => {
            createToast({
                title: 'Greška prilikom izbrisanja bilješke',
            },
                {
                    position: 'top-right',
                    showCloseButton: 'false',
                    swipeClose: 'false',
                    hideProgressBar: 'true',
                    transition: 'bounce',
                    type: 'danger',
                    showIcon: 'true',
                })

            internalInstance.appContext.config.globalProperties.$Progress.fail();
            console.log(e);
        });


    closeRemoveModal();
};

const getData = () => {
    internalInstance.appContext.config.globalProperties.$Progress.start();

    IncidentsDataService.get(route.query.id)
        .then(response => {
            incident.value = response.data;

            IncidentsDataService.getComments(route.query.id)
                .then(response => {
                    internalInstance.appContext.config.globalProperties.$Progress.finish();
                    comments.value = response.data;
                })
                .catch(e => {
                    internalInstance.appContext.config.globalProperties.$Progress.fail();
                    console.log(e);
                });
        })
        .catch(e => {
            internalInstance.appContext.config.globalProperties.$Progress.fail();
            console.log(e);
        });
}

const filterComments = () => {
    return comments.value.filter(i => {
        for (const key in i) {
            if (Object.hasOwnProperty.call(i, key)) {
                const value = i[key];
                if (value && value.toString().toLowerCase().includes(searchQuery.value.toLowerCase())) {
                    return true;
                }
            }
        }
        return false;
    });
};

</script>

<template>
    <div class="page-content container">
        <div class="row mt-5 d-flex align-items-center">
            <div class="col-auto text-end">
                <input type="submit" value="Natrag" class="btn btn-secondary" @click="handleBackClick()">
            </div>

            <div class="col">
                <input type="text" class="form-control form-input p-2 ps-3" placeholder="Pretraži nešto..."
                    v-model="searchQuery">
            </div>

            <div class="col-auto text-end">
                <input type="submit" value="Dodaj bilješku" class="btn btn-success" @click="openAddEditModal">
            </div>
        </div>

        <div class="card shadow-sm mt-4">
            <h5 class="mb-3">{{ incident.title }}</h5>
            <small class="text-muted p-t-30 db mt-2">Interval:</small>
            <div>{{ (incident.open_from != null ? format(incident.open_from, 'dd.MM.yyyy. hh:mm') : "") }}{{
                (incident.open_until != null ? " -> " +
                    format(incident.open_until, 'dd.MM.yyyy. hh:mm') : "") }}</div>
            <small class="text-muted p-t-30 db mt-2">Adresa:</small>
            <div>{{ incident.location }}</div>
            <small class="text-muted p-t-30 db mt-2">Radnici:</small>
            <div>{{ incident.workers.map(entry => entry.name + ' ' + entry.surname).join(', ') }}</div>
        </div>

        <div class="items mt-4">
            <div class="item" v-for="item in filterComments()" :key="item.id">
                <div :style="{ height: `${item}px` }" class="card shadow-sm">
                    <h5 class="mb-3">{{ item.created_by }}</h5>
                    <small class="text-muted p-t-30 db mt-2">Datum:</small>
                    <div>{{ format(item.created_at, 'dd.MM.yyyy. hh:mm') }}</div>
                    <small class="text-muted p-t-30 db mt-2">Bilješka:</small>
                    <div>{{ item.text }}</div>
                    <div class="mt-auto d-flex justify-content-end pt-4">
                        <button class="btn btn-outline-primary btn-sm me-2"
                            @click.stop="openAddEditModal(item.id)">Uredi</button>
                        <button class="btn btn-outline-danger btn-sm"
                            @click.stop="openRemoveModal(item.id)">Ukloni</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Edit/Add Comment Modal -->
    <div class="modal fade" id="editModal" tabindex="-1" aria-hidden="true"
        :class="{ show: activeAddEditModal, 'd-block modal-open': activeAddEditModal }">
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Dodaj/Uredi bilješku</h5>
                    <button type="button" class="btn-close" @click="closeAddEditModal"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="comment-text" class="col-form-label">Bilješka:</label>
                            <textarea class="form-control" id="comment-text" rows="15"
                                v-model="addEditForm.text"></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="closeAddEditModal">Odustani</button>
                    <button type="button" class="btn btn-primary" @click="addEditComment">Spremi</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Remove Comment Modal -->
    <div class="modal fade" id="removeModal" tabindex="-1" aria-hidden="true"
        :class="{ show: activeRemoveModal, 'd-block modal-open': activeRemoveModal }">
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Potvrda brisanja</h5>
                    <button type="button" class="btn-close" @click="closeRemoveModal"></button>
                </div>
                <div class="modal-body">
                    <p>Jeste li sigurni da želite obrisati ovu bilješku?</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="closeRemoveModal">Odustani</button>
                    <button type="button" class="btn btn-danger" @click="removeComment">Obriši</button>
                </div>
            </div>
        </div>
    </div>

    <div v-if="activeAddEditModal || activeRemoveModal" class="modal-backdrop fade show"></div>
</template>

<style scoped>
.items {
    column-count: 2;
    column-gap: 25px;
}

.item {
    display: inline-block;
    width: 100%;
}

.card {
    user-select: none;

    position: relative;
    display: flex;
    flex-direction: column;
    background-color: #fff;
    margin-bottom: 30px;
    border: 0 solid transparent;
    border-radius: 10px;
    padding: 1.57rem;
}

@media only screen and (max-width: 400px) {
    .items {
        column-count: 1;
    }
}
</style>