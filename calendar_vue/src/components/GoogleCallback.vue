<template>
    <div>
        <h1>Waiting for Google Authentication</h1>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            code: "",
            slug: ""
        }
    },
    methods: {
        setBackendToken(data){
            let token = data.token
            this.$store.commit('setToken', token)
            axios.defaults.headers.common["Authorization"] = "Token " + token
            localStorage.setItem("token", token)

            this.slug = data.calendar.slug
            this.$router.push({ path: `/me/${this.slug}`});
      },
        async getBackendToken() {
            let url = new URL(window.location.href)
            this.code = url.searchParams.get("code")

            await axios.get(`/oauth/login/success/?code=${this.code}`)
                .then(response => {
                    this.setBackendToken(response.data)
                })
        }
    },
    mounted() {
        this.getBackendToken()
    }
}
</script>