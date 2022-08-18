<template>
    <v-app-bar app
    >
        <v-btn icon id='homeButton' to='/'>
            <v-icon>mdi-home</v-icon>
        </v-btn>
        <v-tabs centered class="ml-n9">
            <v-tab v-for="link in links" :key="link.text" :to='link.route'>
                {{link.text}}
            </v-tab>
        </v-tabs>
        <v-menu>
            <template v-slot:activator="{ on, attrs }">
                <v-btn 
                icon
                v-bind="attrs"
                v-on=on
                >
                    <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
            </template>

            <v-list>
                <v-list-item-group
                    @click="() => {}"
                    >
                <v-list-item
                >
                    <v-list-item-title>
                    Use API
                    </v-list-item-title>
                </v-list-item>
                <v-list-item>
                    <v-list-item-title>
                    Delete Library 
                    </v-list-item-title>
                </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-menu>
    </v-app-bar>
</template>
<style>
    #homeButton {
        margin: 1%;
        margin-left: 1px;
        padding: 1%;
        box-sizing: border-box
    }
</style>

<script charset="utf-8">
    import {
        sharedState
    } from '../SharedState';
    export default {
        data: () => ({
            links: [{
                    text: 'Explore library',
                    route: `/library/explore?library_id=${sharedState.library_id}`
                },
                {
                    text: 'Interpet my hand signs',
                    route: `/library/test?library_id=${sharedState.library_id}`
                },
                /*
                {
                    text: 'Add sign',
                    route: 'library/train'
                }*/
            ],
        }),
        methods: {
            /*
            navigate(link) {
                // Only try to navigate if we are not navigating to the page we're on.
                if (link.route != '') {
                    this.$router.push(`${link.route}?library_id=${this.library_id}`);
                } else {
                    this.$router.go(-1);
                }
            }
						*/
        }
    }
</script>
