<template>
        <div class="alert alert-success" role="alert" v-if="type == 0">
            {{ message }}
        </div>
        <div class="alert alert-danger" role="alert" v-else>
            {{ message }}
        </div>
        <br />
</template>
  
<script>
export default {
    props: ['message', 'type'],
};
</script>