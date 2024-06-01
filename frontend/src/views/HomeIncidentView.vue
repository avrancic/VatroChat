<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const incident = ref();

const router = useRouter();

incident.value = {
    id: "dsadadsadsadsa",
    open_from: "21.05.2024. 19:09",
    open_until: "21.05.2024. 19:09",
    location: "Vladimir Gortan 18",
    title: "Text test test test test testText test test test test test",
    workers: "Elvis Prenc, Adrian Vrančić, Berislav Vrančić, Elvis Prenc, Adrian Vrančić, Berislav Vrančić"
};

const comments = ref([]);
const activeEditModal = ref(false);
const activeRemoveModal = ref(false);
const currentCommentId = ref(null);

const addForm = ref({
    name: "",
    surname: ''
});

for (let i = 0; i < 5; i++) {
    comments.value.push({
        id: `comment-${i}`,
        created_at: "22.05.2024. 23:59",
        user: "Arian Vrančić",
        text: "Text test test test test testText test test test test testText test test test test testText test test test test testText test test test test test.."
    });
}

const handleBackClick = () => {
    router.push({ path: '/' });
};

const toggleEditModal = (commentId = null) => {
    activeEditModal.value = !activeEditModal.value;
    currentCommentId.value = commentId;
};

const toggleRemoveModal = (commentId = null) => {
    activeRemoveModal.value = !activeRemoveModal.value;
    currentCommentId.value = commentId;
};

const addComment = () => {
    // Add comment logic here
    toggleEditModal();
};

const removeComment = () => {
    comments.value = comments.value.filter(comment => comment.id !== currentCommentId.value);
    toggleRemoveModal();
};
</script>

<template>
    <div class="page-content container">
        <div class="row mt-5">
            <div class="col">
                <input type="submit" value="Natrag" class="btn btn-secondary" @click="handleBackClick()">
            </div>
            <div class="col-auto text-end">
                <button class="btn btn-success" @click="toggleEditModal">Dodaj bilješku</button>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col">
                <div class="profile-user-box card-box col shadow-sm">
                    <div class="media-body">
                        <h5 class="mb-3">{{ incident.title }}</h5>
                        <small class="text-muted p-t-30 db mt-2">Interval:</small>
                        <div>{{ incident.open_from }} &rarr; {{ incident.open_until }}</div>
                        <small class="text-muted p-t-30 db mt-2">Adresa:</small>
                        <div>{{ incident.location }}</div>
                        <small class="text-muted p-t-30 db mt-2">Radnici:</small>
                        <div>{{ incident.workers }}</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="tab-content bg-transparent">
            <div id="incident-container" class="incidents-grid row">
                <div class="col-md-6 incident-item" v-for="comment in comments" :key="comment.id">
                    <div class="card incident-card-body shadow-sm">
                        <h5 class="incident-title">{{ comment.user }}</h5>
                        <div class="font-13">{{ comment.created_at }}</div>
                        <div class="incident-content">{{ comment.text }}</div>
                        <div class="mt-auto d-flex justify-content-end pt-4">
                            <button class="btn btn-outline-primary btn-sm me-2" @click.stop="toggleEditModal(comment.id)">Edit</button>
                            <button class="btn btn-outline-danger btn-sm" @click.stop="toggleRemoveModal(comment.id)">Remove</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Edit/Add Comment Modal -->
        <div class="modal fade" id="editModal" tabindex="-1" aria-hidden="true" :class="{ show: activeEditModal, 'd-block modal-open': activeEditModal }">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Dodaj/Uredi bilješku</h5>
                        <button type="button" class="btn-close" @click="toggleEditModal"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <div class="mb-3">
                                <label for="comment-text" class="col-form-label">Bilješka:</label>
                                <textarea class="form-control" id="comment-text" rows="15"></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="toggleEditModal">Odustani</button>
                        <button type="button" class="btn btn-primary" @click="addComment">Spremi</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Remove Comment Modal -->
        <div class="modal fade" id="removeModal" tabindex="-1" aria-hidden="true" :class="{ show: activeRemoveModal, 'd-block modal-open': activeRemoveModal }">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Potvrda brisanja</h5>
                        <button type="button" class="btn-close" @click="toggleRemoveModal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Jeste li sigurni da želite obrisati ovu bilješku?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="toggleRemoveModal">Odustani</button>
                        <button type="button" class="btn btn-danger" @click="removeComment">Obriši</button>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="activeEditModal || activeRemoveModal" class="modal-backdrop fade show"></div>
    </div>
</template>

<style scoped>
.thumb-lg {
    height: 88px;
    width: 88px;
}

.profile-user-box {
    position: relative;
    border-radius: 5px
}

.bg-custom {
    background-color: #02c0ce !important;
}

.profile-user-box {
    position: relative;
    border-radius: 5px;
}

.card-box {
    padding: 20px;
    border-radius: 3px;
    margin-bottom: 30px;
    background-color: #fff;
}

.inbox-widget .inbox-item img {
    width: 40px;
}

.inbox-widget .inbox-item {
    border-bottom: 1px solid #f3f6f8;
    overflow: hidden;
    padding: 10px 0;
    position: relative
}

.inbox-widget .inbox-item .inbox-item-img {
    display: block;
    float: left;
    margin-right: 15px;
    width: 40px
}

.inbox-widget .inbox-item img {
    width: 40px
}

.inbox-widget .inbox-item .inbox-item-author {
    color: #313a46;
    display: block;
    margin: 0
}

.inbox-widget .inbox-item .inbox-item-text {
    color: #98a6ad;
    display: block;
    font-size: 14px;
    margin: 0
}

.inbox-widget .inbox-item .inbox-item-date {
    color: #98a6ad;
    font-size: 11px;
    position: absolute;
    right: 7px;
    top: 12px
}

.comment-list .comment-box-item {
    position: relative
}

.comment-list .comment-box-item .commnet-item-date {
    color: #98a6ad;
    font-size: 11px;
    position: absolute;
    right: 7px;
    top: 2px
}

.comment-list .comment-box-item .commnet-item-msg {
    color: #313a46;
    display: block;
    margin: 10px 0;
    font-weight: 400;
    font-size: 15px;
    line-height: 24px
}

.comment-list .comment-box-item .commnet-item-user {
    color: #98a6ad;
    display: block;
    font-size: 14px;
    margin: 0
}

.comment-list a+a {
    margin-top: 15px;
    display: block
}

.ribbon-box .ribbon-primary {
    background: #2d7bf4;
}

.ribbon-box .ribbon {
    position: relative;
    float: left;
    clear: both;
    padding: 5px 12px 5px 12px;
    margin-left: -30px;
    margin-bottom: 15px;
    font-family: Rubik, sans-serif;
    -webkit-box-shadow: 2px 5px 10px rgba(49, 58, 70, .15);
    -o-box-shadow: 2px 5px 10px rgba(49, 58, 70, .15);
    box-shadow: 2px 5px 10px rgba(49, 58, 70, .15);
    color: #fff;
    font-size: 13px;
}

.text-custom {
    color: #02c0ce !important;
}

.badge-custom {
    background: #02c0ce;
    color: #fff;
}

.badge {
    font-family: Rubik, sans-serif;
    -webkit-box-shadow: 0 0 24px 0 rgba(0, 0, 0, .06), 0 1px 0 0 rgba(0, 0, 0, .02);
    box-shadow: 0 0 24px 0 rgba(0, 0, 0, .06), 0 1px 0 0 rgba(0, 0, 0, .02);
    padding: .35em .5em;
    font-weight: 500;
}

.text-muted {
    color: #98a6ad !important;
}

.font-13 {
    font-size: 13px !important;
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