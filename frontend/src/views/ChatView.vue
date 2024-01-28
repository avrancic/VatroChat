<template>
    <div>
        <div class="sidebar">
            <a href="#" class="close-sidebar"><i class="icon feather icon-x-square"></i></a>
            <div class="logo">
                <i class="icon feather icon-message-square"></i>
                VatroChat
                <a href="#" class="nav-link p-0 float-end" data-bs-toggle="dropdown" aria-expanded="false">
                    <CaUserAvatar class="img-fluid rounded-circle" />
                </a>
                <div class="dropdown-menu dropdown-menu-right" style="">
                    <a href="profile.html" class="dropdown-item px-3 align-self-center d-flex">
                        <span class="icon feather icon-user me-2 h6 mb-0"></span> Administration</a>
                    <a href="#" class="dropdown-item px-3 align-self-center d-flex chat-setting">
                        <span class="icon feather icon-settings me-2 h6 mb-0"></span> Account Settings</a>
                    <a href="page-login.html" class="dropdown-item px-3 text-danger align-self-center d-flex">
                        <span class="icon feather icon-log-out me-2 h6  mb-0"></span> Sign Out</a>
                </div>
            </div>
            <ul class="nav nav-tabs  border-bottom theme-border" id="tabs-tab" role="tablist">
                <li class="nav-item" role="presentation">
                    <a class="nav-link border-0" data-bs-toggle="tab" href="#tabs-contacts" role="tab"
                        aria-controls="tabs-contacts" aria-selected="false" tabindex="-1">
                        <i class="icon feather icon-user"></i><br>Contacts</a>
                </li>
                <li class="nav-item" role="presentation">
                    <a class="nav-link border-0" data-bs-toggle="tab" href="#tabs-group" role="tab"
                        aria-controls="tabs-group" aria-selected="false" tabindex="-1">
                        <i class="icon feather icon-users"></i><br>Groups</a>
                </li>
            </ul>
            <div class="tab-content scroller-section sidebar-menu-section">
                <div class="tab-pane fade active show" id="tabs-contacts" role="tabpanel" aria-labelledby="tabs-contacts">
                    <ul class="nav flex-column chat-menu">
                        <li class="nav-item active px-3">
                            <div class="media d-block d-flex text-start py-3">
                                <div class="avtar me-3 bg-warning text-white"><span><i
                                            class="icon feather icon-users"></i></span></div>
                                <div class="media-body align-self-center mt-0">
                                    <h6 class="mb-1">Test name</h6>
                                    Test text
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
                <div class="tab-pane fade" id="tabs-group" role="tabpanel" aria-labelledby="tabs-group">
                    <ul class="nav flex-column chat-menu">
                        <li class="nav-item active  px-3">
                            <div class="media d-block d-flex text-start py-3">
                                <div class="avtar me-3 bg-warning text-white"><span><i
                                            class="icon feather icon-users"></i></span></div>
                                <div class="media-body align-self-center mt-0">
                                    <h6 class="mb-1">Test name</h6>
                                    Test text
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <main>
            <div class="container-fluid">
                <div class="row border-start theme-border row-eq-height">
                    <div class="col-12 p-0 chat-history">
                        <ul class="scrollerchat p-3 scroller-section">
                            <li class="clearfix" v-for="message in messages"
                                :class="[message.type == 0 ? 'left' : 'right']">

                                <div class="message my-message">
                                    <strong class="name">{{ message.name }}</strong>
                                    <br>
                                    <span class="text">{{ message.text }}</span>
                                </div>

                                <span class="message-data-time">{{ message.date }}</span>
                            </li>
                        </ul>
                        <div class="border-top theme-border py-3 d-flex submit-form-control">
                            <input type="text" class="form-control me-2 border-0 rounded-0 h-100"
                                placeholder="Type message here ...">

                            <a href="#" class="me-2 rounded line-height-21">
                                <i class="icon feather icon-send align-middle">
                                </i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import { CaUserAvatar } from "@kalimahapps/vue-icons";

export default {
    components: {
        CaUserAvatar
    },
    data() {
        return {
            rooms: [
                { id: 1, name: 'General', description: 'General Chat Room', image: 'path-to-image', lastUpdated: '12:00 PM', messages: [] },
            ],
            messages: [
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 0 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 0 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 0 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 0 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 0 },
            { id: 0, name: "Arian Vrančić", date: "28.01.2024.", text: "Test text text text text text text text text text", type: 1 },
            ],
        };
    },
    methods: {
    },
};
</script>  

<style>
.chat-history {
    padding: 20px;
    border-bottom: 2px solid #fff
}

.chat-history ul {
    padding: 0
}

.chat-history ul li {
    list-style: none;
    margin-bottom: 30px
}

.chat-history ul li.left {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.chat-history ul li.right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.chat-history ul li:last-child {
    margin-bottom: 0px
}

.chat-history .message-data {
    margin-bottom: 15px
}

.chat-history .message-data img {
    border-radius: 40px;
    width: 40px
}

.chat-history .message-data-time,
.chat-history .name {
    color: #434651;
}

.chat-history .message {
    color: #444;
    padding: 18px 20px;
    line-height: 26px;
    font-size: 16px;
    border-radius: 7px;
    display: inline-block;
    position: relative;
    margin-bottom: 10px;
}

.chat-history .my-message {
    background: #efefef
}

.chat-history .other-message {
    background: #e8f1f3;
    text-align: right
}

.chat-history .other-message:after {
    border-bottom-color: #e8f1f3;
    left: 93%
}

.text-right {
    text-align: right !important;
}

.chat-message {
    padding: 20px
}

.float-right {
    float: right
}

.clearfix:after {
    visibility: hidden;
    display: block;
    font-size: 0;
    content: " ";
    clear: both;
    height: 0
}

body {
    background-color: #74EBD5;
    background-image: linear-gradient(90deg, #74EBD5 0%, #9FACE6 100%);
    font-size: 13px;

}

::-webkit-scrollbar {
    width: 5px;
}

::-webkit-scrollbar-track {
    width: 5px;
    background: #f5f5f5;
}

::-webkit-scrollbar-thumb {
    width: 1em;
    background-color: #ddd;
    outline: 1px solid slategrey;
    border-radius: 1rem;
}

:root {
    --primarycolor: #1e3d73;
    --sidebarbg: #ebebeb;
    --sidebarcolor: #292b3a;
    --bodycolor: #495057;
    --bodybackground: #d5dbd8;
    --bordercolor: rgba(72, 94, 144, 0.16);
    --mainbackground: #fff;
}

.bg-success {
    background-color: #28a745 !important;
}

small {
    font-size: 80%;
    font-weight: 400;
}

.media {
    display: flex;
    align-items: flex-start;
}

.media-body {
    flex: 1 1 0% !important;
}

.icon-x-square::before {
    display: none;
}

.rounded {
    border-radius: .25rem !important;
}

.form-inline {
    display: flex;
    flex-flow: row wrap;
    align-items: center;
}

.sidebar .searchform button i {
    color: var(--bodycolor) !important;
}

.sidebar .chat-menu li img {
    height: 50px;
}

.new-message {
    width: 20px;
    height: 20px;
    border-radius: 20px;
    text-align: center;
}

.form-control {
    display: block;
    width: 100%;
    height: calc(1.5em + .75rem + 2px);
    padding: .375rem .75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid #ced4da;
    border-radius: .25rem;
    transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;
}

.form-control-sm {
    height: calc(1.5em + .5rem + 2px);
    padding: .25rem .5rem;
    font-size: .875rem;
    line-height: 1.5;
    border-radius: .2rem;
}

@-moz-keyframes spin {
    from {
        -moz-transform: rotate(0deg);
    }

    to {
        -moz-transform: rotate(360deg);
    }
}

@-webkit-keyframes spin {
    from {
        -webkit-transform: rotate(0deg);
    }

    to {
        -webkit-transform: rotate(360deg);
    }
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.btn-primary:not(:disabled):not(.disabled).active,
.btn-primary:not(:disabled):not(.disabled):active {
    background-color: var(--primarycolor) !important;
    border-color: var(--primarycolor);
}

.theme-border {
    border-color: var(--bordercolor) !important;
}

.scroller-section {
    overflow: scroll;
}

.scroller-section::-webkit-scrollbar {
    display: none;
}

a {
    color: var(--primarycolor);
    text-decoration: none;
}

a:hover {
    text-decoration: none;
    color: var(--primarycolor);
}

.se-pre-con {
    position: fixed;
    left: 0px;
    top: 0px;
    width: 100%;
    height: 100%;
    z-index: 9999;
    background: var(--mainbackground);
    text-align: center;
    transition: all 0.3s;
}

.se-pre-con .spin {
    position: relative;
    font-size: 30px;
    top: 50%;
    margin-top: -15px;

    -webkit-animation: spin 4s linear infinite;
    -moz-animation: spin 4s linear infinite;
    animation: spin 4s linear infinite;
}

.se-pre-con .spin i {
    margin: auto;
    color: var(--primarycolor);
}

.wrapper {
    box-shadow: 0 1px 1px 0 rgba(0, 0, 0, 0.06), 0 2px 5px 0 rgba(0, 0, 0, 0.2);
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
}

@media (max-width: 1450px) {
    .wrapper {
        width: 87%;
    }
}

@media (max-width: 767px) {
    .wrapper {
        width: 100%;
        top: 0px;
    }
}

.avtar {
    height: 3rem;
    width: 3rem;
    min-width: 3rem;
    display: inline-block;
    position: relative;
    border-radius: 50%;
    box-shadow: 0 0 1px 1px var(--bordercolor);
    font-size: 25px;
}

.avtar span {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    display: flex;
    align-items: center;
    justify-content: center;
}

.sidebar {
    position: absolute;
    width: 350px;
    background: #E5E8EF;
    transition: all 0.5s;
}

@media (max-width: 991px) {
    .sidebar {
        border-radius: 5px;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
        position: fixed;
        top: 65px;
        bottom: 0;
        transform: translateX(-767px);
    }
}

.sidebar .logo {
    font-size: 20px;
    padding: 10px;
}

.sidebar .logo i {
    color: var(--bodycolor);
}

.sidebar .searchform {
    position: relative;
}

.sidebar .searchform input {
    border-radius: 20px;
    border: none;
    color: var(--bodycolor);
    background: var(--bodybackground);
}

.sidebar .searchform button {
    position: absolute;
    background: transparent;
    border: none;
    right: 0px;
}

.sidebar .searchform button i {
    color: var(--bordercolor);
}

.sidebar .tab-content {
    height: calc(100vh - 116px);
}

.sidebar .nav-tabs .nav-link {
    color: var(--bodycolor);
}

.sidebar .nav-tabs .nav-link i {
    font-size: 20px;
}

.sidebar .nav-tabs .nav-link.active,
.sidebar .nav-tabs .nav-link:hover {
    font-weight: bold;
    background-color: transparent;
}

.sidebar .chat-menu li {
    border-bottom: 1px solid var(--bordercolor);
}

.sidebar .chat-menu li.active,
.sidebar .chat-menu li:hover {
    background-color: var(--mainbackground);
}

.sidebar .chat-menu li:last-child {
    border-bottom: none;
}

.form-control {
    padding: 10px;
    background: transparent;
    border: 1px solid var(--bordercolor);
}

.form-control:focus {
    outline: none;
    box-shadow: none;
}

.submit-form-control a {
    font-size: 24px;
}

.speech-bubble {
    position: relative;
    background: var(--primarycolor);
    border-radius: .4em;
    color: #fff;
    z-index: 1;
    max-width: 50%;
}

@media (max-width: 767px) {
    .speech-bubble {
        max-width: auto;
    }
}

.speech-bubble:after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 100%;
    width: 0;
    height: 0;
    border: 20px solid transparent;
    border-top-color: var(--primarycolor);
    border-bottom: 0;
    border-left: 0;
    margin-left: 0px;
    top: 20px;
    z-index: -1;
}

.speech-bubble.alt {
    color: var(--bodycolor);
    background: transparent;
}

.speech-bubble.alt:before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: var(--primarycolor);
    opacity: 0.1;
    top: 0px;
    left: 0px;
    border-radius: .4em;
    z-index: -1;
}

.speech-bubble.alt:after {
    content: '';
    position: absolute;
    bottom: 0;
    left: auto;
    right: 100%;
    width: 0;
    height: 0;
    opacity: 0.1;
    border: 20px solid transparent;
    border-right-color: var(--primarycolor);
    border-bottom: 0;
    border-left: 0;
    margin-left: 0px;
    top: 10px;
}

.dropdown-menu {
    font-size: 13px;
}

.online-status {
    position: relative;
}

.online-status:before {
    content: "";
    position: absolute;
    width: 8px;
    height: 8px;
    border-radius: 8px;
    z-index: 1;
    top: 16px;
}

main {
    margin-left: 350px;
    background: var(--mainbackground);
}

@media (max-width: 991px) {
    main {
        margin-left: 0px;
    }
}

main .profile-bar {
    background: var(--sidebarbg);
}

main .scrollerchat {
    height: calc(100vh - 92px);
}

@-moz-keyframes spin {
    from {
        -moz-transform: rotate(0deg);
    }

    to {
        -moz-transform: rotate(360deg);
    }
}

@-webkit-keyframes spin {
    from {
        -webkit-transform: rotate(0deg);
    }

    to {
        -webkit-transform: rotate(360deg);
    }
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.dropdown-menu {
    font-size: 13px;
    background: var(--mainbackground);
    margin-top: 10px;
    border: 1px solid var(--bordercolor);
}

.dropdown-menu .dropdown-item {
    padding: 8px 10px;
    color: var(--bodycolor);
}

.dropdown-menu .dropdown-item:hover,
.dropdown-menu .dropdown-item:focus {
    background: transparent;
    color: var(--primarycolor);
}
</style>

