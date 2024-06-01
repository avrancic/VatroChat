<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import UsersDataService from "@/services/usersDataService";

const router = useRouter();

const users = ref([]);
const usersTypes = ref([]);

const activeAddEditModal = ref(false);
const activeRemoveModal = ref(false);
const searchQuery = ref('');

const currentId = ref(null);

const addEditForm = ref({
  id: null,
  name: null,
  surname: null,
  username: null,
  type: null,
  is_admin: false,
  password: null
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
  const itemToEdit = users.value.find(i => i.id === id);

  if (itemToEdit) {
    addEditForm.value = {
      name: itemToEdit.name,
      surname: itemToEdit.surname,
      username: itemToEdit.username,
      type: itemToEdit.type,
      is_admin: itemToEdit.is_admin,
      password: null
    };
  } else {
    addEditForm.value = {
      name: null,
      surname: null,
      username: null,
      type: null,
      is_admin: false,
      password: null
    };
  }

  activeAddEditModal.value = true;

  currentId.value = id;
};

const closeAddEditModal = () => {
  activeAddEditModal.value = false;
};

const addEditItem = () => {
  const itemToEdit = users.value.find(i => i.id === currentId.value);

  if (!itemToEdit) {
    UsersDataService.create(addEditForm.value)
    .then((response) => {
      users.value.push(response.data);

      closeAddEditModal();
    })
    .catch(error => {
      console.log(error);
    });
  } else {
    UsersDataService.update(itemToEdit.id, addEditForm.value)
    .then((response) => {
      const index = users.value.findIndex(i => i.id === currentId.value);
      users.value[index] = response.data;
      closeAddEditModal();
    })
    .catch(error => {
      console.log(error);
    });
  }
};

const removeItem = () => {
  UsersDataService.delete(currentId.value)
    .then(response => {
      const index = users.value.findIndex(i => i.id === currentId.value);

      if (index !== -1) {
        users.value.splice(index, 1);
      }

      closeRemoveModal();
    })
    .catch(e => {
      console.log(e);
    });

};

const filterUsers = () => {
  return users.value.filter(i => {
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

const getData = () => {
  UsersDataService.getAll()
    .then(response => {
      users.value = response.data;
    })
    .catch(e => {
      console.log(e);
    });

  UsersDataService.getTypes()
    .then(response => {
      usersTypes.value = response.data;
    })
    .catch(e => {
      console.log(e);
    });
}

getData();
</script>

<template>
  <div class="page-content container">
    <div class="row mt-5">
      <div class="col-auto text-end">
        <input type="submit" value="Natrag" class="btn btn-secondary" @click="handleBackClick()">
      </div>

      <div class="col">
        <input type="text" class="form-control form-input p-2 ps-3" placeholder="Search anything..."
          v-model="searchQuery">
      </div>

      <div class="col-auto text-end">
        <input type="submit" value="Dodaj korisnik" class="btn btn-success" @click="openAddEditModal">
      </div>
    </div>

    <div class="tab-content bg-transparent mt-4">
      <div id="incident-container" class="incidents-grid row">
        <div class="col-md-4 incident-item" v-for="i in filterUsers()" :key="i.id">
          <div class="card incident-card-body shadow-sm">
            <h5 class="mb-3">{{ i.name }} {{ i.surname }}</h5>
            <small class="text-muted p-t-30 db mt-2">Korisničko ime:</small>
            <div>{{ i.username }}</div>
            <small class="text-muted p-t-30 db mt-2">Vrsta postrojbe:</small>
            <div>{{ (i.type != null ? i.type.name : "") }}</div>
            <small class="text-muted p-t-30 db mt-2">Administator:</small>
            <div>{{ (i.is_admin ? "da" : "ne") }}</div>
            <div class="mt-auto d-flex justify-content-end pt-4">
              <button class="btn btn-outline-primary btn-sm me-2" @click.stop="openAddEditModal(i.id)">Edit</button>
              <button class="btn btn-outline-danger btn-sm" @click.stop="openRemoveModal(i.id)">Remove</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit/Add Comment Modal -->
    <div class="modal fade" id="editModal" tabindex="-1" aria-hidden="true"
      :class="{ show: activeAddEditModal, 'd-block modal-open': activeAddEditModal }">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Dodaj/Uredi korisnik</h5>
            <button type="button" class="btn-close" @click="closeAddEditModal"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addEditForm-name" class="col-form-label">Ime:</label>
                <input type="text" class="form-control" id="addEditForm-name" v-model="addEditForm.name">
              </div>
              <div class="mb-3">
                <label for="addEditForm-surname" class="col-form-label">Prezime:</label>
                <input type="text" class="form-control" id="addEditForm-surname" v-model="addEditForm.surname">
              </div>
              <div class="mb-3">
                <label for="addEditForm-username" class="col-form-label">Korisničko ime:</label>
                <input type="text" class="form-control" id="addEditForm-username" v-model="addEditForm.username">
              </div>
              <div class="mb-3">
                <label for="addRole" class="form-label">Vrsta postrojbe:</label>
                <select class="form-control" id="addRole" v-model="addEditForm.type">
                  <option v-for="option in usersTypes" :key="option.id" :value="option">
                    {{ option.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <div class="form-check">
                  <input type="checkbox" class="form-check-input" id="addEditForm-is_admin"
                    v-model="addEditForm.is_admin">
                  <label for="addEditForm-is_admin" class="form-check-label">Administrator</label>
                </div>
              </div>
              <div class="mb-3">
                <label for="addEditForm-type" class="col-form-label">Lozinka:</label>
                <input type="text" class="form-control" id="addEditForm-type" v-model="addEditForm.password">
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
            <p>Jeste li sigurni da želite obrisati ovaj korisnik?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeRemoveModal">Odustani</button>
            <button type="button" class="btn btn-danger" @click="removeItem">Obriši</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="activeAddEditModal || activeRemoveModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<style scoped>
.card {
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