<template>
  <v-img
  lazy-src="https://picsum.photos/id/11/10/6"
  max-height="150"
  max-width="250"
  src= "https://picsum.photos/id/11/500/300"
></v-img>
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
         
        }),

        methods: {
          async getImages() {
                try {
                    const url = new URL('http://localhost:5000/library/signs');
                    console.log(this.library_id);
                    url.searchParams.append('library_name', this.library_id);
                    const config = {
                        method: 'get',
                        url: url,
                        headers: {
                            Authorization: 'Bearer ' + localStorage.getItem('access_token')
                        }
                    }
                    const res = await axios(config);
                    this.signs = res.data.signs.map(
                        sign => sign.meaning
                    ).filter(
                        (item, index, self) => self.indexOf(item) === index
                    );
                    this.signs = this.signs.map(meaning => ({
                        name: meaning,
                        status: 'trained'
                    }));
                } catch (err) {
                    console.error(err);
                }
            },
        }
        }
</script>
