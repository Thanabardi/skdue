<template>
    <div>
        <header class="form-header">
            <h1>Skdue</h1>
            <h3 style="font-size: 30px; color: #b4b4b4">Create your own Skdue!</h3>
        </header>
        <form @submit.prevent="getData" class="form-form">
            <p>Your calendar Name</p>
            <input class="form-input" type="text" v-model="dataForm.name" required ><br>
            <button class="app-button-main">Create</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "CalendarCreate",
    data(){
        return {
            dataForm:{
                name:null,
                // is_test : 'True'
            },
            slug : ''
        }
    },
    methods: {
        setData(data){
            this.slug = data.slug
            this.$router.push({ path: `/calendar/${this.slug}`});

        },
        getData(e){
            e.preventDefault();

            axios.post(`/api/calendar/`, this.dataForm)
                .then(response => {
                this.setData(response.data);
                })
                .catch(error => {
                console.log(error)
            })
        },
        
    }
};
</script>

<style lang='scss' scoped>

@import './../assets/style.css';

.form-header {
    color: #006664;
    font-size: 60px;
    font-weight: 500px;
    text-align: center;
    line-height: 0px;
}
.form-form {
    background: #f5f5f5;
	color: black;
	text-align: center;
    position: absolute;
	font-size: 26px;
	padding: 20px;
    border-radius: 8px;
    top: 200%;
    left: 50%;
    line-height: 0px;
    transform: translate(-50%, -50%);
}
.form-input {
	background: white;
	font-size: 20px;
	padding: 10px;
	width: 300px;
	border: none;
	border-radius: 8px;
}
</style>