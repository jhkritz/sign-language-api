<template>
<img v-bind:src="'data:image/jpeg;base64,'+image_b64" />
</template>

<script>
    const axios = require('axios');
    //import {
    //    baseUrl
    //} from '../BaseRequestUrl';
    export default {
        components: {},
        props: {
            library_id: null
        },
        data: () => ({ 
         library_name: 'newlibrary',
         image_name: 'a',
         image_b64: '',
        }),

        methods: {
          async getImage() {
                try {
                    const url = new URL('http://localhost:5000/library/imageb64');
                    url.searchParams.append('library_name', this.library_name);
                    url.searchParams.append('image_name', this.image_name);
                    const config = {
                        method: 'get',
                        url: url,
                        headers: {
                            Authorization: 'Bearer ' + localStorage.getItem('access_token')
                        },
                    }
                    const res = await axios(config);
                    this.image_b64 = res.data;
                    //console.log(res.data)
                     
                } catch (err) {
                    console.error(err);
                }
            },
            
        },
        beforeMount() {
            this.getImage()
        }

        }
</script>
