<template>
    <div id='mainContainer'>
        <v-main class="grey lighten-3" id='mainContainer'>
            <v-form v-model="valid">
                <v-container id='sheet'>
                    <v-sheet id='sheet' rounded="lg" class='justify-center align-center'>
                        <v-row id='row'>
                            <v-col cols=4>
                                <v-card>
                                    <v-card-title>
                                        Users without any permissions
                                    </v-card-title>
                                    <v-list>
                                        <template v-for="user in permissionlessUsers">
                                            <v-divider :key="user + 'div'" />
                                            <v-list-item :key="user">
                                                <v-list-item-content>
                                                    {{user}}
                                                </v-list-item-content>
                                                <v-list-item-action>
                                                    <v-icon @click='grantUserAccess(user)'>
                                                        mdi-check
                                                    </v-icon>
                                                    <v-icon @click='grantAdminAccess(user)'>
                                                        mdi-account-check
                                                    </v-icon>
                                                </v-list-item-action>
                                            </v-list-item>
                                        </template>
                                    </v-list>
                                </v-card>
                            </v-col>
                            <v-col cols=4>
                                <v-card>
                                    <v-card-title>
                                        Users with basic permissions
                                    </v-card-title>
                                    <v-list>
                                        <template v-for="user in normalUsers">
                                            <v-divider :key="user + 'div'" />
                                            <v-list-item :key="user">
                                                <v-list-item-content>
                                                    {{user}}
                                                </v-list-item-content>
                                                <v-list-item-action>
                                                    <v-icon @click='revokePermissions(user)'>
                                                        mdi-close-box
                                                    </v-icon>
                                                </v-list-item-action>
                                            </v-list-item>
                                        </template>
                                    </v-list>
                                </v-card>
                            </v-col>
                            <v-col cols=4>
                                <v-card>
                                    <v-card-title>
                                        Users with admin permissions
                                    </v-card-title>
                                    <v-list>
                                        <template v-for="user in adminUsers">
                                            <v-divider :key="user + 'div'" />
                                            <v-list-item :key="user">
                                                <v-list-item-content>
                                                    {{user}}
                                                </v-list-item-content>
                                                <v-list-item-action>
                                                    <v-icon @click='revokePermissions(user)'>
                                                        mdi-close-box
                                                    </v-icon>
                                                </v-list-item-action>
                                            </v-list-item>
                                        </template>
                                    </v-list>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-sheet>
                </v-container>
            </v-form>
        </v-main>
    </div>
</template>

<style>
    #row {
        align-content: center;
        justify-content: center;
        box-sizing: border-box;
        display: flex;
    }

    #sheet {
        width: 100%;
        padding: 2.5%;
        min-height: 80vh;
        box-sizing: border-box;
        text-align: center;
    }

    #mainContainer {
        height: 100%;
        box-sizing: border-box;
    }

    #webcamVideo {
        border: 3px solid;
        width: 100%;
        display: none;
    }
</style>

<script>
    import {
        baseUrl
    } from '../BaseRequestUrl';
    const axios = require('axios');
    const FormData = require('form-data');
    export default {
        props: {
            library_id: null
        },
        data: () => ({
            permissionlessUsers: ["John", "Shelly"],
            normalUsers: ["Steve", "Harry"],
            adminUsers: ["Admin", "user"],
            valid: false,
            signname: '',
            signrules: [
                v => !!v || 'Sign name is required'
            ],
            file: null,
            videoRecorder: null,
            videoRecorded: [],
            options: ['Video', 'Single image', 'Zip file'],
            selectedOption: 0,
            recording: false,
        }),
        created() {
            this.getUserGroups();
        },
        methods: {
            async getUserGroups() {
                console.log('getting users');
                const url = new URL(baseUrl + '/library/get/user/groups');
                url.searchParams.append('library_name', localStorage.getItem('library_id'));
                const config = {
                    method: 'get',
                    url: url,
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                    }
                }
                try {
                    const res = await axios(config);
                    console.log(res.data);
                    this.permissionlessUsers = res.data.permissionlessUsers;
                    this.normalUsers = res.data.normalUsers;
                    this.adminUsers = res.data.adminUsers;
                } catch (err) {
                    alert(err);
                }
            },
            async grantUserAccess(userEmail) {
                const config = {
                    method: 'post',
                    url: baseUrl + '/library/adduser',
                    data: JSON.stringify({
                        library_name: localStorage.getItem('library_id'),
                        user_email: userEmail
                    }),
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                        'Content-Type': 'application/json'
                    }
                };
                try {
                    console.log(config);
                    await axios(config);
                    this.normalUsers.push(userEmail);
                    this.permissionlessUsers = this.permissionlessUsers.filter(
                        item => item !== userEmail
                    );
                } catch (err) {
                    alert('Failed to grant user permission');
                }
            },
            async grantAdminAccess(userEmail) {
                const config = {
                    method: 'post',
                    url: baseUrl + '/library/addadmin',
                    data: JSON.stringify({
                        library_name: localStorage.getItem('library_id'),
                        user_email: userEmail
                    }),
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                        'Content-Type': 'application/json'
                    }
                };
                try {
                    console.log(config);
                    await axios(config);
                    this.adminUsers.push(userEmail);
                    this.permissionlessUsers = this.permissionlessUsers.filter(
                        item => item !== userEmail
                    );
                } catch (err) {
                    alert('Failed to grant user permission');
                }
            },
            async revokePermissions(email) {
                const url = new URL(baseUrl + '/library/revoke/permissions');
                url.searchParams.append('library_name', localStorage.getItem('library_id'));
                url.searchParams.append('user_email', email);
                const config = {
                    method: 'delete',
                    url: url,
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                    }
                };
                try {
                    console.log(config);
                    await axios(config);
                    this.permissionlessUsers.push(email);
                    this.adminUsers = this.adminUsers.filter(item => item !== email);
                    this.normalUsers = this.normalUsers.filter(item => item !== email);
                } catch (err) {
                    alert('Failed to revoke user permissions');
                }
            },
            async submitInput() {
                const data = new FormData();
                data.append('sign_name', this.signname);
                data.append('lib_name', this.library_id);
                var url = '';
                switch (this.selectedOption) {
                    case 0:
                        url = baseUrl + '/library/upload_sign_video';
                        data.append('video', new Blob(this.videoRecorded.map(e => e.data), {
                            type: 'video/webm'
                        }));
                        break;
                    case 1:
                        url = baseUrl + '/library/uploadsign';
                        data.append('image_file', this.file);
                        break;
                    case 2:
                        url = baseUrl + '/library/uploadsigns';
                        data.append('zip_file', this.file);
                        break;
                    default:
                        console.log('Error: default case reached.');
                        break;
                }
                const config = {
                    method: 'post',
                    url: url,
                    data: data,
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token')
                    }
                };
                try {
                    const res = await axios(config);
                    if (res.status == 200) {
                        alert('Success');
                    }
                } catch (err) {
                    console.error(err);
                    alert('Failed to upload image.');
                }
            },
        },
    }
</script>
