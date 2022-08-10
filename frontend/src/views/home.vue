<template>
    <div>
        <div class="header">
            <div class="center">

                <h1 class="maintitle">Sign Language API</h1>

                <v-toolbar flat floating rounded>
                    <v-text-field hide-details label="Search for a library..." prepend-icon="mdi-magnify" single-line>
                    </v-text-field>
                </v-toolbar>


            </div>
        </div>

        <div class="libraries">

           

            <v-card class="mx-auto" elevation=6>
                <v-card-text>
                    <p class="text-h4 text--primary">
                        Test library name 1
                    </p>
                    <div class="text--primary">
                        Test description of the library.
                    </div>
                </v-card-text>
                <v-card-actions>
                    <v-btn text color="deep-purple accent-4">
                        Explore
                    </v-btn>
                    <v-btn text color="deep-purple accent-4">
                        Use API
                    </v-btn>
                </v-card-actions>
            </v-card>

            <v-card class="mx-auto" elevation="6">
                <v-card-text>
                    <p class="text-h4 text--primary">
                        Test library name 2
                    </p>
                    <div class="text--primary">
                        Test description of the library.
                    </div>
                </v-card-text>
                <v-card-actions>
                    <v-btn text color="deep-purple accent-4">
                        Explore
                    </v-btn>
                    <v-btn text color="deep-purple accent-4">
                        Use API
                    </v-btn>
                </v-card-actions>
            </v-card>

            <v-card class="mx-auto" elevation="6">
                <v-card-text>
                    <p class="text-h4 text--primary">
                        Test library name 3
                    </p>
                    <div class="text--primary">
                        Test description of the library.
                    </div>
                </v-card-text>
                <v-card-actions>
                    <v-btn text color="deep-purple accent-4">
                        Explore
                    </v-btn>
                    <v-btn text color="deep-purple accent-4">
                        Use API
                    </v-btn>
                </v-card-actions>
            </v-card>

        </div>

        <div class="addLibraryButton">
                   
                        <v-btn class="mx-2" fab dark color="indigo" v-bind="attrs" v-on="on">
                        <v-icon dark>
                            mdi-plus
                        </v-icon>
                    </v-btn> 

                </div>

    </div>
</template>

<style>
.header {
    background-repeat: repeat-x;
    min-height: 25vw;
    max-height: 30vw;
    background-image: url('../assets/Tile.svg');
    background-color: cadetblue;
    background-size: contain;

}

.center {
    text-align: center;
    margin: auto;
    padding: 8%;
}

.maintitle {

    padding-bottom: 1%;
    font-size: 4vw;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: lighter;
    backdrop-filter: blur(20px) opacity(0.8);
}

.addLibraryButton{
    padding: 2%;
    display: inline-flex;
    position: relative;
    float: right;
}

.libraries {
    padding: 2%;
    display: inline-flex;
    align-content: left;
    flex-wrap: wrap;
    flex-direction: row;
    gap: 2vw;
}


.libraries>v-card {
    max-height: 10vw;
    max-width: 20vw;
    display: flex;
    justify-content: left;
    justify-items: left;
    align-items: left;

}
</style>
<script>
</script>