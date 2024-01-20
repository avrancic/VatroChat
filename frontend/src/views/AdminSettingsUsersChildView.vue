<template>
    <div class="container">
      <div class="row">
        <div>
          <h1>Accounts</h1>
          <hr><br><br>
          <alert :message=alertMessage :type=alertMessageType v-if="showMessage"></alert>
          <button type="button" class="btn btn-success btn-sm" @click="toggleAddModal">
            Add Account
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
              <h5 class="modal-title">Add a new user</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="toggleAddModal">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form>
                <div class="mb-3">
                  <label for="addName" class="form-label">Name:</label>
                  <input type="text" class="form-control" id="addName" v-model="addForm.name" placeholder="Enter name">
                </div>
                <div class="mb-3">
                  <label for="addUsername" class="form-label">Username:</label>
                  <input type="text" class="form-control" id="addUsername" v-model="addForm.username"
                    placeholder="Enter username">
                </div>
                <div class="mb-3">
                  <label for="addPassword" class="form-label">Password:</label>
                  <input type="text" class="form-control" id="addPassword" v-model="addForm.password"
                    placeholder="Enter password">
                </div>
                <div class="mb-3">
                  <label for="addRole" class="form-label">Role:</label>
                  <select class="form-control" id="addRole" v-model="addForm.role">
                    <option v-for="option in userRolesList" :key="option._id" :value="option._id">
                      {{ option.name }}
                    </option>
                  </select>
                </div>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-primary btn-sm me-1" @click="handleAddSubmit">Submit</button>
                  <button type="button" class="btn btn-danger btn-sm" @click="handleAddReset">Reset</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
  
      <div v-if="activeAddModal" class="modal-backdrop fade show"></div>
  
      <!-- edit modal -->
      <div ref="editModal" class="modal fade" :class="{ show: activeEditModal, 'd-block': activeEditModal }" tabindex="-1"
        role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Update</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="toggleEditModal(null)">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form>
                <div class="mb-3">
                  <label for="editName" class="form-label">Name:</label>
                  <input type="text" class="form-control" id="editName" v-model="editForm.name" placeholder="Enter name">
                </div>
                <div class="mb-3">
                  <label for="editPassword" class="form-label">Password:</label>
                  <input type="text" class="form-control" id="addPassword" v-model="editForm.password"
                    placeholder="Enter password">
                </div>
                <div class="mb-3">
                  <label for="editRole" class="form-label">Role:</label>
                  <select class="form-control" id="editRole" v-model="editForm.role">
                    <option v-for="option in userRolesList" :key="option.name" :value="option._id">
                      {{ option.name }}
                    </option>
                  </select>
                </div>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-primary btn-sm me-1" @click="handleEditSubmit">Submit</button>
                  <button type="button" class="btn btn-danger btn-sm" @click="handleEditCancel">Cancel</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div v-if="activeEditModal" class="modal-backdrop fade show"></div>
    </div>
  </template>
  
  <script>
  import MessageAlert from '@/components/AdminMessage.vue';
  import UsersDataService from "@/services/AdminSettingsUsersDataService";
  
  export default {
    data() {
      return {
        columns: [
          {
            label: 'Name',
            field: 'name'
          },
          {
            label: 'Username',
            field: 'username'
          },
          {
            label: 'Role',
            field: 'role.name',
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
          username: '',
          password: '',
          role: ''
        },
        usersList: [],
        editForm: {
          id: '',
          name: '',
          password: '',
          role: ''
        },
        alertMessage: '',
        alertMessageType: 1,
        showMessage: false,
        userRolesList:[]
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
            this.userRolesList = response.data.userRoles;
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
        this.updateItem(this.editForm, this.editForm.id);
      },
      initForm() {
        this.addForm.name = '';
        this.addForm.username = '';
        this.addForm.password = '';
        this.addForm.role = [];
        this.editForm.id = '';
        this.editForm.name = '';
        this.editForm.role = [];
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
          this.editForm.password = "";
          this.editForm.role = item.role._id;
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