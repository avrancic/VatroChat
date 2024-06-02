<script setup>
import { ref, getCurrentInstance } from 'vue';
import { useRouter } from 'vue-router';
import { createToast } from 'mosha-vue-toastify';

import UsersDataService from "@/services/usersDataService.js";
const internalInstance = getCurrentInstance();

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

  internalInstance.appContext.config.globalProperties.$Progress.start();

  if (!itemToEdit) {

    UsersDataService.create(addEditForm.value)
      .then((response) => {
        createToast({
          title: 'Korisnik kreiran',
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
        users.value.unshift(response.data);

        closeAddEditModal();
      })
      .catch(error => {
        createToast({
          title: 'Greška prilikom kreiranja korisnika',
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
    UsersDataService.update(itemToEdit.id, addEditForm.value)
      .then((response) => {
        createToast({
          title: 'Korisnik ažuriran',
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
        const index = users.value.findIndex(i => i.id === currentId.value);
        users.value[index] = response.data;
        closeAddEditModal();
      })
      .catch(error => {
        createToast({
          title: 'Greška prilikom ažuriranja korisnika',
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

const removeItem = () => {
  internalInstance.appContext.config.globalProperties.$Progress.start();
  UsersDataService.delete(currentId.value)
    .then(response => {
      createToast({
        title: 'Korisnik izbrisan',
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
      const index = users.value.findIndex(i => i.id === currentId.value);

      if (index !== -1) {
        users.value.splice(index, 1);
      }

      closeRemoveModal();
    })
    .catch(e => {
      createToast({
        title: 'Greška prilikom izbrisanja korisnika',
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
  internalInstance.appContext.config.globalProperties.$Progress.start();
  UsersDataService.getAll()
    .then(response => {
      internalInstance.appContext.config.globalProperties.$Progress.finish();
      users.value = response.data;
    })
    .catch(e => {
      internalInstance.appContext.config.globalProperties.$Progress.fail();
      console.log(e);
    });

  UsersDataService.getTypes()
    .then(response => {
      internalInstance.appContext.config.globalProperties.$Progress.finish();
      usersTypes.value = response.data;
    })
    .catch(e => {
      internalInstance.appContext.config.globalProperties.$Progress.fail();
      console.log(e);
    });
}

getData();
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
        <input type="submit" value="Dodaj korisnik" class="btn btn-success" @click="openAddEditModal">
      </div>
    </div>

    <div class="items mt-4">
      <div class="item" v-for="item in filterUsers()" :key="item.id">
        <div :style="{ height: `${item}px` }" class="card shadow-sm">
          <h3 class="mb-3">{{ item.name }} {{ item.surname }}</h3>
          <small class="text-muted p-t-30 db mt-2">Korisničko ime:</small>
          <div>{{ item.username }}</div>
          <small class="text-muted p-t-30 db mt-2">Vrsta postrojbe:</small>
          <div>{{ (item.type != null ? item.type.name : "") }}</div>
          <small class="text-muted p-t-30 db mt-2">Administator:</small>
          <div>{{ (item.is_admin ? "da" : "ne") }}</div>
          <div class="mt-auto d-flex justify-content-end pt-4">
            <button class="btn btn-outline-primary btn-sm me-2" @click.stop="openAddEditModal(item.id)">Uredi</button>
            <button class="btn btn-outline-danger btn-sm" @click.stop="openRemoveModal(item.id)">Ukloni</button>
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
</template>

<style scoped>
.items {
  column-count: 3;
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

@media only screen and (max-width: 600px) {
  .items {
    column-count: 2;
  }
}

@media only screen and (max-width: 400px) {
  .items {
    column-count: 1;
  }
}
</style>