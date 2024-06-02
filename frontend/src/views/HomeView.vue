<script setup>
import TopNav from '@/components/TopNav.vue'
</script>

<template>
  <main>
    <TopNav />
    <RouterView />
  </main>
</template>

<style >
#app{
  background-color: #f3f6f8;
}
</style>