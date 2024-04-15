<template>
  <div class="container">
    <div class="row">
      <div>
        <h1>Korisnici</h1>
        <hr><br><br>
        <alert :message=alertMessage :type=alertMessageType v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" @click="toggleAddModal">
          Kreiraj korisnik
        </button>
        <br><br>
        <vue-good-table :rows="usersList" :columns="columns" :pagination-options="{ enabled: true, mode: 'records' }">
          <template #table-row="props">
            <span v-if="props.column.field == 'after'">
              <button type="button" class="btn btn-warning btn-sm me-1" @click="toggleEditModal(props.row)">E</button>
              <button type="button" class="btn btn-danger btn-sm" @click="handleDeleteItem(props.row)">D</button>
            </span>
            <span v-else>
              {{ props.formattedRow[props.column.field] }}
            </span>
          </template>
        </vue-good-table>
      </div>
    </div>

    <!-- add new modal -->
    <div ref="addModal" class="modal fade" :class="{ show: activeAddModal, 'd-block': activeAddModal }" tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title text-danger" id="exampleModalLabel">Novi korisnik</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
              @click="toggleAddModal"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addName" class="form-label">Ime:</label>
                <input type="text" class="form-control" id="addName" v-model="addForm.name" placeholder="Unesite ime">
              </div>
              <div class="mb-3">
                <label for="addName" class="form-label">Prezime:</label>
                <input type="text" class="form-control" id="addName" v-model="addForm.surname"
                  placeholder="Unesite prezime">
              </div>
              <div class="mb-3">
                <label for="addUsername" class="form-label">Username:</label>
                <input type="text" class="form-control" id="addUsername" v-model="addForm.username"
                  placeholder="Unesite username">
              </div>
              <div class="mb-3">
                <label for="addPassword" class="form-label">Password:</label>
                <input type="text" class="form-control" id="addPassword" v-model="addForm.password"
                  placeholder="Unesite lozinku">
              </div>
              <div class="mb-3">
                <label for="addRole" class="form-label">Vrsta postrojbe:</label>
                <select class="form-control" id="addRole" v-model="addForm.type">
                  <option v-for="option in typeList" :key="option.id" :value="option.id">
                    {{ option }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" v-model="addForm.admin">
                  <label class="form-check-label" for="flexCheckDefault">Admin</label>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="handleAddSubmit">Submit</button>
          </div>
        </div>
      </div>
    </div>

    <!-- edit modal -->
    <div ref="editModal" class="modal fade" :class="{ show: activeEditModal, 'd-block': activeEditModal }" tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title text-danger" id="exampleModalLabel">Uredi korisnika</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
              @click="toggleEditModal(null)"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addName" class="form-label">Ime:</label>
                <input type="text" class="form-control" id="addName" v-model="editForm.name" placeholder="Unesite ime">
              </div>
              <div class="mb-3">
                <label for="addName" class="form-label">Prezime:</label>
                <input type="text" class="form-control" id="addName" v-model="editForm.surname"
                  placeholder="Unesite prezime">
              </div>
              <div class="mb-3">
                <label for="addUsername" class="form-label">Username:</label>
                <input type="text" class="form-control" id="addUsername" v-model="editForm.username"
                  placeholder="Unesite username">
              </div>
              <div class="mb-3">
                <label for="addPassword" class="form-label">Password:</label>
                <input type="text" class="form-control" id="addPassword" v-model="editForm.password"
                  placeholder="Unesite lozinku">
              </div>
              <div class="mb-3">
                <label for="addRole" class="form-label">Vrsta postrojbe:</label>
                <select class="form-control" id="addRole" v-model="editForm.type">
                  <option v-for="option in typeList">
                    {{ option }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" v-model="editForm.admin">
                  <label class="form-check-label" for="flexCheckDefault">Admin</label>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="handleEditSubmit">Submit</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="activeAddModal || activeEditModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import MessageAlert from '@/components/AdminMessage.vue';
import UsersDataService from "@/services/AdminUsersDataService";

export default {
  data() {
    return {
      columns: [
        {
          label: 'Ime',
          field: 'name'
        },
        {
          label: 'Prezime',
          field: 'surname'
        },
        {
          label: 'Username',
          field: 'username'
        },
        {
          label: 'Vrsta postrojbe',
          field: 'type',
        },
        {
          label: 'Admin',
          field: 'is_admin',
        },
        {
          field: 'after',
          width: '85px'
        },
      ],
      activeAddModal: false,
      activeEditModal: false,
      addForm: {
        name: '',
        surname: '',
        username: '',
        password: '',
        type: '',
        admin: false
      },
      editForm: {
        name: '',
        surname: '',
        username: '',
        password: '',
        type: '',
        admin: false
      },
      alertMessage: '',
      alertMessageType: 1,
      showMessage: false,
      typeList: ['JVP', 'DVD'],
      usersList: []
    };
  },
  components: {
    alert: MessageAlert
  },
  methods: {
    addItem(payload) {
      UsersDataService.create(payload)
        .then(() => {
          this.getData();
          this.alertMessage = 'Account added!';
          this.alertMessageType = 0;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.alertMessage = 'Account cannot be added!';
          this.alertMessageType = 1;
          this.showMessage = true;
          this.getData();
        });
    },
    getData() {
      UsersDataService.getAll()
        .then(response => {
          this.usersList = response.data.users;
        })
        .catch(e => {
          console.log(e);
        });
    },
    handleAddReset() {
      this.initForm();
    },
    handleAddSubmit() {
      this.toggleAddModal();
      this.addItem(this.addForm);
      this.initForm();
    },
    handleDeleteItem(item) {
      this.removeItem(item._id);
    },
    handleEditCancel() {
      this.toggleEditModal();
      this.initForm();
      this.getData(); // why?
    },
    handleEditSubmit() {
      this.toggleEditModal();
      this.updateItem(this.editForm, this.editForm._id);
    },
    initForm() {
      this.addForm.name = '';
      this.addForm.surname = '';
      this.addForm.username = '';
      this.addForm.password = '';
      this.addForm.password = '';
      this.addForm.type = '';
      this.addForm.admin = false;

      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.surname = '';
      this.editForm.username = '';
      this.editForm.password = '';
      this.editForm.password = '';
      this.editForm.type = '';
      this.editForm.admin = false;
    },
    removeItem(itemID) {
      UsersDataService.delete(itemID)
        .then(() => {
          this.getData();
          this.alertMessage = 'Account removed!';
          this.alertMessageType = 0;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.alertMessage = 'Account cannot be removed!';
          this.alertMessageType = 1;
          this.showMessage = true;
          this.getData();
        });
    },
    toggleAddModal() {
      const body = document.querySelector('body');
      this.activeAddModal = !this.activeAddModal;
      if (this.activeAddModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
    toggleEditModal(item) {
      if (item) {
        this.editForm.id = item._id;
        this.editForm.name = item.name;
        this.editForm.surname = item.surname;
        this.editForm.username = item.username;
        this.editForm.password = "";
        this.editForm.type = item.type;
        this.editForm.admin = item.is_admin;
      }
      const body = document.querySelector('body');
      this.activeEditModal = !this.activeEditModal;
      if (this.activeEditModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
    updateItem(payload, itemID) {
      UsersDataService.update(itemID, payload)
        .then(() => {
          this.getData();
          this.alertMessage = 'Account updated!';
          this.alertMessageType = 0;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.alertMessage = 'Account cannot be updated!';
          this.alertMessageType = 1;
          this.showMessage = true;
          this.getData();
        });
    }
  },
  created() {
    this.getData();
  },
};
</script>