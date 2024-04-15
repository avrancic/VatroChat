<template>
  <div class="container">
    <div class="row">
      <div>
        <h1>Employees</h1>
        <hr><br><br>
        <alert :message=alertMessage :type=alertMessageType v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" @click="toggleAddModal">
          Add employee
        </button>
        <br><br>
        <vue-good-table :rows="employees" :columns="columns" :pagination-options="{ enabled: true, mode: 'records' }">
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
            <h5 class="modal-title">Add a new employee</h5>
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
                <label for="addSurname" class="form-label">Surname:</label>
                <input type="text" class="form-control" id="addSurname" v-model="addForm.surname"
                  placeholder="Enter surname">
              </div>
              <div class="mb-3">
                <label for="addType" class="form-label">Type:</label>
                <select class="form-control" id="addType" v-model="addForm.type">
                  <option v-for="option in employeeTypes" :key="option._id" :value="option._id">
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
                <label for="editSurname" class="form-label">Surname:</label>
                <input type="text" class="form-control" id="editSurname" v-model="editForm.surname"
                  placeholder="Enter surname">
              </div>
              <div class="mb-3">
                <label for="editType" class="form-label">Type</label>
                <select class="form-control" id="editType" v-model="editForm.type">
                  <option v-for="option in employeeTypes" :key="option._id" :value="option._id">
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
import EmployeesDataService from "@/services/AdminEmployeesDataService";

export default {
  data() {
    return {
      columns: [
        {
          label: 'Name',
          field: 'name'
        },
        {
          label: 'Surname',
          field: 'surname'
        },
        {
          label: 'Type',
          field: 'type.name',
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
        type: ''
      },
      employees: [],
      editForm: {
        id: '',
        name: '',
        surname: '',
        type: ''
      },
      alertMessage: '',
      alertMessageType: 1,
      showMessage: false,
      employeeTypes: [
      ]
    };
  },
  components: {
    alert: MessageAlert
  },
  methods: {
    addItem(payload) {
      EmployeesDataService.create(payload)
        .then(() => {
          this.getData();
          this.alertMessage = 'Employee added!';
          this.alertMessageType = 0;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.alertMessage = 'Employee cannot be added!';
          this.alertMessageType = 1;
          this.showMessage = true;
          this.getData();
        });
    },
    getData() {
      EmployeesDataService.getAll()
        .then(response => {
          this.employees = response.data.employees;
          this.employeeTypes = response.data.employeeTypes;
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
      this.toggleEditModal(null);
      this.initForm();
      this.getData(); // why?
    },
    handleEditSubmit() {
      this.toggleEditModal(null);
      this.updateItem(this.editForm, this.editForm.id);
    },
    initForm() {
      this.addForm.name = '';
      this.addForm.surname = '';
      this.addForm.type = '';
      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.surname = '';
      this.editForm.type = '';
    },
    removeItem(itemID) {
      EmployeesDataService.delete(itemID)
        .then(() => {
          this.getData();
          this.alertMessage = 'Employee removed!';
          this.alertMessageType = 0;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.alertMessage = 'Employee cannot be removed!';
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
        this.editForm.type = item.type._id;
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
      EmployeesDataService.update(itemID, payload)
        .then(() => {
          this.getData();
          this.alertMessage = 'Employee updated!';
          this.alertMessageType = 0;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.alertMessage = 'Employee cannot be updated!';
          this.alertMessageType = 1;
          this.showMessage = true;
          this.getData();
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>